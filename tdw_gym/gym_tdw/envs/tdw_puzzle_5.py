from gym_tdw.envs.tdw_env import TdwEnv
import os
from gym_tdw.envs.utils import gym_utils

class TdwEnv_puzzle_5(TdwEnv):

    def __init__(self):
        self.tdw_docker_id, self.port = gym_utils.setup_tdw_instance()
        self.tdw_instance = gym_utils.TDW_sim(5, self.port)
        self.puzzle_type = "non-goal"
        self.tdw_instance.run(self.puzzle_type)
        self.output_images = False
        self.reward_tracker = {}
        self.init_reward(self.tdw_instance.objects)
        self.episode = False
        print("Tdw initialised")