"""Pick the box, hold it still for five seconds, then release it in place."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from box_pick import DEFAULT_DISCOVERSE_ROOT, DEFAULT_MJCF_FILE_PATH, DEFAULT_URDF_PATH


def load_lift_hold_drop_box_pick():
    source = Path(__file__).with_name("box_pick.py")
    source_text = source.read_text(encoding="utf-8")

    clamp_marker = '                    ">>> bilateral closed-gripper clamp acquired; "'
    marker_pos = source_text.rfind(clamp_marker)
    if marker_pos < 0:
        raise RuntimeError("stable box_pick.py clamp-acquired marker was not found")

    steps_start = source_text.find(
        "                execution_steps[step_index + 1:] = [",
        marker_pos,
    )
    if steps_start < 0:
        raise RuntimeError("stable box_pick.py post-clamp step block was not found")

    steps_end_marker = (
        "                step_index += 1\n"
        "                current_step_name = None"
    )
    steps_end = source_text.find(steps_end_marker, steps_start)
    if steps_end < 0:
        raise RuntimeError("stable box_pick.py post-clamp step block end was not found")

    replacement_steps = """                execution_steps[step_index + 1:] = [
                    {
                        "kind": "closed_pair_cartesian_lift",
                        "name": "lift clamped package 5cm then hold",
                        "height": 0.050,
                        "duration": 3.8,
                        "pre_hold": 0.30,
                        "post_hold": 0.35,
                        "settle_timeout": 3.0,
                        "left_endpoint_target": np.asarray(
                            closed_pair_targets_world[0], dtype=float
                        ).copy(),
                        "right_endpoint_target": np.asarray(
                            closed_pair_targets_world[1], dtype=float
                        ).copy(),
                    },
                    {
                        "kind": "lift_hold_still",
                        "name": "hold lifted package still for 5s",
                        "duration": float(hold_seconds),
                    },
                    {
                        "kind": "spread_release_drop",
                        "name": "spread arms and drop package",
                        "duration": 1.6,
                        "settle_duration": 3.0,
                        "spread": 0.065,
                    },
                    {
                        "kind": "hold",
                        "name": "final hold after in-place drop",
                        "duration": 1.0e9,
                    },
                ]
"""

    patched_text = (
        source_text[:steps_start]
        + replacement_steps
        + source_text[steps_end:]
    )

    hold_anchor = '        elif step["kind"] == "hold":\n'
    hold_pos = patched_text.rfind(hold_anchor)
    if hold_pos < 0:
        raise RuntimeError("stable box_pick.py hold handler was not found")

    release_handlers = """        elif step["kind"] == "lift_hold_still":
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if "left_arm_q" not in step:
                step["left_arm_q"] = np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float).copy()
                step["right_arm_q"] = np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float).copy()
                step["start_box"] = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3].copy()
                print(
                    ">>> lifted hold started: "
                    f"duration={float(step['duration']):.1f}s, "
                    f"box={np.round(step['start_box'], 4)}"
                )
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()
            if now - step_enter_time >= float(step["duration"]):
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                print(f">>> lifted hold complete; box={np.round(box_now, 4)}")
                step_index += 1
                current_step_name = None

        elif step["kind"] == "spread_release_drop":
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if "start_left_endpoint" not in step:
                step["start_left_endpoint"] = np.asarray(
                    sim_node.mj_data.site("lft_endpoint").xpos, dtype=float
                ).copy()
                step["start_right_endpoint"] = np.asarray(
                    sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float
                ).copy()
                step["left_ref"] = np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float).copy()
                step["right_ref"] = np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float).copy()
                step["start_box"] = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3].copy()
                print(
                    ">>> release drop started: "
                    f"spread={float(step['spread']) * 100:.1f}cm, "
                    f"box={np.round(step['start_box'], 4)}"
                )
            elapsed = float(now - step_enter_time)
            duration = max(float(step["duration"]), 1.0e-6)
            progress = min(1.0, max(0.0, elapsed / duration))
            alpha = progress * progress * (3.0 - 2.0 * progress)
            spread = float(step["spread"]) * alpha
            left_target = np.asarray(step["start_left_endpoint"], dtype=float).copy()
            right_target = np.asarray(step["start_right_endpoint"], dtype=float).copy()
            left_target[1] += spread
            right_target[1] -= spread
            try:
                left_q = sim_node.solveArmEndTarget(
                    world_to_base(left_target),
                    sim_node.arm_action,
                    "l",
                    np.asarray(step["left_ref"], dtype=float),
                    left_grip_rot,
                )
                right_q = sim_node.solveArmEndTarget(
                    world_to_base(right_target),
                    sim_node.arm_action,
                    "r",
                    np.asarray(step["right_ref"], dtype=float),
                    right_grip_rot,
                )
                step["left_ref"] = np.asarray(left_q, dtype=float).copy()
                step["right_ref"] = np.asarray(right_q, dtype=float).copy()
                sim_node.tctr_left_arm[:] = left_q
                sim_node.tctr_right_arm[:] = right_q
                sim_node.set_left_arm_new_target = True
                sim_node.set_right_arm_new_target = True
                update_joint_move_ratio()
            except ValueError as exc:
                print(f">>> RELEASE DROP IK FAILED: {exc}")
                execution_steps = [
                    {"kind": "hold", "name": "release drop IK failed - inspect scene", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None
                continue
            if elapsed >= duration + float(step.get("settle_duration", 3.0)):
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                physical_grasp_validated = False
                print(
                    ">>> release drop complete; "
                    f"box={np.round(box_now, 4)}, "
                    f"drop={(float(step['start_box'][2]) - float(box_now[2])) * 100:.1f}cm"
                )
                step_index += 1
                current_step_name = None

"""

    patched_text = patched_text[:hold_pos] + release_handlers + patched_text[hold_pos:]

    temp_runtime = source.with_name("_tmp_box_pick_lift_hold_drop_runtime.py")
    temp_runtime.write_text(patched_text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(
        "_box_pick_lift_hold_drop_runtime",
        temp_runtime,
    )
    if spec is None or spec.loader is None:
        temp_runtime.unlink(missing_ok=True)
        raise RuntimeError("could not load lift-hold-drop box_pick module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return temp_runtime, module


def main():
    parser = argparse.ArgumentParser(
        description="Pick the box, hold it still for five seconds, then drop it in place."
    )
    parser.add_argument("--mjcf", default=DEFAULT_MJCF_FILE_PATH)
    parser.add_argument("--discoverse-root", default=DEFAULT_DISCOVERSE_ROOT)
    parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
    parser.add_argument("--headless-preview-seconds", type=float, default=None)
    parser.add_argument("--hold-seconds", type=float, default=5.0)
    args = parser.parse_args()

    temp_runtime, box_pick_runtime = load_lift_hold_drop_box_pick()
    print(
        ">>> lift-hold-drop mode: "
        f"hold={float(args.hold_seconds):.1f}s, release_spread=6.5cm"
    )
    try:
        box_pick_runtime.run_box_pick_grasp_scene(
            args.mjcf,
            args.discoverse_root,
            urdf_path=args.urdf,
            headless=args.headless_preview_seconds is not None,
            max_seconds=args.headless_preview_seconds,
            hold_seconds=args.hold_seconds,
            randomize_scene=False,
            scene_seed=0,
        )
    finally:
        try:
            temp_runtime.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
