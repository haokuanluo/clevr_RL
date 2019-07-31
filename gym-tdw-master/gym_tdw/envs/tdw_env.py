import gym
from gym_tdw.envs.utils import gym_utils
import random
import time
import os


class TdwEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print(os.getcwd())
        self.game_thread, self.tracker = gym_utils.setup_connection()

        gym_utils.load_scene("example")
        print("Done loading the scene")
        self.objects = gym_utils.load_puzzle(1)
        self.puzzle_state = gym_utils.puzzle_state(self.objects)
        print("Done loading the puzzle")
        self.output_images = False
        # Wait until the tdw has finished initialisation
        gym_utils.scene_state_data.object_updated = False
        gym_utils.update_info()
        while not gym_utils.scene_state_data.object_updated:
            pass
        print("Tdw initialised")

    def step(self, action):
        """
            Parameters
            ----------
            action :

            Returns
            -------
            ob, reward, episode_over, info : tuple
                ob (object) :
                    an environment-specific object representing your observation of
                    the environment.
                reward (float) :
                    amount of reward achieved by the previous action. The scale
                    varies between environments, but the goal is always to increase
                    your total reward.
                episode_over (bool) :
                    whether it's time to reset the environment again. Most (but not
                    all) tasks are divided up into well-defined episodes, and done
                    being True indicates the episode has terminated. (For example,
                    perhaps the pole tipped too far, or you lost your last life.)
                info (dict) :
                     diagnostic information useful for debugging. It can sometimes
                     be useful for learning (for example, it might contain the raw
                     probabilities behind the environment's last state change).
                     However, official evaluations of your agent are not allowed to
                     use this for learning.
        """
        gym_utils.scene_state_data.collided = False

        if self.output_images:
            gym_utils.scene_state_data.image_1_ready = False
            # gym_utils.scene_state_data.image_2_ready = False
            gym_utils.scene_state_data.object_updated = False
        gym_utils.take_action(self.objects, action)
        if self.output_images:
            while not gym_utils.scene_state_data.image_1_ready :
                pass
        else:
            time.sleep(0.1)

        obs = {
            "image_1": gym_utils.scene_state_data.image_1,
            # "image_2": gym_utils.scene_state_data.image_2
        }
        if gym_utils.scene_state_data.collided:
            c1, c2 = gym_utils.scene_state_data.parse_collision_data()
            self.puzzle_state.process_collision(c1, c2)

        while not gym_utils.scene_state_data.object_updated:
            pass
        obs["object_information"] = gym_utils.scene_state_data.parse_object_data()
        reward = self.puzzle_state.get_reward()
        return obs, reward, self.puzzle_state.episode_complete(obs["object_information"]), None

    def check_collision(self):
        gym_utils.scene_state_data.parse_collision_data()
        return True

    def sample_random_action(self):
        return {
            "x": random.randint(-50, 50),
            "z": random.randint(-50, 50)
        }

    def set_observation(self, output=False):
        if self.output_images != output:
            gym_utils.set_output(output)
            self.output_images = output

    def reset(self):
        gym_utils.reset_scene(self.objects)
        self.puzzle_state.init_tgt_sphere_reward_state(self.objects)

    def _render(self):
        pass

    def _get_reward(self):
        """ Reward is given for XY. """
        pass

    def _seed(self):
        pass

    def close(self):
        self.tracker.free_up_port()
        pass