from gym_tdw.envs.tdw_env import TdwEnv
import os
from gym_tdw.envs.utils import gym_utils

class TdwEnv_puzzle_3(TdwEnv):

    def __init__(self):
        print(os.getcwd())
        self.game_thread, self.tracker = gym_utils.setup_connection()

        gym_utils.load_scene("example")
        print("Done loading the scene")
        self.objects = gym_utils.load_puzzle(3)
        self.puzzle_state = gym_utils.puzzle_state(self.objects)
        print("Done loading the puzzle")
        self.output_images = False
        # Wait until the tdw has finished initialisation
        gym_utils.scene_state_data.object_updated = False
        gym_utils.update_info()
        while not gym_utils.scene_state_data.object_updated:
            pass
        print("Tdw initialised")