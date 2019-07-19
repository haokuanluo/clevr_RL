from gym_tdw.envs.TDW.utils import load_scene_example, step_one_frame
from TDW import tdw
from gym_tdw.envs.utils import primitives, control_tasks, control_task_sol, demonstration
from gym_tdw.envs.utils.object_utils import create_object
from os.path import join
from json import loads
import base64
from PIL import Image
import io
import numpy as np


class SceneState:
    def __init__(self):
        self.collision_data = None
        self.collided = False
        self.object_data = None
        self.object_updated = False
        self.image_1 = None
        self.image_2 = None
        self.image_1_ready = False
        self.image_2_ready = False

    def set_collision_data(self, data):
        self.collision_data = data
        self.collided = True

    def set_object_data(self, data):
        self.object_data = data
        self.object_updated = True

    def parse_collision_data(self):
        collider_id = self.collision_data["collider_id"]
        collidee_id = self.collision_data["collidee_id"]
        return collider_id, collidee_id

    def parse_object_data(self):
        return_data = {}
        for objs in self.object_data:
            if "model_name" in objs.keys():
                return_data[objs["id"]] = {
                    "model_name": objs["model_name"],
                    "position": objs["position"],
                    "velocity": objs["velocity"],
                    "rotation": objs["rotation"],
                    "mass": objs["mass"]
                }
        return return_data

scene_state_data = SceneState()


class puzzle_state():
    def __init__(self, objects):
        self.target_sphere = {}
        for sphere in objects["target_spheres"]:
            self.target_sphere[sphere] = 0
        self.sphere = objects["sphere"]

    def process_collision(self, collider_id, collidee_id):

        if collider_id == self.sphere and collidee_id in list(self.target_sphere.keys()):
            if self.target_sphere[collidee_id] != 1:
                self.target_sphere[collidee_id] = 1

    def get_reward(self):
        return sum(self.target_sphere.values())

    def episode_complete(self):
        for key, value in self.target_sphere.items():
            if value != 1:
                return False
        return True


def load_scene(dir_name):
    load_scene_example(8, 10, 1, dir_name=dir_name)
    tdw.send_to_server({"$type": "set_screen_size", "height": 480, "width": 640})
    # Setup camera 1
    tdw.send_to_server([{"$type": "create_avatar", "type": "A_Img_Caps_Kinematic", "id": "uniqueid1"},
                        {"$type": "teleport_avatar_to", "avatar_id": "uniqueid1", "env_id": 0,
                         "position": {"x": -4.858, "y": 2.169, "z": -6.496}},
                        ])

    tdw.send_to_server({"$type": "set_pass_masks", "avatar_id": "uniqueid1", "pass_masks": ["_img"]})
    tdw.send_to_server({"$type": "rotate_avatar_to_euler_angles", "avatar_id": "uniqueid1", "env_id": 0,
                        "euler_angles": {"x": 41.021, "y": 24.494, "z": 0}})

    # Setup camera 2
    tdw.send_to_server([{"$type": "create_avatar", "type": "A_Img_Caps_Kinematic", "id": "uniqueid2"},
                        {"$type": "teleport_avatar_to", "avatar_id": "uniqueid2", "env_id": 0,
                         "position": {"x": -4.194, "y": 4.108, "z": -4.626}},
                        ])

    tdw.send_to_server({"$type": "set_pass_masks", "avatar_id": "uniqueid2", "pass_masks": ["_img"]})
    tdw.send_to_server({"$type": "rotate_avatar_to_euler_angles", "avatar_id": "uniqueid2", "env_id": 0,
                        "euler_angles": {"x": 90, "y": 0, "z": 0}})

    # Setup environment
    tdw.send_to_server({"$type": "init_enviro_sky"})
    tdw.send_to_server({"$type": "set_time_of_day", "hour": 13.0})
    tdw.send_to_server({"$type": "set_post_process", "value": True})
    tdw.send_to_server({"$type": "set_shadows", "value": True})

    # Setup table
    step_one_frame(40)
    ramp = create_object("billiardtable", {"x": -4.125461, "y": 0.0, "z": -4.608}, {"x": 0.0, "y": 0.0, "z": 0.0})
    tdw.send_to_server({"$type": "set_kinematic_state", "id": ramp, "is_kinematic": True, "use_gravity": False})


def on_recv(messages):
    """
    Example on_recv callback.

    :param messages: The received messages.
    """

    # Create the image save directory.
    global avatar_ball_collision, object_data, objects_ready, image_count1,image_count2, task, scene_state_data
    tdw.global_message_count += 1

    for message_dict in messages:
        # Convert the byte array to a JSON object.
        message_dict = loads(message_dict)

        if message_dict["$type"] == "objects_data":
            scene_state_data.set_object_data(message_dict["objects"])

        if "collision" in message_dict["$type"]:
            scene_state_data.set_collision_data(message_dict)
        # Grab image data
        if message_dict["$type"] == "image_data":

            for image_pass in message_dict["passes"]:
                image_bytes = base64.decodebytes(image_pass["image"].encode('utf-8'))
                image = Image.open(io.BytesIO(image_bytes))

                if message_dict["avatar_id"] == "uniqueid1":
                    print("image 1 added")
                    scene_state_data.image_1 = np.array(image)
                    scene_state_data.image_1_ready = True

                else:
                    print("image 2 added")
                    scene_state_data.image_2 = np.array(image)
                    scene_state_data.image_2_ready = True


def on_send():
    """
    Example on_send callback.
    """
    print("Sent a message!")


def setup_connection():
    tdw.set_controller_id(tdw.get_unique_id())
    tdw.connect_send_to_server_socket("tcp://52.116.149.123:", 1339)
    tdw.connect_recv_from_server_socket("tcp://52.116.149.123:", 1340)
    t = tdw.thread(tdw.run, args=[on_send, on_recv])
    return t


def load_puzzle(puzzle=1):
    if puzzle == 1:
        objects = control_tasks.control_task1()
        return objects


def take_action(objects, actions):
    # If there is no force skip sending this command to save computation
    if actions["x"] != 0 or actions["z"] != 0:
        tdw.send_to_server([{"$type": "apply_force_to_object", "force": {"x": actions["x"], "y": 0, "z": actions["z"]},
                            "id": objects["sphere"]}, {"$type": "get_objects_data"}])
    else:
        tdw.send_to_server([{"$type": "step_physics", "frames": 0}, {"$type": "get_objects_data"}])


def set_output(output):
    tdw.send_to_server([{"$type": "set_avatar_output", "avatar_id": "uniqueid1", "env_id": 0, "images": output,
                        "object_info": True, "avatar_info": True, "child_info": True,
                        "collision_info": True, "sensors_info": True}, {"$type": "set_avatar_output", "avatar_id": "uniqueid2", "env_id": 0, "images": output,
                        "object_info": True, "avatar_info": True, "child_info": True,
                        "collision_info": True, "sensors_info": True}])


def update_info():
    tdw.send_to_server({"$type": "get_objects_data"})