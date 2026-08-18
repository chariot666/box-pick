"""Left/right-only random box pick test using the stable box_pick logic."""

from __future__ import annotations

import argparse
import random
import xml.etree.ElementTree as ET
from pathlib import Path

from box_pick import (
    DEFAULT_DISCOVERSE_ROOT,
    DEFAULT_MJCF_FILE_PATH,
    DEFAULT_URDF_PATH,
    run_box_pick_grasp_scene,
)


def make_left_right_mjcf(source_mjcf, seed, dy_range, fixed_dy):
    source = Path(source_mjcf)
    if not source.exists():
        raise FileNotFoundError(f"MJCF file does not exist: {source}")

    actual_seed = random.randrange(0, 2**31) if seed is None else int(seed)
    rng = random.Random(actual_seed)
    box_dy = float(fixed_dy) if fixed_dy is not None else rng.uniform(-float(dy_range), float(dy_range))

    tree = ET.parse(source)
    root = tree.getroot()
    box = root.find(".//body[@name='box_yellow']")
    if box is None:
        raise ValueError("box_yellow body not found in MJCF")

    pos = [float(v) for v in box.attrib["pos"].split()]
    pos[1] += box_dy
    box.attrib["pos"] = " ".join(f"{v:.6f}" for v in pos)

    temp_mjcf = source.with_name("_tmp_box_pick_lr_random.xml")
    tree.write(temp_mjcf, encoding="utf-8", xml_declaration=True)
    return temp_mjcf, actual_seed, box_dy


def main():
    parser = argparse.ArgumentParser(
        description="Run box_pick with only left/right box position randomized."
    )
    parser.add_argument("--mjcf", default=DEFAULT_MJCF_FILE_PATH)
    parser.add_argument("--discoverse-root", default=DEFAULT_DISCOVERSE_ROOT)
    parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
    parser.add_argument("--scene-seed", type=int, default=None)
    parser.add_argument("--dy-range", type=float, default=0.15)
    parser.add_argument("--fixed-dy", type=float, default=None)
    parser.add_argument("--headless-preview-seconds", type=float, default=None)
    args = parser.parse_args()

    temp_mjcf, seed, box_dy = make_left_right_mjcf(
        args.mjcf,
        args.scene_seed,
        args.dy_range,
        args.fixed_dy,
    )
    print(
        ">>> left/right-only randomized scene: "
        f"seed={seed}, box_dy={box_dy:.4f}, dy_range={float(args.dy_range):.4f}"
    )

    try:
        run_box_pick_grasp_scene(
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


if __name__ == "__main__":
    main()
