import gym, os
import numpy as np
import matplotlib.pyplot as plt
from itertools import count
from collections import namedtuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical
import time
import pickle
from scipy.spatial import distance


#Parameters
env = gym.make('gym_tdw:tdw_puzzle_1-v0')
env.set_observation(True)

#env.seed(1)
torch.manual_seed(1)

C,H,W = 3,480,640
grid = 20
action_space = grid*grid


#Hyperparameters
learning_rate = 0.01
gamma = 0.99
episodes = 20000
render = False
eps = np.finfo(np.float32).eps.item()
SavedAction = namedtuple('SavedAction', ['log_prob', 'value'])
rewards = []

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()

        self.conv1 = torch.nn.Conv2d(3, 18, kernel_size=3, stride=1, padding=1)
        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        # 4608 input features, 64 output features (see sizing flow below)
        self.fc1 = torch.nn.Linear(18 * H * W // 4, 64)

        # 64 input features, 10 output features for our 10 defined classes
        self.fc2 = torch.nn.Linear(64, 32)





        self.action_head = nn.Linear(32, action_space)
        self.value_head = nn.Linear(32, 1) # Scalar Value

        self.save_actions = []
        self.rewards = []

    def forward(self, x):
        x = x.permute(2,0,1)
        x.unsqueeze_(0)

        x = F.relu(self.conv1(x))

        # Size changes from (18, 32, 32) to (18, 16, 16)
        x = self.pool(x)


        x = x.view(-1, 18 * H * W // 4)


        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        action_score = self.action_head(x)
        state_value = self.value_head(x)

        return F.softmax(action_score, dim=-1), state_value

model = Policy()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)



def select_action(state):
    if state is None:
        return 100
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
    multiplier = 200/grid
    return {'x':(action//grid)*multiplier-100,'z':(action%grid)*multiplier-100}

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
    sum_reward = 0
    for i_episode in count(episodes):
        state = None
        for t in count():
            action = select_action(state)
            state, reward, done, info = env.step(transform_action(action))
            sum_reward = sum_reward + reward
            reward = 10000*reward + aux_reward(state)
            state = state['image_1']
            if render: env.render()
            model.rewards.append(reward)
            rewards.append(reward)
            print(action,reward,t,i_episode,sum_reward)


            if done or t >= 100:
                break
        if i_episode % 1 == 0:
            print(i_episode,sum_reward)
            pickle.dump(rewards,open('AC_rewards.p','wb'))
        finish_episode()

if __name__ == '__main__':
    main()
