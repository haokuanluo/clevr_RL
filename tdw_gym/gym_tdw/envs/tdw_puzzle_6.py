from gym_tdw.envs.tdw_env import TdwEnv
import os
from gym_tdw.envs.utils import gym_utils
import time


class TdwEnv_puzzle_6(TdwEnv):

    def __init__(self):
        self.tdw_docker_id, self.port = gym_utils.setup_tdw_instance()
        self.tdw_instance = gym_utils.TDW_sim(6, self.port)
        self.puzzle_type = "goal"
        self.tdw_instance.run(self.puzzle_type)
        self.output_images = False
        self.reward_tracker = {}
        self.init_reward(self.tdw_instance.objects)
        self.episode = False
        print("Tdw initialised")


    # def step(self, action):
    #     """
    #         Parameters
    #         ----------
    #         action :
    #
    #         Returns
    #         -------
    #         ob, reward, episode_over, info : tuple
    #             ob (object) :
    #                 an environment-specific object representing your observation of
    #                 the environment.
    #             reward (float) :
    #                 amount of reward achieved by the previous action. The scale
    #                 varies between environments, but the goal is always to increase
    #                 your total reward.
    #             episode_over (bool) :
    #                 whether it's time to reset the environment again. Most (but not
    #                 all) tasks are divided up into well-defined episodes, and done
    #                 being True indicates the episode has terminated. (For example,
    #                 perhaps the pole tipped too far, or you lost your last life.)
    #             info (dict) :
    #                  diagnostic information useful for debugging. It can sometimes
    #                  be useful for learning (for example, it might contain the raw
    #                  probabilities behind the environment's last state change).
    #                  However, official evaluations of your agent are not allowed to
    #                  use this for learning.
    #     """
    #
    #
    #     if self.output_images:
    #         gym_utils.scene_state_data.image_1_ready = False
    #         # gym_utils.scene_state_data.image_2_ready = False
    #         gym_utils.scene_state_data.object_updated = False
    #     gym_utils.take_action(self.objects, action)
    #     if self.output_images:
    #         while not gym_utils.scene_state_data.image_1_ready:
    #             pass
    #     else:
    #         time.sleep(0.1)
    #
    #     obs = {
    #         "image_1": gym_utils.scene_state_data.image_1
    #     }
    #
    #     while not gym_utils.scene_state_data.object_updated:
    #         pass
    #     obs["object_information"] = gym_utils.scene_state_data.parse_object_data()
    #     reward = self.puzzle_state.get_reward(obs["object_information"])
    #     return obs, reward, self.puzzle_state.episode_complete(), None
