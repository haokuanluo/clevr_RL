import gym, os
import numpy as np
import matplotlib.pyplot as plt
from itertools import count
from collections import namedtuple
import torchvision.utils as vutils
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical
import time
import pickle
from scipy.spatial import distance
#from tensorboardX import SummaryWriter
from cv2 import resize
from skimage.color import rgb2gray
#from universe import vectorized
#from universe.wrappers import Unvectorize, Vectorize
from torch.autograd import Variable
from gym.spaces.box import Box
from torch.multiprocessing import Process
import torch.multiprocessing as mp
from model import Policy
import copy
#from SharedOptimizers import SharedAdam

#import gym_pull


#writer = SummaryWriter('logimg4')

#Parameters









#Hyperparameters
learning_rate = 0.001

grid = 5
action_space = grid*grid

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cuda'
#device = 'cpu'


def ensure_shared_grads(model, shared_model):
    for param, shared_param in zip(model.parameters(), shared_model.parameters()):
        if shared_param.grad is not None and device == 'cpu':
            return
        if device == 'cpu':
            shared_param._grad = param.grad
        else:
            shared_param._grad = param.grad.clone().cpu()


class atari_env(object):
    def __init__(self,env_id):
        self.env = gym.make(env_id)
        self.env.set_observation(True)
        self.observation_space = np.array([1])

    def transform_action(self,action):
        multiplier = 15 / grid
        return {'x': (action // grid) * multiplier - 7, 'z': (action % grid) * multiplier - 7}

    def aux_reward(self,state):
        # print(state['object_information'])
        # return 0
        pos = []
        for k, v in state['object_information'].items():
            if v['model_name'] == 'prim_sphere':
                x = v['position']

                pos.append((x['x'], x['y'], x['z']))

        return -distance.euclidean(pos[0], pos[1])

    def step(self,action):
        action = self.transform_action(action)
        a,b,c,d = self.env.step(action)
        b = b + self.aux_reward(a)
        print(b,action)
        if c and b<0:
            b = b - 5

        a = _process_frame(a['image_1'],None)
        return a,b,c,d

    def reset(self):
        a = self.env.reset()

        a = np.zeros((1,80,80))
        return a

    def render(self):
        self.env.render()

    def seed(self,seed):
        pass
        #self.env.seed(seed)

    def close(self):
        self.env.close()





def _process_frame(frame, conf):
    #print(frame.shape)
    #frame = frame[conf["crop1"]:conf["crop2"] + 160, :160]
    #frame = resize(rgb2gray(frame), (80, conf["dimension2"]))
    frame = rgb2gray(frame)
    #print(frame.shape)
    frame = resize(frame, (80, 80))
    frame = np.reshape(frame, [1, 80, 80])
    if True:
        from PIL import Image
        img = Image.fromarray(frame[0])
        img.save('my.png')
    return frame



class Agent(object):
    def __init__(self, model, env, args, state,gpu_id = 0):
        self.model = model
        self.env = env
        self.current_life = 0
        self.state = state
        self.hx = None
        self.cx = None
        self.eps_len = 0
        self.args = args
        self.values = []
        self.log_probs = []
        self.rewards = []
        self.entropies = []
        self.done = True
        self.info = None
        self.reward = 0
        self.gpu_id = gpu_id

    def action_train(self):
        if self.done:

            with torch.cuda.device(self.gpu_id):
                self.cx = Variable(torch.zeros(1, 256).float().to(device))
                self.hx = Variable(torch.zeros(1, 256).float().to(device))
        else:
            self.cx = Variable(self.cx.data)
            self.hx = Variable(self.hx.data)

        with torch.cuda.device(self.gpu_id):
            value, logit, (self.hx, self.cx) = self.model((Variable(self.state.unsqueeze(0).float().to(device)), (self.hx, self.cx)))
        prob = F.softmax(logit)
        log_prob = F.log_softmax(logit)
        entropy = -(log_prob * prob).sum(1)
        self.entropies.append(entropy)
        action = prob.multinomial(num_samples = 1).data
        log_prob = log_prob.gather(1, Variable(action))
        state, self.reward, self.done, self.info = self.env.step(action.cpu().numpy())
        self.state = torch.from_numpy(state).float()
        self.eps_len += 1
        self.done = self.done or self.eps_len >= self.args['M']
        #self.reward = max(min(self.reward, 1), -1)
        self.values.append(value)
        self.log_probs.append(log_prob)
        self.rewards.append(self.reward)
        return self

    def action_test(self):
        if self.done:
            with torch.cuda.device(self.gpu_id):
                self.cx = Variable(torch.zeros(1, 256).float().to(device), volatile=True)
                self.hx = Variable(torch.zeros(1, 256).float().to(device), volatile=True)
        else:
            self.cx = Variable(self.cx.data, volatile=True)
            self.hx = Variable(self.hx.data, volatile=True)
        with torch.cuda.device(self.gpu_id):
            value, logit, (self.hx, self.cx) = self.model((Variable(self.state.unsqueeze(0).float().to(device), volatile=True), (self.hx, self.cx)))
        prob = F.softmax(logit)
        action = prob.max(1)[1].data.cpu().numpy()
        state, self.reward, self.done, self.info = self.env.step(action[0])
        with torch.cuda.device(self.gpu_id):
            self.state = torch.from_numpy(state).float().to(device)
        self.eps_len += 1
        self.done = self.done or self.eps_len >= self.args['M']
        return self

    def check_state(self):
        if self.current_life > self.info['ale.lives']:
            self.done = True
        self.current_life = self.info['ale.lives']
        return self

    def clear_actions(self):
        self.values = []
        self.log_probs = []
        self.rewards = []
        self.entropies = []
        return self
loss = []
def test(args, shared_model,render=False):

    torch.manual_seed(args['seed'])
    torch.cuda.manual_seed(args['seed'])

    # gym_pull.pull('github.com/ppaquette/gym-doom')
    env = atari_env(args['ENV'])
    reward_sum = 0
    start_time = time.time()
    num_tests = 0
    reward_total_sum = 0
    player = Agent(None, env, args, None,0)
    player.model = copy.deepcopy(shared_model)
    gpu_id = 0
    with torch.cuda.device(gpu_id):
        player.model = player.model.cuda() if gpu_id >= 0 else player.model
    player.state = player.env.reset()
    with torch.cuda.device(gpu_id):
        player.state = torch.from_numpy(player.state).float().to(device)
    player.model.eval()

    while True:
        if player.done:
            player.model.load_state_dict(shared_model.state_dict())
            print('loaded model')
        if render:
            env.render()
        player.action_test()
        reward_sum += player.reward

        if player.done:
            num_tests += 1
            player.current_life = 0
            reward_total_sum += reward_sum
            reward_mean = reward_total_sum / num_tests
            print("test ",reward_sum, player.reward)
            loss.append((reward_sum,player.reward))
            import pickle
            pickle.dump(loss,open('A3Closs','wb'))
            #log['{}_log'.format(args['ENV'])].info(
            #    "Time {0}, episode reward {1}, episode length {2}, reward mean {3:.4f}".
            #    format(
            #        time.strftime("%Hh %Mm %Ss",
            #                      time.gmtime(time.time() - start_time)),
            #        reward_sum, player.eps_len, reward_mean))

            #if reward_sum > args['SSL']:
            #    player.model.load_state_dict(shared_model.state_dict())
            #    state_to_save = player.model.state_dict()
            #    torch.save(state_to_save, '{0}{1}.dat'.format(
            #        args['SMD'], args['ENV']))

            reward_sum = 0
            player.eps_len = 0
            state = player.env.reset()
            time.sleep(60)
            with torch.cuda.device(gpu_id):
                player.state = torch.from_numpy(state).float().to(device)


def train(args, optimizer, rank, shared_model):

    gpu_id = args['gpu_ids'][rank]
    #torch.manual_seed(args['seed'] )
    torch.manual_seed(args['seed'] + rank)
    torch.cuda.manual_seed(args['seed'] + rank)
    #gym_pull.pull('github.com/ppaquette/gym-doom')
    env = atari_env(args['ENV'])

    try:
        env.seed(args['seed'] + rank)
        if optimizer == None:
            optimizer = optim.Adam(shared_model.parameters(), lr=learning_rate)

        player = Agent(None, env, args, None, gpu_id)
        player.model = copy.deepcopy(shared_model)

        with torch.cuda.device(gpu_id):
            player.model = player.model.cuda() if gpu_id >= 0 else player.model

        player.model.train()

        player.state = player.env.reset()
        player.state = torch.from_numpy(player.state).float().to(device)
        while True:
            with torch.cuda.device(gpu_id):
                player.model.load_state_dict(shared_model.state_dict())
            for step in range(args['NS']):
                player.action_train()
                # if args['CL']:
                #    player.check_state()
                if player.done:
                    break

            if player.done:
                player.eps_len = 0
                player.current_life = 0
                state = player.env.reset()
                with torch.cuda.device(gpu_id):
                    player.state = torch.from_numpy(state).float().to(device)

            with torch.cuda.device(gpu_id):
                R = torch.zeros(1, 1).to(device)
            if not player.done:
                with torch.cuda.device(gpu_id):
                    value, _, _ = player.model(
                        (Variable(player.state.unsqueeze(0).float().to(device)), (player.hx, player.cx)))
                    R = value.data

            player.values.append(Variable(R))
            policy_loss = 0
            value_loss = 0
            R = Variable(R)
            with torch.cuda.device(gpu_id):
                gae = torch.zeros(1, 1).to(device)
            reward_sum = 0
            for i in reversed(range(len(player.rewards))):
                reward_sum = reward_sum + player.rewards[i]
                R = args['G'] * R + player.rewards[i]
                advantage = R - player.values[i]
                value_loss = value_loss + 0.5 * advantage.pow(2)

                # Generalized Advantage Estimataion
                delta_t = player.rewards[i] + args['G'] * \
                          player.values[i + 1].data - player.values[i].data
                gae = gae * args['G'] * args['T'] + delta_t

                policy_loss = policy_loss - \
                              player.log_probs[i] * \
                              Variable(gae) - 0.01 * player.entropies[i]
            print(reward_sum, len(player.rewards), reward_sum / len(player.rewards))
            optimizer.zero_grad()
            (policy_loss + 0.5 * value_loss).backward()
            torch.nn.utils.clip_grad_norm(player.model.parameters(), 40)
            ensure_shared_grads(player.model, shared_model)
            optimizer.step()
            player.clear_actions()
            player.env.close()  #######
            break  #######
    except:
        env.close()


def loadarguments():
    global env_conf
    global env
    global setup_json
    global shared_model
    global saved_state
    global optimizer
    global torch



    torch.set_default_tensor_type('torch.FloatTensor')
    torch.manual_seed(args['seed'])




    env = atari_env(args['ENV'])
    the_gpu_id = 1
    shared_model = Policy(env.observation_space.shape[0], action_space)
    if device == 'cuda' and False:
        with torch.cuda.device(the_gpu_id):
            shared_model.cuda()
    if args['L']:
        saved_state = torch.load(
            '{0}{1}.dat'.format(args['LMD'], args['ENV']))
        shared_model.load_state_dict(saved_state)
    shared_model.share_memory()

    if args['SO']:
        #if args['OPT'] == 'RMSprop':
        #    optimizer = SharedRMSprop(shared_model.parameters(), lr=args['LR'])
        if args['OPT'] == 'Adam':
            optimizer = None
        #if args['OPT'] == 'LrSchedAdam':
        #    optimizer = SharedLrSchedAdam(
        #        shared_model.parameters(), lr=args['LR'])
        #optimizer.share_memory()
    else:
        optimizer = None

args = {'LR': 0.0001, "G":0.01, "T":1.00,"NS":10,"M":10,'W':1,   ###############
         "seed":42,'LMD':'/modeldata/','SMD':'/modeldata/','ENV':'gym_tdw:tdw_puzzle_1-v0','L':False,'SO':False,'OPT':'Adam',
        'gpu_ids':[0]}

if __name__ == '__main__':
    torch.backends.cudnn.benchmark = False
    processes = []
    loadarguments()
    torch.manual_seed(args['seed'])
    torch.cuda.manual_seed(args['seed'])
    mp.set_start_method('spawn')

    #p = Process(target=test, args=(args, shared_model))
    #p.start()
    #processes.append(p)

    time.sleep(0.1)
    for rank in range(0, args['W']):
        p = Process(
            target=train, args=(args, optimizer, rank, shared_model))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
