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
from tensorboardX import SummaryWriter

writer = SummaryWriter('logimg4')

#Parameters
env = gym.make('gym_tdw:tdw_puzzle_1-v0')
env.set_observation(True)

#env.seed(1)
torch.manual_seed(1)

C,H,W = 3,480,640
grid = 5
action_space = grid*grid


#Hyperparameters
learning_rate = 0.001
gamma = 0
episodes = 20000
render = False
eps = np.finfo(np.float32).eps.item()
SavedAction = namedtuple('SavedAction', ['log_prob', 'value'])
rewards = []

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, kernel_size=8, stride=4)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.fc4 = nn.Linear(7 * 7 * 64, 512)
        self.head = nn.Linear(512, 32)



        #self.conv1 = torch.nn.Conv2d(3, 18, kernel_size=3, stride=1, padding=1)
        #self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        # 4608 input features, 64 output features (see sizing flow below)
        #self.fc1 = torch.nn.Linear(18 * H * W // 4, 64)

        # 64 input features, 10 output features for our 10 defined classes
        #self.fc2 = torch.nn.Linear(64, 32)





        self.action_head = nn.Linear(32, action_space)
        self.value_head = nn.Linear(32, 1) # Scalar Value

        self.save_actions = []
        self.rewards = []

    def forward(self, x):
        x = x.permute(2,0,1)
        x.unsqueeze_(0)

        x = x.float() / 255
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.fc4(x.view(x.size(0), -1)))
        x = F.relu(self.head(x))
        action_score = self.action_head(x)
        state_value = self.value_head(x)

        return F.softmax(action_score, dim=-1), state_value

model = Policy()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)



def select_action(state):
    if state is None:
        return 10
    state = torch.from_numpy(state).float()
    probs, state_value = model(state)
    m = Categorical(probs)
    action = m.sample()
    model.save_actions.append(SavedAction(m.log_prob(action), state_value))

    return action.item()


def finish_episode():
    R = 0
    save_actions = model.save_actions
    policy_loss = []
    value_loss = []
    rewards = []

    for r in model.rewards[::-1]:
        R = r + gamma * R
        rewards.insert(0, R)

    rewards = torch.tensor(rewards)
    rewards = (rewards - rewards.mean()) / (rewards.std() + eps)

    for (log_prob , value), r in zip(save_actions, rewards):
        reward = r - value.item()
        policy_loss.append(-log_prob * reward)
        value_loss.append(F.smooth_l1_loss(value, torch.tensor([r])))

    optimizer.zero_grad()
    loss = torch.stack(policy_loss).sum() + torch.stack(value_loss).sum()
    loss.backward()
    optimizer.step()

    del model.rewards[:]
    del model.save_actions[:]

def transform_action(action):
    multiplier = 15/grid
    return {'x':(action//grid)*multiplier-7,'z':(action%grid)*multiplier-7}

def aux_reward(state):
    #print(state['object_information'])
    #return 0
    pos = []
    for k,v in state['object_information'].items():
        if v['model_name']=='prim_sphere':
            x=v['position']

            pos.append((x['x'],x['y'],x['z']))

    return -distance.euclidean(pos[0],pos[1])

def main():
    running_reward = 10
    live_time = []
    imag = []
    sum_reward = 0
    img_it = 0
    steps = 0
    final_reward = []
    for i_episode in count(episodes):
        state = None
        #env = gym.make('gym_tdw:tdw_puzzle_1-v0')
        k = env.reset()
        print(type(k))
        steps = 0
        finished = 0
        for t in range(100):
            action = select_action(state)
            state, reward, done, info = env.step(transform_action(action))
            sum_reward = sum_reward + reward
            if done:
                print('finished')
                finished = finished + 1
                reward = reward - 5
            reward = reward + aux_reward(state)
            if reward < -100:
                done = True
            state = state['image_1']
            imag.append(state)
            #if img_it > 50:
            #    imag = np.concatenate(imag,axis=0)
            #    imag = torch.from_numpy(imag).float()

            #    x = vutils.make_grid(imag, normalize=True, scale_each=True)
            #    writer.add_image('Image_seq', x, 0)
            #print(type(state),state.shape)
            #img = torch.from_numpy(state).float()
            #img = img.permute(2,0,1)
            #writer.add_image('Image', img, img_it)
            #img_it = img_it + 1
            pickle.dump(state,open('img.p','wb'))
            if render: env.render()
            model.rewards.append(reward)
            rewards.append(reward)
            print(transform_action(action),reward,t,i_episode,sum_reward)
            steps = steps + 1

            if t >= 100 or reward>0 or finished > 5:
                break
        if i_episode % 1 == 0:
            print(i_episode,sum_reward)
            pickle.dump(rewards,open('AC_rewards.p','wb'))
            torch.save(model.state_dict(),'AC_model')
        finish_episode()
        if finished > 5:
            steps = 100
        final_reward.append(steps)
        pickle.dump(final_reward,open('AC_steps.p','wb'))
        #env.close()

if __name__ == '__main__':
    main()
