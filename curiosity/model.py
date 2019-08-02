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

final_dim = 640
class Policy(nn.Module):
    def __init__(self,num_inputs,action_space):
        super(Policy,self).__init__()

        self.conv1 = nn.Conv2d(num_inputs, 32, kernel_size=3, stride=2,padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, stride=2,padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(32)
        self.conv4 = nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1)
        self.bn4 = nn.BatchNorm2d(32)


        self.lstm = nn.LSTMCell(final_dim, 256)

        self.critic_linear = nn.Linear(256, 1)
        # The actor layer
        self.actor_linear = nn.Linear(256, action_space)

        self.save_actions = []
        self.rewards = []

    def forward(self, x):
        x, (hx,cx) = x
        
        x = x.permute(0,3,1,2)
        #x.unsqueeze_(0)

        #x = x.float() / 255


        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = x.view(x.size(0),-1)

        hx, cx = self.lstm(x, (hx, cx))
        x = hx

        action_score = self.actor_linear(x)
        state_value = self.critic_linear(x)

        return state_value, action_score,(hx,cx)

class Inverse(nn.Module):
    def __init__(self,num_inputs,action_space):
        super(Inverse, self).__init__()

        self.conv1 = nn.Conv2d(num_inputs, 32, kernel_size=3, stride=2,padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, stride=2,padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(32)
        self.conv4 = nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1)
        self.bn4 = nn.BatchNorm2d(32)
        self.action_space = action_space



        #self.embed = nn.Linear(288*2, 256)
        #self.output = nn.Linear(256,action_space)


    def forward(self, x):

        x = x.permute(0,3,1,2)
        #x = x.permute(2,0,1)
        #x.unsqueeze_(0)

        #x = x.float() / 255


        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = x.view(x.size(0),-1)

        #x = F.relu(self.embed(x))
        #x = self.output(x)
        return x


class mapping(nn.Module):
    def __init__(self,action_space,final_dim):
        super(mapping, self).__init__()



        self.embed = nn.Linear(final_dim*2, 256)
        self.output = nn.Linear(256,action_space)


    def forward(self, x):
        print("the shape of x for mapping is ",x.shape)
        #x = torch.cat(x,0)
        #x = x.permute(2,0,1)
        #x.unsqueeze_(0)
        #x = x.float() / 255
        x = F.relu(self.embed(x))
        x = self.output(x)
        return F.log_softmax(x, dim=1)

class prediction(nn.Module):
    def __init__(self,action_space,final_dim):
        super(prediction, self).__init__()



        self.f1= nn.Linear(final_dim + action_space, 256)
        self.f2 = nn.Linear(256,final_dim)


    def forward(self, x):
        print("the shape of x for prediction is ",x.shape)
        #x = torch.cat(x,0)
        #x = x.permute(2,0,1)
        #x.unsqueeze_(0)
        #x = x.float() / 255
        x = F.relu(self.embed(x))
        x = self.output(x)
        return x

