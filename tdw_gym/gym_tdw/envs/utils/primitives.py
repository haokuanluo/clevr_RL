# from TDW import tdw
from gym_tdw.envs.utils.object_utils import create_object
from gym_tdw.envs.utils.aux_utils import teleport_object, step_one_frame


global_object_creator = {"x": -7.504, "y": 3, "z": -5.012}
global_ptr = 0
global_list = [0,1,2,1,0,0,0,0,0,2,1,0,2,1,0,1,0,1,0,2,1,0,2,0]


def create_ramp(tdw_object, pos, type=1, rot={"x": 0, "y": 90, "z": 0}, scale={"x": 0.1, "y": 0.1, "z": 0.1}):
    global global_object_creator, global_ptr
    global_object_creator["x"] = global_object_creator["x"] - 1.1
    if type == 1:
        ramp = tdw_object.get_unique_id()
        tdw_object.communicate({"$type": "add_objects", "env_id": 0, "objects":
            [{"name": "ramp_with_platform", "position": dict(global_object_creator), "orientation":
                rot, "id": ramp}
             ]})
        name = "ramp_with_platform"
    elif type == 2:
        ramp = tdw_object.get_unique_id()
        tdw_object.communicate({"$type": "add_objects", "env_id": 0, "objects":
            [{"name": "ramp_with_platform_30", "position": dict(global_object_creator), "orientation":
                rot, "id": ramp}
             ]})
        name = "ramp_with_platform_30"
    else:
        ramp = tdw_object.get_unique_id()
        tdw_object.communicate({"$type": "add_objects", "env_id": 0, "objects":
            [{"name": "ramp_with_platform_60", "position": dict(global_object_creator), "orientation":
                rot, "id": ramp}
             ]})
        name = "ramp_with_platform_60"
    tdw_object.communicate([
        {"$type": "scale_object", "id": ramp, "scale_factor": scale},
        {"$type": "teleport_object", "id": ramp, "position": pos},
        {"$type": "set_kinematic_state", "id": ramp, "is_kinematic": True, "use_gravity": False},
        {"$type": "set_visual_material", "id": ramp, "new_material_name": "plastic_microbead_grain_light",
         "object_name": name,
         "old_material_index": 0}
    ])
    return ramp


def create_main_sphere(tdw_object, tele_pos):
    sphere = create_object(tdw_object, "prim_sphere", {"x": -4.825, "y": 3, "z": -5.012})
    tdw_object.communicate(
        {"$type": "set_visual_material", "id": sphere, "new_material_name": "sls_plastic",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    scale = {"x": 0.1, "y": 0.1, "z": 0.1}
    tdw_object.communicate({"$type": "scale_object", "id": sphere, "scale_factor": scale})
    teleport_object(tdw_object, sphere, tele_pos)
    tdw_object.communicate({"$type": "set_semantic_material", "id": sphere})
    tdw_object.communicate({"$type": "set_mass", "id": sphere, "mass": 7.0})
    tdw_object.communicate(
        {"$type": "set_physic_material", "id": sphere, "dynamic_friction": 0.1,
         "static_friction": 0.1,
         "bounciness": 0.1})
    return sphere


def create_target_sphere(tdw_object, pos, tele_pos):
    sphere = create_object(tdw_object, "prim_sphere", pos)
    scale = {"x": 0.1, "y": 0.1, "z": 0.1}
    tdw_object.communicate({"$type": "scale_object", "id": sphere, "scale_factor": scale})
    tdw_object.communicate(
        {"$type": "set_visual_material", "id": sphere, "new_material_name": "plastic_vinyl_glossy_yellow",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw_object.communicate({"$type": "set_mass", "id": sphere, "mass": 1})
    teleport_object(tdw_object, sphere, tele_pos)
    return sphere


def create_cube(tdw_object, profile, pos, tele_pos):
    material_list = ["linen_viscose_classic_pattern",   "plastic_vinyl_glossy_orange", "polyester_sport_fleece_brushed"]
    mass = [100, 10, 50]
    params = [{"$type": "set_physic_material",  "dynamic_friction": 0.1,
         "static_friction": 0.1,
         "bounciness": 0.5},
              {"$type": "set_physic_material",  "dynamic_friction": 0.3,
               "static_friction": 0.3,
               "bounciness": 0.1},
              {"$type": "set_physic_material",  "dynamic_friction": 0.2,
               "static_friction": 0.2,
               "bounciness": 0.9}
              ]

    cube = tdw_object.get_unique_id()
    tdw_object.communicate({"$type": "add_objects", "env_id": 0, "objects":
            [{"name": "prim_cube", "position": pos, "orientation":
                {"x":0, "y":0, "z":0}, "id": cube}
             ]
         })
    tdw_object.communicate([

        {"$type": "set_mass", "id": cube, "mass": mass[profile]},
        {"$type": "scale_object", "id": cube, "scale_factor": {"x": 0.1, "y": 0.1, "z": 0.1}},
        {"$type": "set_visual_material", "id": cube, "new_material_name": material_list[profile],
         "object_name": "PrimCube_0",
         "old_material_index": 0},
        {"$type": "teleport_object", "id": cube, "position": tele_pos}
                        ])

    cube_params = params[profile]
    cube_params['id'] = cube
    tdw_object.communicate(cube_params)
    return cube


def create_cube_breakable(tdw_object, pos, tele_pos, scale={"x":0.1, "y":0.1, "z":0.1}):
    cube = tdw_object.get_unique_id()
    tdw_object.communicate({"$type": "add_objects", "env_id": 0, "objects":
        [{"name": "prim_cone", "position": pos, "orientation":
            {"x": 0, "y": 0, "z": 0}, "id": cube}
         ]
                        })
    tdw_object.communicate([

        {"$type": "set_mass", "id": cube, "mass": 1},
        {"$type": "scale_object", "id": cube, "scale_factor": scale},
        {"$type": "set_visual_material", "id": cube, "new_material_name": "marble_griotte",
         "object_name": "prim_cone_0",
         "old_material_index": 0},
        {"$type": "teleport_object", "id": cube, "position": tele_pos}
    ])
    tdw_object.communicate({"$type": "set_physic_material", "bounciness": 1.0, "dynamic_friction": 1.0, "id": cube, "static_friction": 1.0})

    return cube


def create_wall(tdw_object, x, z, mode, side, length, gap=0.141, profile=None):
    global global_object_creator, global_ptr, global_list
    reset_param = {}
    if profile is None:
        profile = [global_list[i] for i in range(global_ptr, global_ptr + length)]
        global_ptr += length
    idx = 0
    if mode == "h":
        for _ in range(length):
            global_object_creator["x"] = global_object_creator["x"] - 1.1
            pos = dict({"x": x, "y": 0.8749, "z": z})
            cube_id = create_cube(tdw_object, profile[idx], dict(global_object_creator), pos)
            reset_param[cube_id] = pos
            if side == "r":
                x = x + gap
            else:
                x = x - gap
            idx += 1
    if mode == "v":
        for _ in range(length):
            global_object_creator["x"] = global_object_creator["x"] - 1.1
            pos = dict({"x": x, "y": 0.8749, "z": z})
            cube_id = create_cube(tdw_object, profile[idx], dict(global_object_creator), pos)
            reset_param[cube_id] = pos
            if side == "u":
                z = z + gap
            else:
                z = z - gap
            idx += 1
    return reset_param


def create_cyl(tdw_object, profile, tele_pos, rot={"x": 0, "y": 0, "z": 90}, scale={"x": 0.1, "y": 0.1, "z": 0.1}):
    global global_object_creator, global_ptr
    global_object_creator["x"] = global_object_creator["x"] - 1.1
    material_list = ["linen_viscose_classic_pattern", "plastic_vinyl_glossy_orange", "polyester_sport_fleece_brushed"]
    mass = [100, 10, 50]
    params = [{"$type": "set_physic_material", "dynamic_friction": 0.1,
               "static_friction": 0.1,
               "bounciness": 0.5},
              {"$type": "set_physic_material", "dynamic_friction": 0.3,
               "static_friction": 0.3,
               "bounciness": 0.1},
              {"$type": "set_physic_material", "dynamic_friction": 0.2,
               "static_friction": 0.2,
               "bounciness": 0.9}
              ]

    cyl = tdw_object.get_unique_id()
    tdw_object.communicate({"$type": "add_objects", "env_id": 0, "objects":
        [{"name": "prim_cyl", "position": dict(global_object_creator), "orientation":
            rot, "id": cyl}
         ]
                        })
    tdw_object.communicate([
        {"$type": "set_mass", "id": cyl, "mass": mass[profile]},
        {"$type": "scale_object", "id": cyl, "scale_factor": scale},
        {"$type": "set_visual_material", "id": cyl, "new_material_name": material_list[profile],
         "object_name": "PrimCyl_0",
         "old_material_index": 0},
        {"$type": "teleport_object", "id": cyl, "position": tele_pos}
    ])

    cube_params = params[profile]
    cube_params['id'] = cyl
    tdw_object.communicate(cube_params)
    return cyl


def lever(tdw_object, pos, orientation="h", centering=0, side="r"):
    # create_cyl(1, pos, scale={"x": 0.09, "y": 0.3, "z": 0.09})
    # stopper1 = create_cyl(1, {"x": -3.990618, "y": 0.886, "z": -4.208851}, {"x": 0, "y": 0, "z": 0},
    #                       scale={"x": 0.01, "y": 0.06, "z": 0.01})
    # stopper2 = create_cyl(1, {"x": -3.990618, "y": 0.886, "z": -4.307}, {"x": 0, "y": 0, "z": 0},
    #                       scale={"x": 0.01, "y": 0.06, "z": 0.01})
    # tdw.send_to_server({"$type": "set_kinematic_state", "id": stopper1, "is_kinematic": True, "use_gravity": False})
    # tdw.send_to_server({"$type": "set_kinematic_state", "id": stopper2, "is_kinematic": True, "use_gravity": False})
    reset_params = {}
    gap = 0.0522
    stopper1_pos = dict(pos)
    stopper2_pos = dict(pos)
    if orientation == "h":
        cyl_id = create_cyl(tdw_object, 1, pos, rot={"x": 0, "y": 0, "z": 90}, scale={"x": 0.09, "y": 0.3, "z": 0.09})
        reset_params[cyl_id] = {
            "position": dict(pos),
            "rotation": {"x": 0, "y": 0, "z": 90}
        }
        stopper1_pos["z"] = stopper1_pos["z"] - gap
        stopper2_pos["z"] = stopper2_pos["z"] + gap
        if side == "r":
            stopper1_pos["x"] = stopper1_pos["x"] + centering
            stopper2_pos["x"] = stopper2_pos["x"] + centering
        else:
            stopper1_pos["x"] = stopper1_pos["x"] - centering
            stopper2_pos["x"] = stopper2_pos["x"] - centering
        stopper1 = create_cyl(tdw_object, 1, stopper1_pos, {"x": 0, "y": 0, "z": 0},
                              scale={"x": 0.01, "y": 0.06, "z": 0.01})
        stopper2 = create_cyl(tdw_object, 1, stopper2_pos, {"x": 0, "y": 0, "z": 0},
                              scale={"x": 0.01, "y": 0.06, "z": 0.01})
    if orientation == "v":
        cyl_id = create_cyl(tdw_object, 1, pos, rot={"x": 90, "y": 0, "z": 0}, scale={"x": 0.09, "y": 0.2, "z": 0.09})
        reset_params[cyl_id] = {
            "position": dict(pos),
            "rotation": {"x": 90, "y": 0, "z": 0}
        }
        stopper1_pos["x"] = stopper1_pos["x"] - gap
        stopper2_pos["x"] = stopper2_pos["x"] + gap
        if side == "r":
            stopper1_pos["z"] = stopper1_pos["z"] + centering
            stopper2_pos["z"] = stopper2_pos["z"] + centering
        else:
            stopper1_pos["z"] = stopper1_pos["z"] - centering
            stopper2_pos["z"] = stopper2_pos["z"] - centering
        stopper1 = create_cyl(tdw_object, 1, stopper1_pos, {"x": 0, "y": 0, "z": 0},
                              scale={"x": 0.01, "y": 0.06, "z": 0.01})
        stopper2 = create_cyl(tdw_object, 1, stopper2_pos, {"x": 0, "y": 0, "z": 0},
                              scale={"x": 0.01, "y": 0.06, "z": 0.01})

    tdw_object.communicate({"$type": "set_kinematic_state", "id": stopper1, "is_kinematic": True, "use_gravity": False})
    tdw_object.communicate({"$type": "set_kinematic_state", "id": stopper2, "is_kinematic": True, "use_gravity": False})
    return reset_params


def lever_small(tdw_object, pos, orientation="h", centering=0, side="r", lower_stopper=True, upper_stopper=True):

    gap = 0.0522
    stopper1_pos = dict(pos)
    stopper2_pos = dict(pos)
    reset_params = {}
    if orientation == "h":

        cyl_id = create_cyl(tdw_object, 1, pos, rot={"x": 0, "y": 0, "z": 90}, scale={"x": 0.09, "y": 0.2, "z": 0.09})
        reset_params[cyl_id] = {
            "position": dict(pos),
            "rotation": {"x": 0, "y": 0, "z": 90}
        }
        stopper1_pos["z"] = stopper1_pos["z"] - gap
        stopper2_pos["z"] = stopper2_pos["z"] + gap
        if side == "r":
            stopper1_pos["x"] = stopper1_pos["x"] + centering
            stopper2_pos["x"] = stopper2_pos["x"] + centering
        else:
            stopper1_pos["x"] = stopper1_pos["x"] - centering
            stopper2_pos["x"] = stopper2_pos["x"] - centering
        if lower_stopper:
            stopper1 = create_cyl(tdw_object, 1, stopper1_pos, {"x": 0, "y": 0, "z": 0},
                                  scale={"x": 0.01, "y": 0.06, "z": 0.01})
        if upper_stopper:
            stopper2 = create_cyl(tdw_object, 1, stopper2_pos, {"x": 0, "y": 0, "z": 0},
                                  scale={"x": 0.01, "y": 0.06, "z": 0.01})
    if orientation == "v":
        cyl_id = create_cyl(tdw_object, 1, pos, rot={"x": 90, "y": 0, "z": 0}, scale={"x": 0.09, "y": 0.2, "z": 0.09})
        reset_params[cyl_id] = {
            "position": dict(pos),
            "rotation": {"x": 90, "y": 0, "z": 0}
        }
        stopper1_pos["x"] = stopper1_pos["x"] - gap
        stopper2_pos["x"] = stopper2_pos["x"] + gap
        if side == "r":
            stopper1_pos["z"] = stopper1_pos["z"] + centering
            stopper2_pos["z"] = stopper2_pos["z"] + centering
        else:
            stopper1_pos["z"] = stopper1_pos["z"] - centering
            stopper2_pos["z"] = stopper2_pos["z"] - centering
        if lower_stopper:
            stopper1 = create_cyl(tdw_object, 1, stopper1_pos, {"x": 0, "y": 0, "z": 0},
                                  scale={"x": 0.01, "y": 0.06, "z": 0.01})
        if upper_stopper:
            stopper2 = create_cyl(tdw_object, 1, stopper2_pos, {"x": 0, "y": 0, "z": 0},
                                  scale={"x": 0.01, "y": 0.06, "z": 0.01})

    if lower_stopper:
        tdw_object.communicate({"$type": "set_kinematic_state", "id": stopper1, "is_kinematic": True, "use_gravity": False})
    if upper_stopper:
        tdw_object.communicate({"$type": "set_kinematic_state", "id": stopper2, "is_kinematic": True, "use_gravity": False})
    return reset_params


def create_goal(tdw_object, x, z):
    gap = 0.11
    create_wall(tdw_object, x, z, "v", "d", 3, gap=gap, profile=[2]*3)
    create_wall(tdw_object, x + gap, z - 3*gap, "h", "r", 3, gap=gap,profile=[2] * 3)
    create_wall(tdw_object, x + 4*gap, z, "v", "d", 3, gap=gap, profile=[2] * 3)
    boundaries = {
        "z_top": z,
        "z_bottom": z - 0.2281,
        "x_left": x + 0.1012,
        "x_right": x + 0.3381
    }

    return boundaries


def create_breakable_wall(tdw_object, x, z, mode, side, length, gap=0.141, y=0.8749):
    reset_params = {}
    global global_object_creator, global_ptr, global_list
    idx = 0
    if mode == "h":
        for _ in range(length):
            global_object_creator["x"] = global_object_creator["x"] - 1.1
            pos = dict({"x": x, "y": 0.8332242, "z": z})
            wall_id = create_cube_breakable(tdw_object, dict(global_object_creator), pos, scale={"x": 0.1, "y": 0.1, "z": 0.1})

            reset_params[wall_id] = pos
            if side == "r":
                x = x + gap
            else:
                x = x - gap
            idx += 1
    if mode == "v":
        for _ in range(length):
            global_object_creator["x"] = global_object_creator["x"] - 1.1
            pos = dict({"x": x, "y": 0.8332242, "z": z})
            wall_id = create_cube_breakable(tdw_object, dict(global_object_creator), pos, scale={"x": 0.1, "y": 0.1, "z": 0.1})
            reset_params[wall_id] = pos
            if side == "u":
                z = z + gap
            else:
                z = z - gap
            idx += 1
    return reset_params


def create_cube_stack(tdw_object, stack_length, x, z, profiles=None):
    y = 0.8830635
    reset_params = {}
    global global_object_creator, global_ptr, global_list
    idx = 0
    for _ in range(stack_length):
        global_object_creator["x"] = global_object_creator["x"] - 1.1
        new_pos = dict(global_object_creator)
        new_pos["y"] = 0
        if profiles != None and len(profiles) == stack_length:
            pos = {"x": x, "y": y, "z": z}
            cube_id = create_cube(tdw_object, profiles[idx], dict(global_object_creator), pos)
            reset_params[cube_id] = pos
            idx += 1
        y = y + 0.09991
    step_one_frame(tdw_object, 100)
    return reset_params
