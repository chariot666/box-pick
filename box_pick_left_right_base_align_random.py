from __future__ import annotations

import argparse
import random
import re
import sys
import types
from pathlib import Path

import numpy as np

DEFAULT_URDF_PATH = (
    "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/models/urdf/mmk2_s_g2.urdf"
)
DEFAULT_DISCOVERSE_ROOT = "D:/thingscatch/DISCOVERSE-main/DISCOVERSE"
DEFAULT_MJCF_FILE_PATH = (
    "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/"
    "models/mjcf/tasks_mmk2/task1_pick_and_place.xml"
)
DEFAULT_BOX_CENTER_Y = 0.715

__all__ = [
    "grasp_object",
    "move_robot_to_table_front",
    "prepare_table_front_pose",
    "main",
]


def choose_scene_params(seed, dy_range, fixed_dy):
    actual_seed = random.randrange(0, 2**31) if seed is None else int(seed)
    rng = random.Random(actual_seed)
    box_dy = (
        float(fixed_dy)
        if fixed_dy is not None
        else rng.uniform(-float(dy_range), float(dy_range))
    )
    return actual_seed, box_dy


def _replace_once(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"{label} was not found")
    return text.replace(old, new, 1)


def _replace_last(text, old, new, label):
    pos = text.rfind(old)
    if pos < 0:
        raise RuntimeError(f"{label} was not found")
    return text[:pos] + new + text[pos + len(old) :]


def _install_wam_stubs():
    class _DummyWAM:
        legacy_transport_labels = False

        def __init__(self, *args, **kwargs):
            pass

        def add(self, *args, **kwargs):
            return None

        def flush(self, *args, **kwargs):
            return None

        def predict(self, *args, **kwargs):
            return {
                "safe": 0.0,
                "four_finger_contact": 0.0,
                "transport_ready": 0.0,
                "slot_ready": 0.0,
            }

    for module_name in ("wam_critic", "action_wam", "visual_wam"):
        stub = types.ModuleType(module_name)
        stub.WAMCritic = _DummyWAM
        stub.WAMCriticRecorder = _DummyWAM
        stub.ActionWAMCritic = _DummyWAM
        stub.VisualWAMCritic = _DummyWAM
        stub.VisualWAMRecorder = _DummyWAM
        sys.modules[module_name] = stub


def _normalize_world_point(point):
    if point is None:
        return None
    arr = np.asarray(point, dtype=float).reshape(-1)
    if arr.size != 3:
        raise ValueError(f"world point must have 3 values, got {arr.size}")
    return arr.tolist()


def _load_patched_box_pick_module(
    external_box_dy,
    external_target_world=None,
    external_base_position=None,
    move_only=False,
    startup_only=False,
):
    source_path = Path(__file__).with_name("box_pick.py")
    source_text = source_path.read_text(encoding="utf-8")

    source_text = _replace_once(
        source_text,
        '        "enabled": bool(randomize_scene),\n',
        '        "enabled": bool(randomize_scene or external_randomized_box_dy is not None),\n',
        "scene_randomization enabled flag",
    )

    source_text = _replace_once(
        source_text,
        "    scene_rng = np.random.default_rng(int(scene_seed))\n",
        "    scene_rng = np.random.default_rng(int(scene_seed))\n"
        '    external_randomized_box_dy = globals().get("EXTERNAL_RANDOMIZED_BOX_DY", None)\n',
        "external box dy hook",
    )

    if external_base_position is not None:
        source_text = _replace_last(
            source_text,
            '    cfg.init_state["base_position"] = [0.58, 0.715, 0.0]\n',
            "    cfg.init_state[\"base_position\"] = "
            f"{list(np.asarray(external_base_position, dtype=float).tolist())}\n",
            "base position override",
        )

    randomization_old = (
        "    if randomize_scene:\n"
        "        box_body_id_random = int(sim_node.mj_model.body(target_body_name).id)\n"
        "        box_joint_id_random = int(sim_node.mj_model.body_jntadr[box_body_id_random])\n"
        "        box_qpos_adr_random = int(\n"
        "            sim_node.mj_model.jnt_qposadr[box_joint_id_random]\n"
        "        )\n"
        "        scene_randomization.update({\n"
        "            \"box_dx\": 0.0,\n"
        "            \"box_dy\": 0.0,\n"
        "            \"box_yaw_deg\": 0.0,\n"
        "            \"mass_kg\": float(scene_rng.uniform(0.35, 0.80)),\n"
        "            \"friction_coefficient\": float(scene_rng.uniform(0.15, 0.25)),\n"
        "            \"target_dx_error\": 0.0,\n"
        "            \"target_dz_error\": 0.0,\n"
        "        })\n"
        "        sim_node.mj_data.qpos[box_qpos_adr_random] += scene_randomization[\"box_dx\"]\n"
        "        sim_node.mj_data.qpos[box_qpos_adr_random + 1] += scene_randomization[\"box_dy\"]\n"
        "        yaw = np.deg2rad(scene_randomization[\"box_yaw_deg\"])\n"
        "        # MuJoCo free-joint quaternion order is w, x, y, z.\n"
        "        sim_node.mj_data.qpos[box_qpos_adr_random + 3:box_qpos_adr_random + 7] = [\n"
        "            np.cos(0.5 * yaw), 0.0, 0.0, np.sin(0.5 * yaw)\n"
        "        ]\n"
        "        scene_randomization[\"mass_scale\"] = (\n"
        "            scene_randomization[\"mass_kg\"] / nominal_box_mass_kg\n"
        "        )\n"
        "        scene_randomization[\"friction_scale\"] = (\n"
        "            scene_randomization[\"friction_coefficient\"] / 0.18\n"
        "        )\n"
        "        sim_node.mj_model.body_mass[box_body_id_random] = scene_randomization[\"mass_kg\"]\n"
        "        sim_node.mj_model.body_inertia[box_body_id_random] = (\n"
        "            scene_randomization[\"mass_kg\"]\n"
        "            / nominal_box_mass_kg\n"
        "            * sim_node.mj_model.body_inertia[box_body_id_random]\n"
        "        )\n"
        "        geom_start = int(sim_node.mj_model.body_geomadr[box_body_id_random])\n"
        "        geom_num = int(sim_node.mj_model.body_geomnum[box_body_id_random])\n"
        "        sim_node.mj_model.geom_friction[\n"
        "            geom_start:geom_start + geom_num, 0\n"
        "        ] = scene_randomization[\"friction_coefficient\"]\n"
        "        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)\n"
    )
    randomization_new = (
        "    if randomize_scene or external_randomized_box_dy is not None:\n"
        "        box_body_id_random = int(sim_node.mj_model.body(target_body_name).id)\n"
        "        box_joint_id_random = int(sim_node.mj_model.body_jntadr[box_body_id_random])\n"
        "        box_qpos_adr_random = int(\n"
        "            sim_node.mj_model.jnt_qposadr[box_joint_id_random]\n"
        "        )\n"
        "        scene_randomization.update({\n"
        "            \"box_dx\": 0.0,\n"
        "            \"box_dy\": float(external_randomized_box_dy) if external_randomized_box_dy is not None else 0.0,\n"
        "            \"box_yaw_deg\": 0.0,\n"
        "            \"mass_kg\": float(scene_rng.uniform(0.35, 0.80)) if randomize_scene else nominal_box_mass_kg,\n"
        "            \"friction_coefficient\": float(scene_rng.uniform(0.15, 0.25)) if randomize_scene else 0.18,\n"
        "            \"target_dx_error\": 0.0,\n"
        "            \"target_dz_error\": 0.0,\n"
        "        })\n"
        "        sim_node.mj_data.qpos[box_qpos_adr_random] += scene_randomization[\"box_dx\"]\n"
        "        sim_node.mj_data.qpos[box_qpos_adr_random + 1] += scene_randomization[\"box_dy\"]\n"
        "        yaw = np.deg2rad(scene_randomization[\"box_yaw_deg\"])\n"
        "        # MuJoCo free-joint quaternion order is w, x, y, z.\n"
        "        sim_node.mj_data.qpos[box_qpos_adr_random + 3:box_qpos_adr_random + 7] = [\n"
        "            np.cos(0.5 * yaw), 0.0, 0.0, np.sin(0.5 * yaw)\n"
        "        ]\n"
        "        if randomize_scene:\n"
        "            scene_randomization[\"mass_scale\"] = (\n"
        "                scene_randomization[\"mass_kg\"] / nominal_box_mass_kg\n"
        "            )\n"
        "            scene_randomization[\"friction_scale\"] = (\n"
        "                scene_randomization[\"friction_coefficient\"] / 0.18\n"
        "            )\n"
        "            sim_node.mj_model.body_mass[box_body_id_random] = scene_randomization[\"mass_kg\"]\n"
        "            sim_node.mj_model.body_inertia[box_body_id_random] = (\n"
        "                scene_randomization[\"mass_kg\"]\n"
        "                / nominal_box_mass_kg\n"
        "                * sim_node.mj_model.body_inertia[box_body_id_random]\n"
        "            )\n"
        "            geom_start = int(sim_node.mj_model.body_geomadr[box_body_id_random])\n"
        "            geom_num = int(sim_node.mj_model.body_geomnum[box_body_id_random])\n"
        "            sim_node.mj_model.geom_friction[\n"
        "                geom_start:geom_start + geom_num, 0\n"
        "            ] = scene_randomization[\"friction_coefficient\"]\n"
        "        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)\n"
    )
    source_text = _replace_once(
        source_text,
        randomization_old,
        randomization_new,
        "scene randomization block",
    )

    if startup_only:
        source_text = _replace_once(
            source_text,
            "    sync_reset_pose(sim_node, action, mujoco, preserve_free_objects=randomize_scene)\n",
            "    sync_reset_pose(sim_node, action, mujoco, preserve_free_objects=randomize_scene)\n"
            '    if bool(globals().get("EXTERNAL_STARTUP_ONLY", False)):\n'
            '        print(">>> table-front startup pose ready; navigation and grasp skipped")\n'
            '        return True\n',
            "startup-only early return",
        )

    base_nav_old = (
        '        print(\n'
        '            ">>> randomized scene:",\n'
        '            ", ".join(\n'
        '                f"{key}={value:.4f}" if isinstance(value, float) else f"{key}={value}"\n'
        '                for key, value in scene_randomization.items()\n'
        '            ),\n'
        '        )\n\n'
        '    tmat_box = get_body_tmat(sim_node.mj_data, target_body_name)\n'
    )
    base_nav_new = (
        '        print(\n'
        '            ">>> randomized scene:",\n'
        '            ", ".join(\n'
        '                f"{key}={value:.4f}" if isinstance(value, float) else f"{key}={value}"\n'
        '                for key, value in scene_randomization.items()\n'
        '            ),\n'
        '        )\n\n'
        '    nav_target_world = globals().get("EXTERNAL_TARGET_WORLD", None)\n'
        '    if nav_target_world is not None:\n'
        '        nav_target_world = np.asarray(nav_target_world, dtype=float)\n'
        '        target_base_x = float(nav_target_world[0])\n'
        '        target_base_y = float(nav_target_world[1])\n'
        '        nav_delta_y = float(target_base_y - base_lock_y)\n'
        '    else:\n'
        '        nav_delta_y = float(scene_randomization["box_dy"])\n'
        '        target_base_x = float(base_lock_x)\n'
        '        target_base_y = float(base_lock_y + scene_randomization["box_dy"])\n'
        '    if abs(nav_delta_y) > 1.0e-6:\n'
        '        nav_start_time = float(sim_node.mj_data.time)\n'
        '        nav_timeout = 24.0\n'
        '        nav_last_log = -1.0e9\n'
        '        print(\n'
        '            ">>> base lateral alignment by wheel drive started:",\n'
        '            f"start=({float(sim_node.sensor_base_position[0]):.4f}, "\n'
        '            f"{float(sim_node.sensor_base_position[1]):.4f}), ",\n'
        '            f"target=({target_base_x:.4f}, {target_base_y:.4f}), "\n'
        '            f"delta_y={nav_delta_y:+.4f}m",\n'
        '        )\n'
        '        while sim_node.running:\n'
        '            now = float(sim_node.mj_data.time)\n'
        '            if now - nav_start_time > nav_timeout:\n'
        '                print(">>> base lateral alignment timeout")\n'
        '                break\n'
        '            base_pos = np.asarray(sim_node.sensor_base_position, dtype=float)\n'
        '            quat = np.asarray(sim_node.sensor_base_orientation, dtype=float)\n'
        '            yaw = math.atan2(\n'
        '                2.0 * (quat[0] * quat[3] + quat[1] * quat[2]),\n'
        '                1.0 - 2.0 * (quat[2] ** 2 + quat[3] ** 2),\n'
        '            )\n'
        '            x_error = float(target_base_x - base_pos[0])\n'
        '            y_error = float(target_base_y - base_pos[1])\n'
        '            distance = float(math.hypot(x_error, y_error))\n'
        '            if distance < 0.010:\n'
        '                yaw_error = math.atan2(math.sin(-yaw), math.cos(-yaw))\n'
        '                linear_speed = 0.0\n'
        '                angular_speed = float(np.clip(2.0 * yaw_error, -0.85, 0.85))\n'
        '                if abs(yaw_error) < 0.05:\n'
        '                    break\n'
        '            else:\n'
        '                desired_heading = math.atan2(y_error, x_error)\n'
        '                heading_error = math.atan2(\n'
        '                    math.sin(desired_heading - yaw),\n'
        '                    math.cos(desired_heading - yaw),\n'
        '                )\n'
        '                direction = 1.0\n'
        '                if abs(heading_error) > 0.5 * math.pi:\n'
        '                    desired_heading = math.atan2(\n'
        '                        math.sin(desired_heading + math.pi),\n'
        '                        math.cos(desired_heading + math.pi),\n'
        '                    )\n'
        '                    heading_error = math.atan2(\n'
        '                        math.sin(desired_heading - yaw),\n'
        '                        math.cos(desired_heading - yaw),\n'
        '                    )\n'
        '                    direction = -1.0\n'
        '                linear_speed = (\n'
        '                    0.0\n'
        '                    if abs(heading_error) > 0.65\n'
        '                    else direction * float(np.clip(0.75 * distance, 0.035, 0.16))\n'
        '                )\n'
        '                angular_speed = float(np.clip(2.4 * heading_error, -0.90, 0.90))\n'
        '            if now - nav_last_log >= 0.75:\n'
        '                nav_last_log = now\n'
        '                print(\n'
        '                    ">>> base navigation:",\n'
        '                    f"pose=({base_pos[0]:.3f}, {base_pos[1]:.3f}, yaw={yaw:.3f}), ",\n'
        '                    f"err=({x_error:+.3f}, {y_error:+.3f}), ",\n'
        '                    f"cmd=(v={linear_speed:+.3f}, w={angular_speed:+.3f})",\n'
        '                )\n'
        '            wheel_target = np.asarray(\n'
        '                [\n'
        '                    (linear_speed - angular_speed * sim_node.wheel_distance)\n'
        '                    / sim_node.wheel_radius,\n'
        '                    (linear_speed + angular_speed * sim_node.wheel_distance)\n'
        '                    / sim_node.wheel_radius,\n'
        '                ],\n'
        '                dtype=float,\n'
        '            )\n'
        '            wheel_error = np.clip(\n'
        '                wheel_target - np.asarray(sim_node.sensor_wheel_qvel, dtype=float),\n'
        '                -2.5,\n'
        '                2.5,\n'
        '            )\n'
        '            action[:2] = np.clip(\n'
        '                7.5 * wheel_error,\n'
        '                sim_node.mj_model.actuator_ctrlrange[:2, 0],\n'
        '                sim_node.mj_model.actuator_ctrlrange[:2, 1],\n'
        '            )\n'
        '            obs, _, _, _, _ = sim_node.step(action)\n'
        '        action[:2] = 0.0\n'
        '        sim_node.mj_data.ctrl[:2] = 0.0\n'
        '        base_lock_x = float(sim_node.sensor_base_position[0])\n'
        '        base_lock_y = float(sim_node.sensor_base_position[1])\n'
        '        cfg.init_state["base_position"] = [base_lock_x, base_lock_y, 0.0]\n'
        '        print(\n'
        '            ">>> base lateral alignment complete:",\n'
        '            f"measured=({base_lock_x:.4f}, {base_lock_y:.4f}), ",\n'
        '            f"target=({target_base_x:.4f}, {target_base_y:.4f}), yaw={yaw:.4f}rad",\n'
        '        )\n'
        '        if bool(globals().get("EXTERNAL_MOVE_ONLY", False)):\n'
        '            return True\n'
        '    if bool(globals().get("EXTERNAL_MOVE_ONLY", False)):\n'
        '        return True\n'
        '    tmat_box = get_body_tmat(sim_node.mj_data, target_body_name)\n'
    )
    source_text = _replace_once(
        source_text,
        base_nav_old,
        base_nav_new,
        "base navigation insertion",
    )

    module_name = f"_box_pick_lr_base_align_trial_{random.randrange(1 << 30)}"
    module = types.ModuleType(module_name)
    module.__file__ = str(source_path)
    module.__package__ = ""
    module.__dict__["__builtins__"] = __builtins__
    module.EXTERNAL_RANDOMIZED_BOX_DY = float(external_box_dy)
    module.EXTERNAL_TARGET_WORLD = external_target_world
    module.EXTERNAL_BASE_POSITION = external_base_position
    module.EXTERNAL_MOVE_ONLY = bool(move_only)
    module.EXTERNAL_STARTUP_ONLY = bool(startup_only)
    module.EXTERNAL_GRASP_WORLD = None
    _install_wam_stubs()
    sys.modules[module_name] = module
    exec(compile(source_text, str(source_path), "exec"), module.__dict__)
    return module


def grasp_object(env, target_world, grasp_world=None, move_only=False):
    """
    输入:
        env           : 当前已经运行的 DISCOVERSE 环境
        target_world   : 目标物世界坐标 [x, y, z]
        grasp_world    : 推荐抓取点世界坐标 [x, y, z]

    输出:
        True  : 成功抓取
        False : 抓取失败
    """
    mjcf_path = getattr(env, "mjcf_path", DEFAULT_MJCF_FILE_PATH)
    discoverse_root = getattr(env, "discoverse_root", DEFAULT_DISCOVERSE_ROOT)
    urdf_path = getattr(env, "urdf_path", DEFAULT_URDF_PATH)
    target_world = _normalize_world_point(target_world)
    grasp_world = _normalize_world_point(grasp_world)

    scene_seed = getattr(env, "scene_seed", None)
    dy_range = float(getattr(env, "dy_range", 0.15))
    fixed_dy = getattr(env, "fixed_dy", None)
    headless_preview_seconds = getattr(env, "headless_preview_seconds", None)
    external_base_position = None
    if move_only and target_world is not None:
        external_base_position = target_world
    if target_world is not None and not move_only:
        nominal_box_center_y = float(
            getattr(env, "nominal_box_center_y", DEFAULT_BOX_CENTER_Y)
        )
        fixed_dy = float(target_world[1]) - nominal_box_center_y

    seed, box_dy = choose_scene_params(scene_seed, dy_range, fixed_dy)
    print(
        ">>> randomized scene:",
        f"seed={seed}, box_dy={box_dy:+.4f}, dy_range={dy_range:.4f}",
    )
    print(
        ">>> base lateral alignment enabled:",
        f"target_dy={box_dy:+.4f}m, base will move by wheel drive before grasping",
    )

    module = _load_patched_box_pick_module(
        box_dy,
        external_target_world=target_world if move_only else None,
        external_base_position=external_base_position,
        move_only=move_only,
        startup_only=False,
    )
    setattr(env, "target_world", target_world)
    setattr(env, "grasp_world", grasp_world)
    module.EXTERNAL_TARGET_WORLD = target_world
    module.EXTERNAL_GRASP_WORLD = grasp_world
    return bool(
        module.run_box_pick_grasp_scene(
            str(Path(mjcf_path)),
            discoverse_root,
            urdf_path=urdf_path,
            headless=headless_preview_seconds is not None,
            max_seconds=headless_preview_seconds,
            randomize_scene=True,
            scene_seed=seed,
        )
    )


def move_robot_to_table_front(env, target_world, grasp_world=None):
    return grasp_object(env, target_world, grasp_world=grasp_world, move_only=True)


def prepare_table_front_pose(env, base_world=None):
    base_world = _normalize_world_point(base_world)
    if base_world is None:
        base_world = [0.58, 0.55, 0.0]

    mjcf_path = getattr(env, "mjcf_path", DEFAULT_MJCF_FILE_PATH)
    discoverse_root = getattr(env, "discoverse_root", DEFAULT_DISCOVERSE_ROOT)
    urdf_path = getattr(env, "urdf_path", DEFAULT_URDF_PATH)
    scene_seed = getattr(env, "scene_seed", None)
    headless_preview_seconds = getattr(env, "headless_preview_seconds", None)

    print(
        ">>> table-front startup pose:",
        f"base_position={np.round(np.asarray(base_world, dtype=float), 4).tolist()}",
    )

    module = _load_patched_box_pick_module(
        0.0,
        external_base_position=base_world,
        move_only=False,
        startup_only=True,
    )
    return bool(
        module.run_box_pick_grasp_scene(
            str(Path(mjcf_path)),
            discoverse_root,
            urdf_path=urdf_path,
            headless=headless_preview_seconds is not None,
            max_seconds=headless_preview_seconds,
            randomize_scene=False,
            scene_seed=scene_seed if scene_seed is not None else 0,
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="Random left-right box pick with base lateral alignment."
    )
    parser.add_argument("--mjcf", default=DEFAULT_MJCF_FILE_PATH)
    parser.add_argument("--discoverse-root", default=DEFAULT_DISCOVERSE_ROOT)
    parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
    parser.add_argument("--scene-seed", type=int, default=None)
    parser.add_argument("--dy-range", type=float, default=0.15)
    parser.add_argument("--fixed-dy", type=float, default=None)
    parser.add_argument("--headless-preview-seconds", type=float, default=None)
    args = parser.parse_args()

    env = types.SimpleNamespace(
        mjcf_path=args.mjcf,
        discoverse_root=args.discoverse_root,
        urdf_path=args.urdf,
        scene_seed=args.scene_seed,
        dy_range=args.dy_range,
        fixed_dy=args.fixed_dy,
        headless_preview_seconds=args.headless_preview_seconds,
    )
    grasp_object(env, target_world=None, grasp_world=None)


if __name__ == "__main__":
    main()
