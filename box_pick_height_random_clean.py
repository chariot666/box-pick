"""Height-only random box pick test using the stable box_pick logic."""

from __future__ import annotations

import argparse
import importlib.util
import random
import xml.etree.ElementTree as ET
from pathlib import Path

from box_pick import (
    DEFAULT_DISCOVERSE_ROOT,
    DEFAULT_MJCF_FILE_PATH,
    DEFAULT_URDF_PATH,
)


SHELF_LAYER_Z = {
    1: 0.311,
    2: 0.611,
    3: 0.911,
    4: 1.211,
    5: 1.511,
    6: 1.811,
}


def load_lower_grasp_box_pick():
    source = Path(__file__).with_name("box_pick.py")
    source_text = source.read_text(encoding="utf-8")
    original = (
        "    grasp_z = box_top_z + 0.005\n"
        "    slot_align_z = box_top_z + 0.055\n"
        "    approach_z = slot_align_z + 0.025"
    )
    replacement = (
        "    grasp_z = box_top_z - 0.065\n"
        "    slot_align_z = box_top_z + 0.006\n"
        "    approach_z = slot_align_z + 0.006"
    )
    source_pos = source_text.rfind(original)
    if source_pos < 0:
        raise RuntimeError("stable box_pick.py grasp height block was not found")

    patched_text = (
        source_text[:source_pos]
        + replacement
        + source_text[source_pos + len(original):]
    )
    settle_original = '                "settle_error": 0.100,'
    settle_replacement = '                "settle_error": 0.220,'
    settle_pos = patched_text.rfind(settle_original)
    if settle_pos < 0:
        raise RuntimeError("stable box_pick.py high alignment settle threshold was not found")
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

    temp_runtime = source.with_name("_tmp_box_pick_height_runtime.py")
    temp_runtime.write_text(
        patched_text,
        encoding="utf-8",
    )
    spec = importlib.util.spec_from_file_location(
        "_box_pick_height_runtime",
        temp_runtime,
    )
    if spec is None or spec.loader is None:
        temp_runtime.unlink(missing_ok=True)
        raise RuntimeError("could not load lower-grasp box_pick module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return temp_runtime, module


def make_height_mjcf(source_mjcf, seed, layer_min, layer_max, fixed_layer):
    source = Path(source_mjcf)
    if not source.exists():
        raise FileNotFoundError(f"MJCF file does not exist: {source}")

    actual_seed = random.randrange(0, 2**31) if seed is None else int(seed)
    rng = random.Random(actual_seed)
    if fixed_layer is None:
        box_layer = rng.randint(int(layer_min), int(layer_max))
    else:
        box_layer = int(fixed_layer)

    if box_layer not in SHELF_LAYER_Z:
        raise ValueError(f"box layer must be one of {sorted(SHELF_LAYER_Z)}")

    tree = ET.parse(source)
    root = tree.getroot()
    box = root.find(".//body[@name='box_yellow']")
    if box is None:
        raise ValueError("box_yellow body not found in MJCF")

    pos = [float(v) for v in box.attrib["pos"].split()]
    pos[2] = SHELF_LAYER_Z[box_layer]
    box.attrib["pos"] = " ".join(f"{v:.6f}" for v in pos)

    temp_mjcf = source.with_name("_tmp_box_pick_height_random.xml")
    tree.write(temp_mjcf, encoding="utf-8", xml_declaration=True)
    return temp_mjcf, actual_seed, box_layer, pos[2]


def main():
    parser = argparse.ArgumentParser(
        description="Run box_pick with only the box height randomized."
    )
    parser.add_argument("--mjcf", default=DEFAULT_MJCF_FILE_PATH)
    parser.add_argument("--discoverse-root", default=DEFAULT_DISCOVERSE_ROOT)
    parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
    parser.add_argument("--scene-seed", type=int, default=None)
    parser.add_argument("--layer-min", type=int, default=3)
    parser.add_argument("--layer-max", type=int, default=4)
    parser.add_argument("--fixed-layer", type=int, default=None)
    parser.add_argument("--headless-preview-seconds", type=float, default=None)
    args = parser.parse_args()

    layer_min = max(2, int(args.layer_min))
    layer_max = min(4, int(args.layer_max))
    if layer_min > layer_max:
        raise ValueError("layer-min must be <= layer-max")

    temp_mjcf, seed, box_layer, box_z = make_height_mjcf(
        args.mjcf,
        args.scene_seed,
        layer_min,
        layer_max,
        args.fixed_layer,
    )
    print(
        ">>> height-only randomized scene: "
        f"seed={seed}, box_layer={box_layer}, box_z={box_z:.3f}, "
        f"layer_range={layer_min}-{layer_max}"
    )

    temp_runtime, box_pick_runtime = load_lower_grasp_box_pick()
    print(
        ">>> lower grasp heights: "
        "grasp=box_top-0.065, slot_align=box_top+0.006, "
        "approach=slot_align+0.006"
    )
    print(">>> high alignment settle tolerance: 0.220 rad")
    print(">>> synchronized insertion step: 0.003 m")

    try:
        box_pick_runtime.run_box_pick_grasp_scene(
            str(temp_mjcf),
            args.discoverse_root,
            urdf_path=args.urdf,
            headless=args.headless_preview_seconds is not None,
            max_seconds=args.headless_preview_seconds,
            randomize_scene=False,
            scene_seed=0,
        )
    finally:
        try:
            temp_mjcf.unlink()
        except OSError:
            pass
        try:
            temp_runtime.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
