from gym_tdw.envs.utils import primitives
from TDW.utils import step_one_frame
from gym_tdw.envs.utils.object_utils import create_object, teleport_object
from TDW import tdw


def puzzle_6():
    sphere = primitives.create_main_sphere({"x": -4.536, "y": 0.8749, "z":-3.762})
    ramp1 = primitives.create_ramp({"x": -4.349, "y": 0.8285, "z": -4.249}, rot={"x": 0, "y": 90, "z": 0}, scale=0.08)
    # ramp2 = primitives.create_ramp({"x": -4.564, "y": 0.8285, "z": -4.24}, rot={"x": 0, "y": 90, "z": 0}, scale=0.08)
    # ramp3 = primitives.create_ramp({"x": -4.193, "y": 0.83, "z": -3.871}, rot={"x": 0, "y": 0, "z": 0}, type=3, scale=0.08)
    # ramp4 = primitives.create_ramp({"x": -3.967, "y": 0.83, "z": -3.612}, rot={"x": 0, "y": 180, "z": 0}, type=3,
    #                                scale=0.08)
    # ramp5 = primitives.create_ramp({"x": -3.79, "y": 0.83, "z": -4.927}, rot={"x": 0, "y": 90, "z": 0}, type=2, scale=0.08)

    primitives.lever({"x": -4.104, "y": 0.8827949, "z": -4.679}, orientation="h", centering=-0.13, side="r")


    # primitives.create_wall(-4.274, -4.368, "v", "u", 3, profile=[2]*6)


    # primitives.create_wall(-3.9, -4.076, "h", "r", 3, profile=[2, 1, 0])
    # primitives.create_wall(-3.605, -4.804, "v", "d", 2, profile=[1, 1])
    target_spheres = []
    goal_boundaries = primitives.create_goal(-4.657, -5.333)
    target_spheres.append(primitives.create_target_sphere({"x": -19.787, "y": 3, "z": -5.012}, {"x":-4.059,"y":0.8749,"z":-4.573}))
    target_spheres.append(primitives.create_target_sphere({"x": -20.787, "y": 3, "z": -5.012}, {"x": -3.723, "y": 0.8749, "z": -5.102}))
    target_spheres.append(primitives.create_target_sphere({"x": -21.787, "y": 3, "z": -5.012}, {"x":-4.357,"y":0.8749,"z":-4.784}))

    return {"sphere": sphere,
            "target_spheres": target_spheres,
            "goal_boundaries": goal_boundaries}


def puzzle_5():
    sphere = primitives.create_main_sphere({"x": -3.941007, "y": 0.8749, "z": -4.725})
    ramp1 = primitives.create_ramp({"x": -3.868, "y": 0.8285, "z": -4.428}, rot={"x": 0, "y": -90, "z": 0},
                                   scale=0.08)
    ramp2 = primitives.create_ramp({"x": -3.75, "y": 0.8285, "z": -3.841}, rot={"x": 0, "y": 90, "z": 0},
                                   scale=0.08)

    # ramp3 = primitives.create_ramp({"x": -4.171, "y": 0.8285, "z": -5.243}, rot={"x": 0, "y": 0, "z": 0},
    #                                scale=0.08, type=1)

    ramp4 = primitives.create_ramp({"x": -4.236, "y": 0.8285, "z": -5.372}, rot={"x": 0, "y": 0, "z": 0},
                                   scale=0.08, type=2)
    # ramp4 = primitives.create_ramp({"x": -4.178, "y": 0.8285, "z": -5.572}, rot={"x": 0, "y": 0, "z": 0},
    #                                scale=0.08, type=3)

    primitives.lever_small({"x":-4.364, "y": 0.8827949, "z": -4.927}, centering=0.07, upper_stopper=False)
    primitives.create_wall(-4.205, -4.069, "v", "u", 4, profile=[2] * 6)
    primitives.create_wall(-4.042, -4.083, "h", "r", 4, profile=[2] * 6)
    primitives.create_wall(-4.673, -4.931, "h", "r", 1, profile=[2])
    primitives.create_wall(-4.072, -4.975, "h", "r", 4, profile=[2]*5)
    primitives.create_wall(-4.072, -5.146, "h", "r", 1, profile=[1])
    primitives.create_wall(-4.095, -5.591, "h", "r", 1, profile=[1])
    break_ids = []
    break_ids.extend(primitives.create_breakable_wall(-4.509, -4.532, "h", "r", 1))
    break_ids.extend(primitives.create_breakable_wall(-3.622, -4.79, "h", "r", 1))
    target_spheres = []
    target_spheres.append(primitives.create_target_sphere({"x": -19.787, "y": 3, "z": -5.012}, {"x": -3.944025, "y": 0.8749, "z": -3.794}))
    target_spheres.append(primitives.create_target_sphere({"x": -20.787, "y": 3, "z": -5.012}, {"x": -4.501, "y": 0.8749, "z": -5.309}))
    target_spheres.append(primitives.create_target_sphere({"x": -21.787, "y": 3, "z": -5.012}, {"x": -3.644, "y": 0.8749, "z": -5.436}))
    return {"sphere": sphere,
            "walls": break_ids,
            "target_spheres": target_spheres
            }


def puzzle_3():
    main_sphere = primitives.create_main_sphere({"x": -4.46, "y": 0.8749, "z": -3.944})
    primitives.create_wall(-4.433, -4.305, "h", "r", 1)
    primitives.create_wall(-3.807, -4.305, "h", "r", 2)
    primitives.create_wall(-3.948, -4.446, "v", "d", 3)
    # create_wall(-4.048, -3.62, "v", "d", 3)
    primitives.create_wall(-3.907, -3.901999, "h", "r", 3)
    # create_wall(-3.948, -5.01, "h", "r", 3)
    target_spheres = []
    sphere = primitives.create_target_sphere({"x": -17.504, "y": 3, "z": -5.012}, {"x": -4.246, "y": 0.8749, "z": -5.33})
    target_spheres.append(sphere)
    target_spheres.append(primitives.create_target_sphere({"x": -18.504, "y": 3, "z": -5.012}, {"x": -3.764, "y": 0.8749, "z": -3.685}))
    target_spheres.append(primitives.create_target_sphere({"x": -19.504, "y": 3, "z": -5.012}, {"x": -3.692, "y": 0.8749, "z": -4.551}))
    primitives.create_cube_stack(2, -4.431, -5.027, [1, 1])
    primitives.teleport_object(sphere, {"x": -4.431, "y": 1.082928, "z": -5.027})

    return {"sphere":main_sphere,
            "target_spheres": target_spheres
            }


def puzzle_2():
    main_sphere = primitives.create_main_sphere({"x": -3.601, "y": 0.8749, "z": -3.608})
    primitives.create_wall(-3.781, -4.444, "h", "r", 2)
    primitives.create_wall(-4.158, -4.914, "v", "d", 3)
    sphere = primitives.create_target_sphere({"x": -17.504, "y": 3, "z": -5.012}, {"x": -4.246, "y": 0.8749, "z": -5.33})
    target_spheres = []
    target_spheres.append(sphere)
    target_spheres.append(primitives.create_target_sphere({"x": -18.504, "y": 3, "z": -5.012}, {"x": -3.954, "y": 0.8749, "z": -5.197}))
    target_spheres.append(primitives.create_target_sphere({"x": -19.504, "y": 3, "z": -5.012}, {"x": -3.622, "y": 0.8749, "z": -4.589}))
    primitives.create_cube_stack(2, -4.11, -4.072, [1, 0])
    primitives.teleport_object(sphere, {"x": -4.11, "y": 1.082928, "z": -4.072})
    return {"sphere":main_sphere,
            "target_spheres": target_spheres
            }


def puzzle_4():
    sphere = primitives.create_main_sphere({"x": -4.533, "y": 0.8749, "z": -3.688})
    target_spheres = []
    target_spheres.append(primitives.create_target_sphere({"x": -19.787, "y": 3, "z": -5.012}, {"x": -4.492, "y": 0.8749, "z": -4.459}))
    target_spheres.append(primitives.create_target_sphere({"x": -23.787, "y": 3, "z": -5.012}, {"x": -4.072, "y": 0.8749, "z": -3.899}))
    target_spheres.append(primitives.create_target_sphere({"x": -25.787, "y": 3, "z": -5.012}, {"x": -3.921, "y": 0.8749, "z": -4.52}))
    # target_spheres.append(
    #     primitives.create_target_sphere({"x": -19.787, "y": 3, "z": -5.012}, {"x": -4.215, "y": 0.8749, "z": -5.185}))
    # target_spheres.append(
    #     primitives.create_target_sphere({"x": -23.787, "y": 3, "z": -5.012}, {"x": -4.027, "y": 0.8749, "z": -5.152}))
    # target_spheres.append(
    #     primitives.create_target_sphere({"x": -25.787, "y": 3, "z": -5.012}, {"x": -4.076, "y": 0.8749, "z": -4.935}))
    primitives.create_wall(-4.387, -4.129, "h", "r", 5)
    primitives.create_wall(-4.092, -4.437, "v", "d", 3, profile=[0,1,2])
    goal_boundaries = primitives.create_goal(-4.349, -5.086)
    return_objects = {
        "sphere": sphere,
        "target_spheres": target_spheres,
        "goal_boundaries": goal_boundaries
    }
    return return_objects


def puzzle_7():
    sphere = primitives.create_main_sphere({"x": -3.677, "y": 0.8749, "z": -5.253})
    primitives.create_cyl(1, {"x": -4.101419, "y": 0.8827949, "z": -4.254929}, scale={"x": 0.09, "y": 0.3, "z": 0.09})
    stopper1 = primitives.create_cyl(1, {"x": -3.990618, "y": 0.886, "z": -4.208851}, {"x": 0, "y": 0, "z": 0}, scale={"x": 0.01, "y": 0.06, "z": 0.01})
    stopper2 = primitives.create_cyl(1, {"x": -3.990618, "y": 0.886, "z": -4.307}, {"x": 0, "y": 0, "z": 0}, scale={"x": 0.01, "y": 0.06, "z": 0.01})
    tdw.send_to_server({"$type": "set_kinematic_state", "id": stopper1, "is_kinematic": True, "use_gravity": False})
    tdw.send_to_server({"$type": "set_kinematic_state", "id": stopper2, "is_kinematic": True, "use_gravity": False})
    target_sphere = []
    target_sphere.append(primitives.create_target_sphere({"x": -19.787, "y": 3, "z": -5.012}, {"x": -4.352, "y": 0.883, "z": -4.372}))
    target_sphere.append(primitives.create_target_sphere({"x": -20.787, "y": 3, "z": -5.012}, {"x": -4.446, "y": 0.883, "z": -5.487}))
    target_sphere.append(primitives.create_target_sphere({"x": -21.787, "y": 3, "z": -5.012}, {"x": -3.663, "y": 0.883, "z": -3.679}))
    primitives.create_ramp({"x": -4.374, "y": 0.8304, "z": -4.689}, type=2, rot={"x":0, "y":90, "z":0})
    primitives.create_wall(-4.024, -4.414,"v", "d", 2, profile=[2,2,2])
    primitives.create_wall(-4.168, -4.661, "v", "d", 1, profile=[2])
    primitives.create_wall(-4.574, -4.35, "v", "u", 2, profile=[2, 2])
    primitives.create_wall(-4.427, -4.111, "h", "r", 2, profile=[2, 2, 2])
    primitives.create_wall(-4.2, -5.361, "v", "d", 2, profile=[1, 2])
    return {"sphere":sphere,
            "target_spheres": target_sphere}


def control_task_cyl_1():
    sphere = primitives.create_main_sphere({"x":-4.147, "y": 0.8749, "z": -5.248})
    cyl = primitives.create_cyl(1, {"x": -4.159, "y": 0.8749, "z": -4.578})
    return {"sphere": sphere}


def control_task_wall():
    sphere = primitives.create_main_sphere({"x": -4.262, "y": 0.8749, "z": -5.248})
    wall_ids = []
    target_sphere = primitives.create_target_sphere({"x": -17.504, "y": 3, "z": -5.012}, {"x": -4.46, "y": 0.8749, "z": -3.944})
    wall_ids.extend(primitives.create_breakable_wall(-4.521, -4.492, "h", "r", 4, gap=0.11))
    # wall_ids.extend(create_breakable_wall(-4.497, -4.492, "h", "r", 4, gap=0.11, y=0.98399))
    # wall_ids.extend(create_breakable_wall(-4.521, -4.492, "h", "r", 4, gap=0.11, y=1.0836))
    # tdw.send_to_server({"$type": "set_semantic_material_to", "id": sphere, "material_type": "Wood"})

    return {"sphere": sphere,
            "walls": wall_ids,
            "target": target_sphere}


def puzzle_1():

    material_list = ["polyester_sport_fleece_brushed", "sls_plastic", "metallic_car_paint", "carbon_fiber_twill_weave",
                     "plastic_vinyl_glossy_orange", "plastic_hammered"]

    sphere = primitives.create_main_sphere({"x": -4.093, "y": 0.8749, "z": -5.463})
    # sphere = primitives.create_main_sphere({"x": -4.522, "y": 0.8749, "z": -4.51})
    target_spheres = []
    target_spheres.append(primitives.create_target_sphere({"x": -17.504, "y": 3, "z": -5.012}, {"x": -4.46, "y": 0.8749, "z": -3.944}))
    # target_spheres.append(
    #     primitives.create_target_sphere({"x": -17.504, "y": 3, "z": -5.012}, {"x": -4.158, "y": 0.8749, "z": -4.502}))

    scale = 0.1

    # tdw.send_to_server({"$type": "set_mass", "id": cube, "mass": 75.0})
    # tdw.send_to_server({"$type": "set_mass", "id": cube2, "mass": 15.0})

    tdw.send_to_server({"$type": "set_mass", "id": sphere, "mass": 7.0})
    # tdw.send_to_server({"$type": "scale_object", "id": cube, "scale_factor": scale})
    # tdw.send_to_server({"$type": "scale_object", "id": cube2, "scale_factor": scale})
    # tdw.send_to_server({"$type": "scale_object", "id": cube3, "scale_factor": scale})

    # teleport_object(cube, {"x": -4.578, "y": 0.8749, "z": -4.196})
    # teleport_object(cube2, {"x": -4.413, "y": 0.8749, "z": -4.196})
    # teleport_object(cube3, {"x": -4.247, "y": 0.8749, "z": -4.196})
    primitives.create_wall(-4.578, -4.196, "h", "r", 3)
    primitives.create_wall(-4.254, -5.288, "h", "r", 3)
    primitives.create_wall(-4.246, -4.761, "h", "r", 3)
    primitives.create_wall(-3.806, -4.537, "h", "r", 2)
    primitives.create_wall(-4.41, -5.483, "h", "r", 1)
    primitives.create_wall(-4.157, -3.991, "h", "r", 1)
    return {"sphere": sphere,
            "target_spheres": target_spheres}


def stacked_cube_sphere():
    material_list = ["plastic_vinyl_glossy_orange", "sls_plastic", "metallic_car_paint", "carbon_fiber_twill_weave",
                     "plastic_vinyl_glossy_orange", "plastic_hammered"]

    sphere = create_object("prim_sphere", {"x": -7.825, "y": 0, "z": -8.012})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere, "new_material_name": "sls_plastic",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    scale = 0.1
    tdw.send_to_server({"$type": "scale_object", "id": sphere, "scale_factor": scale})
    tdw.send_to_server({"$type": "set_mass", "id": sphere, "mass": 7.0})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere, "dynamic_friction": 0.1,
         "static_friction": 0.1,
         "bounciness": 0.1})
    sphere_target = primitives.create_target_sphere({"x": -17.504, "y": 0, "z": -5.012}, {"x": -4.46, "y": 0.8749, "z": -3.944})

    scale = 0.1

    tdw.send_to_server({"$type": "set_mass", "id": sphere, "mass": 7.0})

    tdw.send_to_server({"$type": "stop_object", "id": sphere_target})

    tdw.send_to_server({"$type": "stop_object", "id": sphere_target})
    teleport_object(sphere, {"x": -4.469, "y": 1.193, "z": -3.829})

    primitives.create_wall(-4.653, -4.305, "h", "r", 5)
    primitives.create_wall(-3.807, -4.305, "h", "r", 2)
    primitives.create_wall(-3.948, -4.446, "v", "d", 4)
    # create_wall(-4.048, -3.62, "v", "d", 3)
    # create_wall(-3.907, -3.901999, "h", "r", 3)
    # create_wall(-3.948, -5.01, "h", "r", 3)
    primitives.create_cube_stack(3, -3.678, -4.673)

    teleport_object(sphere_target, {"x": -3.678, "y": 1.182574, "z": -4.673})
    step_one_frame(40)
    return {"sphere": sphere}


def three_ball_config():
    # Teleport objects
    sphere = create_object("prim_sphere", {"x": -4.825, "y": 3, "z": -5.012})
    sphere2 = create_object("prim_sphere", {"x": -3.545, "y": 0.3447, "z": -5.012})
    # sphere3 = create_object("prim_sphere", {"x": -2.349609, "y": 3, "z": -5.012})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere, "new_material_name": "marble_griotte", "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere2, "new_material_name": "ceramic_porcelain", "object_name": "PrimSphere_0",
         "old_material_index": 0})
    # tdw.send_to_server(
    #     {"$type": "set_visual_material", "id": sphere3, "new_material_name": "wood_beech_mid_brown", "object_name": "PrimSphere_0",
    #      "old_material_index": 0})
    tdw.send_to_server({"$type": "scale_object", "id": sphere, "scale_factor": 0.1})
    tdw.send_to_server({"$type": "scale_object", "id": sphere2, "scale_factor": 0.1})
    # tdw.send_to_server({"$type": "scale_object", "id": sphere3, "scale_factor": 0.1})

    teleport_object(sphere, {"x": -3.359, "y": 0.347, "z": -4.808})
    teleport_object(sphere2, {"x": -3.04, "y": 0.347, "z": -4.808})
    # teleport_object(sphere3, {"x": -2.721, "y": 0.347, "z": -4.808})

    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere, "dynamic_friction": 0.1,
         "static_friction": 0.3,
         "bounciness": 0.5})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere2, "dynamic_friction": 0.5,
         "static_friction": 0.5,
         "bounciness": 0.5})
    # tdw.send_to_server(
    #     {"$type": "set_physic_material", "id": sphere3, "dynamic_friction": 0.8,
    #      "static_friction": 0.8,
    #      "bounciness": 0.5})

    return sphere, sphere2


def ball_cube_config():
    sphere = create_object("prim_sphere", {"x": -4.825, "y": 3, "z": -5.012})
    sphere2 = create_object("prim_sphere", {"x": -3.51, "y": 3, "z": -5.012})
    sphere3 = create_object("prim_sphere", {"x": -2.349609, "y": 3, "z": -5.012})
    cube = create_object("prim_sphere", {"x": -7.504, "y": 3, "z": -5.012})
    sphere4 = create_object("prim_sphere", {"x": -1.186, "y": 3, "z": -5.012})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere, "new_material_name": "marble_griotte",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere2, "new_material_name": "ceramic_porcelain",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere3, "new_material_name": "wood_beech_mid_brown",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server({"$type": "scale_object", "id": sphere, "scale_factor": 0.1})
    tdw.send_to_server({"$type": "scale_object", "id": sphere2, "scale_factor": 0.1})
    tdw.send_to_server({"$type": "scale_object", "id": sphere3, "scale_factor": 0.1})
    tdw.send_to_server({"$type": "scale_object", "id": cube, "scale_factor": 0.1})
    tdw.send_to_server({"$type": "scale_object", "id": sphere4, "scale_factor": 0.1})

    teleport_object(sphere, {"x": -3.388, "y": 0.347, "z": -4.879})
    teleport_object(sphere2, {"x": -3.104, "y": 0.347, "z": -5.158})
    teleport_object(sphere3, {"x": -3.104, "y": 0.347, "z": -4.648})
    teleport_object(cube, {"x": -2.742, "y": 0.347, "z": -4.091})
    teleport_object(sphere4, {"x": -2.742, "y": 0.347, "z": -3.9})

    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere, "dynamic_friction": 0.1,
         "static_friction": 0.3,
         "bounciness": 0.5})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere2, "dynamic_friction": 0.5,
         "static_friction": 0.5,
         "bounciness": 0.5})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere3, "dynamic_friction": 0.8,
         "static_friction": 0.8,
         "bounciness": 0.5})

    return sphere, sphere2, sphere3,  sphere4


def control_task__simple_cubes():
    material_list = ["synthetic_eco_lor_french_terry", "sls_plastic", "metallic_car_paint", "carbon_fiber_twill_weave", "plastic_vinyl_glossy_orange", "plastic_hammered"]

    sphere = create_object("prim_sphere", {"x": -4.825, "y": 3, "z": -5.012})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere, "new_material_name": material_list[1],
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    scale = 0.1
    tdw.send_to_server({"$type": "scale_object", "id": sphere, "scale_factor": scale})
    teleport_object(sphere, {"x": -4.46, "y": 0.8749, "z": -3.944})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere, "dynamic_friction": 0.1,
         "static_friction": 0.1,
         "bounciness": 0.1})

    cube = create_object("prim_cube", {"x": -7.504, "y": 3, "z": -5.012})
    cube2 = create_object("prim_cube", {"x": -10.504, "y": 3, "z": -5.012})
    cube3 = create_object("prim_cube", {"x": -13.504, "y": 3, "z": -5.012})
    cube4 = create_object("prim_cube", {"x": -15.504, "y": 3, "z": -5.012})
    cube5 = create_object("prim_cube", {"x": -17.504, "y": 3, "z": -5.012})
    cube6 = create_object("prim_cube", {"x": -19.504, "y": 3, "z": -5.012})
    cube7 = create_object("prim_cube", {"x": -21.504, "y": 3, "z": -5.012})
    sphere5 = create_object("prim_sphere", {"x": -19.787, "y": 3, "z": -5.012})
    sphere6 = create_object("prim_sphere", {"x": -23.787, "y": 3, "z": -5.012})
    sphere7 = create_object("prim_sphere", {"x": -25.787, "y": 3, "z": -5.012})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube, "new_material_name": material_list[0],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube2, "new_material_name": material_list[4],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube3, "new_material_name": material_list[4],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube4, "new_material_name": material_list[5],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube5, "new_material_name": material_list[0],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube6, "new_material_name": material_list[0],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": cube7, "new_material_name": material_list[5],
         "object_name": "PrimCube_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere5, "new_material_name": "plastic_vinyl_glossy_yellow",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere6, "new_material_name": "plastic_vinyl_glossy_yellow",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server(
        {"$type": "set_visual_material", "id": sphere7, "new_material_name": "plastic_vinyl_glossy_yellow",
         "object_name": "PrimSphere_0",
         "old_material_index": 0})
    tdw.send_to_server({"$type": "set_mass", "id": cube, "mass": 75.0})
    tdw.send_to_server({"$type": "set_mass", "id": cube2, "mass": 15.0})
    tdw.send_to_server({"$type": "set_mass", "id": cube3, "mass": 15.0})
    tdw.send_to_server({"$type": "set_mass", "id": cube4, "mass": 45.0})
    tdw.send_to_server({"$type": "set_mass", "id": cube5, "mass": 75.0})
    tdw.send_to_server({"$type": "set_mass", "id": cube6, "mass": 75.0})
    tdw.send_to_server({"$type": "set_mass", "id": cube7, "mass": 45.0})
    tdw.send_to_server({"$type": "set_mass", "id": sphere, "mass": 7.0})
    tdw.send_to_server({"$type": "scale_object", "id": cube, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": cube2, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": cube3, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": cube4, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": cube5, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": cube6, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": cube7, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": sphere5, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": sphere6, "scale_factor": scale})
    tdw.send_to_server({"$type": "scale_object", "id": sphere7, "scale_factor": scale})

    teleport_object(cube, {"x": -4.512, "y": 0.8749, "z": -4.305})
    teleport_object(cube2, {"x": -3.651, "y": 0.8749, "z": -4.577})
    teleport_object(cube3, {"x": -4.14, "y": 0.8749, "z": -5.015})
    teleport_object(cube4, {"x": -4.065, "y": 0.8749, "z": -4.299})
    teleport_object(cube5, {"x": -3.726, "y": 0.8749, "z": -4.85})
    teleport_object(cube6, {"x": -4.317, "y": 0.8749, "z": -4.727})
    teleport_object(cube7, {"x": -4.565, "y": 0.8749, "z": -4.82})
    teleport_object(sphere5, {"x": -4.431, "y": 0.8749, "z": -5.027})
    teleport_object(sphere6, {"x":-3.853, "y": 0.8749, "z": -5.051})
    teleport_object(sphere7, {"x": -3.913, "y": 0.8749, "z": -4.551})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": sphere, "dynamic_friction": 0.9,
         "static_friction": 0.9,
         "bounciness": 0.1})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube, "dynamic_friction": 0.9,
         "static_friction": 0.9,
         "bounciness": 0.5})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube2, "dynamic_friction": 0.1,
         "static_friction": 0.1,
         "bounciness": 0.1})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube3, "dynamic_friction": 0.1,
         "static_friction": 0.1,
         "bounciness": 0.1})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube4, "dynamic_friction": 0.5,
         "static_friction": 0.5,
         "bounciness": 0.9})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube5, "dynamic_friction": 0.9,
         "static_friction": 0.9,
         "bounciness": 0.5})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube6, "dynamic_friction": 0.9,
         "static_friction": 0.9,
         "bounciness": 0.5})
    tdw.send_to_server(
        {"$type": "set_physic_material", "id": cube7, "dynamic_friction": 0.5,
         "static_friction": 0.5,
         "bounciness": 0.9})


    return_objects = {
        "sphere": sphere,
        "cube": cube,
        "cube2": cube2,
        "cube3": cube3,
        "cube4": cube4,
        "cube5": cube5,
        "cube6": cube6
    }

    return return_objects