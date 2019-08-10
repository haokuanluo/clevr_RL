import gym
from gym_tdw.envs.utils import gym_utils
import random
import time
import os

from tdw.output_data import Collision
from tdw.tdw_utils import TDWUtils
from tdw.output_data import Images, OutputData, Collision, Transforms, Rigidbodies
from PIL import Image as pil_Image
import io
import numpy as np




class TdwEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.tdw_docker_id, self.port = gym_utils.setup_tdw_instance()
        self.tdw_instance = gym_utils.TDW_sim(1, self.port)
        self.puzzle_type = "non-goal"
        self.tdw_instance.run(self.puzzle_type)
        self.output_images = False
        self.reward_tracker = {}
        self.init_reward(self.tdw_instance.objects)
        self.episode = False
        # print(os.getcwd())
        # self.game_thread, self.tracker = gym_utils.setup_connection()
        #
        # gym_utils.load_scene("example")
        # print("Done loading the scene")
        # self.objects = gym_utils.load_puzzle(1)
        # self.puzzle_state = gym_utils.puzzle_state(self.objects)
        # print("Done loading the puzzle")

        # # Wait until the tdw has finished initialisation
        # gym_utils.scene_state_data.object_updated = False
        # gym_utils.update_info()
        # while not gym_utils.scene_state_data.object_updated:
        #     pass
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
        resp = self.tdw_instance.take_action(action)
        # images = Images(resp[0])
        obs = {}
        obs['object_information'] = {}
        for r in resp:
            r_id = OutputData.get_data_type_id(r)
            if r_id == "imag":
                images = Images(r)
                obs['image'] = np.array(pil_Image.open(io.BytesIO(images.get_image(0))))
            if r_id == "coll":
                self.process_collision(Collision(r))
            if r_id == "rigi":
                rigi_body_data = Rigidbodies(r)
                for object_index in range(rigi_body_data.get_num()):
                    if rigi_body_data.get_id(object_index) not in  obs['object_information'].keys():
                        obs['object_information'][rigi_body_data.get_id(object_index)] = {}
                    obs['object_information'][rigi_body_data.get_id(object_index)][
                        'velocity'] = rigi_body_data.get_velocity(object_index)
                    obs['object_information'][rigi_body_data.get_id(object_index)][
                        'mass'] = rigi_body_data.get_mass(object_index)
                    obs['object_information'][rigi_body_data.get_id(object_index)][
                        'angular_velocity'] = rigi_body_data.get_angular_velocity(object_index)
            if r_id == "tran":
                transform_data = Transforms(r)
                for object_index in range(transform_data.get_num()):
                    if transform_data.get_id(object_index) not in obs['object_information'].keys():
                        obs['object_information'][transform_data.get_id(object_index)] = {}
                    obs['object_information'][transform_data.get_id(object_index)][
                        'position'] = transform_data.get_position(object_index)
                    obs['object_information'][transform_data.get_id(object_index)][
                        'rotation'] = transform_data.get_rotation(object_index)
        if self.puzzle_type == 'goal':
            reward = self.get_reward(obs['object_information'])
        else:
            reward = self.get_reward()
        self.update_episode_state(obs['object_information'])
        return obs, reward, self.episode, None
        # gym_utils.scene_state_data.collided = False
        #
        # if self.output_images:
        #     gym_utils.scene_state_data.image_1_ready = False
        #     # gym_utils.scene_state_data.image_2_ready = False
        #     gym_utils.scene_state_data.object_updated = False
        # gym_utils.take_action(self.objects, action)
        # if self.output_images:
        #     w`hile not gym_utils.scene_state_data.image_1_ready :
        #         pass
        # else:
        #     time.sleep(0.1)
        #
        # obs = {
        #     "image_1": gym_utils.scene_state_data.image_1,
        #     # "image_2": gym_utils.scene_state_data.image_2
        # }
        # if gym_utils.scene_state_data.collided:
        #     c1, c2 = gym_utils.scene_state_data.parse_collision_data()
        #     self.puzzle_state.process_collision(c1, c2)
        #
        # while not gym_utils.scene_state_data.object_updated:
        #     pass
        # obs["object_information"] = gym_utils.scene_state_data.parse_object_data()
        # reward = self.puzzle_state.get_reward()
        # return obs, reward, self.puzzle_state.episode_complete(obs["object_information"]), None

    def process_collision(self, collision_data):
        objects = self.tdw_instance.objects
        if "walls" in objects.keys():
            wall_ids = objects["walls"]
            if (collision_data.get_collider_id() in wall_ids or collision_data.get_collidee_id() in wall_ids) and ( objects["sphere"] == collision_data.get_collider_id() or objects["sphere"] == collision_data.get_collidee_id()):
                self.episode = True
        if (objects["sphere"] == collision_data.get_collider_id() and collision_data.get_collidee_id() in objects["target_spheres"]) or (objects["sphere"] == collision_data.get_collidee_id() and collision_data.get_collider_id() in objects["target_spheres"]):
            self.update_reward(collision_data.get_collidee_id() if collision_data.get_collidee_id() in objects["target_spheres"] else collision_data.get_collider_id())

    def update_episode_state(self, object_information=None):
        # If episode is already done than return
        if self.episode:
            return
        for _sphere in self.tdw_instance.objects['target_spheres'] + [self.tdw_instance.objects['sphere']]:
            pos = object_information[_sphere]["position"]
            if not (-4.718 < pos[0] < -3.532 and -5.687 < pos[2] < -3.527):
                self.episode = True
        for key, value in self.reward_tracker.items():
            if value != 1:
                self.episode = False
                return
        self.episode = True

    def update_reward(self, tgt_id):
        if self.reward_tracker[tgt_id] == 0:
            self.reward_tracker[tgt_id] = 1
            self.tdw_instance.change_material(tgt_id)

    def get_reward(self, object_information=None):
        if 'goal_boundaries' in self.tdw_instance.objects:
            for tgt_sphere in self.tdw_instance.objects['target_spheres']:
                pos = object_information[tgt_sphere]["position"]
                goal_boundaries = self.tdw_instance.objects["goal_boundaries"]
                if goal_boundaries["x_left"] < pos[0] < goal_boundaries["x_right"] and goal_boundaries["z_bottom"] < \
                        pos[2] < goal_boundaries["z_top"]:
                    print(self.tdw_instance.objects["goal_boundaries"], pos)
                    if self.reward_tracker[tgt_sphere] != 1:
                        self.reward_tracker[tgt_sphere] = 1
                        self.tdw_instance.change_material(tgt_sphere)
        return sum(self.reward_tracker.values())

    def sample_random_action(self):
        return {
            "x": random.randint(-50, 50),
            "z": random.randint(-50, 50)
        }

    def set_observation(self, output=False):
        self.tdw_instance.output_images(output)

    def init_reward(self, objects):
        for sphere in objects["target_spheres"]:
            self.reward_tracker[sphere] = 0

    def reset(self):
        gym_utils.reset_scene(self.tdw_instance, self.tdw_instance.objects)
        self.init_reward(self.tdw_instance.objects)
        self.episode = False

    def _render(self):
        pass

    def _get_reward(self):
        """ Reward is given for XY. """
        pass

    def _seed(self):
        pass

    def close(self):
        # self.tracker.free_up_port()
        gym_utils.kill_tdw(self.tdw_docker_id)
        gym_utils.free_port(self.port)