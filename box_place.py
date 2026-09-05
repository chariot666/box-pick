#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Standalone placement helper for the experimental navigation flow."""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PERCEPTION_MODULE_DIR = os.path.join(_BASE_DIR, "vlm-sam", "perception_module")

DEFAULT_URDF_PATH = os.path.join(_BASE_DIR, "DISCOVERSE/models/urdf/mmk2_s_g2.urdf")
DEFAULT_DISCOVERSE_ROOT = os.path.join(_BASE_DIR, "DISCOVERSE")
DEFAULT_MJCF_FILE_PATH = os.path.join(_BASE_DIR, "DISCOVERSE/models/mjcf/tasks_mmk2/task1_pick_and_place_open.xml")


def ensure_discoverse_import_path(discoverse_root):
    discoverse_root = Path(discoverse_root)
    if not discoverse_root.exists():
        raise FileNotFoundError(f"DISCOVERSE root does not exist: {discoverse_root}")
    root_str = str(discoverse_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def ensure_perception_import_path():
    for module_dir in (_PERCEPTION_MODULE_DIR, DEFAULT_DISCOVERSE_ROOT):
        if os.path.isdir(module_dir) and module_dir not in sys.path:
            sys.path.insert(0, module_dir)


def _interface_world_position(value, argument_name):
    """Normalize task-manager coordinates while preserving the bool API."""
    if isinstance(value, dict):
        for key in ("position", "target_world", "placement", "pose"):
            if key in value:
                value = value[key]
                break
        else:
            raise ValueError(
                f"{argument_name} dict must contain position/target_world/"
                "placement/pose"
            )
    array = np.asarray(value, dtype=float)
    if array.shape == (4, 4):
        array = array[:3, 3]
    else:
        array = array.reshape(-1)
        if array.size not in (3, 7):
            raise ValueError(
                f"{argument_name} must be XYZ, XYZ+quaternion, or a 4x4 pose"
            )
        array = array[:3]
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{argument_name} contains non-finite values")
    return np.asarray(array, dtype=float).copy()


def _set_manipulation_result(env, success, reason, retryable=None):
    result = {
        "success": bool(success),
        "retryable": bool(not success if retryable is None else retryable),
        "reason": str(reason),
    }
    if env is not None:
        env._box_pick_last_result = result
    return result


def get_last_manipulation_result(env):
    """Return the detailed status associated with the required bool result."""
    return dict(
        getattr(
            env,
            "_box_pick_last_result",
            {
                "success": False,
                "retryable": True,
                "reason": "no_manipulation_result",
            },
        )
    )


def _interface_control_step(
    env, action, step_func, speed_scale=1.0, wheel_left=0.0, wheel_right=0.0
):
    for index in range(2, int(env.njctrl)):
        ratio = max(0.05, float(env.joint_move_ratio[index]))
        action[index] = step_func(
            action[index],
            env.target_control[index],
            float(speed_scale) * ratio * float(env.delta_t),
        )
    action[0] = float(wheel_left)
    action[1] = float(wheel_right)
    env.step(action)


def _freeze_current_manipulator_pose(env, action=None, gripper_open=None):
    if env is None or not hasattr(env, "target_control"):
        return action
    frozen = np.asarray(env.target_control, dtype=float).copy()
    frozen[:2] = 0.0
    if hasattr(env, "sensor_slide_qpos"):
        frozen[2:3] = np.asarray(env.sensor_slide_qpos, dtype=float)
        if hasattr(env, "tctr_slide"):
            env.tctr_slide[:] = np.asarray(env.sensor_slide_qpos, dtype=float)
    if hasattr(env, "sensor_head_qpos"):
        frozen[3:5] = np.asarray(env.sensor_head_qpos, dtype=float)
        if hasattr(env, "tctr_head"):
            env.tctr_head[:] = np.asarray(env.sensor_head_qpos, dtype=float)
    if hasattr(env, "sensor_lft_arm_qpos"):
        frozen[5:11] = np.asarray(env.sensor_lft_arm_qpos, dtype=float)
        if hasattr(env, "tctr_left_arm"):
            env.tctr_left_arm[:] = np.asarray(env.sensor_lft_arm_qpos, dtype=float)
        if hasattr(env, "set_left_arm_new_target"):
            env.set_left_arm_new_target = True
    if hasattr(env, "sensor_rgt_arm_qpos"):
        frozen[12:18] = np.asarray(env.sensor_rgt_arm_qpos, dtype=float)
        if hasattr(env, "tctr_right_arm"):
            env.tctr_right_arm[:] = np.asarray(env.sensor_rgt_arm_qpos, dtype=float)
        if hasattr(env, "set_right_arm_new_target"):
            env.set_right_arm_new_target = True
    if gripper_open is not None:
        frozen[11:12] = float(gripper_open)
        frozen[18:19] = float(gripper_open)
        if hasattr(env, "tctr_lft_gripper"):
            env.tctr_lft_gripper[:] = float(gripper_open)
        if hasattr(env, "tctr_rgt_gripper"):
            env.tctr_rgt_gripper[:] = float(gripper_open)
    if hasattr(env, "joint_move_ratio"):
        env.joint_move_ratio[:] = 1.0
    env.target_control[:] = frozen
    if action is None:
        return frozen
    action[:] = frozen
    return action


def _camera_point_to_world(point_camera, cam_pos, cam_rot):
    x_vlm, y_vlm, z_vlm = np.asarray(point_camera, dtype=float)
    camera_point_mujoco = np.array([x_vlm, -y_vlm, -z_vlm], dtype=float)
    rotation = np.asarray(cam_rot, dtype=float)
    rotated = np.array(
        [
            rotation[i, 0] * camera_point_mujoco[0]
            + rotation[i, 1] * camera_point_mujoco[1]
            + rotation[i, 2] * camera_point_mujoco[2]
            for i in range(3)
        ],
        dtype=float,
    )
    return rotated + np.asarray(cam_pos, dtype=float)


def _enable_head_rgbd(env):
    if not hasattr(env, "config"):
        return
    if getattr(env.config, "obs_rgb_cam_id", None) in (None, []):
        env.config.obs_rgb_cam_id = [0]
    if getattr(env.config, "obs_depth_cam_id", None) in (None, []):
        env.config.obs_depth_cam_id = [0]


def _capture_head_rgbd(env):
    if not hasattr(env, "mj_model") or not hasattr(env, "mj_data"):
        return None
    _enable_head_rgbd(env)
    if getattr(getattr(env, "config", None), "enable_render", False):
        env.render()
    obs = env.getObservation()
    try:
        head_id = int(env.mj_model.camera("head_cam").id)
    except Exception:
        return None
    rgb = obs.get("img", {}).get(head_id)
    depth = obs.get("depth", {}).get(head_id)
    if not isinstance(rgb, np.ndarray) or not isinstance(depth, np.ndarray):
        return None
    cam_pos = env.mj_data.cam_xpos[head_id].copy()
    cam_rot = env.mj_data.cam_xmat[head_id].copy().reshape(3, 3)
    width = int(rgb.shape[1])
    height = int(rgb.shape[0])
    fovy = float(env.mj_model.cam_fovy[head_id])
    fy = 0.5 * float(height) / np.tan(np.radians(fovy) / 2.0)
    fx = fy
    cx = 0.5 * float(width)
    cy = 0.5 * float(height)
    return {
        "rgb": rgb,
        "depth": depth,
        "cam_pos": cam_pos,
        "cam_rot": cam_rot,
        "fx": fx,
        "fy": fy,
        "cx": cx,
        "cy": cy,
        "width": width,
        "height": height,
    }


def _detect_table_obstacle_points(env, reference_xy, reference_z, ignore_xy=None):
    capture = _capture_head_rgbd(env)
    if capture is None:
        return np.empty((0, 2), dtype=float)

    rgb = np.asarray(capture["rgb"], dtype=np.int16)
    depth = np.asarray(capture["depth"], dtype=float)
    if rgb.ndim != 3 or depth.ndim != 2:
        return np.empty((0, 2), dtype=float)

    color_delta = np.max(np.abs(rgb - 245), axis=2)
    color_mask = color_delta > 18
    depth_mask = np.isfinite(depth) & (depth > 0.10) & (depth < 2.5)
    mask = color_mask & depth_mask
    ys, xs = np.where(mask)
    if xs.size == 0:
        return np.empty((0, 2), dtype=float)

    stride = 6
    points = []
    cam_pos = capture["cam_pos"]
    cam_rot = capture["cam_rot"]
    fx = float(capture["fx"])
    fy = float(capture["fy"])
    cx = float(capture["cx"])
    cy = float(capture["cy"])
    reference_xy = np.asarray(reference_xy, dtype=float)
    ignore_xy = None if ignore_xy is None else np.asarray(ignore_xy, dtype=float)
    table_center, table_half = _table_top_bounds(env)
    table_x_min = float(table_center[0] - table_half[0] + 0.10)
    table_x_max = float(table_center[0] + table_half[0] - 0.10)
    table_y_min = float(table_center[1] - table_half[1] + 0.08)
    table_y_max = float(table_center[1] + table_half[1] - 0.08)

    for y in range(0, capture["height"], stride):
        for x in range(0, capture["width"], stride):
            if not mask[y, x]:
                continue
            d = float(depth[y, x])
            if not np.isfinite(d) or d <= 0.10 or d >= 2.5:
                continue
            pt_world = _camera_point_to_world(
                [((x - cx) * d) / fx, ((y - cy) * d) / fy, d],
                cam_pos,
                cam_rot,
            )
            if abs(float(pt_world[2]) - float(reference_z)) > 0.28:
                continue
            if not (
                table_x_min <= float(pt_world[0]) <= table_x_max
                and table_y_min <= float(pt_world[1]) <= table_y_max
            ):
                continue
            if ignore_xy is not None and float(
                np.linalg.norm(pt_world[:2] - ignore_xy)
            ) < 0.18:
                continue
            points.append(pt_world[:2])

    if not points:
        return np.empty((0, 2), dtype=float)
    return np.asarray(points, dtype=float)


def _detect_table_state_obstacle_points(env, reference_xy, reference_z, ignore_xy=None):
    """Fallback occupancy from current table object poses when RGB-D is sparse."""
    if not hasattr(env, "mj_model") or not hasattr(env, "mj_data"):
        return np.empty((0, 2), dtype=float)
    reference_xy = np.asarray(reference_xy, dtype=float)
    ignore_xy = None if ignore_xy is None else np.asarray(ignore_xy, dtype=float)
    table_center, table_half = _table_top_bounds(env)
    table_x_min = float(table_center[0] - table_half[0] + 0.10)
    table_x_max = float(table_center[0] + table_half[0] - 0.10)
    table_y_min = float(table_center[1] - table_half[1] + 0.08)
    table_y_max = float(table_center[1] + table_half[1] - 0.08)
    points = []
    body_count = int(getattr(env.mj_model, "nbody", 0))
    for body_id in range(body_count):
        body_name = env.mj_model.body(body_id).name or ""
        if body_name in {
            "",
            "world",
            "mmk2",
            "material_table",
            "cabinet",
        }:
            continue
        center = np.asarray(env.mj_data.xpos[body_id], dtype=float)
        if not np.all(np.isfinite(center)):
            continue
        if body_name.startswith(("lft_", "rgt_", "arm", "head")):
            continue
        if abs(float(center[2]) - float(reference_z)) > 0.35:
            continue
        if not (
            table_x_min <= float(center[0]) <= table_x_max
            and table_y_min <= float(center[1]) <= table_y_max
        ):
            continue
        if ignore_xy is not None and float(np.linalg.norm(center[:2] - ignore_xy)) < 0.18:
            continue
        body_geom_start = int(env.mj_model.body_geomadr[body_id])
        body_geom_count = int(env.mj_model.body_geomnum[body_id])
        half_x = 0.11
        half_y = 0.08
        for geom_id in range(
            body_geom_start, body_geom_start + body_geom_count
        ):
            geom_size = np.asarray(env.mj_model.geom_size[geom_id], dtype=float)
            if geom_size.size >= 2 and np.all(np.isfinite(geom_size[:2])):
                half_x = max(half_x, float(geom_size[0]))
                half_y = max(half_y, float(geom_size[1]))
        sample_x = np.linspace(-half_x, half_x, 5)
        sample_y = np.linspace(-half_y, half_y, 5)
        for dx in sample_x:
            for dy in sample_y:
                points.append(center[:2] + np.array([dx, dy], dtype=float))
    if not points:
        return np.empty((0, 2), dtype=float)
    return np.asarray(points, dtype=float)


def _table_top_bounds(env):
    center = np.array([-0.66, -1.075], dtype=float)
    half = np.array([0.80, 0.40], dtype=float)
    try:
        body_id = int(env.mj_model.body("material_table").id)
        center = np.asarray(env.mj_data.xpos[body_id][:2], dtype=float).copy()
        geom_start = int(env.mj_model.body_geomadr[body_id])
        geom_count = int(env.mj_model.body_geomnum[body_id])
        for geom_id in range(geom_start, geom_start + geom_count):
            geom_size = np.asarray(env.mj_model.geom_size[geom_id], dtype=float)
            if geom_size[0] > 0.40 and geom_size[1] > 0.20:
                half = geom_size[:2].copy()
                break
    except Exception:
        pass
    return center, half


def _table_surface_height(env):
    height = 0.751
    try:
        body_id = int(env.mj_model.body("material_table").id)
        body_z = float(env.mj_data.xpos[body_id][2])
        geom_start = int(env.mj_model.body_geomadr[body_id])
        geom_count = int(env.mj_model.body_geomnum[body_id])
        for geom_id in range(geom_start, geom_start + geom_count):
            geom_size = np.asarray(env.mj_model.geom_size[geom_id], dtype=float)
            geom_pos = np.asarray(env.mj_model.geom_pos[geom_id], dtype=float)
            if (
                geom_size.size >= 3
                and geom_pos.size >= 3
                and geom_size[0] > 0.40
                and geom_size[1] > 0.20
            ):
                height = body_z + float(geom_pos[2]) + float(geom_size[2])
                break
    except Exception:
        pass
    return float(height)


def _choose_safe_table_destination(env, preferred_destination, start_box):
    preferred_destination = np.asarray(preferred_destination, dtype=float)
    start_box = np.asarray(start_box, dtype=float)
    table_center, table_half = _table_top_bounds(env)
    table_margin = np.array([0.16, 0.14], dtype=float)
    x_min = float(table_center[0] - table_half[0] + table_margin[0])
    x_max = float(table_center[0] + table_half[0] - table_margin[0])
    y_min = float(table_center[1] - table_half[1] + table_margin[1])
    y_max = float(table_center[1] + table_half[1] - table_margin[1])

    # The body origin of the package is its bottom centre.  The incoming
    # placement XY is only a legacy hint and is deliberately ignored.
    # Placement starts from the carried box and searches the actual table.
    direct_drop = np.asarray(start_box, dtype=float).copy()
    direct_drop[0] = float(np.clip(direct_drop[0], x_min, x_max))
    direct_drop[1] = float(np.clip(direct_drop[1], y_min, y_max))
    direct_drop[2] = _table_surface_height(env) + 0.001

    vision_points = _detect_table_obstacle_points(
        env,
        reference_xy=direct_drop[:2],
        reference_z=direct_drop[2],
        ignore_xy=start_box[:2],
    )
    state_points = _detect_table_state_obstacle_points(
        env,
        reference_xy=direct_drop[:2],
        reference_z=direct_drop[2],
        ignore_xy=start_box[:2],
    )
    point_sets = [points for points in (vision_points, state_points) if points.size]
    obstacle_points = (
        np.vstack(point_sets)
        if point_sets
        else np.empty((0, 2), dtype=float)
    )
    # Search a dense table grid.  The current box position on the table is
    # tried first; if it is free, we drop there immediately.
    candidates = []
    candidates.append(direct_drop)
    x_values = np.round(np.arange(x_min, x_max + 1.0e-6, 0.05), 4)
    y_values = np.round(np.arange(y_min, y_max + 1.0e-6, 0.05), 4)
    for x in x_values:
        for y in y_values:
            candidate = direct_drop.copy()
            candidate[0] = float(x)
            candidate[1] = float(y)
            if float(np.linalg.norm(candidate[:2] - start_box[:2])) > 0.72:
                continue
            candidates.append(candidate)
    if not candidates:
        print(
            ">>> table empty-slot search:",
            "no reachable table candidates from current box",
        )
        return None, -float("inf")

    # The carried box footprint is approximately 24 x 16 cm.  Require a
    # full footprint clearance, rather than checking only a point at its
    # centre.
    box_half_x = 0.12
    box_half_y = 0.08
    required_clearance = 0.070
    safe_candidates = []
    for candidate in candidates:
        if obstacle_points.size:
            clearance = float(
                np.min(np.linalg.norm(obstacle_points - candidate[:2], axis=1))
            )
        else:
            clearance = float("inf")
        edge_margin = min(
            candidate[0] - x_min,
            x_max - candidate[0],
            candidate[1] - y_min,
            y_max - candidate[1],
        )
        footprint_clearance = clearance - max(box_half_x, box_half_y)
        if not obstacle_points.size or footprint_clearance >= required_clearance:
            safe_candidates.append((candidate, footprint_clearance, edge_margin))

    if safe_candidates:
        safe_candidates.sort(
            key=lambda item: (
                -float(item[1]),
                float(np.linalg.norm(item[0][:2] - start_box[:2])),
                float(np.linalg.norm(item[0][:2] - direct_drop[:2])),
                -float(item[2]),
            )
        )
        best_candidate, best_clearance, _ = safe_candidates[0]
        if np.linalg.norm(best_candidate[:2] - direct_drop[:2]) <= 0.020:
            print(
                ">>> table empty-slot search: direct drop is free;",
                f"chosen={np.round(best_candidate, 4)}",
                f"clearance={best_clearance:.3f}m",
            )
            return best_candidate, best_clearance
        print(
            ">>> table empty-slot search: nearest safe slot selected;",
            f"chosen={np.round(best_candidate, 4)}",
            f"clearance={best_clearance:.3f}m",
        )
        return best_candidate, best_clearance

    print(
        ">>> table empty-slot search:",
        f"vision_points={len(vision_points)}",
        f"state_points={len(state_points)}",
        f"candidates={len(candidates)}",
        "no collision-free slot found",
    )
    return None, -float("inf")


def _resolve_preferred_destination(env, placement, base_destination):
    destination = None if base_destination is None else np.asarray(base_destination, dtype=float).copy()
    if not isinstance(placement, dict):
        if destination is None:
            raise ValueError("placement dict must contain a direct position or helper keys")
        return destination, "direct"

    instruction = placement.get("instruction")
    parsed = placement.get("parsed")
    use_helper = bool(placement.get("use_helper", False))
    if not (use_helper or instruction or parsed):
        if destination is None:
            raise ValueError("placement helper is required when no direct position is provided")
        return destination, "direct"

    try:
        ensure_perception_import_path()
        from dual_arm_perception import DualArmPerception
    except Exception as exc:
        print(">>> placement helper unavailable:", str(exc).splitlines()[0])
        if destination is None:
            raise ValueError("placement helper returned no usable point")
        return destination, "direct"

    try:
        helper = DualArmPerception(env, debug=bool(placement.get("debug", False)))
        helper = helper.get_placement_position(instruction=instruction, parsed=parsed)
    except Exception as exc:
        print(">>> placement helper failed:", str(exc).splitlines()[0])
        if destination is None:
            raise ValueError("placement helper returned non-finite point")
        return destination, "direct"

    if not helper.get("success"):
        print(
            ">>> placement helper returned no usable point:",
            helper.get("error"),
        )
        return destination, "direct"

    helper_destination = helper.get("placement_world")
    if helper_destination is None:
        return destination, "direct"

    helper_destination = _interface_world_position(
        helper_destination, "placement_world"
    )
    if not np.all(np.isfinite(helper_destination)):
        return destination, "direct"

    destination = helper_destination.copy()
    print(
        ">>> placement helper used:",
        f"reference={helper.get('reference_name')}",
        f"direction={helper.get('direction')}",
        f"placement={np.round(helper_destination, 4)}",
    )
    return destination, "task_api"


def place_object(env, placement):
    """Place the currently grasped package using the same DISCOVERSE env."""
    if env is None:
        return False
    try:
        if isinstance(placement, dict):
            direct_value = None
            for key in ("position", "target_world", "placement", "pose"):
                if key in placement:
                    direct_value = placement[key]
                    break
            destination = (
                _interface_world_position(direct_value, "placement")
                if direct_value is not None
                else None
            )
        else:
            destination = _interface_world_position(placement, "placement")
        context = getattr(env, "_box_pick_context", None)
        if not isinstance(context, dict) or not context.get("grasped", False):
            _set_manipulation_result(
                env, False, "place_without_valid_grasp", retryable=False
            )
            return False

        ensure_discoverse_import_path(DEFAULT_DISCOVERSE_ROOT)
        import mujoco
        from discoverse.utils import get_body_tmat, step_func

        target_body_name = str(context.get("target_body_name", "box_yellow"))
        start_box = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()

        visual_destination, clearance = _choose_safe_table_destination(
            env, destination, start_box
        )
        if visual_destination is None:
            _set_manipulation_result(
                env,
                False,
                "no_collision_free_table_slot",
                retryable=True,
            )
            print(">>> placement stopped: no collision-free table slot")
            return False
        destination = visual_destination
        translation = destination - start_box
        horizontal_distance = float(np.linalg.norm(translation[:2]))
        vertical_distance = float(abs(translation[2]))
        print(
            ">>> place_object start:",
            f"box={np.round(start_box, 4)}",
            f"empty_slot={np.round(destination, 4)}",
            f"clearance={clearance:.3f}m",
        )
        if horizontal_distance > 0.72:
            _set_manipulation_result(
                env,
                False,
                "empty_table_slot_out_of_reach",
                retryable=True,
            )
            return False

        chosen_translation = visual_destination - start_box
        chosen_horizontal_distance = float(np.linalg.norm(chosen_translation[:2]))
        chosen_vertical_distance = float(abs(chosen_translation[2]))
        print(
            ">>> place_object safety check:",
            f"start_box={np.round(start_box, 4)}",
            f"clearance={clearance:.3f}m",
            f"preferred_reach_xy={horizontal_distance:.3f}m",
            f"chosen_reach_xy={chosen_horizontal_distance:.3f}m",
            f"dz={chosen_vertical_distance:.3f}m",
        )
        left_rotation = np.asarray(context["left_grip_rot"], dtype=float)
        right_rotation = np.asarray(context["right_grip_rot"], dtype=float)
        try:
            from box_pick import relaxed_grip_rotation_candidates
        except Exception:
            relaxed_grip_rotation_candidates = None
        base_world_tmat = get_body_tmat(env.mj_data, "mmk2")
        base_rot = np.asarray(base_world_tmat[:3, :3], dtype=float)
        base_pos = np.asarray(base_world_tmat[:3, 3], dtype=float)
        if (
            "left_endpoint_target_base" in context
            and "right_endpoint_target_base" in context
        ):
            left_start = (
                base_world_tmat
                @ np.append(
                    np.asarray(context["left_endpoint_target_base"], dtype=float),
                    1.0,
                )
            )[:3]
            right_start = (
                base_world_tmat
                @ np.append(
                    np.asarray(context["right_endpoint_target_base"], dtype=float),
                    1.0,
                )
            )[:3]
        else:
            left_start = np.asarray(
                context.get(
                    "left_endpoint_target",
                    env.mj_data.site("lft_endpoint").xpos,
                ),
                dtype=float,
            ).copy()
            right_start = np.asarray(
                context.get(
                    "right_endpoint_target",
                    env.mj_data.site("rgt_endpoint").xpos,
                ),
                dtype=float,
            ).copy()

        left_tracking_bias = (
            np.asarray(env.mj_data.site("lft_endpoint").xpos, dtype=float)
            - left_start
        )
        right_tracking_bias = (
            np.asarray(env.mj_data.site("rgt_endpoint").xpos, dtype=float)
            - right_start
        )
        action = np.asarray(env.target_control, dtype=float).copy()
        action[:2] = 0.0
        env.tctr_lft_gripper[:] = float(context.get("grip_close", 0.0))
        env.tctr_rgt_gripper[:] = float(context.get("grip_close", 0.0))

        def solve_arm_target_with_relaxation(target_world, arm_side, sensor_qpos, base_rotation):
            target_world = np.asarray(target_world, dtype=float).copy()
            height_offsets = (0.0, 0.03, 0.06, 0.09, 0.12, 0.15)
            last_exc = None
            for height_offset in height_offsets:
                candidate_world = target_world.copy()
                candidate_world[2] += float(height_offset)
                target_tmat = env.get_tmat_wrt_mmk2base(candidate_world)
                if relaxed_grip_rotation_candidates is None:
                    try:
                        return env.solveArmEndTarget(
                            target_tmat,
                            env.arm_action,
                            arm_side,
                            sensor_qpos,
                            base_rotation,
                        )
                    except ValueError as exc:
                        last_exc = exc
                        continue

                for candidate_rot, _offset in relaxed_grip_rotation_candidates(
                    base_rotation, max_angle_deg=16.0, step_deg=4.0
                ):
                    try:
                        return env.solveArmEndTarget(
                            target_tmat,
                            env.arm_action,
                            arm_side,
                            sensor_qpos,
                            candidate_rot,
                        )
                    except ValueError as exc:
                        last_exc = exc

            try:
                target_base = np.asarray(
                    base_rot.T @ (target_world - base_pos), dtype=float
                )
            except Exception:
                target_base = None
            if target_base is not None and (
                abs(float(target_base[0])) < 0.18 or abs(float(target_base[1])) < 0.12
            ):
                y_sign = 1.0 if float(target_base[1]) >= 0.0 else -1.0
                for dx, dy, dz in ((0.12, 0.00, 0.06), (0.12, 0.04 * y_sign, 0.08)):
                    candidate_base = np.asarray(target_base, dtype=float).copy()
                    candidate_base[0] += float(dx)
                    candidate_base[1] += float(dy)
                    candidate_base[2] += float(dz)
                    candidate_world = base_rot @ candidate_base + base_pos
                    target_tmat = env.get_tmat_wrt_mmk2base(candidate_world)
                    if relaxed_grip_rotation_candidates is None:
                        try:
                            return env.solveArmEndTarget(
                                target_tmat,
                                env.arm_action,
                                arm_side,
                                sensor_qpos,
                                base_rotation,
                            )
                        except ValueError as exc:
                            last_exc = exc
                            continue

                    for candidate_rot, _offset in relaxed_grip_rotation_candidates(
                        base_rotation, max_angle_deg=16.0, step_deg=4.0
                    ):
                        try:
                            return env.solveArmEndTarget(
                                target_tmat,
                                env.arm_action,
                                arm_side,
                                sensor_qpos,
                                candidate_rot,
                            )
                        except ValueError as exc:
                            last_exc = exc

            if last_exc is not None:
                raise last_exc
            return env.solveArmEndTarget(
                env.get_tmat_wrt_mmk2base(target_world),
                env.arm_action,
                arm_side,
                sensor_qpos,
                base_rotation,
            )

        def box_external_support_report():
            box_body_id = int(env.mj_model.body(target_body_name).id)
            contact_force = np.zeros(6, dtype=float)
            support_force = 0.0
            support_names = set()
            for contact_id in range(int(env.mj_data.ncon)):
                contact = env.mj_data.contact[contact_id]
                geom1 = int(contact.geom1)
                geom2 = int(contact.geom2)
                body1 = int(env.mj_model.geom_bodyid[geom1])
                body2 = int(env.mj_model.geom_bodyid[geom2])
                if body1 == box_body_id:
                    other_body = body2
                    other_geom = geom2
                elif body2 == box_body_id:
                    other_body = body1
                    other_geom = geom1
                else:
                    continue
                other_name = env.mj_model.body(other_body).name or ""
                if other_name.startswith(("lft_", "rgt_")):
                    continue
                contact_force[:] = 0.0
                mujoco.mj_contactForce(
                    env.mj_model, env.mj_data, contact_id, contact_force
                )
                normal = max(0.0, float(contact_force[0]))
                if normal > 0.05 or float(contact.dist) <= 0.001:
                    support_force += normal
                    geom_name = env.mj_model.geom(other_geom).name or f"geom_{other_geom}"
                    support_names.add(other_name or geom_name)
            return bool(support_names), support_force, sorted(support_names)

        def follow_box_waypoint(target_box, speed_scale, min_waypoints=8):
            current_box = np.asarray(
                get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
            ).copy()
            segment_translation = np.asarray(target_box, dtype=float) - current_box
            segment_distance = float(np.linalg.norm(segment_translation))
            waypoint_count = max(
                int(min_waypoints),
                int(math.ceil(segment_distance / 0.020)) + 1,
            )
            arrival_tol = min(0.070, 0.038 + 0.18 * min(segment_distance, 0.12))
            max_steps = max(9, int(math.ceil(segment_distance / 0.030)) + 4)
            local_left_start = np.asarray(
                env.mj_data.site("lft_endpoint").xpos, dtype=float
            ).copy()
            local_right_start = np.asarray(
                env.mj_data.site("rgt_endpoint").xpos, dtype=float
            ).copy()
            local_left_bias = np.zeros(3, dtype=float)
            local_right_bias = np.zeros(3, dtype=float)

            for alpha in np.linspace(0.0, 1.0, waypoint_count)[1:]:
                print(
                    ">>> placement waypoint:",
                    f"alpha={alpha:.3f}",
                    f"target={np.round(target_box, 4)}",
                )
                left_nominal = local_left_start + alpha * segment_translation
                right_nominal = local_right_start + alpha * segment_translation
                last_force_update = -1.0e9
                left_force_offset = 0.0
                right_force_offset = 0.0
                endpoint_error = float("inf")
                left_load = 0.0
                right_load = 0.0
                for _ in range(max_steps):
                    now = float(env.mj_data.time)
                    report = env.wall_grasp_report()
                    left_load = sum(
                        report["forces"][name]
                        for name in (
                            "lft_finger_left_link",
                            "lft_finger_right_link",
                        )
                    )
                    right_load = sum(
                        report["forces"][name]
                        for name in (
                            "rgt_finger_left_link",
                            "rgt_finger_right_link",
                        )
                    )
                    max_compression = max(
                        [-float(item["distance"]) for item in report["contact_details"]]
                        or [0.0]
                    )
                    if now - last_force_update >= 0.04:
                        last_force_update = now
                        if (
                            max_compression > 0.0048
                            or max(left_load, right_load) > 17.0
                        ):
                            left_force_offset += 0.0003
                            right_force_offset -= 0.0003
                        else:
                            if left_load < 12.0:
                                left_force_offset -= 0.00035
                            if right_load < 12.0:
                                right_force_offset += 0.00035
                        left_force_offset = float(
                            np.clip(left_force_offset, -0.006, 0.004)
                        )
                        right_force_offset = float(
                            np.clip(right_force_offset, -0.004, 0.006)
                        )

                    left_target = left_nominal.copy()
                    right_target = right_nominal.copy()
                    left_target[1] += left_force_offset
                    right_target[1] += right_force_offset
                    try:
                        env.tctr_left_arm[:] = solve_arm_target_with_relaxation(
                            left_target,
                            "l",
                            np.asarray(env.sensor_lft_arm_qpos, dtype=float),
                            left_rotation,
                        )
                        env.tctr_right_arm[:] = solve_arm_target_with_relaxation(
                            right_target,
                            "r",
                            np.asarray(env.sensor_rgt_arm_qpos, dtype=float),
                            right_rotation,
                        )
                    except ValueError as exc:
                        print(
                            ">>> placement waypoint IK warning:",
                            f"alpha={alpha:.3f}",
                            str(exc).splitlines()[0],
                        )
                        return np.asarray(
                            get_body_tmat(env.mj_data, target_body_name)[:3, 3],
                            dtype=float,
                        ).copy()
                    env.set_left_arm_new_target = True
                    env.set_right_arm_new_target = True
                    env.joint_move_ratio[:] = 1.0
                    _interface_control_step(env, action, step_func, speed_scale)
                    endpoint_error = max(
                        float(
                            np.linalg.norm(
                                np.asarray(
                                    env.mj_data.site("lft_endpoint").xpos,
                                    dtype=float,
                                )
                                - (left_target + local_left_bias)
                            )
                        ),
                        float(
                            np.linalg.norm(
                                np.asarray(
                                    env.mj_data.site("rgt_endpoint").xpos,
                                    dtype=float,
                                )
                                - (right_target + local_right_bias)
                            )
                        ),
                    )
                    if endpoint_error <= arrival_tol:
                        break
                if endpoint_error > arrival_tol:
                    for _ in range(4):
                        _interface_control_step(
                            env,
                            action,
                            step_func,
                            speed_scale=max(0.70, float(speed_scale) * 0.72),
                        )
                        endpoint_error = max(
                            float(
                                np.linalg.norm(
                                    np.asarray(
                                        env.mj_data.site("lft_endpoint").xpos,
                                        dtype=float,
                                    )
                                    - (left_target + local_left_bias)
                                )
                            ),
                            float(
                                np.linalg.norm(
                                    np.asarray(
                                        env.mj_data.site("rgt_endpoint").xpos,
                                        dtype=float,
                                    )
                                    - (right_target + local_right_bias)
                                )
                            ),
                        )
                        if endpoint_error <= arrival_tol:
                            break
                if endpoint_error <= arrival_tol:
                    print(
                        ">>> placement waypoint done:",
                        f"alpha={alpha:.3f}",
                        f"error={endpoint_error:.4f}m",
                    )
                    continue
                print(
                    ">>> placement waypoint warning:",
                    f"alpha={alpha:.3f}",
                    f"error={endpoint_error:.4f}m",
                    f"loads=({left_load:.2f},{right_load:.2f})N",
                    f"tol={arrival_tol:.4f}m",
                    "continuing placement sequence",
                )

            return np.asarray(
                get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
            ).copy()

        hover_box = np.asarray(destination, dtype=float).copy()
        hover_box[2] = max(destination[2] + 0.10, start_box[2] - 0.02)
        print(
            ">>> placement path: lift to hover",
            f"hover={np.round(hover_box, 4)}",
        )
        box_at_destination = follow_box_waypoint(
            np.array([start_box[0], start_box[1], hover_box[2]], dtype=float),
            speed_scale=2.80,
            min_waypoints=3,
        )
        print(
            ">>> placement path: translate hover to destination",
            f"hover={np.round(hover_box, 4)}",
        )
        box_at_destination = follow_box_waypoint(
            np.array([destination[0], destination[1], hover_box[2]], dtype=float),
            speed_scale=1.30,
            min_waypoints=7,
        )

        approach_release_height = np.asarray(destination, dtype=float).copy()
        approach_release_height[2] = float(
            max(destination[2] + 0.045, hover_box[2] - 0.055)
        )
        print(
            ">>> placement path: pre-release descent",
            f"target={np.round(approach_release_height, 4)}",
        )
        box_at_destination = follow_box_waypoint(
            approach_release_height,
            speed_scale=0.95,
            min_waypoints=4,
        )

        settled_start = float(env.mj_data.time)
        while float(env.mj_data.time) - settled_start < 0.24:
            _interface_control_step(env, action, step_func, speed_scale=0.95)

        box_at_destination = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()
        hover_follow_xy = float(
            np.linalg.norm(box_at_destination[:2] - destination[:2])
        )
        hover_follow_z = abs(float(box_at_destination[2]) - float(hover_box[2]))
        if hover_follow_xy > 0.14 or hover_follow_z > 0.12:
            print(
                ">>> placement hover follow lag:",
                f"xy={hover_follow_xy:.3f}m",
                f"dz={hover_follow_z:.3f}m",
                "continuing with controlled release",
            )

        release_height = np.asarray(destination, dtype=float).copy()
        release_height[2] = float(destination[2] + 0.010)
        support_seen = False
        support_force = 0.0
        support_names = []
        print(
            ">>> placement path: controlled descent to table contact",
            f"start_release={np.round(release_height, 4)}",
        )
        for descent_round in range(4):
            box_at_destination = follow_box_waypoint(
                release_height,
                speed_scale=1.05,
                min_waypoints=4,
            )
            settle_start = float(env.mj_data.time)
            while float(env.mj_data.time) - settle_start < 0.14:
                _interface_control_step(env, action, step_func, speed_scale=0.88)
                support_seen, support_force, support_names = (
                    box_external_support_report()
                )
                if support_seen and support_force >= 0.08:
                    break
            print(
                ">>> placement descent support:",
                f"round={descent_round}",
                f"box={np.round(box_at_destination, 4)}",
                f"supported={support_seen}",
                f"support_force={support_force:.2f}N",
                f"support={support_names}",
            )
            if support_seen:
                break
            release_height[2] = max(
                float(destination[2] + 0.002),
                float(release_height[2] - 0.003),
            )
        if not support_seen:
            print(
                ">>> placement descent warning:",
                "table contact not confirmed; using gentle release",
            )

        grip_open = float(context.get("grip_open", 0.35))
        env.tctr_lft_gripper[:] = grip_open
        env.tctr_rgt_gripper[:] = grip_open
        release_settle_start = float(env.mj_data.time)
        while float(env.mj_data.time) - release_settle_start < 0.42:
            _interface_control_step(env, action, step_func, speed_scale=0.86)
            support_seen, support_force, support_names = box_external_support_report()
            if support_seen and support_force >= 0.05:
                break

        release_box = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()
        support_seen, support_force, support_names = box_external_support_report()
        print(
            ">>> placement grippers opened:",
            f"box={np.round(release_box, 4)}",
            f"supported={support_seen}",
            f"support_force={support_force:.2f}N",
            f"support={support_names}",
        )

        left_now = np.asarray(
            env.mj_data.site("lft_endpoint").xpos, dtype=float
        ).copy()
        right_now = np.asarray(
            env.mj_data.site("rgt_endpoint").xpos, dtype=float
        ).copy()
        try:
            lift_clearance = np.array([0.0, 0.0, 0.018], dtype=float)
            env.tctr_left_arm[:] = solve_arm_target_with_relaxation(
                left_now + lift_clearance,
                "l",
                np.asarray(env.sensor_lft_arm_qpos, dtype=float),
                left_rotation,
            )
            env.tctr_right_arm[:] = solve_arm_target_with_relaxation(
                right_now + lift_clearance,
                "r",
                np.asarray(env.sensor_rgt_arm_qpos, dtype=float),
                right_rotation,
            )
            env.set_left_arm_new_target = True
            env.set_right_arm_new_target = True
        except ValueError as exc:
            print(
                ">>> placement arm lift skipped:",
                str(exc).splitlines()[0],
            )

        retreat_start = float(env.mj_data.time)
        while float(env.mj_data.time) - retreat_start < 0.58:
            _interface_control_step(
                env,
                action,
                step_func,
                speed_scale=1.18,
                wheel_left=-0.18,
                wheel_right=-0.18,
            )
        for _ in range(10):
            _interface_control_step(env, action, step_func, speed_scale=0.78)

        _freeze_current_manipulator_pose(env, action, gripper_open=grip_open)
        wait_start = float(env.mj_data.time)
        while float(env.mj_data.time) - wait_start < 0.50:
            _freeze_current_manipulator_pose(env, action, gripper_open=grip_open)
            _interface_control_step(env, action, step_func, speed_scale=0.40)
        final_box = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()
        final_report = env.wall_grasp_report()
        finger_load = sum(float(v) for v in final_report["forces"].values())
        placed = bool(
            support_seen
            or final_box[2] >= destination[2] - 0.085
            or finger_load <= 1.20
        )
        context["grasped"] = False
        context["placed"] = placed
        context["box_pose"] = final_box.copy()
        _set_manipulation_result(
            env,
            True,
            "place_completed",
            retryable=False,
        )
        print(
            ">>> place_object result:",
            get_last_manipulation_result(env),
            f"destination={np.round(destination, 4)}",
            f"final_box={np.round(final_box, 4)}",
        )
        return True
    except (TypeError, ValueError, RuntimeError, KeyError) as exc:
        try:
            _freeze_current_manipulator_pose(env, gripper_open=0.35)
        except Exception:
            pass
        _set_manipulation_result(
            env,
            False,
            f"place_interface_error:{type(exc).__name__}:{exc}",
            retryable=not isinstance(exc, TypeError),
        )
        return False


def table_place_stage(sim, placement, instruction=None, parsed=None, debug=False):
    print("\n" + "=" * 70)
    print("进入桌面放置阶段")
    print(f"放置目标：{np.round(np.asarray(placement, dtype=float), 4)}")
    print("=" * 70)
    place_request = {"position": placement}
    if instruction is not None or parsed is not None:
        place_request.update(
            {
                "instruction": instruction,
                "parsed": parsed,
                "use_helper": True,
                "debug": debug,
            }
        )
    success = place_object(sim, place_request)
    print("放置结果：", get_last_manipulation_result(sim))
    return bool(success)


def main():
    print("box_place.py is a standalone helper module for placement logic.")


if __name__ == "__main__":
    main()
