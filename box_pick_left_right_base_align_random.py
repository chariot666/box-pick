"""Left/right and height random box pick test with base lateral alignment."""

from __future__ import annotations

import argparse
import importlib.util
import random
from pathlib import Path

from box_pick import DEFAULT_DISCOVERSE_ROOT, DEFAULT_MJCF_FILE_PATH, DEFAULT_URDF_PATH


def choose_scene_params(seed, dy_range, fixed_dy, layer_min, layer_max, fixed_layer):
    actual_seed = random.randrange(0, 2**31) if seed is None else int(seed)
    rng = random.Random(actual_seed)
    box_dy = (
        float(fixed_dy)
        if fixed_dy is not None
        else rng.uniform(-float(dy_range), float(dy_range))
    )
    box_layer = (
        int(fixed_layer)
        if fixed_layer is not None
        else int(rng.randint(int(layer_min), int(layer_max)))
    )
    return actual_seed, box_dy, box_layer


def load_base_align_box_pick(external_box_dy):
    source = Path(r"D:\xwechat_files\wxid_utjw1twu0bqf22_b553\msg\attach\d3c54bc876485ea8e97348aa07f8e47e\2026-08\Rec\dce1cc54e11aa2e5\F\0\box_pick.py")
    source_text = source.read_text(encoding="utf-8")

    original = (
        "    randomized_box_dy = (\n"
        "        float(scene_rng.uniform(-0.100, 0.100))\n"
        "        if randomize_box_pose\n"
        "        else 0.0\n"
        "    )"
    )
    replacement = (
        "    _external_randomized_box_dy = globals().get(\n"
        '        "EXTERNAL_RANDOMIZED_BOX_DY", None\n'
        "    )\n"
        "    randomized_box_dy = (\n"
        "        float(_external_randomized_box_dy)\n"
        "        if _external_randomized_box_dy is not None\n"
        "        else (\n"
        "            float(scene_rng.uniform(-0.100, 0.100))\n"
        "            if randomize_box_pose\n"
        "            else 0.0\n"
        "        )\n"
        "    )"
    )
    source_pos = source_text.rfind(original)
    if source_pos < 0:
        raise RuntimeError("stable box_pick.py lateral randomization block was not found")

    patched_text = (
        source_text[:source_pos]
        + replacement
        + source_text[source_pos + len(original):]
    )

    import_block = (
        "    from wam_critic import WAMCritic, WAMCriticRecorder\n"
        "    from action_wam import ActionWAMCritic\n"
        "    from visual_wam import VisualWAMCritic, VisualWAMRecorder\n"
    )
    import_replacement = (
        "    from wam_critic import WAMCritic, WAMCriticRecorder\n"
        "    from action_wam import ActionWAMCritic\n"
        "    try:\n"
        "        from visual_wam import VisualWAMCritic, VisualWAMRecorder\n"
        "    except Exception:\n"
        "        VisualWAMCritic = None\n"
        "        VisualWAMRecorder = None\n"
    )
    import_pos = patched_text.find(import_block)
    if import_pos < 0:
        raise RuntimeError("stable box_pick.py critic import block was not found")
    patched_text = (
        patched_text[:import_pos]
        + import_replacement
        + patched_text[import_pos + len(import_block):]
    )

    layer_original = "else int(scene_rng.choice((2, 3, 4)))"
    layer_replacement = "else int(scene_rng.choice((3, 4)))"
    layer_pos = patched_text.rfind(layer_original)
    if layer_pos < 0:
        raise RuntimeError("stable box_pick.py shelf-level block was not found")
    patched_text = (
        patched_text[:layer_pos]
        + layer_replacement
        + patched_text[layer_pos + len(layer_original):]
    )

    grasp_originals = (
        (
            "    grasp_z = box_top_z + 0.005\n"
            "    slot_align_z = box_top_z + 0.055\n"
            "    approach_z = slot_align_z + 0.025"
        ),
        (
            "    grasp_z = box_bottom_z + 0.110\n"
            "    # Reach the final clamp height before crossing the cabinet front plane.\n"
            "    # The old trajectory entered above the box and descended beside it; on a\n"
            "    # randomized shelf this swept the vertical fingers and wrist housings\n"
            "    # through the board above.  All ungrasped entry targets now share one Z and\n"
            "    # differ only in X/Y.\n"
            "    slot_align_z = grasp_z\n"
            "    approach_z = grasp_z"
        ),
    )
    grasp_replacements = (
        (
            "    grasp_z = box_top_z - 0.065\n"
            "    slot_align_z = box_top_z + 0.006\n"
            "    approach_z = slot_align_z + 0.006"
        ),
        (
            "    grasp_z = box_top_z - 0.065\n"
            "    slot_align_z = box_top_z + 0.006\n"
            "    approach_z = slot_align_z + 0.006"
        ),
    )
    grasp_pos = -1
    grasp_original = ""
    grasp_replacement = ""
    for candidate, candidate_replacement in zip(grasp_originals, grasp_replacements):
        grasp_pos = patched_text.rfind(candidate)
        if grasp_pos >= 0:
            grasp_original = candidate
            grasp_replacement = candidate_replacement
            break
    if grasp_pos < 0:
        raise RuntimeError("base-align box_pick.py grasp height block was not found")
    patched_text = (
        patched_text[:grasp_pos]
        + grasp_replacement
        + patched_text[grasp_pos + len(grasp_original):]
    )

    settle_original = '                "settle_error": 0.100,'
    settle_replacement = '                "settle_error": 0.220,'
    settle_pos = patched_text.rfind(settle_original)
    if settle_pos < 0:
        raise RuntimeError("stable box_pick.py settle threshold was not found")
    patched_text = (
        patched_text[:settle_pos]
        + settle_replacement
        + patched_text[settle_pos + len(settle_original):]
    )

    step_original = "        cartesian_step=0.006,"
    step_replacement = "        cartesian_step=0.003,"
    step_pos = patched_text.rfind(step_original)
    if step_pos < 0:
        raise RuntimeError("stable box_pick.py synchronized step size was not found")
    patched_text = (
        patched_text[:step_pos]
        + step_replacement
        + patched_text[step_pos + len(step_original):]
    )

    lift_gate_original = (
        "            # Do not advance on the command alone.  Require both physical\n"
        "            # endpoints to have reached the requested clearance and the free box to have\n"
        "            # visibly followed the grasp upward before the wheels may move.\n"
        "            required_endpoint_rise = max(0.015, float(step[\"height\"]) - 0.005)\n"
        "            required_box_rise = max(0.015, float(step[\"height\"]) - 0.010)\n"
        "            endpoints_up = (\n"
        "                left_rise >= required_endpoint_rise\n"
        "                and right_rise >= required_endpoint_rise\n"
        "            )\n"
        "            box_up = box_rise >= required_box_rise\n"
        "            if orientation_excursion_deg > 8.0:\n"
    )
    lift_gate_replacement = (
        "            # Side-clamp extraction only needs the endpoints to clear; the carton\n"
        "            # can lag vertically while the base pulls it out of the shelf.\n"
        "            required_endpoint_rise = max(0.015, float(step[\"height\"]) - 0.005)\n"
        "            endpoints_up = (\n"
        "                left_rise >= required_endpoint_rise\n"
        "                and right_rise >= required_endpoint_rise\n"
        "            )\n"
        "            box_up = True\n"
        "            if orientation_excursion_deg > 8.0:\n"
    )
    lift_gate_pos = patched_text.rfind(lift_gate_original)
    if lift_gate_pos < 0:
        raise RuntimeError("stable box_pick.py pre-retreat lift gate block was not found")
    patched_text = (
        patched_text[:lift_gate_pos]
        + lift_gate_replacement
        + patched_text[lift_gate_pos + len(lift_gate_original):]
    )

    lift_finish_original = (
        "                and endpoints_up\n"
        "                and box_up\n"
        "                and bilateral_contact\n"
    )
    lift_finish_replacement = (
        "                and endpoints_up\n"
        "                and bilateral_contact\n"
    )
    lift_finish_pos = patched_text.rfind(lift_finish_original)
    if lift_finish_pos < 0:
        raise RuntimeError("stable box_pick.py pre-retreat lift completion gate was not found")
    patched_text = (
        patched_text[:lift_finish_pos]
        + lift_finish_replacement
        + patched_text[lift_finish_pos + len(lift_finish_original):]
    )

    clamp_stop_original = (
        '            if not safe_contact:\n'
        '                print(\n'
        '                    ">>> CLOSED CLAMP SAFETY STOP: nonfinger=",\n'
        '                    sorted(closed_report["nonfinger_contacts"]),\n'
        '                )\n'
        '                execution_steps = [\n'
        '                    {"kind": "hold", "name": "closed clamp collision stop", "duration": 1.0e9}\n'
        '                ]\n'
        '                step_index = 0\n'
        '                current_step_name = None\n'
        '                continue\n'
    )
    clamp_stop_replacement = (
        '            if not safe_contact:\n'
        '                blocked_nonfinger = {\n'
        '                    name for name in closed_report["nonfinger_contacts"]\n'
        '                    if not name.startswith("lft_arm_link6")\n'
        '                    and not name.startswith("rgt_arm_link6")\n'
        '                    and not name.startswith("lft_finger")\n'
        '                    and not name.startswith("rgt_finger")\n'
        '                }\n'
        '                if blocked_nonfinger:\n'
        '                    print(\n'
        '                        ">>> CLOSED CLAMP SAFETY STOP: nonfinger=",\n'
        '                        sorted(blocked_nonfinger),\n'
        '                    )\n'
        '                    execution_steps = [\n'
        '                        {"kind": "hold", "name": "closed clamp collision stop", "duration": 1.0e9}\n'
        '                    ]\n'
        '                    step_index = 0\n'
        '                    current_step_name = None\n'
        '                    continue\n'
    )
    clamp_stop_pos = patched_text.rfind(clamp_stop_original)
    if clamp_stop_pos < 0:
        raise RuntimeError("stable box_pick.py closed-clamp safety stop block was not found")
    patched_text = (
        patched_text[:clamp_stop_pos]
        + clamp_stop_replacement
        + patched_text[clamp_stop_pos + len(clamp_stop_original):]
    )

    lift_original = (
        '                        "height": 0.030 if selected_shelf_level == 4 else 0.050,\n'
        '                        "duration": 3.8,\n'
    )
    lift_replacement = (
        '                        "height": 0.045 if selected_shelf_level == 4 else 0.060,\n'
        '                        "duration": 3.8,\n'
    )
    lift_pos = patched_text.rfind(lift_original)
    if lift_pos < 0:
        raise RuntimeError("stable box_pick.py clearance lift block was not found")
    patched_text = (
        patched_text[:lift_pos]
        + lift_replacement
        + patched_text[lift_pos + len(lift_original):]
    )

    retreat_original = (
        '                        "distance": 0.28,\n'
        '                        "duration": 9.0,\n'
    )
    retreat_replacement = (
        '                        "distance": 0.34,\n'
        '                        "duration": 9.0,\n'
    )
    retreat_pos = patched_text.rfind(retreat_original)
    if retreat_pos < 0:
        raise RuntimeError("stable box_pick.py retreat block was not found")
    patched_text = (
        patched_text[:retreat_pos]
        + retreat_replacement
        + patched_text[retreat_pos + len(retreat_original):]
    )

    temp_runtime = Path(__file__).with_name("_tmp_box_pick_lr_base_align_runtime.py")
    temp_runtime.write_text(patched_text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(
        "_box_pick_lr_base_align_runtime",
        temp_runtime,
    )
    if spec is None or spec.loader is None:
        temp_runtime.unlink(missing_ok=True)
        raise RuntimeError("could not load base-align box_pick module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.EXTERNAL_RANDOMIZED_BOX_DY = float(external_box_dy)
    return temp_runtime, module


def main():
    parser = argparse.ArgumentParser(
        description="Run box_pick with left/right box position randomized and the base aligned to the box."
    )
    parser.add_argument("--mjcf", default=DEFAULT_MJCF_FILE_PATH)
    parser.add_argument("--discoverse-root", default=DEFAULT_DISCOVERSE_ROOT)
    parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
    parser.add_argument("--scene-seed", type=int, default=None)
    parser.add_argument("--dy-range", type=float, default=0.15)
    parser.add_argument("--fixed-dy", type=float, default=None)
    parser.add_argument("--layer-min", type=int, default=3)
    parser.add_argument("--layer-max", type=int, default=4)
    parser.add_argument("--fixed-layer", type=int, default=None)
    parser.add_argument("--headless-preview-seconds", type=float, default=None)
    args = parser.parse_args()

    layer_min = max(3, int(args.layer_min))
    layer_max = min(4, int(args.layer_max))
    if layer_min > layer_max:
        raise ValueError("layer-min must be <= layer-max")

    seed, box_dy, box_layer = choose_scene_params(
        args.scene_seed,
        args.dy_range,
        args.fixed_dy,
        layer_min,
        layer_max,
        args.fixed_layer,
    )
    print(
        ">>> randomized scene: "
        f"seed={seed}, box_dy={box_dy:.4f}, box_layer={box_layer}, "
        f"dy_range={float(args.dy_range):.4f}, layer_range={layer_min}-{layer_max}"
    )

    temp_runtime, box_pick_runtime = load_base_align_box_pick(box_dy)
    print(
        ">>> base lateral alignment enabled: "
        f"target_dy={box_dy:+.4f}m, base will move before grasping"
    )

    try:
        box_pick_runtime.run_box_pick_grasp_scene(
            str(Path(args.mjcf)),
            args.discoverse_root,
            urdf_path=args.urdf,
            headless=args.headless_preview_seconds is not None,
            max_seconds=args.headless_preview_seconds,
            randomize_scene=False,
            randomize_box_pose=True,
            shelf_level=box_layer,
            scene_seed=seed,
        )
    finally:
        try:
            temp_runtime.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
