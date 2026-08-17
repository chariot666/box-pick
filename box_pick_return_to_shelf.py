# # import argparse
# # import math
# # import random
# # import sys
# # import time
# # from dataclasses import dataclass
# # from pathlib import Path

# # import numpy as np

# # pin = None
# # go = None


# # DEFAULT_URDF_PATH = (
# #     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/models/urdf/mmk2_s_g2.urdf"
# # )
# # DEFAULT_DISCOVERSE_ROOT = (
# #     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE"
# # )

# # DEFAULT_MJCF_FILE_PATH = (
# #     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/"
# #     "models/mjcf/tasks_mmk2/task1_pick_and_place.xml"
# # )

# # LEFT_EEF_FRAME = "left_end_link"
# # RIGHT_EEF_FRAME = "right_end_link"
# # ACTIVE_JOINT_NAMES = [
# #     "left_joint1",
# #     "left_joint2",
# #     "left_joint3",
# #     "left_joint4",
# #     "left_joint5",
# #     "left_joint6",
# #     "right_joint1",
# #     "right_joint2",
# #     "right_joint3",
# #     "right_joint4",
# #     "right_joint5",
# #     "right_joint6",
# # ]

# # DEFAULT_BOX_HALF_WIDTH_Y = 0.08
# # LEFT_GRIP_ROT = np.array([
# #     [0.0, 0.998482379, 0.055072124],
# #     [0.422618262, -0.049912294, 0.904932355],
# #     [0.906307787, 0.023274485, -0.421976887],
# # ])
# # RIGHT_GRIP_ROT = np.array([
# #     [0.0, -0.998482379, 0.055072124],
# #     [-0.422618262, -0.049912294, -0.904932355],
# #     [0.906307787, -0.023274485, -0.421976887],
# # ])


# # @dataclass
# # class AABB:
# #     name: str
# #     minimum: np.ndarray
# #     maximum: np.ndarray

# #     def inflated(self, radius):
# #         return AABB(self.name, self.minimum - radius, self.maximum + radius)


# # def ensure_discoverse_import_path(discoverse_root):
# #     discoverse_root = Path(discoverse_root)
# #     if not discoverse_root.exists():
# #         raise FileNotFoundError(f"DISCOVERSE root does not exist: {discoverse_root}")
# #     root_str = str(discoverse_root)
# #     if root_str not in sys.path:
# #         sys.path.insert(0, root_str)


# # def mat3_mul(a, b):
# #     a = np.asarray(a, dtype=float)
# #     b = np.asarray(b, dtype=float)
# #     out = np.empty((3, 3), dtype=float)
# #     for i in range(3):
# #         for j in range(3):
# #             out[i, j] = (
# #                 a[i, 0] * b[0, j]
# #                 + a[i, 1] * b[1, j]
# #                 + a[i, 2] * b[2, j]
# #             )
# #     return out


# # def get_box_half_extent_y(mj_model, body_name="box_yellow"):
# #     import mujoco

# #     try:
# #         body_id = int(mj_model.body(body_name).id)
# #     except Exception as exc:
# #         print(f"warning: body {body_name!r} not found ({exc}); use default half-y")
# #         return DEFAULT_BOX_HALF_WIDTH_Y

# #     geom_start = int(mj_model.body_geomadr[body_id])
# #     geom_num = int(mj_model.body_geomnum[body_id])
# #     if geom_num == 0:
# #         return DEFAULT_BOX_HALF_WIDTH_Y

# #     for geom_id in range(geom_start, geom_start + geom_num):
# #         geom_type = mj_model.geom_type[geom_id]
# #         if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
# #             return float(mj_model.geom_size[geom_id, 1])
# #         if geom_type == mujoco.mjtGeom.mjGEOM_MESH:
# #             mesh_id = int(mj_model.geom_dataid[geom_id])
# #             vert_adr = int(mj_model.mesh_vertadr[mesh_id])
# #             vert_num = int(mj_model.mesh_vertnum[mesh_id])
# #             verts = mj_model.mesh_vert[vert_adr: vert_adr + vert_num]
# #             return float((verts[:, 1].max() - verts[:, 1].min()) / 2.0)

# #     return DEFAULT_BOX_HALF_WIDTH_Y


# # def show_discoverse_mjcf_scene(
# #     mjcf_path,
# #     discoverse_root=DEFAULT_DISCOVERSE_ROOT,
# #     headless=False,
# #     max_seconds=None,
# # ):
# #     """Open the same DISCOVERSE MJCF task window used by the competition code."""
# #     ensure_discoverse_import_path(discoverse_root)

# #     from discoverse.robots_env.mmk2_base import MMK2Base, MMK2Cfg
# #     from discoverse.utils import step_func

# #     class MjcfPreviewNode(MMK2Base):
# #         def __init__(self, config):
# #             super().__init__(config)
# #             if "head_cam" in self.camera_names:
# #                 self.cam_id = self.camera_names.index("head_cam")
# #                 self.config.obs_rgb_cam_id = [self.cam_id]
# #                 print("render camera: head_cam", "id=", self.cam_id)
# #             elif self.camera_names:
# #                 self.cam_id = 0
# #                 self.config.obs_rgb_cam_id = [0]
# #                 print("render camera:", self.camera_names[0], "id= 0")
# #             else:
# #                 self.cam_id = -1
# #                 self.config.obs_rgb_cam_id = [-1]
# #                 print("render camera: free")

# #         def post_physics_step(self):
# #             pass

# #         def getChangedObjectPose(self):
# #             return {}

# #         def checkTerminated(self):
# #             return False

# #         def getObservation(self):
# #             return {}

# #         def getPrivilegedObservation(self):
# #             return {}

# #         def getReward(self):
# #             return 0.0

# #     def set_stage_targets(target_control, stage):
# #         if stage == 1:
# #             print(">>> stage 1: lift/head ready")
# #             target_control[2] = 0.14
# #             target_control[3:5] = [0.0, -0.25]
# #             target_control[11] = 0.0
# #             target_control[18] = 0.0
# #         elif stage == 2:
# #             print(">>> stage 2: move arms forward")
# #             target_control[5:11] = [0.31, -1.473, 2.076, -1.391, 1.496, -2.0]
# #             target_control[12:18] = [-0.31, -1.473, 2.076, 1.391, -1.496, 2.0]
# #         elif stage == 3:
# #             print(">>> stage 3: extend grippers deeper toward box sides")
# #             target_control[5:11] = [0.45, -1.473, 2.076, -1.391, 1.496, -2.0]
# #             target_control[12:18] = [-0.45, -1.473, 2.076, 1.391, -1.496, 2.0]
# #             target_control[11] = 0.0
# #             target_control[18] = 0.0
# #         elif stage == 4:
# #             print(">>> stage 4: hold clamp")
# #             target_control[11] = 0.0
# #             target_control[18] = 0.0

# #     cfg = MMK2Cfg()
# #     cfg.mjcf_file_path = str(mjcf_path)
# #     cfg.use_gaussian_renderer = False
# #     cfg.headless = headless
# #     cfg.enable_render = not headless
# #     cfg.sync = True
# #     cfg.render_set = {
# #         "fps": 30,
# #         "width": 1280,
# #         "height": 720,
# #         "window_title": "DISCOVERSE MJCF",
# #     }
# #     cfg.obs_rgb_cam_id = None
# #     cfg.obs_depth_cam_id = None
# #     cfg.init_state = {
# #         "base_position": [0.58, 0.715, 0.0],
# #         "base_orientation": [1.0, 0.0, 0.0, 0.0],
# #         "slide_qpos": [0.0],
# #         "head_qpos": [0.0, 0.0],
# #         "lft_arm_qpos": [0.0, -0.166, 0.032, 0.0, 1.571, 2.223],
# #         "lft_gripper_qpos": [0.0],
# #         "rgt_arm_qpos": [0.0, -0.166, 0.032, 0.0, -1.571, -2.223],
# #         "rgt_gripper_qpos": [0.0],
# #     }

# #     sim_node = MjcfPreviewNode(cfg)
# #     obs = sim_node.reset()
# #     target_control = sim_node.init_joint_ctrl.copy()
# #     action = target_control.copy()
# #     stage = 0
# #     stage_start_time = sim_node.mj_data.time
# #     print("DISCOVERSE MJCF window opened. Auto motion enabled. Close the window to exit.")
# #     while sim_node.running:
# #         now = sim_node.mj_data.time
# #         if max_seconds is not None and now >= max_seconds:
# #             print(
# #                 "preview finished:",
# #                 "time=", round(float(now), 3),
# #                 "slide=", np.array2string(sim_node.sensor_slide_qpos, precision=3),
# #                 "head=", np.array2string(sim_node.sensor_head_qpos, precision=3),
# #                 "left_arm=", np.array2string(sim_node.sensor_lft_arm_qpos, precision=3),
# #                 "right_arm=", np.array2string(sim_node.sensor_rgt_arm_qpos, precision=3),
# #             )
# #             break
# #         stage_elapsed = now - stage_start_time

# #         if stage == 0 and stage_elapsed > 0.5:
# #             stage = 1
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)
# #         elif stage == 1 and stage_elapsed > 1.2:
# #             stage = 2
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)
# #         elif stage == 2 and stage_elapsed > 2.5:
# #             stage = 3
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)
# #         elif stage == 3 and stage_elapsed > 2.0:
# #             stage = 4
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)

# #         for i in range(2, sim_node.njctrl):
# #             action[i] = step_func(action[i], target_control[i], 0.8 * sim_node.delta_t)
# #         action[0] = 0.0
# #         action[1] = 0.0
# #         obs, _, _, _, _ = sim_node.step(action)


# # def run_box_pick_grasp_scene(
# #     mjcf_path,
# #     discoverse_root=DEFAULT_DISCOVERSE_ROOT,
# #     headless=False,
# #     max_seconds=None,
# # ):
# #     """Run the self-contained box side-wall grasp state machine."""
# #     ensure_discoverse_import_path(discoverse_root)

# #     import mujoco
# #     import types

# #     if "mediapy" not in sys.modules:
# #         mediapy_stub = types.ModuleType("mediapy")
# #         mediapy_stub.write_video = lambda *args, **kwargs: None
# #         sys.modules["mediapy"] = mediapy_stub

# #     from discoverse.robots import AirbotPlayIK, MMK2FIK
# #     from discoverse.robots_env.mmk2_base import MMK2Cfg
# #     from discoverse.task_base import MMK2TaskBase
# #     from discoverse.utils import get_body_tmat, step_func

# #     class StableAirbotPlayIK(AirbotPlayIK):
# #         def properIK(self, pos, ori, ref_q=None):
# #             return self.inverseKin(pos, mat3_mul(ori, self.arm_rot_mat), ref_q)

# #         def inverseKin(self, pos, ori, ref_q=None):
# #             assert len(pos) == 3 and ori.shape == (3, 3)
# #             pos = self.move_joint6_2_joint5(pos, ori)
# #             angle = [0.0] * 6
# #             candidates = []

# #             for i1 in [1, -1]:
# #                 angle[0] = np.arctan2(i1 * pos[1], i1 * pos[0])
# #                 c3 = (
# #                     pos[0] ** 2
# #                     + pos[1] ** 2
# #                     + (pos[2] - self.a1) ** 2
# #                     - self.a3 ** 2
# #                     - self.a4 ** 2
# #                 ) / (2 * self.a3 * self.a4)
# #                 if c3 > 1 or c3 < -1:
# #                     raise ValueError(f"Fail to solve inverse kinematics: pos={pos}, ori={ori}")

# #                 for i2 in [1, -1]:
# #                     s3 = i2 * np.sqrt(1 - c3 ** 2)
# #                     angle[2] = np.arctan2(s3, c3)
# #                     k1 = self.a3 + self.a4 * c3
# #                     k2 = self.a4 * s3
# #                     reach_xy = np.sqrt(pos[0] ** 2 + pos[1] ** 2)
# #                     angle[1] = np.arctan2(
# #                         k1 * (pos[2] - self.a1) - i1 * k2 * reach_xy,
# #                         i1 * k1 * reach_xy + k2 * (pos[2] - self.a1),
# #                     )
# #                     rot = np.array([
# #                         [
# #                             np.cos(angle[0]) * np.cos(angle[1] + angle[2]),
# #                             -np.cos(angle[0]) * np.sin(angle[1] + angle[2]),
# #                             np.sin(angle[0]),
# #                         ],
# #                         [
# #                             np.sin(angle[0]) * np.cos(angle[1] + angle[2]),
# #                             -np.sin(angle[0]) * np.sin(angle[1] + angle[2]),
# #                             -np.cos(angle[0]),
# #                         ],
# #                         [np.sin(angle[1] + angle[2]), np.cos(angle[1] + angle[2]), 0.0],
# #                     ])
# #                     ori1 = mat3_mul(rot.T, ori)
# #                     for i5 in [1, -1]:
# #                         angle[3] = np.arctan2(i5 * ori1[2, 2], i5 * ori1[1, 2])
# #                         angle[4] = np.arctan2(
# #                             i5 * np.sqrt(ori1[2, 2] ** 2 + ori1[1, 2] ** 2),
# #                             ori1[0, 2],
# #                         )
# #                         angle[5] = np.arctan2(-i5 * ori1[0, 0], -i5 * ori1[0, 1])
# #                         js = self.add_bias(angle)
# #                         if np.all((js > self.arm_joint_range[0]) * (js < self.arm_joint_range[1])):
# #                             candidates.append(js)

# #             if len(candidates) == 0:
# #                 raise ValueError(f"Fail to solve inverse kinematics: pos={pos}, ori={ori}")

# #             if ref_q is not None:
# #                 joint_dist = [
# #                     np.sum(np.abs(ref_q - js) / self.joint_range_scale)
# #                     for js in candidates
# #                 ]
# #                 return candidates[int(np.argmin(joint_dist))]
# #             return candidates[0]

# #     target_body_name = "box_yellow"
# #     grip_close = 0.0
# #     grip_open = 0.35
# #     head_pitch = -0.25
# #     pre_x_backoff = 0.11
# #     grasp_x_backoff = 0.00
# #     pre_clearance = 0.050
# #     deep_pre_clearance = 0.035
# #     contact_z_bias = 0.115
# #     squeeze_clearances = (0.045, 0.035, 0.025)
# #     squeeze_diagonal_x = (0.020, 0.030, 0.035)
# #     pull_clearance = -0.055
# #     pull_dx_steps = (0.025, 0.055, 0.085, 0.115, 0.145, 0.175, 0.205, 0.235, 0.265)
# #     outward_grip_angle = np.deg2rad(5.0)

# #     def rot_z(angle):
# #         c = float(np.cos(angle))
# #         s = float(np.sin(angle))
# #         return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])

# #     left_grip_rot = mat3_mul(LEFT_GRIP_ROT, rot_z(outward_grip_angle))
# #     right_grip_rot = mat3_mul(RIGHT_GRIP_ROT, rot_z(-outward_grip_angle))

# #     class MyAlgorithmNode(MMK2TaskBase):
# #         def __init__(self, config):
# #             self._arm_ik_solver = None
# #             super().__init__(config)
# #             self._arm_ik_solver = StableAirbotPlayIK()
# #             for actuator_name in ("lft_gripper", "rgt_gripper"):
# #                 actuator_id = int(self.mj_model.actuator(actuator_name).id)
# #                 self.mj_model.actuator_gainprm[actuator_id, 0] = 8.0
# #                 self.mj_model.actuator_forcelimited[actuator_id] = 1
# #                 self.mj_model.actuator_forcerange[actuator_id, :] = [-4.0, 4.0]
# #             self._configure_grasp_contacts()
# #             if "head_cam" in self.camera_names:
# #                 self.cam_id = self.camera_names.index("head_cam")
# #                 self.config.obs_rgb_cam_id = [self.cam_id]
# #                 print("render camera: head_cam", "id=", self.cam_id)
# #             elif self.camera_names:
# #                 self.cam_id = 0
# #                 self.config.obs_rgb_cam_id = [0]
# #                 print("render camera:", self.camera_names[0], "id= 0")
# #             else:
# #                 self.cam_id = -1
# #                 self.config.obs_rgb_cam_id = [-1]
# #                 print("render camera: free")

# #         def _configure_grasp_contacts(self):
# #             target_body_id = int(self.mj_model.body(target_body_name).id)
# #             old_mass = float(self.mj_model.body_mass[target_body_id])
# #             if old_mass > 0.25:
# #                 scale = 0.25 / old_mass
# #                 self.mj_model.body_mass[target_body_id] = 0.25
# #                 self.mj_model.body_inertia[target_body_id, :] *= scale
# #                 print("target mass:", old_mass, "->", 0.25)

# #             contact_bodies = {
# #                 target_body_name,
# #                 "lft_finger_left_link",
# #                 "lft_finger_right_link",
# #                 "rgt_finger_left_link",
# #                 "rgt_finger_right_link",
# #             }
# #             for geom_id in range(self.mj_model.ngeom):
# #                 body_name = self.mj_model.body(int(self.mj_model.geom_bodyid[geom_id])).name
# #                 if body_name in contact_bodies:
# #                     self.mj_model.geom_friction[geom_id, :] = [5.0, 0.12, 0.012]
# #                     self.mj_model.geom_solref[geom_id, :] = [0.004, 1.0]
# #                     self.mj_model.geom_solimp[geom_id, :] = [0.98, 0.995, 0.001, 0.5, 2.0]
# #             mujoco.mj_setConst(self.mj_model, self.mj_data)
# #             mujoco.mj_forward(self.mj_model, self.mj_data)
# #             print("grasp contact friction configured")

# #         def setArmEndTarget(self, target_pose, arm_action, arm, q_ref, a_rot):
# #             rotation = mat3_mul(MMK2FIK.action_rot[arm_action][arm], a_rot)
# #             position = target_pose[:3, 3] if target_pose.shape == (4, 4) else target_pose
# #             chest_pos = np.array([0.02371, 0.0, 1.311 - self.tctr_slide[0]])
# #             if arm == "l":
# #                 arm_base_tmat = MMK2FIK.TMat_chest2lft_base
# #             else:
# #                 arm_base_tmat = MMK2FIK.TMat_chest2rgt_base
# #             arm_base_pos = chest_pos + arm_base_tmat[:3, 3]
# #             delta = np.asarray(position, dtype=float) - arm_base_pos
# #             rot = arm_base_tmat[:3, :3]
# #             position_local = np.array([
# #                 rot[0, 0] * delta[0] + rot[1, 0] * delta[1] + rot[2, 0] * delta[2],
# #                 rot[0, 1] * delta[0] + rot[1, 1] * delta[1] + rot[2, 1] * delta[2],
# #                 rot[0, 2] * delta[0] + rot[1, 2] * delta[1] + rot[2, 2] * delta[2],
# #             ])
# #             rq = self._arm_ik_solver.properIK(position_local, rotation, q_ref)
# #             if arm == "l":
# #                 self.tctr_left_arm[:] = rq
# #                 self.set_left_arm_new_target = True
# #             else:
# #                 self.tctr_right_arm[:] = rq
# #                 self.set_right_arm_new_target = True

# #         def post_physics_step(self):
# #             pass

# #         def getChangedObjectPose(self):
# #             return {}

# #         def checkTerminated(self):
# #             return False

# #         def getObservation(self):
# #             return super().getObservation()

# #         def getPrivilegedObservation(self):
# #             return self.obs

# #         def getReward(self):
# #             return 0.0

# #         def check_success(self):
# #             return False

# #     def side_targets(
# #         box_pos,
# #         half_y,
# #         clearance,
# #         x_backoff,
# #         z_lift=0.0,
# #         side_axis=None,
# #         diagonal_x=0.0,
# #     ):
# #         if side_axis is None:
# #             axis = np.array([0.0, 1.0, 0.0])
# #         else:
# #             axis = np.asarray(side_axis, dtype=float).copy()
# #             axis[2] = 0.0
# #             norm = np.linalg.norm(axis)
# #             axis = np.array([0.0, 1.0, 0.0]) if norm < 1e-6 else axis / norm
# #         z = box_pos[2] + contact_z_bias + z_lift
# #         center = np.array([box_pos[0] - x_backoff, box_pos[1], z])
# #         point_a = center + axis * (half_y + clearance)
# #         point_b = center - axis * (half_y + clearance)
# #         if point_a[1] >= point_b[1]:
# #             left, right = point_a, point_b
# #         else:
# #             left, right = point_b, point_a
# #         left = left.copy()
# #         right = right.copy()
# #         left[0] -= diagonal_x
# #         right[0] += diagonal_x
# #         return left, right

# #     def set_dual_targets(sim_node, left_world, right_world, label):
# #         old_l = sim_node.tctr_left_arm.copy()
# #         old_r = sim_node.tctr_right_arm.copy()
# #         try:
# #             left_base = world_to_base(left_world)
# #             right_base = world_to_base(right_world)
# #             sim_node.setArmEndTarget(left_base, sim_node.arm_action, "l", old_l, left_grip_rot)
# #             sim_node.setArmEndTarget(right_base, sim_node.arm_action, "r", old_r, right_grip_rot)
# #             print(label, "LEFT", np.round(left_world, 3), "RIGHT", np.round(right_world, 3))
# #             return True
# #         except Exception as exc:
# #             sim_node.tctr_left_arm[:] = old_l
# #             sim_node.tctr_right_arm[:] = old_r
# #             sim_node.set_left_arm_new_target = False
# #             sim_node.set_right_arm_new_target = False
# #             print(label, "IK failed:", exc)
# #             return False

# #     def update_joint_move_ratio(sim_node, action):
# #         dif = np.abs(action - sim_node.target_control)
# #         sim_node.joint_move_ratio = dif / (np.max(dif) + 1e-6)
# #         sim_node.joint_move_ratio[2] *= 0.35
# #         sim_node.joint_move_ratio[5:11] *= 0.45
# #         sim_node.joint_move_ratio[12:18] *= 0.45

# #     cfg = MMK2Cfg()
# #     cfg.mjcf_file_path = str(mjcf_path)
# #     cfg.use_gaussian_renderer = False
# #     cfg.headless = headless
# #     cfg.enable_render = not headless
# #     cfg.sync = not headless
# #     cfg.render_set = {
# #         "fps": 30,
# #         "width": 1280,
# #         "height": 720,
# #         "window_title": "DISCOVERSE box_pick grasp",
# #     }
# #     cfg.obs_rgb_cam_id = None
# #     cfg.obs_depth_cam_id = None
# #     cfg.init_state = {
# #         "base_position": [0.58, 0.715, 0.0],
# #         "base_orientation": [1.0, 0.0, 0.0, 0.0],
# #         "slide_qpos": [0.0],
# #         "head_qpos": [0.0, head_pitch],
# #         "lft_arm_qpos": [0.0, -0.166, 0.032, 0.0, 1.571, 2.223],
# #         "lft_gripper_qpos": [grip_close],
# #         "rgt_arm_qpos": [0.0, -0.166, 0.032, 0.0, -1.571, -2.223],
# #         "rgt_gripper_qpos": [grip_close],
# #     }

# #     sim_node = MyAlgorithmNode(cfg)
# #     obs = sim_node.reset()
# #     action = sim_node.target_control.copy()
# #     base_lock_x = float(cfg.init_state["base_position"][0])
# #     base_lock_y = float(cfg.init_state["base_position"][1])
# #     box_pos_fixed = None
# #     box_side_axis = None
# #     half_y = 0.08
# #     target_left = None
# #     target_right = None
# #     stage = 0
# #     stage_enter_time = sim_node.mj_data.time
# #     squeeze_idx = 0
# #     pull_idx = 0
# #     print("DISCOVERSE MJCF window opened. box_pick grasp enabled.")

# #     while sim_node.running:
# #         now = sim_node.mj_data.time
# #         elapsed = now - stage_enter_time
# #         if max_seconds is not None and now >= max_seconds:
# #             box_pos = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
# #             print(
# #                 "box_pick preview finished:",
# #                 "stage=", stage,
# #                 "time=", round(float(now), 3),
# #                 "box=", np.array2string(box_pos, precision=3),
# #                 "left_arm=", np.array2string(sim_node.sensor_lft_arm_qpos, precision=3),
# #                 "right_arm=", np.array2string(sim_node.sensor_rgt_arm_qpos, precision=3),
# #             )
# #             break

# #         if stage == 0:
# #             tmat_box = get_body_tmat(sim_node.mj_data, target_body_name)
# #             box_pos = tmat_box[:3, 3]
# #             sim_node.tctr_head[1] = head_pitch
# #             sim_node.tctr_slide[0] = float(np.clip(1.22 - 1.08 * box_pos[2], -0.04, 0.45))
# #             sim_node.tctr_lft_gripper[:] = grip_close
# #             sim_node.tctr_rgt_gripper[:] = grip_close
# #             if elapsed > 0.5:
# #                 stage = 1
# #                 stage_enter_time = now
# #                 box_pos_fixed = box_pos.copy()
# #                 box_side_axis = tmat_box[:3, 0].copy()
# #                 half_y = get_box_half_extent_y(sim_node.mj_model, target_body_name)
# #                 target_left, target_right = side_targets(
# #                     box_pos_fixed, half_y, pre_clearance, pre_x_backoff, side_axis=box_side_axis
# #                 )
# #                 set_dual_targets(sim_node, target_left, target_right, "pre-grasp target")
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 1:
# #             left_pos = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
# #             right_pos = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
# #             left_err = float(np.linalg.norm(left_pos - target_left))
# #             right_err = float(np.linalg.norm(right_pos - target_right))
# #             if elapsed > 1.2 and (left_err < 0.13 and right_err < 0.13 or elapsed > 4.0):
# #                 stage = 2
# #                 stage_enter_time = now
# #                 target_left, target_right = side_targets(
# #                     box_pos_fixed, half_y, deep_pre_clearance, grasp_x_backoff, side_axis=box_side_axis
# #                 )
# #                 set_dual_targets(sim_node, target_left, target_right, "deep pre-grasp target")
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 2:
# #             left_pos = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
# #             right_pos = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
# #             left_err = float(np.linalg.norm(left_pos - target_left))
# #             right_err = float(np.linalg.norm(right_pos - target_right))
# #             if elapsed > 1.0 and (left_err < 0.12 and right_err < 0.12 or elapsed > 3.0):
# #                 stage = 3
# #                 stage_enter_time = now
# #                 squeeze_idx = len(squeeze_clearances) - 1
# #                 target_left, target_right = side_targets(
# #                     box_pos_fixed,
# #                     half_y,
# #                     squeeze_clearances[squeeze_idx],
# #                     grasp_x_backoff,
# #                     side_axis=box_side_axis,
# #                     diagonal_x=squeeze_diagonal_x[squeeze_idx],
# #                 )
# #                 set_dual_targets(sim_node, target_left, target_right, "side-wall clamp pose")
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 3:
# #             left_pos = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
# #             right_pos = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
# #             left_err = float(np.linalg.norm(left_pos - target_left))
# #             right_err = float(np.linalg.norm(right_pos - target_right))
# #             if elapsed > 0.45 and (left_err < 0.06 and right_err < 0.06 or elapsed > 2.0):
# #                 stage = 4
# #                 stage_enter_time = now
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 print(">>> clamp side walls")
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 4:
# #             close_alpha = min(1.0, elapsed / 1.6)
# #             gentle_grip = grip_open + (grip_close - grip_open) * close_alpha
# #             sim_node.tctr_lft_gripper[:] = gentle_grip
# #             sim_node.tctr_rgt_gripper[:] = gentle_grip
# #             if elapsed > 1.1:
# #                 stage = 5
# #                 stage_enter_time = now
# #                 pull_idx = 0

# #         elif stage == 5:
# #             sim_node.tctr_lft_gripper[:] = grip_close
# #             sim_node.tctr_rgt_gripper[:] = grip_close
# #             if elapsed > 0.75:
# #                 if pull_idx < len(pull_dx_steps):
# #                     pull_dx = pull_dx_steps[pull_idx]
# #                     stage_enter_time = now
# #                     target_left, target_right = side_targets(
# #                         box_pos_fixed,
# #                         half_y,
# #                         pull_clearance,
# #                         grasp_x_backoff + pull_dx,
# #                         z_lift=0.02,
# #                         side_axis=box_side_axis,
# #                     )
# #                     set_dual_targets(sim_node, target_left, target_right, "pull target")
# #                     update_joint_move_ratio(sim_node, action)
# #                     pull_idx += 1
# #                 else:
# #                     stage = 6
# #                     stage_enter_time = now
# #                     print(">>> hold after pull")

# #         for i in range(2, sim_node.njctrl):
# #             action[i] = step_func(
# #                 action[i],
# #                 sim_node.target_control[i],
# #                 0.55 * sim_node.joint_move_ratio[i] * sim_node.delta_t,
# #             )
# #         action[0] = 0.0
# #         action[1] = 0.0
# #         obs, _, _, _, _ = sim_node.step(action)
# #         sim_node.mj_data.qpos[0] = base_lock_x
# #         sim_node.mj_data.qpos[1] = base_lock_y
# #         sim_node.mj_data.qvel[0] = 0.0
# #         sim_node.mj_data.qvel[1] = 0.0
# #         mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)


# # def fk_position(model, data, frame_id, q):
# #     pin.forwardKinematics(model, data, q)
# #     pin.updateFramePlacements(model, data)
# #     return data.oMf[frame_id].translation.copy()


# # def frame_position(model, data, frame_name):
# #     if not model.existFrame(frame_name):
# #         return None
# #     return data.oMf[model.getFrameId(frame_name)].translation.copy()


# # def clamp_to_limits(model, q):
# #     lower = model.lowerPositionLimit.copy()
# #     upper = model.upperPositionLimit.copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi
# #     return np.clip(q, lower, upper)


# # def joint_indices(model, joint_names):
# #     q_indices = []
# #     v_indices = []
# #     for name in joint_names:
# #         jid = model.getJointId(name)
# #         if jid == 0:
# #             raise ValueError(f"joint not found: {name}")
# #         joint = model.joints[jid]
# #         if joint.nq != 1 or joint.nv != 1:
# #             raise ValueError(f"joint {name} is not 1-DoF, nq={joint.nq}, nv={joint.nv}")
# #         q_indices.append(joint.idx_q)
# #         v_indices.append(joint.idx_v)
# #     return np.array(q_indices, dtype=int), np.array(v_indices, dtype=int)


# # def make_full_configuration(model, base_position, slide_value=0.2):
# #     q = pin.neutral(model)
# #     if model.nq >= 7:
# #         q[0:3] = np.asarray(base_position, dtype=float)
# #         # Pinocchio free-flyer quaternion order is x, y, z, w.
# #         q[3:7] = np.array([0.0, 0.0, 0.0, 1.0])

# #     for joint_name in ("lft_wheel_joint", "rgt_wheel_joint"):
# #         jid = model.getJointId(joint_name)
# #         if jid != 0:
# #             q[model.joints[jid].idx_q : model.joints[jid].idx_q + 2] = 0.0

# #     if model.getJointId("slide_joint") != 0:
# #         sid = model.getJointId("slide_joint")
# #         q[model.joints[sid].idx_q] = slide_value

# #     return clamp_to_limits(model, q)


# # def extract_active_config(q_full, active_q_indices):
# #     return q_full[active_q_indices].copy()


# # def segment_hits_aabb(p0, p1, box, samples=16):
# #     for alpha in np.linspace(0.0, 1.0, samples):
# #         p = (1.0 - alpha) * p0 + alpha * p1
# #         if np.all(p >= box.minimum) and np.all(p <= box.maximum):
# #             return True
# #     return False


# # def chain_points(model, data, q, frame_names):
# #     pin.forwardKinematics(model, data, q)
# #     pin.updateFramePlacements(model, data)
# #     points = []
# #     for name in frame_names:
# #         if model.existFrame(name):
# #             points.append(data.oMf[model.getFrameId(name)].translation.copy())
# #     return [p for p in points if p is not None]


# # def robot_chains(model, data, q):
# #     chains = []
# #     left_chain = [
# #         "left_base_link",
# #         "left_link1",
# #         "left_link2",
# #         "left_link3",
# #         "left_link4",
# #         "left_link5",
# #         "left_link6",
# #         "left_flange",
# #     ]
# #     right_chain = [
# #         "right_base_link",
# #         "right_link1",
# #         "right_link2",
# #         "right_link3",
# #         "right_link4",
# #         "right_link5",
# #         "right_link6",
# #         "right_flange",
# #     ]
# #     body_chain = ["floating_base", "underboard_link", "skin_link", "agv_link"]

# #     for frame_names in (body_chain, left_chain, right_chain):
# #         pts = chain_points(model, data, q, frame_names)
# #         if len(pts) >= 2:
# #             chains.append(pts)
# #     return chains


# # def in_collision(model, data, q, obstacles, robot_radius=0.015):
# #     inflated_obstacles = [obstacle.inflated(robot_radius) for obstacle in obstacles]
# #     for chain in robot_chains(model, data, q):
# #         for p0, p1 in zip(chain[:-1], chain[1:]):
# #             for obstacle in inflated_obstacles:
# #                 if segment_hits_aabb(p0, p1, obstacle):
# #                     return True
# #     return False


# # def edge_in_collision(model, data, q0, q1, obstacles, step=0.05):
# #     distance = np.linalg.norm(q1 - q0)
# #     steps = max(2, int(math.ceil(distance / step)))
# #     for alpha in np.linspace(0.0, 1.0, steps):
# #         q = (1.0 - alpha) * q0 + alpha * q1
# #         if in_collision(model, data, q, obstacles):
# #             return True
# #     return False


# # def solve_damped_least_squares_3d(jacobian, error, damping):
# #     rows = jacobian.tolist()
# #     err = error.tolist()

# #     a = [[0.0 for _ in range(3)] for _ in range(3)]
# #     for i in range(3):
# #         for j in range(3):
# #             a[i][j] = sum(rows[i][k] * rows[j][k] for k in range(len(rows[i])))
# #         a[i][i] += damping

# #     b = err[:]
# #     for col in range(3):
# #         pivot = max(range(col, 3), key=lambda row: abs(a[row][col]))
# #         if abs(a[pivot][col]) < 1e-10:
# #             return np.zeros(jacobian.shape[1])
# #         if pivot != col:
# #             a[col], a[pivot] = a[pivot], a[col]
# #             b[col], b[pivot] = b[pivot], b[col]

# #         pivot_value = a[col][col]
# #         for j in range(col, 3):
# #             a[col][j] /= pivot_value
# #         b[col] /= pivot_value

# #         for row in range(3):
# #             if row == col:
# #                 continue
# #             factor = a[row][col]
# #             for j in range(col, 3):
# #                 a[row][j] -= factor * a[col][j]
# #             b[row] -= factor * b[col]

# #     dq = []
# #     for joint_col in range(len(rows[0])):
# #         dq.append(sum(rows[row][joint_col] * b[row] for row in range(3)))
# #     return np.array(dq, dtype=float)


# # def solve_arm_position_ik(
# #     model,
# #     data,
# #     frame_id,
# #     arm_q_indices,
# #     arm_v_indices,
# #     q_seed,
# #     target_pos,
# #     max_iter=400,
# #     tolerance=0.01,
# # ):
# #     damping = 1e-4
# #     lower = model.lowerPositionLimit[arm_q_indices].copy()
# #     upper = model.upperPositionLimit[arm_q_indices].copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi

# #     seeds = [q_seed.copy()]
# #     for scale in (0.03, 0.06, 0.10):
# #         for _ in range(3):
# #             q_try = q_seed.copy()
# #             q_try[arm_q_indices] += np.random.uniform(-scale, scale, size=len(arm_q_indices))
# #             q_try = clamp_to_limits(model, q_try)
# #             seeds.append(q_try)
# #     for _ in range(35):
# #         q_try = q_seed.copy()
# #         q_try[arm_q_indices] = np.random.uniform(lower, upper)
# #         seeds.append(q_try)

# #     for q_start in seeds:
# #         q = q_start.copy()
# #         for _ in range(max_iter):
# #             pin.forwardKinematics(model, data, q)
# #             pin.computeJointJacobians(model, data, q)
# #             pin.updateFramePlacements(model, data)

# #             ee_pos = data.oMf[frame_id].translation.copy()
# #             error = target_pos - ee_pos
# #             if np.linalg.norm(error) < tolerance:
# #                 return clamp_to_limits(model, q), True

# #             full_jacobian = pin.computeFrameJacobian(
# #                 model,
# #                 data,
# #                 q,
# #                 frame_id,
# #                 pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
# #             )
# #             jacobian = np.asarray(full_jacobian[:3, :][:, arm_v_indices], dtype=float).copy()

# #             dq = solve_damped_least_squares_3d(jacobian, error, damping)
# #             dq = np.clip(dq, -0.06, 0.06)

# #             for idx, delta in zip(arm_q_indices, dq):
# #                 q[idx] += delta
# #             q = clamp_to_limits(model, q)

# #     return q_seed.copy(), False


# # def solve_dual_position_ik(
# #     model,
# #     data,
# #     left_frame_id,
# #     right_frame_id,
# #     active_q_indices,
# #     active_v_indices,
# #     q_seed,
# #     left_target,
# #     right_target,
# #     left_q_indices,
# #     left_v_indices,
# #     right_q_indices,
# #     right_v_indices,
# #     obstacles=None,
# #     max_sweeps=5,
# #     max_attempts=25,
# # ):
# #     for attempt in range(max_attempts):
# #         q = q_seed.copy()
# #         if attempt > 0:
# #             q[active_q_indices] = random_active_configuration(model, active_q_indices)

# #         for _ in range(max_sweeps):
# #             q, left_ok = solve_arm_position_ik(
# #                 model,
# #                 data,
# #                 left_frame_id,
# #                 left_q_indices,
# #                 left_v_indices,
# #                 q,
# #                 left_target,
# #                 max_iter=240,
# #                 tolerance=0.012,
# #             )
# #             q, right_ok = solve_arm_position_ik(
# #                 model,
# #                 data,
# #                 right_frame_id,
# #                 right_q_indices,
# #                 right_v_indices,
# #                 q,
# #                 right_target,
# #                 max_iter=240,
# #                 tolerance=0.012,
# #             )
# #             if not (left_ok and right_ok):
# #                 continue

# #             q = clamp_to_limits(model, q)
# #             if obstacles is None or not in_collision(model, data, q, obstacles):
# #                 return q, True

# #     return q_seed.copy(), False


# # def nearest_node(nodes, q):
# #     distances = [np.linalg.norm(node - q) for node in nodes]
# #     return int(np.argmin(distances))


# # def steer(q_from, q_to, step_size):
# #     direction = q_to - q_from
# #     distance = np.linalg.norm(direction)
# #     if distance <= step_size:
# #         return q_to.copy()
# #     return q_from + direction / distance * step_size


# # def reconstruct_path(nodes, parents, goal_index):
# #     path = []
# #     index = goal_index
# #     while index is not None:
# #         path.append(nodes[index])
# #         index = parents[index]
# #     path.reverse()
# #     return path


# # def clamp_active(model, active_q, active_q_indices):
# #     q = pin.neutral(model)[active_q_indices]
# #     q[:] = active_q
# #     lower = model.lowerPositionLimit[active_q_indices].copy()
# #     upper = model.upperPositionLimit[active_q_indices].copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi
# #     return np.clip(active_q, lower, upper)


# # def random_active_configuration(model, active_q_indices):
# #     lower = model.lowerPositionLimit[active_q_indices].copy()
# #     upper = model.upperPositionLimit[active_q_indices].copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi
# #     return np.random.uniform(lower, upper)


# # def active_to_full(q_template, q_active, active_q_indices):
# #     q = q_template.copy()
# #     q[active_q_indices] = q_active
# #     return q


# # def rrt_plan_active(
# #     model,
# #     data,
# #     q_template,
# #     active_q_indices,
# #     q_start_active,
# #     q_goal_active,
# #     obstacles,
# #     max_iter=7000,
# #     step_size=0.12,
# #     goal_sample_rate=0.22,
# # ):
# #     q_start_full = active_to_full(q_template, q_start_active, active_q_indices)
# #     q_goal_full = active_to_full(q_template, q_goal_active, active_q_indices)
# #     if in_collision(model, data, q_start_full, obstacles):
# #         raise ValueError("q_start is in collision")
# #     if in_collision(model, data, q_goal_full, obstacles):
# #         raise ValueError("q_goal is in collision")
# #     if not edge_in_collision(model, data, q_start_full, q_goal_full, obstacles):
# #         return [q_start_active.copy(), q_goal_active.copy()]

# #     nodes = [q_start_active.copy()]
# #     parents = [None]

# #     for _ in range(max_iter):
# #         q_rand = q_goal_active if random.random() < goal_sample_rate else random_active_configuration(model, active_q_indices)
# #         nearest_index = nearest_node(nodes, q_rand)
# #         q_new = steer(nodes[nearest_index], q_rand, step_size)
# #         q_new = clamp_active(model, q_new, active_q_indices)

# #         q_near_full = active_to_full(q_template, nodes[nearest_index], active_q_indices)
# #         q_new_full = active_to_full(q_template, q_new, active_q_indices)
# #         if edge_in_collision(model, data, q_near_full, q_new_full, obstacles):
# #             continue

# #         nodes.append(q_new)
# #         parents.append(nearest_index)
# #         new_index = len(nodes) - 1

# #         if np.linalg.norm(q_new - q_goal_active) < step_size:
# #             q_new_full = active_to_full(q_template, q_new, active_q_indices)
# #             if not edge_in_collision(model, data, q_new_full, q_goal_full, obstacles):
# #                 nodes.append(q_goal_active.copy())
# #                 parents.append(new_index)
# #                 return reconstruct_path(nodes, parents, len(nodes) - 1)

# #     raise RuntimeError("RRT failed to find a collision-free path")


# # def smooth_path_active(model, data, q_template, active_q_indices, path, obstacles, attempts=120):
# #     path = [q.copy() for q in path]
# #     if len(path) <= 2:
# #         return path

# #     for _ in range(attempts):
# #         if len(path) <= 2:
# #             break
# #         i, j = sorted(random.sample(range(len(path)), 2))
# #         if j <= i + 1:
# #             continue
# #         q_i_full = active_to_full(q_template, path[i], active_q_indices)
# #         q_j_full = active_to_full(q_template, path[j], active_q_indices)
# #         if not edge_in_collision(model, data, q_i_full, q_j_full, obstacles):
# #             path = path[: i + 1] + path[j:]
# #     return path


# # def interpolate_active_path(path, max_step=0.03):
# #     dense_path = []
# #     for q0, q1 in zip(path[:-1], path[1:]):
# #         distance = np.linalg.norm(q1 - q0)
# #         steps = max(2, int(math.ceil(distance / max_step)))
# #         for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
# #             dense_path.append((1.0 - alpha) * q0 + alpha * q1)
# #     dense_path.append(path[-1].copy())
# #     return dense_path


# # def compute_dual_box_pick_targets(
# #     box_center,
# #     box_yaw=0.0,
# #     cabinet_front_x=0.48,
# #     lateral=0.065,
# #     diagonal_x=0.035,
# # ):
# #     # Use the box width direction as the left-right offset axis.
# #     side_axis = np.array([-math.sin(box_yaw), math.cos(box_yaw), 0.0], dtype=float)
# #     if np.linalg.norm(side_axis) < 1e-6:
# #         side_axis = np.array([0.0, 1.0, 0.0])
# #     side_axis /= np.linalg.norm(side_axis)

# #     outside_x = cabinet_front_x - 0.11
# #     mouth_x = cabinet_front_x - 0.015
# #     grasp_x = box_center[0] - 0.02
# #     retreat_x = cabinet_front_x - 0.16

# #     approach_z = box_center[2] + 0.16
# #     grasp_z = box_center[2] + 0.075
# #     lift_z = box_center[2] + 0.15

# #     def side_pair(x, z, skew=False):
# #         center = np.array([x, box_center[1], z], dtype=float)
# #         left = center + side_axis * lateral
# #         right = center - side_axis * lateral
# #         if left[1] >= right[1]:
# #             left_point, right_point = left, right
# #         else:
# #             left_point, right_point = right, left

# #         if skew:
# #             # Bias the grasp diagonally: keep the left arm slightly shallower and
# #             # let the right arm reach a little deeper to avoid upper-shelf elbow hits.
# #             left_point = left_point.copy()
# #             right_point = right_point.copy()
# #             left_point[0] -= diagonal_x
# #             right_point[0] += diagonal_x

# #         return left_point, right_point

# #     outside_left, outside_right = side_pair(outside_x, approach_z)
# #     mouth_left, mouth_right = side_pair(mouth_x, approach_z)
# #     inside_high_left, inside_high_right = side_pair(grasp_x, approach_z, skew=True)
# #     grasp_left, grasp_right = side_pair(grasp_x, grasp_z, skew=True)
# #     lift_left, lift_right = side_pair(grasp_x, lift_z, skew=True)
# #     retreat_left, retreat_right = side_pair(retreat_x, lift_z)

# #     return {
# #         "outside_left": outside_left,
# #         "outside_right": outside_right,
# #         "mouth_left": mouth_left,
# #         "mouth_right": mouth_right,
# #         "inside_mid_left": (mouth_left + inside_high_left) * 0.5,
# #         "inside_mid_right": (mouth_right + inside_high_right) * 0.5,
# #         "inside_high_left": inside_high_left,
# #         "inside_high_right": inside_high_right,
# #         "grasp_left": grasp_left,
# #         "grasp_right": grasp_right,
# #         "lift_left": lift_left,
# #         "lift_right": lift_right,
# #         "retreat_left": retreat_left,
# #         "retreat_right": retreat_right,
# #     }


# # def plan_dual_grasp_sequence(
# #     model,
# #     data,
# #     left_frame_id,
# #     right_frame_id,
# #     q_start_full,
# #     active_q_indices,
# #     active_v_indices,
# #     left_q_indices,
# #     left_v_indices,
# #     right_q_indices,
# #     right_v_indices,
# #     stage_targets,
# #     obstacles,
# # ):
# #     q_path_full = [q_start_full.copy()]
# #     q_current_full = q_start_full.copy()
# #     stage_configs = []
# #     pin.forwardKinematics(model, data, q_current_full)
# #     pin.updateFramePlacements(model, data)
# #     prev_left_target = data.oMf[left_frame_id].translation.copy()
# #     prev_right_target = data.oMf[right_frame_id].translation.copy()

# #     for name, left_target, right_target in stage_targets:
# #         q_goal_full, ik_ok = solve_dual_position_ik(
# #             model,
# #             data,
# #             left_frame_id,
# #             right_frame_id,
# #             active_q_indices,
# #             active_v_indices,
# #             q_current_full,
# #             left_target,
# #             right_target,
# #             left_q_indices,
# #             left_v_indices,
# #             right_q_indices,
# #             right_v_indices,
# #             obstacles=obstacles,
# #         )
# #         if not ik_ok:
# #             raise RuntimeError(
# #                 f"failed to solve dual IK for stage {name}: "
# #                 f"left={np.round(left_target, 3)}, right={np.round(right_target, 3)}"
# #             )

# #         q_start_active = extract_active_config(q_current_full, active_q_indices)
# #         q_goal_active = extract_active_config(q_goal_full, active_q_indices)
# #         try:
# #             segment_active = rrt_plan_active(
# #                 model,
# #                 data,
# #                 q_current_full,
# #                 active_q_indices,
# #                 q_start_active,
# #                 q_goal_active,
# #                 obstacles,
# #                 max_iter=9000,
# #                 step_size=0.10,
# #                 goal_sample_rate=0.30,
# #             )
# #             segment_active = smooth_path_active(
# #                 model,
# #                 data,
# #                 q_current_full,
# #                 active_q_indices,
# #                 segment_active,
# #                 obstacles,
# #                 attempts=50,
# #             )
# #         except RuntimeError:
# #             print(f"RRT fallback: split Cartesian segment for stage {name}")
# #             segment_active = [q_start_active.copy()]
# #             q_bridge = q_current_full.copy()
# #             for alpha in np.linspace(0.2, 1.0, 5):
# #                 left_mid = (1.0 - alpha) * prev_left_target + alpha * left_target
# #                 right_mid = (1.0 - alpha) * prev_right_target + alpha * right_target
# #                 q_next, bridge_ok = solve_dual_position_ik(
# #                     model,
# #                     data,
# #                     left_frame_id,
# #                     right_frame_id,
# #                     active_q_indices,
# #                     active_v_indices,
# #                     q_bridge,
# #                     left_mid,
# #                     right_mid,
# #                     left_q_indices,
# #                     left_v_indices,
# #                     right_q_indices,
# #                     right_v_indices,
# #                     obstacles=obstacles,
# #                     max_attempts=30,
# #                 )
# #                 if not bridge_ok or edge_in_collision(model, data, q_bridge, q_next, obstacles):
# #                     raise
# #                 segment_active.append(extract_active_config(q_next, active_q_indices))
# #                 q_bridge = q_next

# #         q_path_full.extend(
# #             [active_to_full(q_current_full, q_active, active_q_indices) for q_active in segment_active[1:]]
# #         )
# #         q_current_full = q_goal_full
# #         prev_left_target = left_target.copy()
# #         prev_right_target = right_target.copy()
# #         stage_configs.append((name, q_goal_full.copy(), left_target.copy(), right_target.copy()))
# #         print(f"stage {name}: left={np.round(left_target, 3)}, right={np.round(right_target, 3)}")

# #     return q_path_full, stage_configs


# # def arm_chain_points(model, data, q, side):
# #     if side == "left":
# #         frame_names = [
# #             "left_base_link",
# #             "left_link1",
# #             "left_link2",
# #             "left_link3",
# #             "left_link4",
# #             "left_link5",
# #             "left_link6",
# #             "left_flange",
# #         ]
# #     else:
# #         frame_names = [
# #             "right_base_link",
# #             "right_link1",
# #             "right_link2",
# #             "right_link3",
# #             "right_link4",
# #             "right_link5",
# #             "right_link6",
# #             "right_flange",
# #         ]
# #     return chain_points(model, data, q, frame_names)


# # def add_aabb_trace(fig, obstacle):
# #     mn = obstacle.minimum
# #     mx = obstacle.maximum
# #     x = [mn[0], mx[0], mx[0], mn[0], mn[0], mn[0], mx[0], mx[0], mn[0], mn[0], mx[0], mx[0], mx[0], mx[0], mn[0], mn[0]]
# #     y = [mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mx[1], mx[1]]
# #     z = [mn[2], mn[2], mn[2], mn[2], mn[2], mx[2], mx[2], mx[2], mx[2], mx[2], mx[2], mn[2], mn[2], mx[2], mx[2], mn[2]]
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=x,
# #             y=y,
# #             z=z,
# #             mode="lines",
# #             line=dict(color="#4A5568", width=4),
# #             name=obstacle.name,
# #         )
# #     )


# # def visualize_trajectory(
# #     model,
# #     data,
# #     left_frame_id,
# #     right_frame_id,
# #     q_path,
# #     left_points,
# #     right_points,
# #     obstacles,
# #     stage_configs,
# # ):
# #     fig = go.Figure()

# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=left_points[:, 0],
# #             y=left_points[:, 1],
# #             z=left_points[:, 2],
# #             mode="lines+markers",
# #             line=dict(color="#2563EB", width=6),
# #             marker=dict(size=3, color="#2563EB", opacity=0.6),
# #             name="left ee path",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=right_points[:, 0],
# #             y=right_points[:, 1],
# #             z=right_points[:, 2],
# #             mode="lines+markers",
# #             line=dict(color="#EF4444", width=6),
# #             marker=dict(size=3, color="#EF4444", opacity=0.6),
# #             name="right ee path",
# #         )
# #     )

# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[left_points[0, 0]],
# #             y=[left_points[0, 1]],
# #             z=[left_points[0, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#10B981"),
# #             name="left start",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[right_points[0, 0]],
# #             y=[right_points[0, 1]],
# #             z=[right_points[0, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#14B8A6"),
# #             name="right start",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[left_points[-1, 0]],
# #             y=[left_points[-1, 1]],
# #             z=[left_points[-1, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#B91C1C"),
# #             name="left goal",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[right_points[-1, 0]],
# #             y=[right_points[-1, 1]],
# #             z=[right_points[-1, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#7F1D1D"),
# #             name="right goal",
# #         )
# #     )

# #     for obstacle in obstacles:
# #         add_aabb_trace(fig, obstacle)

# #     for name, _q, left_target, right_target in stage_configs:
# #         fig.add_trace(
# #             go.Scatter3d(
# #                 x=[left_target[0], right_target[0]],
# #                 y=[left_target[1], right_target[1]],
# #                 z=[left_target[2], right_target[2]],
# #                 mode="markers+text",
# #                 marker=dict(size=5, color="#111827"),
# #                 text=[f"{name}-L", f"{name}-R"],
# #                 textposition="top center",
# #                 name=f"stage: {name}",
# #             )
# #         )

# #     snapshot_count = min(8, len(q_path))
# #     snapshot_indices = np.linspace(0, len(q_path) - 1, snapshot_count, dtype=int)
# #     for trace_idx, path_idx in enumerate(snapshot_indices):
# #         left_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "left"))
# #         right_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "right"))
# #         if len(left_chain) >= 2:
# #             fig.add_trace(
# #                 go.Scatter3d(
# #                     x=left_chain[:, 0],
# #                     y=left_chain[:, 1],
# #                     z=left_chain[:, 2],
# #                     mode="lines+markers",
# #                     line=dict(color="#1E293B", width=5),
# #                     marker=dict(size=3, color="#1E293B"),
# #                     opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
# #                     name="left arm snapshots" if trace_idx == 0 else None,
# #                     showlegend=trace_idx == 0,
# #                 )
# #             )
# #         if len(right_chain) >= 2:
# #             fig.add_trace(
# #                 go.Scatter3d(
# #                     x=right_chain[:, 0],
# #                     y=right_chain[:, 1],
# #                     z=right_chain[:, 2],
# #                     mode="lines+markers",
# #                     line=dict(color="#374151", width=5),
# #                     marker=dict(size=3, color="#374151"),
# #                     opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
# #                     name="right arm snapshots" if trace_idx == 0 else None,
# #                     showlegend=trace_idx == 0,
# #                 )
# #             )

# #     fig.update_layout(
# #         title="Dual-arm collision-aware grasp motion planning",
# #         scene=dict(
# #             xaxis_title="X (m)",
# #             yaxis_title="Y (m)",
# #             zaxis_title="Z (m)",
# #             aspectmode="data",
# #             camera=dict(eye=dict(x=1.9, y=1.8, z=1.25)),
# #         ),
# #         width=1000,
# #         height=760,
# #         margin=dict(l=0, r=0, t=50, b=0),
# #     )
# #     fig.show()


# # def main():
# #     parser = argparse.ArgumentParser()
# #     parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
# #     parser.add_argument(
# #         "--mjcf",
# #         default=DEFAULT_MJCF_FILE_PATH,
# #         help="DISCOVERSE MJCF scene file to display",
# #     )
# #     parser.add_argument(
# #         "--discoverse-root",
# #         default=DEFAULT_DISCOVERSE_ROOT,
# #         help="local DISCOVERSE source root used to open the MJCF task window",
# #     )
# #     parser.add_argument(
# #         "--plan",
# #         action="store_true",
# #         help="run the Pinocchio RRT planner instead of only opening the MJCF window",
# #     )
# #     parser.add_argument(
# #         "--headless-preview-seconds",
# #         type=float,
# #         default=None,
# #         help="run the MJCF auto-motion preview without a window for this many seconds",
# #     )
# #     parser.add_argument("--left-frame", default=LEFT_EEF_FRAME)
# #     parser.add_argument("--right-frame", default=RIGHT_EEF_FRAME)
# #     parser.add_argument("--base-position", nargs=3, type=float, default=[0.80, 0.238, 0.0])
# #     parser.add_argument("--slide", type=float, default=0.3)
# #     parser.add_argument("--box-center", nargs=3, type=float, default=[1.23, 0.238, 0.82])
# #     parser.add_argument("--box-yaw", type=float, default=0.0)
# #     args = parser.parse_args()

# #     if not args.plan:
# #         run_box_pick_grasp_scene(
# #             args.mjcf,
# #             args.discoverse_root,
# #             headless=args.headless_preview_seconds is not None,
# #             max_seconds=args.headless_preview_seconds,
# #         )
# #         return

# #     global pin, go
# #     import pinocchio as pin
# #     import plotly.graph_objects as go

# #     if not Path(args.urdf).exists():
# #         raise FileNotFoundError(f"URDF file does not exist: {args.urdf}")

# #     model = pin.buildModelFromUrdf(args.urdf)
# #     data = model.createData()

# #     if not model.existFrame(args.left_frame):
# #         raise ValueError(f"Left frame not found: {args.left_frame}")
# #     if not model.existFrame(args.right_frame):
# #         raise ValueError(f"Right frame not found: {args.right_frame}")

# #     left_frame_id = model.getFrameId(args.left_frame)
# #     right_frame_id = model.getFrameId(args.right_frame)
# #     active_q_indices, active_v_indices = joint_indices(model, ACTIVE_JOINT_NAMES)
# #     left_q_indices = active_q_indices[:6]
# #     left_v_indices = active_v_indices[:6]
# #     right_q_indices = active_q_indices[6:]
# #     right_v_indices = active_v_indices[6:]

# #     print("model loaded")
# #     print(f"urdf: {args.urdf}")
# #     print(f"left frame: {args.left_frame}")
# #     print(f"right frame: {args.right_frame}")
# #     print(f"nq: {model.nq}, nv: {model.nv}")
# #     print(f"active joints: {ACTIVE_JOINT_NAMES}")

# #     q_start = make_full_configuration(model, args.base_position, args.slide)

# #     box_center = np.array(args.box_center, dtype=float)
# #     cabinet_center = np.array([box_center[0], box_center[1], 0.0])
# #     obstacles = [
# #         AABB(
# #             "cabinet_left_side",
# #             cabinet_center + np.array([-0.15, 0.39, 0.00]),
# #             cabinet_center + np.array([0.15, 0.41, 2.03]),
# #         ),
# #         AABB(
# #             "cabinet_right_side",
# #             cabinet_center + np.array([-0.15, -0.41, 0.00]),
# #             cabinet_center + np.array([0.15, -0.39, 2.03]),
# #         ),
# #         AABB(
# #             "cabinet_back",
# #             cabinet_center + np.array([0.13, -0.40, 0.00]),
# #             cabinet_center + np.array([0.15, 0.40, 2.03]),
# #         ),
# #         AABB(
# #             "lower_shelf",
# #             cabinet_center + np.array([-0.15, -0.40, 0.72]),
# #             cabinet_center + np.array([0.15, 0.40, 0.74]),
# #         ),
# #         AABB(
# #             "upper_shelf",
# #             cabinet_center + np.array([-0.15, -0.40, 1.05]),
# #             cabinet_center + np.array([0.15, 0.40, 1.07]),
# #         ),
# #     ]
# #     pick_targets = compute_dual_box_pick_targets(
# #         box_center=box_center,
# #         box_yaw=args.box_yaw,
# #         cabinet_front_x=box_center[0] - 0.15,
# #     )
# #     stage_targets = [
# #         ("pregrasp", pick_targets["outside_left"], pick_targets["outside_right"]),
# #         ("mouth", pick_targets["mouth_left"], pick_targets["mouth_right"]),
# #         ("inside_mid", pick_targets["inside_mid_left"], pick_targets["inside_mid_right"]),
# #         ("inside_high", pick_targets["inside_high_left"], pick_targets["inside_high_right"]),
# #         ("grasp_down", pick_targets["grasp_left"], pick_targets["grasp_right"]),
# #         ("lift", pick_targets["lift_left"], pick_targets["lift_right"]),
# #         ("retreat", pick_targets["retreat_left"], pick_targets["retreat_right"]),
# #     ]

# #     q_path, stage_configs = plan_dual_grasp_sequence(
# #         model,
# #         data,
# #         left_frame_id,
# #         right_frame_id,
# #         q_start,
# #         active_q_indices,
# #         active_v_indices,
# #         left_q_indices,
# #         left_v_indices,
# #         right_q_indices,
# #         right_v_indices,
# #         stage_targets,
# #         obstacles,
# #     )
# #     q_path = [q.copy() for q in q_path]
# #     q_path_dense = []
# #     for q0, q1 in zip(q_path[:-1], q_path[1:]):
# #         distance = np.linalg.norm(q1[active_q_indices] - q0[active_q_indices])
# #         steps = max(2, int(math.ceil(distance / 0.03)))
# #         for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
# #             q_path_dense.append((1.0 - alpha) * q0 + alpha * q1)
# #     q_path_dense.append(q_path[-1].copy())

# #     left_points = []
# #     right_points = []
# #     for q in q_path_dense:
# #         pin.forwardKinematics(model, data, q)
# #         pin.updateFramePlacements(model, data)
# #         left_points.append(data.oMf[left_frame_id].translation.copy())
# #         right_points.append(data.oMf[right_frame_id].translation.copy())

# #     left_points = np.array(left_points)
# #     right_points = np.array(right_points)

# #     print(f"planned joint samples: {len(q_path_dense)}")
# #     print(f"left ee start: {left_points[0]}")
# #     print(f"left ee goal:  {left_points[-1]}")
# #     print(f"right ee start: {right_points[0]}")
# #     print(f"right ee goal:  {right_points[-1]}")

# #     visualize_trajectory(
# #         model,
# #         data,
# #         left_frame_id,
# #         right_frame_id,
# #         q_path_dense,
# #         left_points,
# #         right_points,
# #         obstacles,
# #         stage_configs,
# #     )


# # if __name__ == "__main__":
# #     main()
# # import argparse
# # import math
# # import random
# # import sys
# # import time
# # from dataclasses import dataclass
# # from pathlib import Path

# # import numpy as np

# # pin = None
# # go = None


# # DEFAULT_URDF_PATH = (
# #     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/models/urdf/mmk2_s_g2.urdf"
# # )
# # DEFAULT_DISCOVERSE_ROOT = (
# #     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE"
# # )

# # DEFAULT_MJCF_FILE_PATH = (
# #     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/"
# #     "models/mjcf/tasks_mmk2/task1_pick_and_place.xml"
# # )

# # LEFT_EEF_FRAME = "left_end_link"
# # RIGHT_EEF_FRAME = "right_end_link"
# # ACTIVE_JOINT_NAMES = [
# #     "left_joint1",
# #     "left_joint2",
# #     "left_joint3",
# #     "left_joint4",
# #     "left_joint5",
# #     "left_joint6",
# #     "right_joint1",
# #     "right_joint2",
# #     "right_joint3",
# #     "right_joint4",
# #     "right_joint5",
# #     "right_joint6",
# # ]

# # DEFAULT_BOX_HALF_WIDTH_Y = 0.08
# # LEFT_GRIP_ROT = np.array([
# #     [0.0, 0.998482379, 0.055072124],
# #     [0.422618262, -0.049912294, 0.904932355],
# #     [0.906307787, 0.023274485, -0.421976887],
# # ])
# # RIGHT_GRIP_ROT = np.array([
# #     [0.0, -0.998482379, 0.055072124],
# #     [-0.422618262, -0.049912294, -0.904932355],
# #     [0.906307787, -0.023274485, -0.421976887],
# # ])


# # @dataclass
# # class AABB:
# #     name: str
# #     minimum: np.ndarray
# #     maximum: np.ndarray

# #     def inflated(self, radius):
# #         return AABB(self.name, self.minimum - radius, self.maximum + radius)


# # def ensure_discoverse_import_path(discoverse_root):
# #     discoverse_root = Path(discoverse_root)
# #     if not discoverse_root.exists():
# #         raise FileNotFoundError(f"DISCOVERSE root does not exist: {discoverse_root}")
# #     root_str = str(discoverse_root)
# #     if root_str not in sys.path:
# #         sys.path.insert(0, root_str)


# # def mat3_mul(a, b):
# #     a = np.asarray(a, dtype=float)
# #     b = np.asarray(b, dtype=float)
# #     out = np.empty((3, 3), dtype=float)
# #     for i in range(3):
# #         for j in range(3):
# #             out[i, j] = (
# #                 a[i, 0] * b[0, j]
# #                 + a[i, 1] * b[1, j]
# #                 + a[i, 2] * b[2, j]
# #             )
# #     return out


# # def get_box_half_extent_y(mj_model, body_name="box_yellow"):
# #     import mujoco

# #     try:
# #         body_id = int(mj_model.body(body_name).id)
# #     except Exception as exc:
# #         print(f"warning: body {body_name!r} not found ({exc}); use default half-y")
# #         return DEFAULT_BOX_HALF_WIDTH_Y

# #     geom_start = int(mj_model.body_geomadr[body_id])
# #     geom_num = int(mj_model.body_geomnum[body_id])
# #     if geom_num == 0:
# #         return DEFAULT_BOX_HALF_WIDTH_Y

# #     for geom_id in range(geom_start, geom_start + geom_num):
# #         geom_type = mj_model.geom_type[geom_id]
# #         if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
# #             return float(mj_model.geom_size[geom_id, 1])
# #         if geom_type == mujoco.mjtGeom.mjGEOM_MESH:
# #             mesh_id = int(mj_model.geom_dataid[geom_id])
# #             vert_adr = int(mj_model.mesh_vertadr[mesh_id])
# #             vert_num = int(mj_model.mesh_vertnum[mesh_id])
# #             verts = mj_model.mesh_vert[vert_adr: vert_adr + vert_num]
# #             return float((verts[:, 1].max() - verts[:, 1].min()) / 2.0)

# #     return DEFAULT_BOX_HALF_WIDTH_Y


# # def show_discoverse_mjcf_scene(
# #     mjcf_path,
# #     discoverse_root=DEFAULT_DISCOVERSE_ROOT,
# #     headless=False,
# #     max_seconds=None,
# # ):
# #     """Open the same DISCOVERSE MJCF task window used by the competition code."""
# #     ensure_discoverse_import_path(discoverse_root)

# #     from discoverse.robots_env.mmk2_base import MMK2Base, MMK2Cfg
# #     from discoverse.utils import step_func

# #     class MjcfPreviewNode(MMK2Base):
# #         def __init__(self, config):
# #             super().__init__(config)
# #             if "head_cam" in self.camera_names:
# #                 self.cam_id = self.camera_names.index("head_cam")
# #                 self.config.obs_rgb_cam_id = [self.cam_id]
# #                 print("render camera: head_cam", "id=", self.cam_id)
# #             elif self.camera_names:
# #                 self.cam_id = 0
# #                 self.config.obs_rgb_cam_id = [0]
# #                 print("render camera:", self.camera_names[0], "id= 0")
# #             else:
# #                 self.cam_id = -1
# #                 self.config.obs_rgb_cam_id = [-1]
# #                 print("render camera: free")

# #         def post_physics_step(self):
# #             pass

# #         def getChangedObjectPose(self):
# #             return {}

# #         def checkTerminated(self):
# #             return False

# #         def getObservation(self):
# #             return {}

# #         def getPrivilegedObservation(self):
# #             return {}

# #         def getReward(self):
# #             return 0.0

# #     def set_stage_targets(target_control, stage):
# #         if stage == 1:
# #             print(">>> stage 1: lift/head ready")
# #             target_control[2] = 0.14
# #             target_control[3:5] = [0.0, -0.25]
# #             target_control[11] = 0.0
# #             target_control[18] = 0.0
# #         elif stage == 2:
# #             print(">>> stage 2: move arms forward")
# #             target_control[5:11] = [0.31, -1.473, 2.076, -1.391, 1.496, -2.0]
# #             target_control[12:18] = [-0.31, -1.473, 2.076, 1.391, -1.496, 2.0]
# #         elif stage == 3:
# #             print(">>> stage 3: extend grippers deeper toward box sides")
# #             target_control[5:11] = [0.45, -1.473, 2.076, -1.391, 1.496, -2.0]
# #             target_control[12:18] = [-0.45, -1.473, 2.076, 1.391, -1.496, 2.0]
# #             target_control[11] = 0.0
# #             target_control[18] = 0.0
# #         elif stage == 4:
# #             print(">>> stage 4: hold clamp")
# #             target_control[11] = 0.0
# #             target_control[18] = 0.0

# #     cfg = MMK2Cfg()
# #     cfg.mjcf_file_path = str(mjcf_path)
# #     cfg.use_gaussian_renderer = False
# #     cfg.headless = headless
# #     cfg.enable_render = not headless
# #     cfg.sync = True
# #     cfg.render_set = {
# #         "fps": 30,
# #         "width": 1280,
# #         "height": 720,
# #         "window_title": "DISCOVERSE MJCF",
# #     }
# #     cfg.obs_rgb_cam_id = None
# #     cfg.obs_depth_cam_id = None
# #     cfg.init_state = {
# #         "base_position": [0.58, 0.715, 0.0],
# #         "base_orientation": [1.0, 0.0, 0.0, 0.0],
# #         "slide_qpos": [0.0],
# #         "head_qpos": [0.0, 0.0],
# #         "lft_arm_qpos": [0.0, -0.166, 0.032, 0.0, 1.571, 2.223],
# #         "lft_gripper_qpos": [0.0],
# #         "rgt_arm_qpos": [0.0, -0.166, 0.032, 0.0, -1.571, -2.223],
# #         "rgt_gripper_qpos": [0.0],
# #     }

# #     sim_node = MjcfPreviewNode(cfg)
# #     obs = sim_node.reset()
# #     target_control = sim_node.init_joint_ctrl.copy()
# #     action = target_control.copy()
# #     stage = 0
# #     stage_start_time = sim_node.mj_data.time
# #     print("DISCOVERSE MJCF window opened. Auto motion enabled. Close the window to exit.")
# #     while sim_node.running:
# #         now = sim_node.mj_data.time
# #         if max_seconds is not None and now >= max_seconds:
# #             print(
# #                 "preview finished:",
# #                 "time=", round(float(now), 3),
# #                 "slide=", np.array2string(sim_node.sensor_slide_qpos, precision=3),
# #                 "head=", np.array2string(sim_node.sensor_head_qpos, precision=3),
# #                 "left_arm=", np.array2string(sim_node.sensor_lft_arm_qpos, precision=3),
# #                 "right_arm=", np.array2string(sim_node.sensor_rgt_arm_qpos, precision=3),
# #             )
# #             break
# #         stage_elapsed = now - stage_start_time

# #         if stage == 0 and stage_elapsed > 0.5:
# #             stage = 1
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)
# #         elif stage == 1 and stage_elapsed > 1.2:
# #             stage = 2
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)
# #         elif stage == 2 and stage_elapsed > 2.5:
# #             stage = 3
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)
# #         elif stage == 3 and stage_elapsed > 2.0:
# #             stage = 4
# #             stage_start_time = now
# #             set_stage_targets(target_control, stage)

# #         for i in range(2, sim_node.njctrl):
# #             action[i] = step_func(action[i], target_control[i], 0.8 * sim_node.delta_t)
# #         action[0] = 0.0
# #         action[1] = 0.0
# #         obs, _, _, _, _ = sim_node.step(action)


# # def run_box_pick_grasp_scene(
# #     mjcf_path,
# #     discoverse_root=DEFAULT_DISCOVERSE_ROOT,
# #     headless=False,
# #     max_seconds=None,
# # ):
# #     """Run the self-contained box side-wall grasp state machine."""
# #     ensure_discoverse_import_path(discoverse_root)

# #     import mujoco
# #     import types

# #     if "mediapy" not in sys.modules:
# #         mediapy_stub = types.ModuleType("mediapy")
# #         mediapy_stub.write_video = lambda *args, **kwargs: None
# #         sys.modules["mediapy"] = mediapy_stub

# #     from discoverse.robots import AirbotPlayIK, MMK2FIK
# #     from discoverse.robots_env.mmk2_base import MMK2Cfg
# #     from discoverse.task_base import MMK2TaskBase
# #     from discoverse.utils import get_body_tmat, step_func

# #     class StableAirbotPlayIK(AirbotPlayIK):
# #         def properIK(self, pos, ori, ref_q=None):
# #             return self.inverseKin(pos, mat3_mul(ori, self.arm_rot_mat), ref_q)

# #         def inverseKin(self, pos, ori, ref_q=None):
# #             assert len(pos) == 3 and ori.shape == (3, 3)
# #             pos = self.move_joint6_2_joint5(pos, ori)
# #             angle = [0.0] * 6
# #             candidates = []

# #             for i1 in [1, -1]:
# #                 angle[0] = np.arctan2(i1 * pos[1], i1 * pos[0])
# #                 c3 = (
# #                     pos[0] ** 2
# #                     + pos[1] ** 2
# #                     + (pos[2] - self.a1) ** 2
# #                     - self.a3 ** 2
# #                     - self.a4 ** 2
# #                 ) / (2 * self.a3 * self.a4)
# #                 if c3 > 1 or c3 < -1:
# #                     raise ValueError(f"Fail to solve inverse kinematics: pos={pos}, ori={ori}")

# #                 for i2 in [1, -1]:
# #                     s3 = i2 * np.sqrt(1 - c3 ** 2)
# #                     angle[2] = np.arctan2(s3, c3)
# #                     k1 = self.a3 + self.a4 * c3
# #                     k2 = self.a4 * s3
# #                     reach_xy = np.sqrt(pos[0] ** 2 + pos[1] ** 2)
# #                     angle[1] = np.arctan2(
# #                         k1 * (pos[2] - self.a1) - i1 * k2 * reach_xy,
# #                         i1 * k1 * reach_xy + k2 * (pos[2] - self.a1),
# #                     )
# #                     rot = np.array([
# #                         [
# #                             np.cos(angle[0]) * np.cos(angle[1] + angle[2]),
# #                             -np.cos(angle[0]) * np.sin(angle[1] + angle[2]),
# #                             np.sin(angle[0]),
# #                         ],
# #                         [
# #                             np.sin(angle[0]) * np.cos(angle[1] + angle[2]),
# #                             -np.sin(angle[0]) * np.sin(angle[1] + angle[2]),
# #                             -np.cos(angle[0]),
# #                         ],
# #                         [np.sin(angle[1] + angle[2]), np.cos(angle[1] + angle[2]), 0.0],
# #                     ])
# #                     ori1 = mat3_mul(rot.T, ori)
# #                     for i5 in [1, -1]:
# #                         angle[3] = np.arctan2(i5 * ori1[2, 2], i5 * ori1[1, 2])
# #                         angle[4] = np.arctan2(
# #                             i5 * np.sqrt(ori1[2, 2] ** 2 + ori1[1, 2] ** 2),
# #                             ori1[0, 2],
# #                         )
# #                         angle[5] = np.arctan2(-i5 * ori1[0, 0], -i5 * ori1[0, 1])
# #                         js = self.add_bias(angle)
# #                         if np.all((js > self.arm_joint_range[0]) * (js < self.arm_joint_range[1])):
# #                             candidates.append(js)

# #             if len(candidates) == 0:
# #                 raise ValueError(f"Fail to solve inverse kinematics: pos={pos}, ori={ori}")

# #             if ref_q is not None:
# #                 joint_dist = [
# #                     np.sum(np.abs(ref_q - js) / self.joint_range_scale)
# #                     for js in candidates
# #                 ]
# #                 return candidates[int(np.argmin(joint_dist))]
# #             return candidates[0]

# #     target_body_name = "box_yellow"
# #     grip_close = 0.0
# #     grip_open = 0.35
# #     head_pitch = -0.25
# #     pre_x_backoff = 0.11
# #     grasp_x_backoff = 0.00
# #     pre_clearance = 0.050
# #     deep_pre_clearance = 0.035
# #     contact_z_bias = 0.115
# #     squeeze_clearances = (0.045, 0.035, 0.025)
# #     squeeze_diagonal_x = (0.020, 0.030, 0.035)
# #     pull_clearance = -0.055
# #     pull_dx_steps = (0.025, 0.055, 0.085, 0.115, 0.145, 0.175, 0.205, 0.235, 0.265)
# #     outward_grip_angle = np.deg2rad(5.0)

# #     def rot_z(angle):
# #         c = float(np.cos(angle))
# #         s = float(np.sin(angle))
# #         return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])

# #     left_grip_rot = mat3_mul(LEFT_GRIP_ROT, rot_z(outward_grip_angle))
# #     right_grip_rot = mat3_mul(RIGHT_GRIP_ROT, rot_z(-outward_grip_angle))

# #     class MyAlgorithmNode(MMK2TaskBase):
# #         def __init__(self, config):
# #             self._arm_ik_solver = None
# #             super().__init__(config)
# #             self._arm_ik_solver = StableAirbotPlayIK()
# #             for actuator_name in ("lft_gripper", "rgt_gripper"):
# #                 actuator_id = int(self.mj_model.actuator(actuator_name).id)
# #                 self.mj_model.actuator_gainprm[actuator_id, 0] = 8.0
# #                 self.mj_model.actuator_forcelimited[actuator_id] = 1
# #                 self.mj_model.actuator_forcerange[actuator_id, :] = [-4.0, 4.0]
# #             self._configure_grasp_contacts()
# #             if "head_cam" in self.camera_names:
# #                 self.cam_id = self.camera_names.index("head_cam")
# #                 self.config.obs_rgb_cam_id = [self.cam_id]
# #                 print("render camera: head_cam", "id=", self.cam_id)
# #             elif self.camera_names:
# #                 self.cam_id = 0
# #                 self.config.obs_rgb_cam_id = [0]
# #                 print("render camera:", self.camera_names[0], "id= 0")
# #             else:
# #                 self.cam_id = -1
# #                 self.config.obs_rgb_cam_id = [-1]
# #                 print("render camera: free")

# #         def _configure_grasp_contacts(self):
# #             target_body_id = int(self.mj_model.body(target_body_name).id)
# #             old_mass = float(self.mj_model.body_mass[target_body_id])
# #             if old_mass > 0.25:
# #                 scale = 0.25 / old_mass
# #                 self.mj_model.body_mass[target_body_id] = 0.25
# #                 self.mj_model.body_inertia[target_body_id, :] *= scale
# #                 print("target mass:", old_mass, "->", 0.25)

# #             contact_bodies = {
# #                 target_body_name,
# #                 "lft_finger_left_link",
# #                 "lft_finger_right_link",
# #                 "rgt_finger_left_link",
# #                 "rgt_finger_right_link",
# #             }
# #             for geom_id in range(self.mj_model.ngeom):
# #                 body_name = self.mj_model.body(int(self.mj_model.geom_bodyid[geom_id])).name
# #                 if body_name in contact_bodies:
# #                     self.mj_model.geom_friction[geom_id, :] = [5.0, 0.12, 0.012]
# #                     self.mj_model.geom_solref[geom_id, :] = [0.004, 1.0]
# #                     self.mj_model.geom_solimp[geom_id, :] = [0.98, 0.995, 0.001, 0.5, 2.0]
# #             mujoco.mj_setConst(self.mj_model, self.mj_data)
# #             mujoco.mj_forward(self.mj_model, self.mj_data)
# #             print("grasp contact friction configured")

# #         def setArmEndTarget(self, target_pose, arm_action, arm, q_ref, a_rot):
# #             rotation = mat3_mul(MMK2FIK.action_rot[arm_action][arm], a_rot)
# #             position = target_pose[:3, 3] if target_pose.shape == (4, 4) else target_pose
# #             chest_pos = np.array([0.02371, 0.0, 1.311 - self.tctr_slide[0]])
# #             if arm == "l":
# #                 arm_base_tmat = MMK2FIK.TMat_chest2lft_base
# #             else:
# #                 arm_base_tmat = MMK2FIK.TMat_chest2rgt_base
# #             arm_base_pos = chest_pos + arm_base_tmat[:3, 3]
# #             delta = np.asarray(position, dtype=float) - arm_base_pos
# #             rot = arm_base_tmat[:3, :3]
# #             position_local = np.array([
# #                 rot[0, 0] * delta[0] + rot[1, 0] * delta[1] + rot[2, 0] * delta[2],
# #                 rot[0, 1] * delta[0] + rot[1, 1] * delta[1] + rot[2, 1] * delta[2],
# #                 rot[0, 2] * delta[0] + rot[1, 2] * delta[1] + rot[2, 2] * delta[2],
# #             ])
# #             rq = self._arm_ik_solver.properIK(position_local, rotation, q_ref)
# #             if arm == "l":
# #                 self.tctr_left_arm[:] = rq
# #                 self.set_left_arm_new_target = True
# #             else:
# #                 self.tctr_right_arm[:] = rq
# #                 self.set_right_arm_new_target = True

# #         def post_physics_step(self):
# #             pass

# #         def getChangedObjectPose(self):
# #             return {}

# #         def checkTerminated(self):
# #             return False

# #         def getObservation(self):
# #             return super().getObservation()

# #         def getPrivilegedObservation(self):
# #             return self.obs

# #         def getReward(self):
# #             return 0.0

# #         def check_success(self):
# #             return False

# #     def side_targets(
# #         box_pos,
# #         half_y,
# #         clearance,
# #         x_backoff,
# #         z_lift=0.0,
# #         side_axis=None,
# #         diagonal_x=0.0,
# #     ):
# #         if side_axis is None:
# #             axis = np.array([0.0, 1.0, 0.0])
# #         else:
# #             axis = np.asarray(side_axis, dtype=float).copy()
# #             axis[2] = 0.0
# #             norm = np.linalg.norm(axis)
# #             axis = np.array([0.0, 1.0, 0.0]) if norm < 1e-6 else axis / norm
# #         z = box_pos[2] + contact_z_bias + z_lift
# #         center = np.array([box_pos[0] - x_backoff, box_pos[1], z])
# #         point_a = center + axis * (half_y + clearance)
# #         point_b = center - axis * (half_y + clearance)
# #         if point_a[1] >= point_b[1]:
# #             left, right = point_a, point_b
# #         else:
# #             left, right = point_b, point_a
# #         left = left.copy()
# #         right = right.copy()
# #         left[0] -= diagonal_x
# #         right[0] += diagonal_x
# #         return left, right

# #     def set_dual_targets(sim_node, left_world, right_world, label):
# #         old_l = sim_node.tctr_left_arm.copy()
# #         old_r = sim_node.tctr_right_arm.copy()
# #         try:
# #             left_base = world_to_base(left_world)
# #             right_base = world_to_base(right_world)
# #             sim_node.setArmEndTarget(left_base, sim_node.arm_action, "l", old_l, left_grip_rot)
# #             sim_node.setArmEndTarget(right_base, sim_node.arm_action, "r", old_r, right_grip_rot)
# #             print(label, "LEFT", np.round(left_world, 3), "RIGHT", np.round(right_world, 3))
# #             return True
# #         except Exception as exc:
# #             sim_node.tctr_left_arm[:] = old_l
# #             sim_node.tctr_right_arm[:] = old_r
# #             sim_node.set_left_arm_new_target = False
# #             sim_node.set_right_arm_new_target = False
# #             print(label, "IK failed:", exc)
# #             return False

# #     def update_joint_move_ratio(sim_node, action):
# #         dif = np.abs(action - sim_node.target_control)
# #         sim_node.joint_move_ratio = dif / (np.max(dif) + 1e-6)
# #         sim_node.joint_move_ratio[2] *= 0.35
# #         sim_node.joint_move_ratio[5:11] *= 0.45
# #         sim_node.joint_move_ratio[12:18] *= 0.45

# #     cfg = MMK2Cfg()
# #     cfg.mjcf_file_path = str(mjcf_path)
# #     cfg.use_gaussian_renderer = False
# #     cfg.headless = headless
# #     cfg.enable_render = not headless
# #     cfg.sync = not headless
# #     cfg.render_set = {
# #         "fps": 30,
# #         "width": 1280,
# #         "height": 720,
# #         "window_title": "DISCOVERSE box_pick grasp",
# #     }
# #     cfg.obs_rgb_cam_id = None
# #     cfg.obs_depth_cam_id = None
# #     cfg.init_state = {
# #         "base_position": [0.58, 0.715, 0.0],
# #         "base_orientation": [1.0, 0.0, 0.0, 0.0],
# #         "slide_qpos": [0.0],
# #         "head_qpos": [0.0, head_pitch],
# #         "lft_arm_qpos": [0.0, -0.166, 0.032, 0.0, 1.571, 2.223],
# #         "lft_gripper_qpos": [grip_close],
# #         "rgt_arm_qpos": [0.0, -0.166, 0.032, 0.0, -1.571, -2.223],
# #         "rgt_gripper_qpos": [grip_close],
# #     }

# #     sim_node = MyAlgorithmNode(cfg)
# #     obs = sim_node.reset()
# #     action = sim_node.target_control.copy()
# #     base_lock_x = float(cfg.init_state["base_position"][0])
# #     base_lock_y = float(cfg.init_state["base_position"][1])
# #     box_pos_fixed = None
# #     box_side_axis = None
# #     half_y = 0.08
# #     target_left = None
# #     target_right = None
# #     stage = 0
# #     stage_enter_time = sim_node.mj_data.time
# #     squeeze_idx = 0
# #     pull_idx = 0
# #     print("DISCOVERSE MJCF window opened. box_pick grasp enabled.")

# #     while sim_node.running:
# #         now = sim_node.mj_data.time
# #         elapsed = now - stage_enter_time
# #         if max_seconds is not None and now >= max_seconds:
# #             box_pos = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
# #             print(
# #                 "box_pick preview finished:",
# #                 "stage=", stage,
# #                 "time=", round(float(now), 3),
# #                 "box=", np.array2string(box_pos, precision=3),
# #                 "left_arm=", np.array2string(sim_node.sensor_lft_arm_qpos, precision=3),
# #                 "right_arm=", np.array2string(sim_node.sensor_rgt_arm_qpos, precision=3),
# #             )
# #             break

# #         if stage == 0:
# #             tmat_box = get_body_tmat(sim_node.mj_data, target_body_name)
# #             box_pos = tmat_box[:3, 3]
# #             sim_node.tctr_head[1] = head_pitch
# #             sim_node.tctr_slide[0] = float(np.clip(1.22 - 1.08 * box_pos[2], -0.04, 0.45))
# #             sim_node.tctr_lft_gripper[:] = grip_close
# #             sim_node.tctr_rgt_gripper[:] = grip_close
# #             if elapsed > 0.5:
# #                 stage = 1
# #                 stage_enter_time = now
# #                 box_pos_fixed = box_pos.copy()
# #                 box_side_axis = tmat_box[:3, 0].copy()
# #                 half_y = get_box_half_extent_y(sim_node.mj_model, target_body_name)
# #                 target_left, target_right = side_targets(
# #                     box_pos_fixed, half_y, pre_clearance, pre_x_backoff, side_axis=box_side_axis
# #                 )
# #                 set_dual_targets(sim_node, target_left, target_right, "pre-grasp target")
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 1:
# #             left_pos = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
# #             right_pos = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
# #             left_err = float(np.linalg.norm(left_pos - target_left))
# #             right_err = float(np.linalg.norm(right_pos - target_right))
# #             if elapsed > 1.2 and (left_err < 0.13 and right_err < 0.13 or elapsed > 4.0):
# #                 stage = 2
# #                 stage_enter_time = now
# #                 target_left, target_right = side_targets(
# #                     box_pos_fixed, half_y, deep_pre_clearance, grasp_x_backoff, side_axis=box_side_axis
# #                 )
# #                 set_dual_targets(sim_node, target_left, target_right, "deep pre-grasp target")
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 2:
# #             left_pos = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
# #             right_pos = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
# #             left_err = float(np.linalg.norm(left_pos - target_left))
# #             right_err = float(np.linalg.norm(right_pos - target_right))
# #             if elapsed > 1.0 and (left_err < 0.12 and right_err < 0.12 or elapsed > 3.0):
# #                 stage = 3
# #                 stage_enter_time = now
# #                 squeeze_idx = len(squeeze_clearances) - 1
# #                 target_left, target_right = side_targets(
# #                     box_pos_fixed,
# #                     half_y,
# #                     squeeze_clearances[squeeze_idx],
# #                     grasp_x_backoff,
# #                     side_axis=box_side_axis,
# #                     diagonal_x=squeeze_diagonal_x[squeeze_idx],
# #                 )
# #                 set_dual_targets(sim_node, target_left, target_right, "side-wall clamp pose")
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 3:
# #             left_pos = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
# #             right_pos = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
# #             left_err = float(np.linalg.norm(left_pos - target_left))
# #             right_err = float(np.linalg.norm(right_pos - target_right))
# #             if elapsed > 0.45 and (left_err < 0.06 and right_err < 0.06 or elapsed > 2.0):
# #                 stage = 4
# #                 stage_enter_time = now
# #                 sim_node.tctr_lft_gripper[:] = grip_open
# #                 sim_node.tctr_rgt_gripper[:] = grip_open
# #                 print(">>> clamp side walls")
# #                 update_joint_move_ratio(sim_node, action)

# #         elif stage == 4:
# #             close_alpha = min(1.0, elapsed / 1.6)
# #             gentle_grip = grip_open + (grip_close - grip_open) * close_alpha
# #             sim_node.tctr_lft_gripper[:] = gentle_grip
# #             sim_node.tctr_rgt_gripper[:] = gentle_grip
# #             if elapsed > 1.1:
# #                 stage = 5
# #                 stage_enter_time = now
# #                 pull_idx = 0

# #         elif stage == 5:
# #             sim_node.tctr_lft_gripper[:] = grip_close
# #             sim_node.tctr_rgt_gripper[:] = grip_close
# #             if elapsed > 0.75:
# #                 if pull_idx < len(pull_dx_steps):
# #                     pull_dx = pull_dx_steps[pull_idx]
# #                     stage_enter_time = now
# #                     target_left, target_right = side_targets(
# #                         box_pos_fixed,
# #                         half_y,
# #                         pull_clearance,
# #                         grasp_x_backoff + pull_dx,
# #                         z_lift=0.02,
# #                         side_axis=box_side_axis,
# #                     )
# #                     set_dual_targets(sim_node, target_left, target_right, "pull target")
# #                     update_joint_move_ratio(sim_node, action)
# #                     pull_idx += 1
# #                 else:
# #                     stage = 6
# #                     stage_enter_time = now
# #                     print(">>> hold after pull")

# #         for i in range(2, sim_node.njctrl):
# #             action[i] = step_func(
# #                 action[i],
# #                 sim_node.target_control[i],
# #                 0.55 * sim_node.joint_move_ratio[i] * sim_node.delta_t,
# #             )
# #         action[0] = 0.0
# #         action[1] = 0.0
# #         obs, _, _, _, _ = sim_node.step(action)
# #         sim_node.mj_data.qpos[0] = base_lock_x
# #         sim_node.mj_data.qpos[1] = base_lock_y
# #         sim_node.mj_data.qvel[0] = 0.0
# #         sim_node.mj_data.qvel[1] = 0.0
# #         mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)


# # def fk_position(model, data, frame_id, q):
# #     pin.forwardKinematics(model, data, q)
# #     pin.updateFramePlacements(model, data)
# #     return data.oMf[frame_id].translation.copy()


# # def frame_position(model, data, frame_name):
# #     if not model.existFrame(frame_name):
# #         return None
# #     return data.oMf[model.getFrameId(frame_name)].translation.copy()


# # def clamp_to_limits(model, q):
# #     lower = model.lowerPositionLimit.copy()
# #     upper = model.upperPositionLimit.copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi
# #     return np.clip(q, lower, upper)


# # def joint_indices(model, joint_names):
# #     q_indices = []
# #     v_indices = []
# #     for name in joint_names:
# #         jid = model.getJointId(name)
# #         if jid == 0:
# #             raise ValueError(f"joint not found: {name}")
# #         joint = model.joints[jid]
# #         if joint.nq != 1 or joint.nv != 1:
# #             raise ValueError(f"joint {name} is not 1-DoF, nq={joint.nq}, nv={joint.nv}")
# #         q_indices.append(joint.idx_q)
# #         v_indices.append(joint.idx_v)
# #     return np.array(q_indices, dtype=int), np.array(v_indices, dtype=int)


# # def make_full_configuration(model, base_position, slide_value=0.2):
# #     q = pin.neutral(model)
# #     if model.nq >= 7:
# #         q[0:3] = np.asarray(base_position, dtype=float)
# #         # Pinocchio free-flyer quaternion order is x, y, z, w.
# #         q[3:7] = np.array([0.0, 0.0, 0.0, 1.0])

# #     for joint_name in ("lft_wheel_joint", "rgt_wheel_joint"):
# #         jid = model.getJointId(joint_name)
# #         if jid != 0:
# #             q[model.joints[jid].idx_q : model.joints[jid].idx_q + 2] = 0.0

# #     if model.getJointId("slide_joint") != 0:
# #         sid = model.getJointId("slide_joint")
# #         q[model.joints[sid].idx_q] = slide_value

# #     return clamp_to_limits(model, q)


# # def extract_active_config(q_full, active_q_indices):
# #     return q_full[active_q_indices].copy()


# # def segment_hits_aabb(p0, p1, box, samples=16):
# #     for alpha in np.linspace(0.0, 1.0, samples):
# #         p = (1.0 - alpha) * p0 + alpha * p1
# #         if np.all(p >= box.minimum) and np.all(p <= box.maximum):
# #             return True
# #     return False


# # def chain_points(model, data, q, frame_names):
# #     pin.forwardKinematics(model, data, q)
# #     pin.updateFramePlacements(model, data)
# #     points = []
# #     for name in frame_names:
# #         if model.existFrame(name):
# #             points.append(data.oMf[model.getFrameId(name)].translation.copy())
# #     return [p for p in points if p is not None]


# # def robot_chains(model, data, q):
# #     chains = []
# #     left_chain = [
# #         "left_base_link",
# #         "left_link1",
# #         "left_link2",
# #         "left_link3",
# #         "left_link4",
# #         "left_link5",
# #         "left_link6",
# #         "left_flange",
# #     ]
# #     right_chain = [
# #         "right_base_link",
# #         "right_link1",
# #         "right_link2",
# #         "right_link3",
# #         "right_link4",
# #         "right_link5",
# #         "right_link6",
# #         "right_flange",
# #     ]
# #     body_chain = ["floating_base", "underboard_link", "skin_link", "agv_link"]

# #     for frame_names in (body_chain, left_chain, right_chain):
# #         pts = chain_points(model, data, q, frame_names)
# #         if len(pts) >= 2:
# #             chains.append(pts)
# #     return chains


# # def in_collision(model, data, q, obstacles, robot_radius=0.015):
# #     inflated_obstacles = [obstacle.inflated(robot_radius) for obstacle in obstacles]
# #     for chain in robot_chains(model, data, q):
# #         for p0, p1 in zip(chain[:-1], chain[1:]):
# #             for obstacle in inflated_obstacles:
# #                 if segment_hits_aabb(p0, p1, obstacle):
# #                     return True
# #     return False


# # def edge_in_collision(model, data, q0, q1, obstacles, step=0.05):
# #     distance = np.linalg.norm(q1 - q0)
# #     steps = max(2, int(math.ceil(distance / step)))
# #     for alpha in np.linspace(0.0, 1.0, steps):
# #         q = (1.0 - alpha) * q0 + alpha * q1
# #         if in_collision(model, data, q, obstacles):
# #             return True
# #     return False


# # def solve_damped_least_squares_3d(jacobian, error, damping):
# #     rows = jacobian.tolist()
# #     err = error.tolist()

# #     a = [[0.0 for _ in range(3)] for _ in range(3)]
# #     for i in range(3):
# #         for j in range(3):
# #             a[i][j] = sum(rows[i][k] * rows[j][k] for k in range(len(rows[i])))
# #         a[i][i] += damping

# #     b = err[:]
# #     for col in range(3):
# #         pivot = max(range(col, 3), key=lambda row: abs(a[row][col]))
# #         if abs(a[pivot][col]) < 1e-10:
# #             return np.zeros(jacobian.shape[1])
# #         if pivot != col:
# #             a[col], a[pivot] = a[pivot], a[col]
# #             b[col], b[pivot] = b[pivot], b[col]

# #         pivot_value = a[col][col]
# #         for j in range(col, 3):
# #             a[col][j] /= pivot_value
# #         b[col] /= pivot_value

# #         for row in range(3):
# #             if row == col:
# #                 continue
# #             factor = a[row][col]
# #             for j in range(col, 3):
# #                 a[row][j] -= factor * a[col][j]
# #             b[row] -= factor * b[col]

# #     dq = []
# #     for joint_col in range(len(rows[0])):
# #         dq.append(sum(rows[row][joint_col] * b[row] for row in range(3)))
# #     return np.array(dq, dtype=float)


# # def solve_arm_position_ik(
# #     model,
# #     data,
# #     frame_id,
# #     arm_q_indices,
# #     arm_v_indices,
# #     q_seed,
# #     target_pos,
# #     max_iter=400,
# #     tolerance=0.01,
# # ):
# #     damping = 1e-4
# #     lower = model.lowerPositionLimit[arm_q_indices].copy()
# #     upper = model.upperPositionLimit[arm_q_indices].copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi

# #     seeds = [q_seed.copy()]
# #     for scale in (0.03, 0.06, 0.10):
# #         for _ in range(3):
# #             q_try = q_seed.copy()
# #             q_try[arm_q_indices] += np.random.uniform(-scale, scale, size=len(arm_q_indices))
# #             q_try = clamp_to_limits(model, q_try)
# #             seeds.append(q_try)
# #     for _ in range(35):
# #         q_try = q_seed.copy()
# #         q_try[arm_q_indices] = np.random.uniform(lower, upper)
# #         seeds.append(q_try)

# #     for q_start in seeds:
# #         q = q_start.copy()
# #         for _ in range(max_iter):
# #             pin.forwardKinematics(model, data, q)
# #             pin.computeJointJacobians(model, data, q)
# #             pin.updateFramePlacements(model, data)

# #             ee_pos = data.oMf[frame_id].translation.copy()
# #             error = target_pos - ee_pos
# #             if np.linalg.norm(error) < tolerance:
# #                 return clamp_to_limits(model, q), True

# #             full_jacobian = pin.computeFrameJacobian(
# #                 model,
# #                 data,
# #                 q,
# #                 frame_id,
# #                 pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
# #             )
# #             jacobian = np.asarray(full_jacobian[:3, :][:, arm_v_indices], dtype=float).copy()

# #             dq = solve_damped_least_squares_3d(jacobian, error, damping)
# #             dq = np.clip(dq, -0.06, 0.06)

# #             for idx, delta in zip(arm_q_indices, dq):
# #                 q[idx] += delta
# #             q = clamp_to_limits(model, q)

# #     return q_seed.copy(), False


# # def solve_dual_position_ik(
# #     model,
# #     data,
# #     left_frame_id,
# #     right_frame_id,
# #     active_q_indices,
# #     active_v_indices,
# #     q_seed,
# #     left_target,
# #     right_target,
# #     left_q_indices,
# #     left_v_indices,
# #     right_q_indices,
# #     right_v_indices,
# #     obstacles=None,
# #     max_sweeps=5,
# #     max_attempts=25,
# # ):
# #     for attempt in range(max_attempts):
# #         q = q_seed.copy()
# #         if attempt > 0:
# #             q[active_q_indices] = random_active_configuration(model, active_q_indices)

# #         for _ in range(max_sweeps):
# #             q, left_ok = solve_arm_position_ik(
# #                 model,
# #                 data,
# #                 left_frame_id,
# #                 left_q_indices,
# #                 left_v_indices,
# #                 q,
# #                 left_target,
# #                 max_iter=240,
# #                 tolerance=0.012,
# #             )
# #             q, right_ok = solve_arm_position_ik(
# #                 model,
# #                 data,
# #                 right_frame_id,
# #                 right_q_indices,
# #                 right_v_indices,
# #                 q,
# #                 right_target,
# #                 max_iter=240,
# #                 tolerance=0.012,
# #             )
# #             if not (left_ok and right_ok):
# #                 continue

# #             q = clamp_to_limits(model, q)
# #             if obstacles is None or not in_collision(model, data, q, obstacles):
# #                 return q, True

# #     return q_seed.copy(), False


# # def nearest_node(nodes, q):
# #     distances = [np.linalg.norm(node - q) for node in nodes]
# #     return int(np.argmin(distances))


# # def steer(q_from, q_to, step_size):
# #     direction = q_to - q_from
# #     distance = np.linalg.norm(direction)
# #     if distance <= step_size:
# #         return q_to.copy()
# #     return q_from + direction / distance * step_size


# # def reconstruct_path(nodes, parents, goal_index):
# #     path = []
# #     index = goal_index
# #     while index is not None:
# #         path.append(nodes[index])
# #         index = parents[index]
# #     path.reverse()
# #     return path


# # def clamp_active(model, active_q, active_q_indices):
# #     q = pin.neutral(model)[active_q_indices]
# #     q[:] = active_q
# #     lower = model.lowerPositionLimit[active_q_indices].copy()
# #     upper = model.upperPositionLimit[active_q_indices].copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi
# #     return np.clip(active_q, lower, upper)


# # def random_active_configuration(model, active_q_indices):
# #     lower = model.lowerPositionLimit[active_q_indices].copy()
# #     upper = model.upperPositionLimit[active_q_indices].copy()
# #     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
# #     lower[invalid] = -math.pi
# #     upper[invalid] = math.pi
# #     return np.random.uniform(lower, upper)


# # def active_to_full(q_template, q_active, active_q_indices):
# #     q = q_template.copy()
# #     q[active_q_indices] = q_active
# #     return q


# # def rrt_plan_active(
# #     model,
# #     data,
# #     q_template,
# #     active_q_indices,
# #     q_start_active,
# #     q_goal_active,
# #     obstacles,
# #     max_iter=7000,
# #     step_size=0.12,
# #     goal_sample_rate=0.22,
# # ):
# #     q_start_full = active_to_full(q_template, q_start_active, active_q_indices)
# #     q_goal_full = active_to_full(q_template, q_goal_active, active_q_indices)
# #     if in_collision(model, data, q_start_full, obstacles):
# #         raise ValueError("q_start is in collision")
# #     if in_collision(model, data, q_goal_full, obstacles):
# #         raise ValueError("q_goal is in collision")
# #     if not edge_in_collision(model, data, q_start_full, q_goal_full, obstacles):
# #         return [q_start_active.copy(), q_goal_active.copy()]

# #     nodes = [q_start_active.copy()]
# #     parents = [None]

# #     for _ in range(max_iter):
# #         q_rand = q_goal_active if random.random() < goal_sample_rate else random_active_configuration(model, active_q_indices)
# #         nearest_index = nearest_node(nodes, q_rand)
# #         q_new = steer(nodes[nearest_index], q_rand, step_size)
# #         q_new = clamp_active(model, q_new, active_q_indices)

# #         q_near_full = active_to_full(q_template, nodes[nearest_index], active_q_indices)
# #         q_new_full = active_to_full(q_template, q_new, active_q_indices)
# #         if edge_in_collision(model, data, q_near_full, q_new_full, obstacles):
# #             continue

# #         nodes.append(q_new)
# #         parents.append(nearest_index)
# #         new_index = len(nodes) - 1

# #         if np.linalg.norm(q_new - q_goal_active) < step_size:
# #             q_new_full = active_to_full(q_template, q_new, active_q_indices)
# #             if not edge_in_collision(model, data, q_new_full, q_goal_full, obstacles):
# #                 nodes.append(q_goal_active.copy())
# #                 parents.append(new_index)
# #                 return reconstruct_path(nodes, parents, len(nodes) - 1)

# #     raise RuntimeError("RRT failed to find a collision-free path")


# # def smooth_path_active(model, data, q_template, active_q_indices, path, obstacles, attempts=120):
# #     path = [q.copy() for q in path]
# #     if len(path) <= 2:
# #         return path

# #     for _ in range(attempts):
# #         if len(path) <= 2:
# #             break
# #         i, j = sorted(random.sample(range(len(path)), 2))
# #         if j <= i + 1:
# #             continue
# #         q_i_full = active_to_full(q_template, path[i], active_q_indices)
# #         q_j_full = active_to_full(q_template, path[j], active_q_indices)
# #         if not edge_in_collision(model, data, q_i_full, q_j_full, obstacles):
# #             path = path[: i + 1] + path[j:]
# #     return path


# # def interpolate_active_path(path, max_step=0.03):
# #     dense_path = []
# #     for q0, q1 in zip(path[:-1], path[1:]):
# #         distance = np.linalg.norm(q1 - q0)
# #         steps = max(2, int(math.ceil(distance / max_step)))
# #         for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
# #             dense_path.append((1.0 - alpha) * q0 + alpha * q1)
# #     dense_path.append(path[-1].copy())
# #     return dense_path


# # def compute_dual_box_pick_targets(
# #     box_center,
# #     box_yaw=0.0,
# #     cabinet_front_x=0.48,
# #     lateral=0.065,
# #     diagonal_x=0.035,
# # ):
# #     # Use the box width direction as the left-right offset axis.
# #     side_axis = np.array([-math.sin(box_yaw), math.cos(box_yaw), 0.0], dtype=float)
# #     if np.linalg.norm(side_axis) < 1e-6:
# #         side_axis = np.array([0.0, 1.0, 0.0])
# #     side_axis /= np.linalg.norm(side_axis)

# #     outside_x = cabinet_front_x - 0.11
# #     mouth_x = cabinet_front_x - 0.015
# #     grasp_x = box_center[0] - 0.02
# #     retreat_x = cabinet_front_x - 0.16

# #     approach_z = box_center[2] + 0.16
# #     grasp_z = box_center[2] + 0.075
# #     lift_z = box_center[2] + 0.15

# #     def side_pair(x, z, skew=False):
# #         center = np.array([x, box_center[1], z], dtype=float)
# #         left = center + side_axis * lateral
# #         right = center - side_axis * lateral
# #         if left[1] >= right[1]:
# #             left_point, right_point = left, right
# #         else:
# #             left_point, right_point = right, left

# #         if skew:
# #             # Bias the grasp diagonally: keep the left arm slightly shallower and
# #             # let the right arm reach a little deeper to avoid upper-shelf elbow hits.
# #             left_point = left_point.copy()
# #             right_point = right_point.copy()
# #             left_point[0] -= diagonal_x
# #             right_point[0] += diagonal_x

# #         return left_point, right_point

# #     outside_left, outside_right = side_pair(outside_x, approach_z)
# #     mouth_left, mouth_right = side_pair(mouth_x, approach_z)
# #     inside_high_left, inside_high_right = side_pair(grasp_x, approach_z, skew=True)
# #     grasp_left, grasp_right = side_pair(grasp_x, grasp_z, skew=True)
# #     lift_left, lift_right = side_pair(grasp_x, lift_z, skew=True)
# #     retreat_left, retreat_right = side_pair(retreat_x, lift_z)

# #     return {
# #         "outside_left": outside_left,
# #         "outside_right": outside_right,
# #         "mouth_left": mouth_left,
# #         "mouth_right": mouth_right,
# #         "inside_mid_left": (mouth_left + inside_high_left) * 0.5,
# #         "inside_mid_right": (mouth_right + inside_high_right) * 0.5,
# #         "inside_high_left": inside_high_left,
# #         "inside_high_right": inside_high_right,
# #         "grasp_left": grasp_left,
# #         "grasp_right": grasp_right,
# #         "lift_left": lift_left,
# #         "lift_right": lift_right,
# #         "retreat_left": retreat_left,
# #         "retreat_right": retreat_right,
# #     }


# # def plan_dual_grasp_sequence(
# #     model,
# #     data,
# #     left_frame_id,
# #     right_frame_id,
# #     q_start_full,
# #     active_q_indices,
# #     active_v_indices,
# #     left_q_indices,
# #     left_v_indices,
# #     right_q_indices,
# #     right_v_indices,
# #     stage_targets,
# #     obstacles,
# # ):
# #     q_path_full = [q_start_full.copy()]
# #     q_current_full = q_start_full.copy()
# #     stage_configs = []
# #     pin.forwardKinematics(model, data, q_current_full)
# #     pin.updateFramePlacements(model, data)
# #     prev_left_target = data.oMf[left_frame_id].translation.copy()
# #     prev_right_target = data.oMf[right_frame_id].translation.copy()

# #     for name, left_target, right_target in stage_targets:
# #         q_goal_full, ik_ok = solve_dual_position_ik(
# #             model,
# #             data,
# #             left_frame_id,
# #             right_frame_id,
# #             active_q_indices,
# #             active_v_indices,
# #             q_current_full,
# #             left_target,
# #             right_target,
# #             left_q_indices,
# #             left_v_indices,
# #             right_q_indices,
# #             right_v_indices,
# #             obstacles=obstacles,
# #         )
# #         if not ik_ok:
# #             raise RuntimeError(
# #                 f"failed to solve dual IK for stage {name}: "
# #                 f"left={np.round(left_target, 3)}, right={np.round(right_target, 3)}"
# #             )

# #         q_start_active = extract_active_config(q_current_full, active_q_indices)
# #         q_goal_active = extract_active_config(q_goal_full, active_q_indices)
# #         try:
# #             segment_active = rrt_plan_active(
# #                 model,
# #                 data,
# #                 q_current_full,
# #                 active_q_indices,
# #                 q_start_active,
# #                 q_goal_active,
# #                 obstacles,
# #                 max_iter=9000,
# #                 step_size=0.10,
# #                 goal_sample_rate=0.30,
# #             )
# #             segment_active = smooth_path_active(
# #                 model,
# #                 data,
# #                 q_current_full,
# #                 active_q_indices,
# #                 segment_active,
# #                 obstacles,
# #                 attempts=50,
# #             )
# #         except RuntimeError:
# #             print(f"RRT fallback: split Cartesian segment for stage {name}")
# #             segment_active = [q_start_active.copy()]
# #             q_bridge = q_current_full.copy()
# #             for alpha in np.linspace(0.2, 1.0, 5):
# #                 left_mid = (1.0 - alpha) * prev_left_target + alpha * left_target
# #                 right_mid = (1.0 - alpha) * prev_right_target + alpha * right_target
# #                 q_next, bridge_ok = solve_dual_position_ik(
# #                     model,
# #                     data,
# #                     left_frame_id,
# #                     right_frame_id,
# #                     active_q_indices,
# #                     active_v_indices,
# #                     q_bridge,
# #                     left_mid,
# #                     right_mid,
# #                     left_q_indices,
# #                     left_v_indices,
# #                     right_q_indices,
# #                     right_v_indices,
# #                     obstacles=obstacles,
# #                     max_attempts=30,
# #                 )
# #                 if not bridge_ok or edge_in_collision(model, data, q_bridge, q_next, obstacles):
# #                     raise
# #                 segment_active.append(extract_active_config(q_next, active_q_indices))
# #                 q_bridge = q_next

# #         q_path_full.extend(
# #             [active_to_full(q_current_full, q_active, active_q_indices) for q_active in segment_active[1:]]
# #         )
# #         q_current_full = q_goal_full
# #         prev_left_target = left_target.copy()
# #         prev_right_target = right_target.copy()
# #         stage_configs.append((name, q_goal_full.copy(), left_target.copy(), right_target.copy()))
# #         print(f"stage {name}: left={np.round(left_target, 3)}, right={np.round(right_target, 3)}")

# #     return q_path_full, stage_configs


# # def arm_chain_points(model, data, q, side):
# #     if side == "left":
# #         frame_names = [
# #             "left_base_link",
# #             "left_link1",
# #             "left_link2",
# #             "left_link3",
# #             "left_link4",
# #             "left_link5",
# #             "left_link6",
# #             "left_flange",
# #         ]
# #     else:
# #         frame_names = [
# #             "right_base_link",
# #             "right_link1",
# #             "right_link2",
# #             "right_link3",
# #             "right_link4",
# #             "right_link5",
# #             "right_link6",
# #             "right_flange",
# #         ]
# #     return chain_points(model, data, q, frame_names)


# # def add_aabb_trace(fig, obstacle):
# #     mn = obstacle.minimum
# #     mx = obstacle.maximum
# #     x = [mn[0], mx[0], mx[0], mn[0], mn[0], mn[0], mx[0], mx[0], mn[0], mn[0], mx[0], mx[0], mx[0], mx[0], mn[0], mn[0]]
# #     y = [mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mx[1], mx[1]]
# #     z = [mn[2], mn[2], mn[2], mn[2], mn[2], mx[2], mx[2], mx[2], mx[2], mx[2], mx[2], mn[2], mn[2], mx[2], mx[2], mn[2]]
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=x,
# #             y=y,
# #             z=z,
# #             mode="lines",
# #             line=dict(color="#4A5568", width=4),
# #             name=obstacle.name,
# #         )
# #     )


# # def visualize_trajectory(
# #     model,
# #     data,
# #     left_frame_id,
# #     right_frame_id,
# #     q_path,
# #     left_points,
# #     right_points,
# #     obstacles,
# #     stage_configs,
# # ):
# #     fig = go.Figure()

# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=left_points[:, 0],
# #             y=left_points[:, 1],
# #             z=left_points[:, 2],
# #             mode="lines+markers",
# #             line=dict(color="#2563EB", width=6),
# #             marker=dict(size=3, color="#2563EB", opacity=0.6),
# #             name="left ee path",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=right_points[:, 0],
# #             y=right_points[:, 1],
# #             z=right_points[:, 2],
# #             mode="lines+markers",
# #             line=dict(color="#EF4444", width=6),
# #             marker=dict(size=3, color="#EF4444", opacity=0.6),
# #             name="right ee path",
# #         )
# #     )

# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[left_points[0, 0]],
# #             y=[left_points[0, 1]],
# #             z=[left_points[0, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#10B981"),
# #             name="left start",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[right_points[0, 0]],
# #             y=[right_points[0, 1]],
# #             z=[right_points[0, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#14B8A6"),
# #             name="right start",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[left_points[-1, 0]],
# #             y=[left_points[-1, 1]],
# #             z=[left_points[-1, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#B91C1C"),
# #             name="left goal",
# #         )
# #     )
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=[right_points[-1, 0]],
# #             y=[right_points[-1, 1]],
# #             z=[right_points[-1, 2]],
# #             mode="markers",
# #             marker=dict(size=8, color="#7F1D1D"),
# #             name="right goal",
# #         )
# #     )

# #     for obstacle in obstacles:
# #         add_aabb_trace(fig, obstacle)

# #     for name, _q, left_target, right_target in stage_configs:
# #         fig.add_trace(
# #             go.Scatter3d(
# #                 x=[left_target[0], right_target[0]],
# #                 y=[left_target[1], right_target[1]],
# #                 z=[left_target[2], right_target[2]],
# #                 mode="markers+text",
# #                 marker=dict(size=5, color="#111827"),
# #                 text=[f"{name}-L", f"{name}-R"],
# #                 textposition="top center",
# #                 name=f"stage: {name}",
# #             )
# #         )

# #     snapshot_count = min(8, len(q_path))
# #     snapshot_indices = np.linspace(0, len(q_path) - 1, snapshot_count, dtype=int)
# #     for trace_idx, path_idx in enumerate(snapshot_indices):
# #         left_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "left"))
# #         right_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "right"))
# #         if len(left_chain) >= 2:
# #             fig.add_trace(
# #                 go.Scatter3d(
# #                     x=left_chain[:, 0],
# #                     y=left_chain[:, 1],
# #                     z=left_chain[:, 2],
# #                     mode="lines+markers",
# #                     line=dict(color="#1E293B", width=5),
# #                     marker=dict(size=3, color="#1E293B"),
# #                     opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
# #                     name="left arm snapshots" if trace_idx == 0 else None,
# #                     showlegend=trace_idx == 0,
# #                 )
# #             )
# #         if len(right_chain) >= 2:
# #             fig.add_trace(
# #                 go.Scatter3d(
# #                     x=right_chain[:, 0],
# #                     y=right_chain[:, 1],
# #                     z=right_chain[:, 2],
# #                     mode="lines+markers",
# #                     line=dict(color="#374151", width=5),
# #                     marker=dict(size=3, color="#374151"),
# #                     opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
# #                     name="right arm snapshots" if trace_idx == 0 else None,
# #                     showlegend=trace_idx == 0,
# #                 )
# #             )

# #     fig.update_layout(
# #         title="Dual-arm collision-aware grasp motion planning",
# #         scene=dict(
# #             xaxis_title="X (m)",
# #             yaxis_title="Y (m)",
# #             zaxis_title="Z (m)",
# #             aspectmode="data",
# #             camera=dict(eye=dict(x=1.9, y=1.8, z=1.25)),
# #         ),
# #         width=1000,
# #         height=760,
# #         margin=dict(l=0, r=0, t=50, b=0),
# #     )
# #     fig.show()


# # def main():
# #     parser = argparse.ArgumentParser()
# #     parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
# #     parser.add_argument(
# #         "--mjcf",
# #         default=DEFAULT_MJCF_FILE_PATH,
# #         help="DISCOVERSE MJCF scene file to display",
# #     )
# #     parser.add_argument(
# #         "--discoverse-root",
# #         default=DEFAULT_DISCOVERSE_ROOT,
# #         help="local DISCOVERSE source root used to open the MJCF task window",
# #     )
# #     parser.add_argument(
# #         "--plan",
# #         action="store_true",
# #         help="run the Pinocchio RRT planner instead of only opening the MJCF window",
# #     )
# #     parser.add_argument(
# #         "--headless-preview-seconds",
# #         type=float,
# #         default=None,
# #         help="run the MJCF auto-motion preview without a window for this many seconds",
# #     )
# #     parser.add_argument("--left-frame", default=LEFT_EEF_FRAME)
# #     parser.add_argument("--right-frame", default=RIGHT_EEF_FRAME)
# #     parser.add_argument("--base-position", nargs=3, type=float, default=[0.80, 0.238, 0.0])
# #     parser.add_argument("--slide", type=float, default=0.3)
# #     parser.add_argument("--box-center", nargs=3, type=float, default=[1.23, 0.238, 0.82])
# #     parser.add_argument("--box-yaw", type=float, default=0.0)
# #     args = parser.parse_args()

# #     if not args.plan:
# #         run_box_pick_grasp_scene(
# #             args.mjcf,
# #             args.discoverse_root,
# #             headless=args.headless_preview_seconds is not None,
# #             max_seconds=args.headless_preview_seconds,
# #         )
# #         return

# #     global pin, go
# #     import pinocchio as pin
# #     import plotly.graph_objects as go

# #     if not Path(args.urdf).exists():
# #         raise FileNotFoundError(f"URDF file does not exist: {args.urdf}")

# #     model = pin.buildModelFromUrdf(args.urdf)
# #     data = model.createData()

# #     if not model.existFrame(args.left_frame):
# #         raise ValueError(f"Left frame not found: {args.left_frame}")
# #     if not model.existFrame(args.right_frame):
# #         raise ValueError(f"Right frame not found: {args.right_frame}")

# #     left_frame_id = model.getFrameId(args.left_frame)
# #     right_frame_id = model.getFrameId(args.right_frame)
# #     active_q_indices, active_v_indices = joint_indices(model, ACTIVE_JOINT_NAMES)
# #     left_q_indices = active_q_indices[:6]
# #     left_v_indices = active_v_indices[:6]
# #     right_q_indices = active_q_indices[6:]
# #     right_v_indices = active_v_indices[6:]

# #     print("model loaded")
# #     print(f"urdf: {args.urdf}")
# #     print(f"left frame: {args.left_frame}")
# #     print(f"right frame: {args.right_frame}")
# #     print(f"nq: {model.nq}, nv: {model.nv}")
# #     print(f"active joints: {ACTIVE_JOINT_NAMES}")

# #     q_start = make_full_configuration(model, args.base_position, args.slide)

# #     box_center = np.array(args.box_center, dtype=float)
# #     cabinet_center = np.array([box_center[0], box_center[1], 0.0])
# #     obstacles = [
# #         AABB(
# #             "cabinet_left_side",
# #             cabinet_center + np.array([-0.15, 0.39, 0.00]),
# #             cabinet_center + np.array([0.15, 0.41, 2.03]),
# #         ),
# #         AABB(
# #             "cabinet_right_side",
# #             cabinet_center + np.array([-0.15, -0.41, 0.00]),
# #             cabinet_center + np.array([0.15, -0.39, 2.03]),
# #         ),
# #         AABB(
# #             "cabinet_back",
# #             cabinet_center + np.array([0.13, -0.40, 0.00]),
# #             cabinet_center + np.array([0.15, 0.40, 2.03]),
# #         ),
# #         AABB(
# #             "lower_shelf",
# #             cabinet_center + np.array([-0.15, -0.40, 0.72]),
# #             cabinet_center + np.array([0.15, 0.40, 0.74]),
# #         ),
# #         AABB(
# #             "upper_shelf",
# #             cabinet_center + np.array([-0.15, -0.40, 1.05]),
# #             cabinet_center + np.array([0.15, 0.40, 1.07]),
# #         ),
# #     ]
# #     pick_targets = compute_dual_box_pick_targets(
# #         box_center=box_center,
# #         box_yaw=args.box_yaw,
# #         cabinet_front_x=box_center[0] - 0.15,
# #     )
# #     stage_targets = [
# #         ("pregrasp", pick_targets["outside_left"], pick_targets["outside_right"]),
# #         ("mouth", pick_targets["mouth_left"], pick_targets["mouth_right"]),
# #         ("inside_mid", pick_targets["inside_mid_left"], pick_targets["inside_mid_right"]),
# #         ("inside_high", pick_targets["inside_high_left"], pick_targets["inside_high_right"]),
# #         ("grasp_down", pick_targets["grasp_left"], pick_targets["grasp_right"]),
# #         ("lift", pick_targets["lift_left"], pick_targets["lift_right"]),
# #         ("retreat", pick_targets["retreat_left"], pick_targets["retreat_right"]),
# #     ]

# #     q_path, stage_configs = plan_dual_grasp_sequence(
# #         model,
# #         data,
# #         left_frame_id,
# #         right_frame_id,
# #         q_start,
# #         active_q_indices,
# #         active_v_indices,
# #         left_q_indices,
# #         left_v_indices,
# #         right_q_indices,
# #         right_v_indices,
# #         stage_targets,
# #         obstacles,
# #     )
# #     q_path = [q.copy() for q in q_path]
# #     q_path_dense = []
# #     for q0, q1 in zip(q_path[:-1], q_path[1:]):
# #         distance = np.linalg.norm(q1[active_q_indices] - q0[active_q_indices])
# #         steps = max(2, int(math.ceil(distance / 0.03)))
# #         for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
# #             q_path_dense.append((1.0 - alpha) * q0 + alpha * q1)
# #     q_path_dense.append(q_path[-1].copy())

# #     left_points = []
# #     right_points = []
# #     for q in q_path_dense:
# #         pin.forwardKinematics(model, data, q)
# #         pin.updateFramePlacements(model, data)
# #         left_points.append(data.oMf[left_frame_id].translation.copy())
# #         right_points.append(data.oMf[right_frame_id].translation.copy())

# #     left_points = np.array(left_points)
# #     right_points = np.array(right_points)

# #     print(f"planned joint samples: {len(q_path_dense)}")
# #     print(f"left ee start: {left_points[0]}")
# #     print(f"left ee goal:  {left_points[-1]}")
# #     print(f"right ee start: {right_points[0]}")
# #     print(f"right ee goal:  {right_points[-1]}")

# #     visualize_trajectory(
# #         model,
# #         data,
# #         left_frame_id,
# #         right_frame_id,
# #         q_path_dense,
# #         left_points,
# #         right_points,
# #         obstacles,
# #         stage_configs,
# #     )


# # if __name__ == "__main__":
# #     main()
# import argparse
# import math
# import random
# import sys
# import time
# from dataclasses import dataclass
# from pathlib import Path

# import numpy as np

# pin = None
# go = None


# DEFAULT_URDF_PATH = (
#     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/models/urdf/mmk2_s_g2.urdf"
# )
# DEFAULT_DISCOVERSE_ROOT = (
#     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE"
# )

# DEFAULT_MJCF_FILE_PATH = (
#     "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/"
#     "models/mjcf/tasks_mmk2/task1_pick_and_place.xml"
# )

# LEFT_EEF_FRAME = "left_end_link"
# RIGHT_EEF_FRAME = "right_end_link"
# ACTIVE_JOINT_NAMES = [
#     "left_joint1",
#     "left_joint2",
#     "left_joint3",
#     "left_joint4",
#     "left_joint5",
#     "left_joint6",
#     "right_joint1",
#     "right_joint2",
#     "right_joint3",
#     "right_joint4",
#     "right_joint5",
#     "right_joint6",
# ]

# DEFAULT_BOX_HALF_WIDTH_Y = 0.08
# LEFT_GRIP_ROT = np.array([
#     [0.0, 0.998482379, 0.055072124],
#     [0.422618262, -0.049912294, 0.904932355],
#     [0.906307787, 0.023274485, -0.421976887],
# ])
# RIGHT_GRIP_ROT = np.array([
#     [0.0, -0.998482379, 0.055072124],
#     [-0.422618262, -0.049912294, -0.904932355],
#     [0.906307787, -0.023274485, -0.421976887],
# ])


# @dataclass
# class AABB:
#     name: str
#     minimum: np.ndarray
#     maximum: np.ndarray

#     def inflated(self, radius):
#         return AABB(self.name, self.minimum - radius, self.maximum + radius)


# def ensure_discoverse_import_path(discoverse_root):
#     discoverse_root = Path(discoverse_root)
#     if not discoverse_root.exists():
#         raise FileNotFoundError(f"DISCOVERSE root does not exist: {discoverse_root}")
#     root_str = str(discoverse_root)
#     if root_str not in sys.path:
#         sys.path.insert(0, root_str)


# def mat3_mul(a, b):
#     a = np.asarray(a, dtype=float)
#     b = np.asarray(b, dtype=float)
#     out = np.empty((3, 3), dtype=float)
#     for i in range(3):
#         for j in range(3):
#             out[i, j] = (
#                 a[i, 0] * b[0, j]
#                 + a[i, 1] * b[1, j]
#                 + a[i, 2] * b[2, j]
#             )
#     return out


# def get_box_half_extent_y(mj_model, body_name="box_yellow"):
#     import mujoco

#     try:
#         body_id = int(mj_model.body(body_name).id)
#     except Exception as exc:
#         print(f"warning: body {body_name!r} not found ({exc}); use default half-y")
#         return DEFAULT_BOX_HALF_WIDTH_Y

#     geom_start = int(mj_model.body_geomadr[body_id])
#     geom_num = int(mj_model.body_geomnum[body_id])
#     if geom_num == 0:
#         return DEFAULT_BOX_HALF_WIDTH_Y

#     for geom_id in range(geom_start, geom_start + geom_num):
#         geom_type = mj_model.geom_type[geom_id]
#         if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
#             return float(mj_model.geom_size[geom_id, 1])
#         if geom_type == mujoco.mjtGeom.mjGEOM_MESH:
#             mesh_id = int(mj_model.geom_dataid[geom_id])
#             vert_adr = int(mj_model.mesh_vertadr[mesh_id])
#             vert_num = int(mj_model.mesh_vertnum[mesh_id])
#             verts = mj_model.mesh_vert[vert_adr: vert_adr + vert_num]
#             return float((verts[:, 1].max() - verts[:, 1].min()) / 2.0)

#     return DEFAULT_BOX_HALF_WIDTH_Y


# def show_discoverse_mjcf_scene(
#     mjcf_path,
#     discoverse_root=DEFAULT_DISCOVERSE_ROOT,
#     headless=False,
#     max_seconds=None,
# ):
#     """Open the same DISCOVERSE MJCF task window used by the competition code."""
#     ensure_discoverse_import_path(discoverse_root)

#     from discoverse.robots_env.mmk2_base import MMK2Base, MMK2Cfg
#     from discoverse.utils import step_func

#     class MjcfPreviewNode(MMK2Base):
#         def __init__(self, config):
#             super().__init__(config)
#             if "head_cam" in self.camera_names:
#                 self.cam_id = self.camera_names.index("head_cam")
#                 self.config.obs_rgb_cam_id = [self.cam_id]
#                 print("render camera: head_cam", "id=", self.cam_id)
#             elif self.camera_names:
#                 self.cam_id = 0
#                 self.config.obs_rgb_cam_id = [0]
#                 print("render camera:", self.camera_names[0], "id= 0")
#             else:
#                 self.cam_id = -1
#                 self.config.obs_rgb_cam_id = [-1]
#                 print("render camera: free")

#         def post_physics_step(self):
#             pass

#         def getChangedObjectPose(self):
#             return {}

#         def checkTerminated(self):
#             return False

#         def getObservation(self):
#             return {}

#         def getPrivilegedObservation(self):
#             return {}

#         def getReward(self):
#             return 0.0

#     def set_stage_targets(target_control, stage):
#         if stage == 1:
#             print(">>> stage 1: lift/head ready")
#             target_control[2] = 0.14
#             target_control[3:5] = [0.0, -0.25]
#             target_control[11] = 0.0
#             target_control[18] = 0.0
#         elif stage == 2:
#             print(">>> stage 2: move arms forward")
#             target_control[5:11] = [0.31, -1.473, 2.076, -1.391, 1.496, -2.0]
#             target_control[12:18] = [-0.31, -1.473, 2.076, 1.391, -1.496, 2.0]
#         elif stage == 3:
#             print(">>> stage 3: extend grippers deeper toward box sides")
#             target_control[5:11] = [0.45, -1.473, 2.076, -1.391, 1.496, -2.0]
#             target_control[12:18] = [-0.45, -1.473, 2.076, 1.391, -1.496, 2.0]
#             target_control[11] = 0.0
#             target_control[18] = 0.0
#         elif stage == 4:
#             print(">>> stage 4: hold clamp")
#             target_control[11] = 0.0
#             target_control[18] = 0.0

#     cfg = MMK2Cfg()
#     cfg.mjcf_file_path = str(mjcf_path)
#     cfg.use_gaussian_renderer = False
#     cfg.headless = headless
#     cfg.enable_render = not headless
#     cfg.sync = True
#     cfg.render_set = {
#         "fps": 30,
#         "width": 1280,
#         "height": 720,
#         "window_title": "DISCOVERSE MJCF",
#     }
#     cfg.obs_rgb_cam_id = None
#     cfg.obs_depth_cam_id = None
#     cfg.init_state = {
#         "base_position": [0.58, 0.715, 0.0],
#         "base_orientation": [1.0, 0.0, 0.0, 0.0],
#         "slide_qpos": [0.0],
#         "head_qpos": [0.0, 0.0],
#         "lft_arm_qpos": [0.0, -0.166, 0.032, 0.0, 1.571, 2.223],
#         "lft_gripper_qpos": [0.0],
#         "rgt_arm_qpos": [0.0, -0.166, 0.032, 0.0, -1.571, -2.223],
#         "rgt_gripper_qpos": [0.0],
#     }

#     sim_node = MjcfPreviewNode(cfg)
#     obs = sim_node.reset()
#     target_control = sim_node.init_joint_ctrl.copy()
#     action = target_control.copy()
#     stage = 0
#     stage_start_time = sim_node.mj_data.time
#     print("DISCOVERSE MJCF window opened. Auto motion enabled. Close the window to exit.")
#     while sim_node.running:
#         now = sim_node.mj_data.time
#         if max_seconds is not None and now >= max_seconds:
#             print(
#                 "preview finished:",
#                 "time=", round(float(now), 3),
#                 "slide=", np.array2string(sim_node.sensor_slide_qpos, precision=3),
#                 "head=", np.array2string(sim_node.sensor_head_qpos, precision=3),
#                 "left_arm=", np.array2string(sim_node.sensor_lft_arm_qpos, precision=3),
#                 "right_arm=", np.array2string(sim_node.sensor_rgt_arm_qpos, precision=3),
#             )
#             break
#         stage_elapsed = now - stage_start_time

#         if stage == 0 and stage_elapsed > 0.5:
#             stage = 1
#             stage_start_time = now
#             set_stage_targets(target_control, stage)
#         elif stage == 1 and stage_elapsed > 1.2:
#             stage = 2
#             stage_start_time = now
#             set_stage_targets(target_control, stage)
#         elif stage == 2 and stage_elapsed > 2.5:
#             stage = 3
#             stage_start_time = now
#             set_stage_targets(target_control, stage)
#         elif stage == 3 and stage_elapsed > 2.0:
#             stage = 4
#             stage_start_time = now
#             set_stage_targets(target_control, stage)

#         for i in range(2, sim_node.njctrl):
#             action[i] = step_func(action[i], target_control[i], 0.8 * sim_node.delta_t)
#         action[0] = 0.0
#         action[1] = 0.0
#         obs, _, _, _, _ = sim_node.step(action)


# def run_box_pick_grasp_scene(
#     mjcf_path,
#     discoverse_root=DEFAULT_DISCOVERSE_ROOT,
#     urdf_path=DEFAULT_URDF_PATH,
#     headless=False,
#     max_seconds=None,
#     hold_seconds=5.0,
# ):
#     """Run collision-aware dual-side grasp and rigid extraction in MuJoCo.

#     Planning/execution policy:
#       1. Read the real ``box_yellow`` pose and width from the code-2 MJCF scene.
#       2. Use RRT + AABB collision checking for the ungrasped approach path.
#       3. Close both grippers gradually on the two side walls.
#       4. After grasping, keep the left/right grasp geometry fixed and move both
#          arms through synchronized Cartesian lift/extraction waypoints.
#       5. Collision-check every constrained transport segment before execution.

#     The scene's object mass and contact friction are left unchanged.
#     """
#     ensure_discoverse_import_path(discoverse_root)

#     import mujoco
#     import types

#     global pin
#     import pinocchio as pin

#     if "mediapy" not in sys.modules:
#         mediapy_stub = types.ModuleType("mediapy")
#         mediapy_stub.write_video = lambda *args, **kwargs: None
#         sys.modules["mediapy"] = mediapy_stub

#     from discoverse.robots import AirbotPlayIK, MMK2FIK
#     from discoverse.robots_env.mmk2_base import MMK2Cfg
#     from discoverse.task_base import MMK2TaskBase
#     from discoverse.utils import get_body_tmat, step_func

#     class StableAirbotPlayIK(AirbotPlayIK):
#         def properIK(self, pos, ori, ref_q=None):
#             return self.inverseKin(pos, mat3_mul(ori, self.arm_rot_mat), ref_q)

#         def inverseKin(self, pos, ori, ref_q=None):
#             assert len(pos) == 3 and ori.shape == (3, 3)
#             pos = self.move_joint6_2_joint5(pos, ori)
#             angle = [0.0] * 6
#             candidates = []

#             for i1 in [1, -1]:
#                 angle[0] = np.arctan2(i1 * pos[1], i1 * pos[0])
#                 c3 = (
#                     pos[0] ** 2
#                     + pos[1] ** 2
#                     + (pos[2] - self.a1) ** 2
#                     - self.a3 ** 2
#                     - self.a4 ** 2
#                 ) / (2 * self.a3 * self.a4)
#                 if c3 > 1 or c3 < -1:
#                     continue

#                 for i2 in [1, -1]:
#                     s3 = i2 * np.sqrt(max(0.0, 1 - c3 ** 2))
#                     angle[2] = np.arctan2(s3, c3)
#                     k1 = self.a3 + self.a4 * c3
#                     k2 = self.a4 * s3
#                     reach_xy = np.sqrt(pos[0] ** 2 + pos[1] ** 2)
#                     angle[1] = np.arctan2(
#                         k1 * (pos[2] - self.a1) - i1 * k2 * reach_xy,
#                         i1 * k1 * reach_xy + k2 * (pos[2] - self.a1),
#                     )
#                     rot = np.array([
#                         [
#                             np.cos(angle[0]) * np.cos(angle[1] + angle[2]),
#                             -np.cos(angle[0]) * np.sin(angle[1] + angle[2]),
#                             np.sin(angle[0]),
#                         ],
#                         [
#                             np.sin(angle[0]) * np.cos(angle[1] + angle[2]),
#                             -np.sin(angle[0]) * np.sin(angle[1] + angle[2]),
#                             -np.cos(angle[0]),
#                         ],
#                         [np.sin(angle[1] + angle[2]), np.cos(angle[1] + angle[2]), 0.0],
#                     ])
#                     ori1 = mat3_mul(rot.T, ori)
#                     for i5 in [1, -1]:
#                         angle[3] = np.arctan2(i5 * ori1[2, 2], i5 * ori1[1, 2])
#                         angle[4] = np.arctan2(
#                             i5 * np.sqrt(ori1[2, 2] ** 2 + ori1[1, 2] ** 2),
#                             ori1[0, 2],
#                         )
#                         angle[5] = np.arctan2(-i5 * ori1[0, 0], -i5 * ori1[0, 1])
#                         js = self.add_bias(angle)
#                         if np.all((js > self.arm_joint_range[0]) * (js < self.arm_joint_range[1])):
#                             candidates.append(js)

#             if not candidates:
#                 raise ValueError(f"Fail to solve inverse kinematics: pos={pos}, ori={ori}")

#             if ref_q is not None:
#                 joint_dist = [
#                     np.sum(np.abs(ref_q - js) / self.joint_range_scale)
#                     for js in candidates
#                 ]
#                 return candidates[int(np.argmin(joint_dist))]
#             return candidates[0]

#     target_body_name = "box_yellow"
#     grip_close = 0.0
#     grip_open = 0.35
#     head_pitch = -0.25
#     clamp_duration = 1.6
#     outward_grip_angle = np.deg2rad(5.0)

#     def rot_z(angle):
#         c = float(np.cos(angle))
#         s = float(np.sin(angle))
#         return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])

#     left_grip_rot = mat3_mul(LEFT_GRIP_ROT, rot_z(outward_grip_angle))
#     right_grip_rot = mat3_mul(RIGHT_GRIP_ROT, rot_z(-outward_grip_angle))

#     class MyAlgorithmNode(MMK2TaskBase):
#         def __init__(self, config):
#             self._arm_ik_solver = None
#             super().__init__(config)
#             self._arm_ik_solver = StableAirbotPlayIK()
#             if "head_cam" in self.camera_names:
#                 self.cam_id = self.camera_names.index("head_cam")
#                 self.config.obs_rgb_cam_id = [self.cam_id]
#                 print("render camera: head_cam", "id=", self.cam_id)
#             elif self.camera_names:
#                 self.cam_id = 0
#                 self.config.obs_rgb_cam_id = [0]
#                 print("render camera:", self.camera_names[0], "id= 0")
#             else:
#                 self.cam_id = -1
#                 self.config.obs_rgb_cam_id = [-1]
#                 print("render camera: free")

#         def solveArmEndTarget(self, target_pose, arm_action, arm, q_ref, a_rot):
#             rotation = mat3_mul(MMK2FIK.action_rot[arm_action][arm], a_rot)
#             position = target_pose[:3, 3] if target_pose.shape == (4, 4) else target_pose
#             chest_pos = np.array([0.02371, 0.0, 1.311 - self.tctr_slide[0]])
#             arm_base_tmat = (
#                 MMK2FIK.TMat_chest2lft_base if arm == "l" else MMK2FIK.TMat_chest2rgt_base
#             )
#             arm_base_pos = chest_pos + arm_base_tmat[:3, 3]
#             delta = np.asarray(position, dtype=float) - arm_base_pos
#             rot = arm_base_tmat[:3, :3]
#             position_local = np.array([
#                 rot[0, 0] * delta[0] + rot[1, 0] * delta[1] + rot[2, 0] * delta[2],
#                 rot[0, 1] * delta[0] + rot[1, 1] * delta[1] + rot[2, 1] * delta[2],
#                 rot[0, 2] * delta[0] + rot[1, 2] * delta[1] + rot[2, 2] * delta[2],
#             ])
#             return self._arm_ik_solver.properIK(position_local, rotation, q_ref)

#         def setArmEndTarget(self, target_pose, arm_action, arm, q_ref, a_rot):
#             rq = self.solveArmEndTarget(target_pose, arm_action, arm, q_ref, a_rot)
#             if arm == "l":
#                 self.tctr_left_arm[:] = rq
#                 self.set_left_arm_new_target = True
#             else:
#                 self.tctr_right_arm[:] = rq
#                 self.set_right_arm_new_target = True
#             return rq

#         def post_physics_step(self):
#             pass

#         def getChangedObjectPose(self):
#             return {}

#         def checkTerminated(self):
#             return False

#         def getObservation(self):
#             return super().getObservation()

#         def getPrivilegedObservation(self):
#             return self.obs

#         def getReward(self):
#             return 0.0

#         def check_success(self):
#             if not all(hasattr(self, name) for name in ("box_start_z", "cabinet_front_x")):
#                 return False
#             box_pos = get_body_tmat(self.mj_data, target_body_name)[:3, 3]
#             outside_ok = box_pos[0] <= self.cabinet_front_x - 0.05
#             not_dropped = box_pos[2] >= self.box_start_z - 0.03
#             print(
#                 "success check:",
#                 f"box_x={box_pos[0]:.3f}",
#                 f"front_x={self.cabinet_front_x:.3f}",
#                 f"box_z={box_pos[2]:.3f}",
#                 f"start_z={self.box_start_z:.3f}",
#             )
#             return bool(outside_ok and not_dropped)

#     cfg = MMK2Cfg()
#     cfg.mjcf_file_path = str(mjcf_path)
#     cfg.use_gaussian_renderer = False
#     cfg.headless = headless
#     cfg.enable_render = not headless
#     cfg.sync = not headless
#     cfg.render_set = {
#         "fps": 30,
#         "width": 1280,
#         "height": 720,
#         "window_title": "DISCOVERSE dual-side grasp + collision-aware extraction",
#     }
#     cfg.obs_rgb_cam_id = None
#     cfg.obs_depth_cam_id = None
#     cfg.init_state = {
#         "base_position": [0.58, 0.715, 0.0],
#         "base_orientation": [1.0, 0.0, 0.0, 0.0],
#         "slide_qpos": [0.0],
#         "head_qpos": [0.0, head_pitch],
#         "lft_arm_qpos": [0.0, -0.166, 0.032, 0.0, 1.571, 2.223],
#         "lft_gripper_qpos": [grip_open],
#         "rgt_arm_qpos": [0.0, -0.166, 0.032, 0.0, -1.571, -2.223],
#         "rgt_gripper_qpos": [grip_open],
#     }

#     sim_node = MyAlgorithmNode(cfg)
#     obs = sim_node.reset()
#     action = sim_node.target_control.copy()
#     base_lock_x = float(cfg.init_state["base_position"][0])
#     base_lock_y = float(cfg.init_state["base_position"][1])

#     tmat_box = get_body_tmat(sim_node.mj_data, target_body_name)
#     box_center = tmat_box[:3, 3].copy()
#     side_axis = tmat_box[:3, 0].copy()
#     side_axis[2] = 0.0
#     if np.linalg.norm(side_axis) < 1e-6:
#         side_axis = np.array([0.0, 1.0, 0.0])
#     side_axis /= np.linalg.norm(side_axis)
#     box_half_width_y = get_box_half_extent_y(sim_node.mj_model, target_body_name)
#     cabinet_front_x = float(box_center[0] - 0.15)
#     planned_slide = float(np.clip(1.22 - 1.08 * box_center[2], -0.04, 0.45))

#     sim_node.box_start_z = float(box_center[2])
#     sim_node.cabinet_front_x = cabinet_front_x
#     sim_node.tctr_head[1] = head_pitch
#     sim_node.tctr_slide[0] = planned_slide
#     sim_node.tctr_lft_gripper[:] = grip_open
#     sim_node.tctr_rgt_gripper[:] = grip_open

#     targets = compute_dual_box_pick_targets(
#         box_center=box_center,
#         cabinet_front_x=cabinet_front_x,
#         box_half_width_y=box_half_width_y,
#         side_axis=side_axis,
#     )
#     obstacles = build_cabinet_obstacles(box_center)

#     if not Path(urdf_path).exists():
#         raise FileNotFoundError(f"URDF file does not exist: {urdf_path}")
#     planner_model = pin.buildModelFromUrdf(str(urdf_path))
#     planner_data = planner_model.createData()
#     active_q_indices, active_v_indices = joint_indices(planner_model, ACTIVE_JOINT_NAMES)

#     def update_joint_move_ratio():
#         dif = np.abs(action - sim_node.target_control)
#         sim_node.joint_move_ratio = dif / (np.max(dif) + 1e-6)
#         sim_node.joint_move_ratio[2] *= 0.35
#         sim_node.joint_move_ratio[5:11] *= 0.45
#         sim_node.joint_move_ratio[12:18] *= 0.45

#     def solve_world_pair(left_world, right_world, left_ref, right_ref):
#         left_base = world_to_base(left_world)
#         right_base = world_to_base(right_world)
#         left_q = sim_node.solveArmEndTarget(
#             left_base, sim_node.arm_action, "l", left_ref, left_grip_rot
#         )
#         right_q = sim_node.solveArmEndTarget(
#             right_base, sim_node.arm_action, "r", right_ref, right_grip_rot
#         )
#         return np.asarray(left_q, dtype=float), np.asarray(right_q, dtype=float)

#     def full_config_from_arms(left_q, right_q):
#         q_full = make_full_configuration(
#             planner_model, cfg.init_state["base_position"], planned_slide
#         )
#         q_full[active_q_indices[:6]] = left_q
#         q_full[active_q_indices[6:]] = right_q
#         return q_full

#     def plan_rrt_stage(q_current_full, left_target, right_target, stage_name):
#         left_ref = q_current_full[active_q_indices[:6]].copy()
#         right_ref = q_current_full[active_q_indices[6:]].copy()
#         left_goal, right_goal = solve_world_pair(
#             left_target, right_target, left_ref, right_ref
#         )
#         q_goal_full = full_config_from_arms(left_goal, right_goal)
#         if in_collision(planner_model, planner_data, q_goal_full, obstacles):
#             raise RuntimeError(f"{stage_name}: IK goal is in cabinet collision")

#         q_start_active = extract_active_config(q_current_full, active_q_indices)
#         q_goal_active = extract_active_config(q_goal_full, active_q_indices)
#         segment = rrt_plan_active(
#             planner_model,
#             planner_data,
#             q_current_full,
#             active_q_indices,
#             q_start_active,
#             q_goal_active,
#             obstacles,
#             max_iter=9000,
#             step_size=0.10,
#             goal_sample_rate=0.30,
#         )
#         segment = smooth_path_active(
#             planner_model,
#             planner_data,
#             q_current_full,
#             active_q_indices,
#             segment,
#             obstacles,
#             attempts=60,
#         )
#         segment = interpolate_active_path(segment, max_step=0.035)
#         print(f"planned {stage_name}: {len(segment)} joint samples")
#         return q_goal_full, segment

#     def plan_rigid_transport_stage(
#         q_current_full,
#         left_start,
#         right_start,
#         left_goal,
#         right_goal,
#         stage_name,
#         cartesian_step=0.015,
#     ):
#         left_delta = np.asarray(left_goal) - np.asarray(left_start)
#         right_delta = np.asarray(right_goal) - np.asarray(right_start)
#         if not np.allclose(left_delta, right_delta, atol=1e-9):
#             raise RuntimeError(f"{stage_name}: left/right transport is not a rigid translation")

#         distance = float(np.linalg.norm(left_delta))
#         samples = max(2, int(math.ceil(distance / cartesian_step)) + 1)
#         q_prev = q_current_full.copy()
#         active_path = [extract_active_config(q_prev, active_q_indices)]

#         for alpha in np.linspace(0.0, 1.0, samples)[1:]:
#             left_target = np.asarray(left_start) + alpha * left_delta
#             right_target = np.asarray(right_start) + alpha * right_delta
#             left_ref = q_prev[active_q_indices[:6]].copy()
#             right_ref = q_prev[active_q_indices[6:]].copy()
#             left_q, right_q = solve_world_pair(
#                 left_target, right_target, left_ref, right_ref
#             )
#             q_next = full_config_from_arms(left_q, right_q)
#             if in_collision(planner_model, planner_data, q_next, obstacles):
#                 raise RuntimeError(
#                     f"{stage_name}: constrained grasp pose collides at alpha={alpha:.2f}"
#                 )
#             if edge_in_collision(
#                 planner_model, planner_data, q_prev, q_next, obstacles, step=0.035
#             ):
#                 raise RuntimeError(
#                     f"{stage_name}: constrained transport edge collides at alpha={alpha:.2f}"
#                 )
#             active_path.append(extract_active_config(q_next, active_q_indices))
#             q_prev = q_next

#         print(f"planned {stage_name}: {len(active_path)} constrained samples")
#         return q_prev, active_path

#     # Build one execution plan. The approach uses RRT; the grasped part uses
#     # synchronized Cartesian waypoints so the two hands keep the same relative
#     # geometry while carrying the box out of the cabinet.
#     q_current = full_config_from_arms(
#         np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
#         np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
#     )
#     execution_steps = []

#     approach_stages = [
#         ("outside", targets["outside_left"], targets["outside_right"]),
#         ("mouth", targets["mouth_left"], targets["mouth_right"]),
#         # From the cabinet mouth, let RRT search directly for a collision-free
#         # path to the side-grasp configuration instead of forcing artificial
#         # inside_mid / inside_high waypoints.
#         ("side_grasp", targets["grasp_left"], targets["grasp_right"]),
#     ]
#     for stage_name, left_target, right_target in approach_stages:
#         q_current, active_path = plan_rrt_stage(
#             q_current, left_target, right_target, stage_name
#         )
#         execution_steps.append(
#             {"kind": "joint_path", "name": stage_name, "path": active_path, "grip": grip_open}
#         )

#     execution_steps.append(
#         {"kind": "clamp", "name": "dual-side clamp", "duration": clamp_duration}
#     )

#     transport_specs = [
#         (
#             "rigid_lift",
#             targets["grasp_left"],
#             targets["grasp_right"],
#             targets["transport_lift_left"],
#             targets["transport_lift_right"],
#         ),
#         (
#             "rigid_to_mouth",
#             targets["transport_lift_left"],
#             targets["transport_lift_right"],
#             targets["transport_mouth_left"],
#             targets["transport_mouth_right"],
#         ),
#         (
#             "rigid_outside",
#             targets["transport_mouth_left"],
#             targets["transport_mouth_right"],
#             targets["transport_outside_left"],
#             targets["transport_outside_right"],
#         ),
#     ]
#     for stage_name, left_start, right_start, left_goal, right_goal in transport_specs:
#         q_current, active_path = plan_rigid_transport_stage(
#             q_current,
#             left_start,
#             right_start,
#             left_goal,
#             right_goal,
#             stage_name,
#         )
#         execution_steps.append(
#             {"kind": "joint_path", "name": stage_name, "path": active_path, "grip": grip_close}
#         )

#     execution_steps.append(
#         {"kind": "hold", "name": "hold outside cabinet", "duration": float(hold_seconds)}
#     )

#     step_index = 0
#     path_index = 0
#     step_enter_time = sim_node.mj_data.time
#     point_enter_time = sim_node.mj_data.time
#     current_step_name = None
#     print(">>> collision-aware plan ready; executing dual-side grasp")

#     while sim_node.running:
#         now = sim_node.mj_data.time
#         if max_seconds is not None and now >= max_seconds:
#             print(">>> preview time limit reached")
#             break
#         if step_index >= len(execution_steps):
#             break

#         step = execution_steps[step_index]
#         if current_step_name != step["name"]:
#             current_step_name = step["name"]
#             step_enter_time = now
#             point_enter_time = now
#             path_index = 0
#             print(f">>> execute: {current_step_name}")

#         if step["kind"] == "joint_path":
#             sim_node.tctr_lft_gripper[:] = step["grip"]
#             sim_node.tctr_rgt_gripper[:] = step["grip"]
#             path = step["path"]
#             target_active = np.asarray(path[min(path_index, len(path) - 1)], dtype=float)
#             sim_node.tctr_left_arm[:] = target_active[:6]
#             sim_node.tctr_right_arm[:] = target_active[6:]
#             sim_node.set_left_arm_new_target = True
#             sim_node.set_right_arm_new_target = True
#             update_joint_move_ratio()

#             left_err = float(np.linalg.norm(sim_node.sensor_lft_arm_qpos - target_active[:6]))
#             right_err = float(np.linalg.norm(sim_node.sensor_rgt_arm_qpos - target_active[6:]))
#             point_elapsed = now - point_enter_time
#             if (left_err < 0.045 and right_err < 0.045) or point_elapsed > 0.55:
#                 path_index += 1
#                 point_enter_time = now
#                 if path_index >= len(path):
#                     step_index += 1
#                     current_step_name = None

#         elif step["kind"] == "clamp":
#             clamp_alpha = min(1.0, (now - step_enter_time) / step["duration"])
#             gripper_target = grip_open + (grip_close - grip_open) * clamp_alpha
#             sim_node.tctr_lft_gripper[:] = gripper_target
#             sim_node.tctr_rgt_gripper[:] = gripper_target
#             if clamp_alpha >= 1.0:
#                 sim_node.tctr_lft_gripper[:] = grip_close
#                 sim_node.tctr_rgt_gripper[:] = grip_close
#                 step_index += 1
#                 current_step_name = None

#         elif step["kind"] == "hold":
#             sim_node.tctr_lft_gripper[:] = grip_close
#             sim_node.tctr_rgt_gripper[:] = grip_close
#             if now - step_enter_time >= step["duration"]:
#                 success = sim_node.check_success()
#                 print(">>> RESULT:", "SUCCESS" if success else "FAILED")
#                 step_index += 1
#                 current_step_name = None

#         for i in range(2, sim_node.njctrl):
#             action[i] = step_func(
#                 action[i],
#                 sim_node.target_control[i],
#                 0.65 * sim_node.joint_move_ratio[i] * sim_node.delta_t,
#             )
#         action[0] = 0.0
#         action[1] = 0.0
#         obs, _, _, _, _ = sim_node.step(action)

#         # Manipulation is planned for a fixed base. Prevent contact forces from
#         # making the mobile base drift and invalidating the collision plan.
#         sim_node.mj_data.qpos[0] = base_lock_x
#         sim_node.mj_data.qpos[1] = base_lock_y
#         sim_node.mj_data.qvel[0] = 0.0
#         sim_node.mj_data.qvel[1] = 0.0
#         mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)

# def fk_position(model, data, frame_id, q):
#     pin.forwardKinematics(model, data, q)
#     pin.updateFramePlacements(model, data)
#     return data.oMf[frame_id].translation.copy()


# def frame_position(model, data, frame_name):
#     if not model.existFrame(frame_name):
#         return None
#     return data.oMf[model.getFrameId(frame_name)].translation.copy()


# def clamp_to_limits(model, q):
#     lower = model.lowerPositionLimit.copy()
#     upper = model.upperPositionLimit.copy()
#     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
#     lower[invalid] = -math.pi
#     upper[invalid] = math.pi
#     return np.clip(q, lower, upper)


# def joint_indices(model, joint_names):
#     q_indices = []
#     v_indices = []
#     for name in joint_names:
#         jid = model.getJointId(name)
#         if jid == 0:
#             raise ValueError(f"joint not found: {name}")
#         joint = model.joints[jid]
#         if joint.nq != 1 or joint.nv != 1:
#             raise ValueError(f"joint {name} is not 1-DoF, nq={joint.nq}, nv={joint.nv}")
#         q_indices.append(joint.idx_q)
#         v_indices.append(joint.idx_v)
#     return np.array(q_indices, dtype=int), np.array(v_indices, dtype=int)


# def make_full_configuration(model, base_position, slide_value=0.2):
#     q = pin.neutral(model)
#     if model.nq >= 7:
#         q[0:3] = np.asarray(base_position, dtype=float)
#         # Pinocchio free-flyer quaternion order is x, y, z, w.
#         q[3:7] = np.array([0.0, 0.0, 0.0, 1.0])

#     for joint_name in ("lft_wheel_joint", "rgt_wheel_joint"):
#         jid = model.getJointId(joint_name)
#         if jid != 0:
#             q[model.joints[jid].idx_q : model.joints[jid].idx_q + 2] = 0.0

#     if model.getJointId("slide_joint") != 0:
#         sid = model.getJointId("slide_joint")
#         q[model.joints[sid].idx_q] = slide_value

#     return clamp_to_limits(model, q)


# def extract_active_config(q_full, active_q_indices):
#     return q_full[active_q_indices].copy()


# def segment_hits_aabb(p0, p1, box, samples=16):
#     for alpha in np.linspace(0.0, 1.0, samples):
#         p = (1.0 - alpha) * p0 + alpha * p1
#         if np.all(p >= box.minimum) and np.all(p <= box.maximum):
#             return True
#     return False


# def chain_points(model, data, q, frame_names):
#     pin.forwardKinematics(model, data, q)
#     pin.updateFramePlacements(model, data)
#     points = []
#     for name in frame_names:
#         if model.existFrame(name):
#             points.append(data.oMf[model.getFrameId(name)].translation.copy())
#     return [p for p in points if p is not None]


# def robot_chains(model, data, q):
#     chains = []
#     left_chain = [
#         "left_base_link",
#         "left_link1",
#         "left_link2",
#         "left_link3",
#         "left_link4",
#         "left_link5",
#         "left_link6",
#         "left_flange",
#     ]
#     right_chain = [
#         "right_base_link",
#         "right_link1",
#         "right_link2",
#         "right_link3",
#         "right_link4",
#         "right_link5",
#         "right_link6",
#         "right_flange",
#     ]
#     body_chain = ["floating_base", "underboard_link", "skin_link", "agv_link"]

#     for frame_names in (body_chain, left_chain, right_chain):
#         pts = chain_points(model, data, q, frame_names)
#         if len(pts) >= 2:
#             chains.append(pts)
#     return chains


# def in_collision(model, data, q, obstacles, robot_radius=0.015):
#     inflated_obstacles = [obstacle.inflated(robot_radius) for obstacle in obstacles]
#     for chain in robot_chains(model, data, q):
#         for p0, p1 in zip(chain[:-1], chain[1:]):
#             for obstacle in inflated_obstacles:
#                 if segment_hits_aabb(p0, p1, obstacle):
#                     return True
#     return False


# def edge_in_collision(model, data, q0, q1, obstacles, step=0.05):
#     distance = np.linalg.norm(q1 - q0)
#     steps = max(2, int(math.ceil(distance / step)))
#     for alpha in np.linspace(0.0, 1.0, steps):
#         q = (1.0 - alpha) * q0 + alpha * q1
#         if in_collision(model, data, q, obstacles):
#             return True
#     return False


# def solve_damped_least_squares_3d(jacobian, error, damping):
#     rows = jacobian.tolist()
#     err = error.tolist()

#     a = [[0.0 for _ in range(3)] for _ in range(3)]
#     for i in range(3):
#         for j in range(3):
#             a[i][j] = sum(rows[i][k] * rows[j][k] for k in range(len(rows[i])))
#         a[i][i] += damping

#     b = err[:]
#     for col in range(3):
#         pivot = max(range(col, 3), key=lambda row: abs(a[row][col]))
#         if abs(a[pivot][col]) < 1e-10:
#             return np.zeros(jacobian.shape[1])
#         if pivot != col:
#             a[col], a[pivot] = a[pivot], a[col]
#             b[col], b[pivot] = b[pivot], b[col]

#         pivot_value = a[col][col]
#         for j in range(col, 3):
#             a[col][j] /= pivot_value
#         b[col] /= pivot_value

#         for row in range(3):
#             if row == col:
#                 continue
#             factor = a[row][col]
#             for j in range(col, 3):
#                 a[row][j] -= factor * a[col][j]
#             b[row] -= factor * b[col]

#     dq = []
#     for joint_col in range(len(rows[0])):
#         dq.append(sum(rows[row][joint_col] * b[row] for row in range(3)))
#     return np.array(dq, dtype=float)


# def solve_arm_position_ik(
#     model,
#     data,
#     frame_id,
#     arm_q_indices,
#     arm_v_indices,
#     q_seed,
#     target_pos,
#     max_iter=400,
#     tolerance=0.01,
# ):
#     damping = 1e-4
#     lower = model.lowerPositionLimit[arm_q_indices].copy()
#     upper = model.upperPositionLimit[arm_q_indices].copy()
#     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
#     lower[invalid] = -math.pi
#     upper[invalid] = math.pi

#     seeds = [q_seed.copy()]
#     for scale in (0.03, 0.06, 0.10):
#         for _ in range(3):
#             q_try = q_seed.copy()
#             q_try[arm_q_indices] += np.random.uniform(-scale, scale, size=len(arm_q_indices))
#             q_try = clamp_to_limits(model, q_try)
#             seeds.append(q_try)
#     for _ in range(35):
#         q_try = q_seed.copy()
#         q_try[arm_q_indices] = np.random.uniform(lower, upper)
#         seeds.append(q_try)

#     for q_start in seeds:
#         q = q_start.copy()
#         for _ in range(max_iter):
#             pin.forwardKinematics(model, data, q)
#             pin.computeJointJacobians(model, data, q)
#             pin.updateFramePlacements(model, data)

#             ee_pos = data.oMf[frame_id].translation.copy()
#             error = target_pos - ee_pos
#             if np.linalg.norm(error) < tolerance:
#                 return clamp_to_limits(model, q), True

#             full_jacobian = pin.computeFrameJacobian(
#                 model,
#                 data,
#                 q,
#                 frame_id,
#                 pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
#             )
#             jacobian = np.asarray(full_jacobian[:3, :][:, arm_v_indices], dtype=float).copy()

#             dq = solve_damped_least_squares_3d(jacobian, error, damping)
#             dq = np.clip(dq, -0.06, 0.06)

#             for idx, delta in zip(arm_q_indices, dq):
#                 q[idx] += delta
#             q = clamp_to_limits(model, q)

#     return q_seed.copy(), False


# def solve_dual_position_ik(
#     model,
#     data,
#     left_frame_id,
#     right_frame_id,
#     active_q_indices,
#     active_v_indices,
#     q_seed,
#     left_target,
#     right_target,
#     left_q_indices,
#     left_v_indices,
#     right_q_indices,
#     right_v_indices,
#     obstacles=None,
#     max_sweeps=5,
#     max_attempts=25,
# ):
#     for attempt in range(max_attempts):
#         q = q_seed.copy()
#         if attempt > 0:
#             q[active_q_indices] = random_active_configuration(model, active_q_indices)

#         for _ in range(max_sweeps):
#             q, left_ok = solve_arm_position_ik(
#                 model,
#                 data,
#                 left_frame_id,
#                 left_q_indices,
#                 left_v_indices,
#                 q,
#                 left_target,
#                 max_iter=240,
#                 tolerance=0.012,
#             )
#             q, right_ok = solve_arm_position_ik(
#                 model,
#                 data,
#                 right_frame_id,
#                 right_q_indices,
#                 right_v_indices,
#                 q,
#                 right_target,
#                 max_iter=240,
#                 tolerance=0.012,
#             )
#             if not (left_ok and right_ok):
#                 continue

#             q = clamp_to_limits(model, q)
#             if obstacles is None or not in_collision(model, data, q, obstacles):
#                 return q, True

#     return q_seed.copy(), False


# def nearest_node(nodes, q):
#     distances = [np.linalg.norm(node - q) for node in nodes]
#     return int(np.argmin(distances))


# def steer(q_from, q_to, step_size):
#     direction = q_to - q_from
#     distance = np.linalg.norm(direction)
#     if distance <= step_size:
#         return q_to.copy()
#     return q_from + direction / distance * step_size


# def reconstruct_path(nodes, parents, goal_index):
#     path = []
#     index = goal_index
#     while index is not None:
#         path.append(nodes[index])
#         index = parents[index]
#     path.reverse()
#     return path


# def clamp_active(model, active_q, active_q_indices):
#     q = pin.neutral(model)[active_q_indices]
#     q[:] = active_q
#     lower = model.lowerPositionLimit[active_q_indices].copy()
#     upper = model.upperPositionLimit[active_q_indices].copy()
#     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
#     lower[invalid] = -math.pi
#     upper[invalid] = math.pi
#     return np.clip(active_q, lower, upper)


# def random_active_configuration(model, active_q_indices):
#     lower = model.lowerPositionLimit[active_q_indices].copy()
#     upper = model.upperPositionLimit[active_q_indices].copy()
#     invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
#     lower[invalid] = -math.pi
#     upper[invalid] = math.pi
#     return np.random.uniform(lower, upper)


# def active_to_full(q_template, q_active, active_q_indices):
#     q = q_template.copy()
#     q[active_q_indices] = q_active
#     return q


# def rrt_plan_active(
#     model,
#     data,
#     q_template,
#     active_q_indices,
#     q_start_active,
#     q_goal_active,
#     obstacles,
#     max_iter=7000,
#     step_size=0.12,
#     goal_sample_rate=0.22,
# ):
#     q_start_full = active_to_full(q_template, q_start_active, active_q_indices)
#     q_goal_full = active_to_full(q_template, q_goal_active, active_q_indices)
#     if in_collision(model, data, q_start_full, obstacles):
#         raise ValueError("q_start is in collision")
#     if in_collision(model, data, q_goal_full, obstacles):
#         raise ValueError("q_goal is in collision")
#     if not edge_in_collision(model, data, q_start_full, q_goal_full, obstacles):
#         return [q_start_active.copy(), q_goal_active.copy()]

#     nodes = [q_start_active.copy()]
#     parents = [None]

#     for _ in range(max_iter):
#         q_rand = q_goal_active if random.random() < goal_sample_rate else random_active_configuration(model, active_q_indices)
#         nearest_index = nearest_node(nodes, q_rand)
#         q_new = steer(nodes[nearest_index], q_rand, step_size)
#         q_new = clamp_active(model, q_new, active_q_indices)

#         q_near_full = active_to_full(q_template, nodes[nearest_index], active_q_indices)
#         q_new_full = active_to_full(q_template, q_new, active_q_indices)
#         if edge_in_collision(model, data, q_near_full, q_new_full, obstacles):
#             continue

#         nodes.append(q_new)
#         parents.append(nearest_index)
#         new_index = len(nodes) - 1

#         if np.linalg.norm(q_new - q_goal_active) < step_size:
#             q_new_full = active_to_full(q_template, q_new, active_q_indices)
#             if not edge_in_collision(model, data, q_new_full, q_goal_full, obstacles):
#                 nodes.append(q_goal_active.copy())
#                 parents.append(new_index)
#                 return reconstruct_path(nodes, parents, len(nodes) - 1)

#     raise RuntimeError("RRT failed to find a collision-free path")


# def smooth_path_active(model, data, q_template, active_q_indices, path, obstacles, attempts=120):
#     path = [q.copy() for q in path]
#     if len(path) <= 2:
#         return path

#     for _ in range(attempts):
#         if len(path) <= 2:
#             break
#         i, j = sorted(random.sample(range(len(path)), 2))
#         if j <= i + 1:
#             continue
#         q_i_full = active_to_full(q_template, path[i], active_q_indices)
#         q_j_full = active_to_full(q_template, path[j], active_q_indices)
#         if not edge_in_collision(model, data, q_i_full, q_j_full, obstacles):
#             path = path[: i + 1] + path[j:]
#     return path


# def interpolate_active_path(path, max_step=0.03):
#     dense_path = []
#     for q0, q1 in zip(path[:-1], path[1:]):
#         distance = np.linalg.norm(q1 - q0)
#         steps = max(2, int(math.ceil(distance / max_step)))
#         for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
#             dense_path.append((1.0 - alpha) * q0 + alpha * q1)
#     dense_path.append(path[-1].copy())
#     return dense_path


# def build_cabinet_obstacles(box_center):
#     """Return the code-2 cabinet approximation used by the collision planner."""
#     box_center = np.asarray(box_center, dtype=float)
#     cabinet_center = np.array([box_center[0], box_center[1], 0.0])
#     return [
#         AABB(
#             "cabinet_left_side",
#             cabinet_center + np.array([-0.15, 0.39, 0.00]),
#             cabinet_center + np.array([0.15, 0.41, 2.03]),
#         ),
#         AABB(
#             "cabinet_right_side",
#             cabinet_center + np.array([-0.15, -0.41, 0.00]),
#             cabinet_center + np.array([0.15, -0.39, 2.03]),
#         ),
#         AABB(
#             "cabinet_back",
#             cabinet_center + np.array([0.13, -0.40, 0.00]),
#             cabinet_center + np.array([0.15, 0.40, 2.03]),
#         ),
#         AABB(
#             "lower_shelf",
#             cabinet_center + np.array([-0.15, -0.40, 0.72]),
#             cabinet_center + np.array([0.15, 0.40, 0.74]),
#         ),
#         AABB(
#             "upper_shelf",
#             cabinet_center + np.array([-0.15, -0.40, 1.05]),
#             cabinet_center + np.array([0.15, 0.40, 1.07]),
#         ),
#     ]


# def compute_dual_box_pick_targets(
#     box_center,
#     box_yaw=0.0,
#     cabinet_front_x=0.48,
#     box_half_width_y=DEFAULT_BOX_HALF_WIDTH_Y,
#     pre_clearance=0.050,
#     grasp_clearance=0.025,
#     diagonal_x=0.030,
#     lift_delta=0.030,
#     side_axis=None,
# ):
#     """Build approach targets and rigid post-grasp transport targets.

#     Before grasping, the two hands may use a small diagonal X offset to create
#     elbow clearance. After grasping, *both hands receive exactly the same XYZ
#     translation*, so their separation vector and grasp geometry are preserved.
#     """
#     box_center = np.asarray(box_center, dtype=float)
#     if side_axis is None:
#         axis = np.array([-math.sin(box_yaw), math.cos(box_yaw), 0.0], dtype=float)
#     else:
#         axis = np.asarray(side_axis, dtype=float).copy()
#         axis[2] = 0.0
#     if np.linalg.norm(axis) < 1e-6:
#         axis = np.array([0.0, 1.0, 0.0])
#     axis /= np.linalg.norm(axis)

#     outside_x = cabinet_front_x - 0.11
#     mouth_x = cabinet_front_x - 0.015
#     grasp_x = box_center[0] - 0.02
#     retreat_x = cabinet_front_x - 0.16

#     approach_z = box_center[2] + 0.16
#     grasp_z = box_center[2] + 0.075
#     approach_lateral = float(box_half_width_y + pre_clearance)
#     grasp_lateral = float(box_half_width_y + grasp_clearance)

#     def side_pair(x, z, lateral, skew=False):
#         center = np.array([x, box_center[1], z], dtype=float)
#         point_a = center + axis * lateral
#         point_b = center - axis * lateral
#         if point_a[1] >= point_b[1]:
#             left_point, right_point = point_a, point_b
#         else:
#             left_point, right_point = point_b, point_a
#         if skew:
#             left_point = left_point.copy()
#             right_point = right_point.copy()
#             left_point[0] -= diagonal_x
#             right_point[0] += diagonal_x
#         return left_point, right_point

#     outside_left, outside_right = side_pair(
#         outside_x, approach_z, approach_lateral, skew=False
#     )
#     mouth_left, mouth_right = side_pair(
#         mouth_x, approach_z, approach_lateral, skew=False
#     )
#     inside_high_left, inside_high_right = side_pair(
#         grasp_x, approach_z, grasp_lateral, skew=True
#     )
#     grasp_left, grasp_right = side_pair(
#         grasp_x, grasp_z, grasp_lateral, skew=True
#     )

#     inside_mid_left = (mouth_left + inside_high_left) * 0.5
#     inside_mid_right = (mouth_right + inside_high_right) * 0.5

#     # Once the grippers close, all subsequent target pairs are generated by
#     # applying the same translation to the original grasp pair.
#     lift_translation = np.array([0.0, 0.0, lift_delta])
#     mouth_translation = np.array([mouth_x - grasp_x, 0.0, lift_delta])
#     outside_translation = np.array([retreat_x - grasp_x, 0.0, lift_delta])

#     transport_lift_left = grasp_left + lift_translation
#     transport_lift_right = grasp_right + lift_translation
#     transport_mouth_left = grasp_left + mouth_translation
#     transport_mouth_right = grasp_right + mouth_translation
#     transport_outside_left = grasp_left + outside_translation
#     transport_outside_right = grasp_right + outside_translation

#     return {
#         "outside_left": outside_left,
#         "outside_right": outside_right,
#         "mouth_left": mouth_left,
#         "mouth_right": mouth_right,
#         "inside_mid_left": inside_mid_left,
#         "inside_mid_right": inside_mid_right,
#         "inside_high_left": inside_high_left,
#         "inside_high_right": inside_high_right,
#         "grasp_left": grasp_left,
#         "grasp_right": grasp_right,
#         "transport_lift_left": transport_lift_left,
#         "transport_lift_right": transport_lift_right,
#         "transport_mouth_left": transport_mouth_left,
#         "transport_mouth_right": transport_mouth_right,
#         "transport_outside_left": transport_outside_left,
#         "transport_outside_right": transport_outside_right,
#         # Backward-compatible aliases used by the optional plan visualizer.
#         "lift_left": transport_lift_left,
#         "lift_right": transport_lift_right,
#         "retreat_left": transport_outside_left,
#         "retreat_right": transport_outside_right,
#     }


# def plan_dual_grasp_sequence(
#     model,
#     data,
#     left_frame_id,
#     right_frame_id,
#     q_start_full,
#     active_q_indices,
#     active_v_indices,
#     left_q_indices,
#     left_v_indices,
#     right_q_indices,
#     right_v_indices,
#     stage_targets,
#     obstacles,
# ):
#     q_path_full = [q_start_full.copy()]
#     q_current_full = q_start_full.copy()
#     stage_configs = []
#     pin.forwardKinematics(model, data, q_current_full)
#     pin.updateFramePlacements(model, data)
#     prev_left_target = data.oMf[left_frame_id].translation.copy()
#     prev_right_target = data.oMf[right_frame_id].translation.copy()

#     for name, left_target, right_target in stage_targets:
#         q_goal_full, ik_ok = solve_dual_position_ik(
#             model,
#             data,
#             left_frame_id,
#             right_frame_id,
#             active_q_indices,
#             active_v_indices,
#             q_current_full,
#             left_target,
#             right_target,
#             left_q_indices,
#             left_v_indices,
#             right_q_indices,
#             right_v_indices,
#             obstacles=obstacles,
#         )
#         if not ik_ok:
#             raise RuntimeError(
#                 f"failed to solve dual IK for stage {name}: "
#                 f"left={np.round(left_target, 3)}, right={np.round(right_target, 3)}"
#             )

#         q_start_active = extract_active_config(q_current_full, active_q_indices)
#         q_goal_active = extract_active_config(q_goal_full, active_q_indices)
#         try:
#             segment_active = rrt_plan_active(
#                 model,
#                 data,
#                 q_current_full,
#                 active_q_indices,
#                 q_start_active,
#                 q_goal_active,
#                 obstacles,
#                 max_iter=9000,
#                 step_size=0.10,
#                 goal_sample_rate=0.30,
#             )
#             segment_active = smooth_path_active(
#                 model,
#                 data,
#                 q_current_full,
#                 active_q_indices,
#                 segment_active,
#                 obstacles,
#                 attempts=50,
#             )
#         except RuntimeError:
#             print(f"RRT fallback: split Cartesian segment for stage {name}")
#             segment_active = [q_start_active.copy()]
#             q_bridge = q_current_full.copy()
#             for alpha in np.linspace(0.2, 1.0, 5):
#                 left_mid = (1.0 - alpha) * prev_left_target + alpha * left_target
#                 right_mid = (1.0 - alpha) * prev_right_target + alpha * right_target
#                 q_next, bridge_ok = solve_dual_position_ik(
#                     model,
#                     data,
#                     left_frame_id,
#                     right_frame_id,
#                     active_q_indices,
#                     active_v_indices,
#                     q_bridge,
#                     left_mid,
#                     right_mid,
#                     left_q_indices,
#                     left_v_indices,
#                     right_q_indices,
#                     right_v_indices,
#                     obstacles=obstacles,
#                     max_attempts=30,
#                 )
#                 if not bridge_ok or edge_in_collision(model, data, q_bridge, q_next, obstacles):
#                     raise
#                 segment_active.append(extract_active_config(q_next, active_q_indices))
#                 q_bridge = q_next

#         q_path_full.extend(
#             [active_to_full(q_current_full, q_active, active_q_indices) for q_active in segment_active[1:]]
#         )
#         q_current_full = q_goal_full
#         prev_left_target = left_target.copy()
#         prev_right_target = right_target.copy()
#         stage_configs.append((name, q_goal_full.copy(), left_target.copy(), right_target.copy()))
#         print(f"stage {name}: left={np.round(left_target, 3)}, right={np.round(right_target, 3)}")

#     return q_path_full, stage_configs


# def arm_chain_points(model, data, q, side):
#     if side == "left":
#         frame_names = [
#             "left_base_link",
#             "left_link1",
#             "left_link2",
#             "left_link3",
#             "left_link4",
#             "left_link5",
#             "left_link6",
#             "left_flange",
#         ]
#     else:
#         frame_names = [
#             "right_base_link",
#             "right_link1",
#             "right_link2",
#             "right_link3",
#             "right_link4",
#             "right_link5",
#             "right_link6",
#             "right_flange",
#         ]
#     return chain_points(model, data, q, frame_names)


# def add_aabb_trace(fig, obstacle):
#     mn = obstacle.minimum
#     mx = obstacle.maximum
#     x = [mn[0], mx[0], mx[0], mn[0], mn[0], mn[0], mx[0], mx[0], mn[0], mn[0], mx[0], mx[0], mx[0], mx[0], mn[0], mn[0]]
#     y = [mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mx[1], mx[1]]
#     z = [mn[2], mn[2], mn[2], mn[2], mn[2], mx[2], mx[2], mx[2], mx[2], mx[2], mx[2], mn[2], mn[2], mx[2], mx[2], mn[2]]
#     fig.add_trace(
#         go.Scatter3d(
#             x=x,
#             y=y,
#             z=z,
#             mode="lines",
#             line=dict(color="#4A5568", width=4),
#             name=obstacle.name,
#         )
#     )


# def visualize_trajectory(
#     model,
#     data,
#     left_frame_id,
#     right_frame_id,
#     q_path,
#     left_points,
#     right_points,
#     obstacles,
#     stage_configs,
# ):
#     fig = go.Figure()

#     fig.add_trace(
#         go.Scatter3d(
#             x=left_points[:, 0],
#             y=left_points[:, 1],
#             z=left_points[:, 2],
#             mode="lines+markers",
#             line=dict(color="#2563EB", width=6),
#             marker=dict(size=3, color="#2563EB", opacity=0.6),
#             name="left ee path",
#         )
#     )
#     fig.add_trace(
#         go.Scatter3d(
#             x=right_points[:, 0],
#             y=right_points[:, 1],
#             z=right_points[:, 2],
#             mode="lines+markers",
#             line=dict(color="#EF4444", width=6),
#             marker=dict(size=3, color="#EF4444", opacity=0.6),
#             name="right ee path",
#         )
#     )

#     fig.add_trace(
#         go.Scatter3d(
#             x=[left_points[0, 0]],
#             y=[left_points[0, 1]],
#             z=[left_points[0, 2]],
#             mode="markers",
#             marker=dict(size=8, color="#10B981"),
#             name="left start",
#         )
#     )
#     fig.add_trace(
#         go.Scatter3d(
#             x=[right_points[0, 0]],
#             y=[right_points[0, 1]],
#             z=[right_points[0, 2]],
#             mode="markers",
#             marker=dict(size=8, color="#14B8A6"),
#             name="right start",
#         )
#     )
#     fig.add_trace(
#         go.Scatter3d(
#             x=[left_points[-1, 0]],
#             y=[left_points[-1, 1]],
#             z=[left_points[-1, 2]],
#             mode="markers",
#             marker=dict(size=8, color="#B91C1C"),
#             name="left goal",
#         )
#     )
#     fig.add_trace(
#         go.Scatter3d(
#             x=[right_points[-1, 0]],
#             y=[right_points[-1, 1]],
#             z=[right_points[-1, 2]],
#             mode="markers",
#             marker=dict(size=8, color="#7F1D1D"),
#             name="right goal",
#         )
#     )

#     for obstacle in obstacles:
#         add_aabb_trace(fig, obstacle)

#     for name, _q, left_target, right_target in stage_configs:
#         fig.add_trace(
#             go.Scatter3d(
#                 x=[left_target[0], right_target[0]],
#                 y=[left_target[1], right_target[1]],
#                 z=[left_target[2], right_target[2]],
#                 mode="markers+text",
#                 marker=dict(size=5, color="#111827"),
#                 text=[f"{name}-L", f"{name}-R"],
#                 textposition="top center",
#                 name=f"stage: {name}",
#             )
#         )

#     snapshot_count = min(8, len(q_path))
#     snapshot_indices = np.linspace(0, len(q_path) - 1, snapshot_count, dtype=int)
#     for trace_idx, path_idx in enumerate(snapshot_indices):
#         left_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "left"))
#         right_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "right"))
#         if len(left_chain) >= 2:
#             fig.add_trace(
#                 go.Scatter3d(
#                     x=left_chain[:, 0],
#                     y=left_chain[:, 1],
#                     z=left_chain[:, 2],
#                     mode="lines+markers",
#                     line=dict(color="#1E293B", width=5),
#                     marker=dict(size=3, color="#1E293B"),
#                     opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
#                     name="left arm snapshots" if trace_idx == 0 else None,
#                     showlegend=trace_idx == 0,
#                 )
#             )
#         if len(right_chain) >= 2:
#             fig.add_trace(
#                 go.Scatter3d(
#                     x=right_chain[:, 0],
#                     y=right_chain[:, 1],
#                     z=right_chain[:, 2],
#                     mode="lines+markers",
#                     line=dict(color="#374151", width=5),
#                     marker=dict(size=3, color="#374151"),
#                     opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
#                     name="right arm snapshots" if trace_idx == 0 else None,
#                     showlegend=trace_idx == 0,
#                 )
#             )

#     fig.update_layout(
#         title="Dual-arm collision-aware grasp motion planning",
#         scene=dict(
#             xaxis_title="X (m)",
#             yaxis_title="Y (m)",
#             zaxis_title="Z (m)",
#             aspectmode="data",
#             camera=dict(eye=dict(x=1.9, y=1.8, z=1.25)),
#         ),
#         width=1000,
#         height=760,
#         margin=dict(l=0, r=0, t=50, b=0),
#     )
#     fig.show()


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
#     parser.add_argument(
#         "--mjcf",
#         default=DEFAULT_MJCF_FILE_PATH,
#         help="DISCOVERSE MJCF scene file to display",
#     )
#     parser.add_argument(
#         "--discoverse-root",
#         default=DEFAULT_DISCOVERSE_ROOT,
#         help="local DISCOVERSE source root used to open the MJCF task window",
#     )
#     parser.add_argument(
#         "--plan",
#         action="store_true",
#         help="run the offline Pinocchio/RRT trajectory visualizer instead of MuJoCo execution",
#     )
#     parser.add_argument(
#         "--headless-preview-seconds",
#         type=float,
#         default=None,
#         help="run the MJCF auto-motion preview without a window for this many seconds",
#     )
#     parser.add_argument("--left-frame", default=LEFT_EEF_FRAME)
#     parser.add_argument("--right-frame", default=RIGHT_EEF_FRAME)
#     parser.add_argument("--base-position", nargs=3, type=float, default=[0.80, 0.238, 0.0])
#     parser.add_argument("--slide", type=float, default=0.3)
#     parser.add_argument("--box-center", nargs=3, type=float, default=[1.23, 0.238, 0.82])
#     parser.add_argument("--box-yaw", type=float, default=0.0)
#     args = parser.parse_args()

#     if not args.plan:
#         run_box_pick_grasp_scene(
#             args.mjcf,
#             args.discoverse_root,
#             urdf_path=args.urdf,
#             headless=args.headless_preview_seconds is not None,
#             max_seconds=args.headless_preview_seconds,
#         )
#         return

#     global pin, go
#     import pinocchio as pin
#     import plotly.graph_objects as go

#     if not Path(args.urdf).exists():
#         raise FileNotFoundError(f"URDF file does not exist: {args.urdf}")

#     model = pin.buildModelFromUrdf(args.urdf)
#     data = model.createData()

#     if not model.existFrame(args.left_frame):
#         raise ValueError(f"Left frame not found: {args.left_frame}")
#     if not model.existFrame(args.right_frame):
#         raise ValueError(f"Right frame not found: {args.right_frame}")

#     left_frame_id = model.getFrameId(args.left_frame)
#     right_frame_id = model.getFrameId(args.right_frame)
#     active_q_indices, active_v_indices = joint_indices(model, ACTIVE_JOINT_NAMES)
#     left_q_indices = active_q_indices[:6]
#     left_v_indices = active_v_indices[:6]
#     right_q_indices = active_q_indices[6:]
#     right_v_indices = active_v_indices[6:]

#     print("model loaded")
#     print(f"urdf: {args.urdf}")
#     print(f"left frame: {args.left_frame}")
#     print(f"right frame: {args.right_frame}")
#     print(f"nq: {model.nq}, nv: {model.nv}")
#     print(f"active joints: {ACTIVE_JOINT_NAMES}")

#     q_start = make_full_configuration(model, args.base_position, args.slide)

#     box_center = np.array(args.box_center, dtype=float)
#     obstacles = build_cabinet_obstacles(box_center)
#     pick_targets = compute_dual_box_pick_targets(
#         box_center=box_center,
#         box_yaw=args.box_yaw,
#         cabinet_front_x=box_center[0] - 0.15,
#     )
#     stage_targets = [
#         ("pregrasp", pick_targets["outside_left"], pick_targets["outside_right"]),
#         ("mouth", pick_targets["mouth_left"], pick_targets["mouth_right"]),
#         ("grasp_down", pick_targets["grasp_left"], pick_targets["grasp_right"]),
#         ("lift", pick_targets["lift_left"], pick_targets["lift_right"]),
#         ("retreat", pick_targets["retreat_left"], pick_targets["retreat_right"]),
#     ]

#     q_path, stage_configs = plan_dual_grasp_sequence(
#         model,
#         data,
#         left_frame_id,
#         right_frame_id,
#         q_start,
#         active_q_indices,
#         active_v_indices,
#         left_q_indices,
#         left_v_indices,
#         right_q_indices,
#         right_v_indices,
#         stage_targets,
#         obstacles,
#     )
#     q_path = [q.copy() for q in q_path]
#     q_path_dense = []
#     for q0, q1 in zip(q_path[:-1], q_path[1:]):
#         distance = np.linalg.norm(q1[active_q_indices] - q0[active_q_indices])
#         steps = max(2, int(math.ceil(distance / 0.03)))
#         for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
#             q_path_dense.append((1.0 - alpha) * q0 + alpha * q1)
#     q_path_dense.append(q_path[-1].copy())

#     left_points = []
#     right_points = []
#     for q in q_path_dense:
#         pin.forwardKinematics(model, data, q)
#         pin.updateFramePlacements(model, data)
#         left_points.append(data.oMf[left_frame_id].translation.copy())
#         right_points.append(data.oMf[right_frame_id].translation.copy())

#     left_points = np.array(left_points)
#     right_points = np.array(right_points)

#     print(f"planned joint samples: {len(q_path_dense)}")
#     print(f"left ee start: {left_points[0]}")
#     print(f"left ee goal:  {left_points[-1]}")
#     print(f"right ee start: {right_points[0]}")
#     print(f"right ee goal:  {right_points[-1]}")

#     visualize_trajectory(
#         model,
#         data,
#         left_frame_id,
#         right_frame_id,
#         q_path_dense,
#         left_points,
#         right_points,
#         obstacles,
#         stage_configs,
#     )


# if __name__ == "__main__":
#     main()
import argparse
import math
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

pin = None
go = None


DEFAULT_URDF_PATH = (
    "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/models/urdf/mmk2_s_g2.urdf"
)
DEFAULT_DISCOVERSE_ROOT = (
    "D:/thingscatch/DISCOVERSE-main/DISCOVERSE"
)

DEFAULT_MJCF_FILE_PATH = (
    "D:/thingscatch/DISCOVERSE-main/DISCOVERSE/"
    "models/mjcf/tasks_mmk2/task1_pick_and_place.xml"
)

LEFT_EEF_FRAME = "left_end_link"
RIGHT_EEF_FRAME = "right_end_link"
ACTIVE_JOINT_NAMES = [
    "left_joint1",
    "left_joint2",
    "left_joint3",
    "left_joint4",
    "left_joint5",
    "left_joint6",
    "right_joint1",
    "right_joint2",
    "right_joint3",
    "right_joint4",
    "right_joint5",
    "right_joint6",
]

DEFAULT_BOX_HALF_WIDTH_Y = 0.08
DEFAULT_BOX_HALF_DEPTH_X = 0.12
DEFAULT_BOX_HEIGHT = 0.19
LEFT_GRIP_ROT = np.array([
    [0.0, 0.998482379, 0.055072124],
    [0.923879533, -0.021074672, 0.382102567],
    [0.382683432, 0.050880237, -0.922477298],
])
RIGHT_GRIP_ROT = np.array([
    [0.0, -0.998482379, 0.055072124],
    [-0.923879533, -0.021074672, -0.382102567],
    [0.382683432, -0.050880237, -0.922477298],
])


@dataclass
class AABB:
    name: str
    minimum: np.ndarray
    maximum: np.ndarray

    def inflated(self, radius):
        return AABB(self.name, self.minimum - radius, self.maximum + radius)


def ensure_discoverse_import_path(discoverse_root):
    discoverse_root = Path(discoverse_root)
    if not discoverse_root.exists():
        raise FileNotFoundError(f"DISCOVERSE root does not exist: {discoverse_root}")
    root_str = str(discoverse_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def mat3_mul(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    out = np.empty((3, 3), dtype=float)
    for i in range(3):
        for j in range(3):
            out[i, j] = (
                a[i, 0] * b[0, j]
                + a[i, 1] * b[1, j]
                + a[i, 2] * b[2, j]
            )
    return out


def _axis_rotation(axis, angle_rad):
    c = float(np.cos(angle_rad))
    s = float(np.sin(angle_rad))
    if axis == "x":
        return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])
    if axis == "y":
        return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])
    if axis == "z":
        return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    raise ValueError(f"unknown rotation axis: {axis}")


def relaxed_grip_rotation_candidates(
    base_rotation,
    previous_offset_deg=(0.0, 0.0, 0.0),
    max_angle_deg=8.0,
    step_deg=2.0,
):
    """Yield small local wrist-rotation alternatives around a nominal grasp pose.

    The nominal orientation is included.  Candidate ordering favors continuity
    with the previously selected offset, then smaller absolute deviation from
    the nominal grasp orientation.  Rotations are applied in the gripper-local
    frame and are bounded so the grasp orientation can relax without becoming
    unconstrained.
    """
    base_rotation = np.asarray(base_rotation, dtype=float)
    previous = tuple(float(v) for v in previous_offset_deg)
    max_angle_deg = float(max_angle_deg)
    step_deg = float(step_deg)
    if max_angle_deg < 0.0 or step_deg <= 0.0:
        raise ValueError("max_angle_deg must be >= 0 and step_deg must be > 0")

    offsets = {(0.0, 0.0, 0.0)}
    magnitudes = []
    value = step_deg
    while value <= max_angle_deg + 1e-9:
        magnitudes.append(round(value, 10))
        value += step_deg

    # First-order relaxation: one local wrist axis at a time.
    for mag in magnitudes:
        for axis_index in range(3):
            for sign in (-1.0, 1.0):
                off = [0.0, 0.0, 0.0]
                off[axis_index] = sign * mag
                offsets.add(tuple(off))

    # A few coupled small-angle alternatives handle poses where one-axis
    # relaxation is insufficient, while still keeping the grasp nearly fixed.
    coupled_magnitudes = [m for m in magnitudes if m <= min(4.0, max_angle_deg)]
    for mag in coupled_magnitudes:
        for i, j in ((0, 1), (0, 2), (1, 2)):
            for sign_i in (-1.0, 1.0):
                for sign_j in (-1.0, 1.0):
                    off = [0.0, 0.0, 0.0]
                    off[i] = sign_i * mag
                    off[j] = sign_j * mag
                    if np.linalg.norm(off) <= max_angle_deg + 1e-9:
                        offsets.add(tuple(off))

    def candidate_key(offset):
        continuity = sum((offset[i] - previous[i]) ** 2 for i in range(3))
        absolute = sum(v * v for v in offset)
        return continuity, absolute, offset

    for offset in sorted(offsets, key=candidate_key):
        rx, ry, rz = np.deg2rad(offset)
        delta = mat3_mul(
            mat3_mul(_axis_rotation("x", rx), _axis_rotation("y", ry)),
            _axis_rotation("z", rz),
        )
        yield mat3_mul(base_rotation, delta), offset


def get_box_half_extent_y(mj_model, body_name="box_yellow"):
    try:
        body_id = int(mj_model.body(body_name).id)
    except Exception as exc:
        print(f"warning: body {body_name!r} not found ({exc}); use default half-y")
        return DEFAULT_BOX_HALF_WIDTH_Y

    geom_start = int(mj_model.body_geomadr[body_id])
    geom_num = int(mj_model.body_geomnum[body_id])
    if geom_num == 0:
        return DEFAULT_BOX_HALF_WIDTH_Y

    for geom_id in range(geom_start, geom_start + geom_num):
        try:
            geom_type = int(mj_model.geom_type[geom_id])
        except Exception:
            continue
        if geom_type == 6:
            return float(mj_model.geom_size[geom_id, 1])

    return DEFAULT_BOX_HALF_WIDTH_Y


def show_discoverse_mjcf_scene(
    mjcf_path,
    discoverse_root=DEFAULT_DISCOVERSE_ROOT,
    headless=False,
    max_seconds=None,
):
    """Open the same DISCOVERSE MJCF task window used by the competition code."""
    ensure_discoverse_import_path(discoverse_root)

    from discoverse.robots_env.mmk2_base import MMK2Base, MMK2Cfg
    from discoverse.utils import step_func

    class MjcfPreviewNode(MMK2Base):
        def __init__(self, config):
            super().__init__(config)
            if "head_cam" in self.camera_names:
                self.cam_id = self.camera_names.index("head_cam")
                self.config.obs_rgb_cam_id = [self.cam_id]
                print("render camera: head_cam", "id=", self.cam_id)
            elif self.camera_names:
                self.cam_id = 0
                self.config.obs_rgb_cam_id = [0]
                print("render camera:", self.camera_names[0], "id= 0")
            else:
                self.cam_id = -1
                self.config.obs_rgb_cam_id = [-1]
                print("render camera: free")

        def post_physics_step(self):
            pass

        def getChangedObjectPose(self):
            return {}

        def checkTerminated(self):
            return False

        def getObservation(self):
            return {}

        def getPrivilegedObservation(self):
            return {}

        def getReward(self):
            return 0.0

    def set_stage_targets(target_control, stage):
        if stage == 1:
            print(">>> stage 1: lift/head ready")
            target_control[2] = 0.14
            target_control[3:5] = [0.0, -0.25]
            target_control[11] = 0.0
            target_control[18] = 0.0
        elif stage == 2:
            print(">>> stage 2: move arms forward")
            target_control[5:11] = [0.31, -1.473, 2.076, -1.391, 1.496, -2.0]
            target_control[12:18] = [-0.31, -1.473, 2.076, 1.391, -1.496, 2.0]
        elif stage == 3:
            print(">>> stage 3: extend grippers deeper toward box sides")
            target_control[5:11] = [0.45, -1.473, 2.076, -1.391, 1.496, -2.0]
            target_control[12:18] = [-0.45, -1.473, 2.076, 1.391, -1.496, 2.0]
            target_control[11] = 0.0
            target_control[18] = 0.0
        elif stage == 4:
            print(">>> stage 4: hold clamp")
            target_control[11] = 0.0
            target_control[18] = 0.0

    cfg = MMK2Cfg()
    cfg.mjcf_file_path = str(mjcf_path)
    cfg.use_gaussian_renderer = False
    cfg.headless = headless
    cfg.enable_render = not headless
    cfg.sync = True
    cfg.render_set = {
        "fps": 30,
        "width": 1280,
        "height": 720,
        "window_title": "DISCOVERSE MJCF",
    }
    cfg.obs_rgb_cam_id = None
    cfg.obs_depth_cam_id = None
    cfg.init_state = MMK2Cfg.init_state.copy()
    cfg.init_state["base_position"] = [0.58, 0.715, 0.0]
    cfg.init_state["base_orientation"] = [1.0, 0.0, 0.0, 0.0]
    cfg.init_state["head_qpos"] = [0.0, 0.0]
    cfg.init_state["lft_gripper_qpos"] = [0.0]
    cfg.init_state["rgt_gripper_qpos"] = [0.0]

    sim_node = MjcfPreviewNode(cfg)
    obs = sim_node.reset()
    target_control = sim_node.init_joint_ctrl.copy()
    action = target_control.copy()
    stage = 0
    stage_start_time = sim_node.mj_data.time
    print("DISCOVERSE MJCF window opened. Auto motion enabled. Close the window to exit.")
    while sim_node.running:
        now = sim_node.mj_data.time
        if max_seconds is not None and now >= max_seconds:
            print(
                "preview finished:",
                "time=", round(float(now), 3),
                "slide=", np.array2string(sim_node.sensor_slide_qpos, precision=3),
                "head=", np.array2string(sim_node.sensor_head_qpos, precision=3),
                "left_arm=", np.array2string(sim_node.sensor_lft_arm_qpos, precision=3),
                "right_arm=", np.array2string(sim_node.sensor_rgt_arm_qpos, precision=3),
            )
            break
        stage_elapsed = now - stage_start_time

        if stage == 0 and stage_elapsed > 0.5:
            stage = 1
            stage_start_time = now
            set_stage_targets(target_control, stage)
        elif stage == 1 and stage_elapsed > 1.2:
            stage = 2
            stage_start_time = now
            set_stage_targets(target_control, stage)
        elif stage == 2 and stage_elapsed > 2.5:
            stage = 3
            stage_start_time = now
            set_stage_targets(target_control, stage)
        elif stage == 3 and stage_elapsed > 2.0:
            stage = 4
            stage_start_time = now
            set_stage_targets(target_control, stage)

        for i in range(2, sim_node.njctrl):
            action[i] = step_func(action[i], target_control[i], 0.8 * sim_node.delta_t)
        action[0] = 0.0
        action[1] = 0.0
        obs, _, _, _, _ = sim_node.step(action)


def run_box_pick_grasp_scene(
    mjcf_path,
    discoverse_root=DEFAULT_DISCOVERSE_ROOT,
    urdf_path=DEFAULT_URDF_PATH,
    headless=False,
    max_seconds=None,
    hold_seconds=5.0,
    wam_dataset_path=None,
    wam_model_path=None,
    wam_branch_planning=False,
    wam_rollout_horizon=1.8,
    randomize_scene=False,
    scene_seed=0,
    wam_action_model_path=None,
    visual_dataset_dir=None,
    visual_model_path=None,
):
    """Run collision-aware dual-wall grasp and physical extraction in MuJoCo.

    Planning/execution policy:
      1. Read the real ``box_yellow`` pose and width from the code-2 MJCF scene.
      2. Use RRT + AABB collision checking for the ungrasped approach path.
      3. Close both grippers gradually on the two side walls.
      4. Keep the package as a free body and retreat with the real wheel drive.
      5. Accept success only if contact/friction transport survives slip checks.

    The scene's object mass and contact friction are left unchanged.
    """
    ensure_discoverse_import_path(discoverse_root)

    # On Windows, load PyTorch before MuJoCo/Pinocchio. Loading their native
    # runtimes first can make torch's shm.dll resolve against an incompatible
    # dependency already present in the process.
    from wam_critic import WAMCritic, WAMCriticRecorder
    from action_wam import ActionWAMCritic
    from visual_wam import VisualWAMCritic, VisualWAMRecorder

    wam_critic_preloaded = WAMCritic(wam_model_path) if wam_model_path else None
    wam_action_critic_preloaded = (
        ActionWAMCritic(wam_action_model_path) if wam_action_model_path else None
    )
    visual_critic_preloaded = (
        VisualWAMCritic(visual_model_path) if visual_model_path else None
    )
    for critic_name, critic in (
        ("state WAM", wam_critic_preloaded),
        ("action WAM", wam_action_critic_preloaded),
        ("visual WAM", visual_critic_preloaded),
    ):
        if critic is not None and getattr(critic, "legacy_transport_labels", False):
            print(
                f">>> WARNING: {critic_name} was trained with legacy attachment-era "
                "transport labels; safe/slot scores remain available, but its "
                "transport_ready score is shadow-only until retrained on physical data"
            )

    import mujoco
    import types

    global pin
    import pinocchio as pin

    if "mediapy" not in sys.modules:
        mediapy_stub = types.ModuleType("mediapy")
        mediapy_stub.write_video = lambda *args, **kwargs: None
        sys.modules["mediapy"] = mediapy_stub

    from discoverse.robots import AirbotPlayIK, MMK2FIK
    from discoverse.robots_env.mmk2_base import MMK2Cfg
    from discoverse.task_base import MMK2TaskBase
    from discoverse.utils import get_body_tmat, step_func

    def sync_reset_pose(sim_node, action, mujoco_module, preserve_free_objects=False):
        """Keep robot qpos, controls, and sensors aligned before execution."""
        sim_node.mj_data.ctrl[:sim_node.njctrl] = action[:sim_node.njctrl]
        sim_node.target_control[:] = action[:sim_node.njctrl]
        if not preserve_free_objects:
            sim_node.mj_data.qpos[:sim_node.njq] = sim_node.init_joint_pose[:]
        sim_node.mj_data.qpos[9:10] = action[2:3]
        sim_node.mj_data.qpos[10:12] = action[3:5]
        sim_node.mj_data.qpos[12:18] = action[5:11]
        # Gripper controls are tendon positions in [0, 1].  Each tendon uses
        # coefficients +/-12.5 on two mirrored fingers, so a control of 1.0
        # corresponds to individual joint positions +/-0.04 m, not +/-1 m.
        left_finger_q = float(action[11]) / 25.0
        right_finger_q = float(action[18]) / 25.0
        sim_node.mj_data.qpos[18:20] = [left_finger_q, -left_finger_q]
        sim_node.mj_data.qpos[20:26] = action[12:18]
        sim_node.mj_data.qpos[26:28] = [right_finger_q, -right_finger_q]
        sim_node.mj_data.qvel[:] = 0.0
        mujoco_module.mj_forward(sim_node.mj_model, sim_node.mj_data)

    class StableAirbotPlayIK(AirbotPlayIK):
        def properIK(self, pos, ori, ref_q=None):
            return self.inverseKin(pos, mat3_mul(ori, self.arm_rot_mat), ref_q)

        def inverseKin(self, pos, ori, ref_q=None):
            assert len(pos) == 3 and ori.shape == (3, 3)
            pos = self.move_joint6_2_joint5(pos, ori)
            angle = [0.0] * 6
            candidates = []

            for i1 in [1, -1]:
                angle[0] = np.arctan2(i1 * pos[1], i1 * pos[0])
                c3 = (
                    pos[0] ** 2
                    + pos[1] ** 2
                    + (pos[2] - self.a1) ** 2
                    - self.a3 ** 2
                    - self.a4 ** 2
                ) / (2 * self.a3 * self.a4)
                if c3 > 1 or c3 < -1:
                    continue

                for i2 in [1, -1]:
                    s3 = i2 * np.sqrt(max(0.0, 1 - c3 ** 2))
                    angle[2] = np.arctan2(s3, c3)
                    k1 = self.a3 + self.a4 * c3
                    k2 = self.a4 * s3
                    reach_xy = np.sqrt(pos[0] ** 2 + pos[1] ** 2)
                    angle[1] = np.arctan2(
                        k1 * (pos[2] - self.a1) - i1 * k2 * reach_xy,
                        i1 * k1 * reach_xy + k2 * (pos[2] - self.a1),
                    )
                    rot = np.array([
                        [
                            np.cos(angle[0]) * np.cos(angle[1] + angle[2]),
                            -np.cos(angle[0]) * np.sin(angle[1] + angle[2]),
                            np.sin(angle[0]),
                        ],
                        [
                            np.sin(angle[0]) * np.cos(angle[1] + angle[2]),
                            -np.sin(angle[0]) * np.sin(angle[1] + angle[2]),
                            -np.cos(angle[0]),
                        ],
                        [np.sin(angle[1] + angle[2]), np.cos(angle[1] + angle[2]), 0.0],
                    ])
                    ori1 = mat3_mul(rot.T, ori)
                    for i5 in [1, -1]:
                        angle[3] = np.arctan2(i5 * ori1[2, 2], i5 * ori1[1, 2])
                        angle[4] = np.arctan2(
                            i5 * np.sqrt(ori1[2, 2] ** 2 + ori1[1, 2] ** 2),
                            ori1[0, 2],
                        )
                        angle[5] = np.arctan2(-i5 * ori1[0, 0], -i5 * ori1[0, 1])
                        js = self.add_bias(angle)
                        if np.all((js > self.arm_joint_range[0]) * (js < self.arm_joint_range[1])):
                            candidates.append(js)

            if not candidates:
                raise ValueError(f"Fail to solve inverse kinematics: pos={pos}, ori={ori}")

            if ref_q is not None:
                joint_dist = [
                    np.sum(np.abs(ref_q - js) / self.joint_range_scale)
                    for js in candidates
                ]
                return candidates[int(np.argmin(joint_dist))]
            return candidates[0]

    target_body_name = "box_yellow"
    # Simplified physical mode: each two-finger gripper stays mechanically
    # coupled and fully closed for the whole task.  The two arms provide the
    # opposing package clamp; there is no per-finger differential control.
    simple_closed_gripper_mode = True
    wall_pinch_mode = False
    grip_close = 0.0
    grip_initial = grip_close
    grip_open = grip_close
    release_open = 0.35
    head_pitch = -0.25
    clamp_duration = 0.8
    outward_grip_angle = np.deg2rad(0.0)
    # LEFT_GRIP_ROT/RIGHT_GRIP_ROT already contain the mirrored +/-90 degree
    # side-grasp yaw from DISCOVERSE's official grasp_pose.py.  This value is
    # only an *additional* local wrist turn, so start at zero rather than
    # applying the side-grasp yaw a second time.
    preferred_into_cabinet_turn_deg = 0.0
    # Keep the wrist housings outside the package and let the closed fingers
    # reach inward to the side walls.  This mirrors the useful geometry of a
    # real two-sided grasp: the forearms are visibly splayed while the contact
    # faces oppose one another across the box.
    side_grip_toe_in_deg = -12.0
    # Mirror-roll the two complete wrists about their longitudinal gripper
    # axes.  This moves the hand-eye camera housings from above the package to
    # the two outer sides, matching the requested reference pose.
    wrist_camera_roll_deg = 90.0
    # Final topology: both grippers independently clamp the robot-facing front
    # wall.  Their opening axes are parallel to world X, so each gripper has one
    # finger inside the open box and one outside.  A 50-degree outward fan keeps
    # the wrists/cameras outside the shelf while the long fingers descend onto
    # two separated portions of the same wall.
    front_wall_finger_tilt_deg = -60.0

    def rot_x(angle):
        c = float(np.cos(angle))
        s = float(np.sin(angle))
        return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])

    def rot_y(angle):
        c = float(np.cos(angle))
        s = float(np.sin(angle))
        return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])

    def rot_z(angle):
        c = float(np.cos(angle))
        s = float(np.sin(angle))
        return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])

    def make_front_wall_grip_rotations(turn_deg=0.0):
        del turn_deg
        rotations = []
        # Outside the shelf, angle the long fingers down and toward the robot.
        # The opening axis is world Y, so each hand straddles one side wall.
        tilt = np.deg2rad(20.0)
        for arm in ("l", "r"):
            finger_axis_world = np.array(
                [np.sin(tilt), 0.0, np.cos(tilt)], dtype=float
            )
            opening_axis_world = np.array([0.0, 1.0, 0.0], dtype=float)
            palm_axis_world = np.cross(finger_axis_world, opening_axis_world)
            endpoint_world_rot = np.column_stack(
                (finger_axis_world, opening_axis_world, palm_axis_world)
            )
            arm_base_tmat = (
                MMK2FIK.TMat_chest2lft_base
                if arm == "l"
                else MMK2FIK.TMat_chest2rgt_base
            )
            action_rot = MMK2FIK.action_rot["pick"][arm]
            rotations.append(
                mat3_mul(
                    action_rot.T,
                    mat3_mul(arm_base_tmat[:3, :3].T, endpoint_world_rot),
                )
            )
        return rotations[0], rotations[1]

    def make_grip_rotations(turn_deg, toe_in_deg=None):
        """Mirrored, wrist-outside side-wall clamp orientation.

        Local -X runs from each wrist toward its fingertips.  Giving endpoint
        +X an outward Y component therefore makes the fingers point inward,
        while the wrist/camera housings remain clear of the package corners.
        The projected opening axis keeps the closed finger pads facing the
        package side wall instead of presenting an edge to it.
        """
        rotations = []
        # Search only the vertical pitch.  The horizontal toe-in is fixed and
        # mirrored so left/right always retain the same useful grasp geometry.
        pitch = np.deg2rad(float(turn_deg))
        toe_in = np.deg2rad(
            side_grip_toe_in_deg if toe_in_deg is None else float(toe_in_deg)
        )
        for arm in ("l", "r"):
            outward_sign = 1.0 if arm == "l" else -1.0
            finger_axis_world = np.array(
                [
                    np.cos(pitch) * np.cos(toe_in),
                    outward_sign * np.cos(pitch) * np.sin(toe_in),
                    np.sin(pitch),
                ],
                dtype=float,
            )
            # Project the side-wall normal into the plane perpendicular to the
            # finger axis, producing a true rotation matrix even with toe-in.
            opening_axis_world = np.array([0.0, 1.0, 0.0], dtype=float)
            opening_axis_world -= (
                np.dot(opening_axis_world, finger_axis_world) * finger_axis_world
            )
            opening_axis_world /= np.linalg.norm(opening_axis_world)
            palm_axis_world = np.cross(finger_axis_world, opening_axis_world)
            palm_axis_world /= np.linalg.norm(palm_axis_world)
            camera_roll = np.deg2rad(
                -wrist_camera_roll_deg if arm == "l" else wrist_camera_roll_deg
            )
            unrolled_opening = opening_axis_world.copy()
            unrolled_palm = palm_axis_world.copy()
            opening_axis_world = (
                np.cos(camera_roll) * unrolled_opening
                + np.sin(camera_roll) * unrolled_palm
            )
            palm_axis_world = (
                -np.sin(camera_roll) * unrolled_opening
                + np.cos(camera_roll) * unrolled_palm
            )
            endpoint_world_rot = np.column_stack(
                (finger_axis_world, opening_axis_world, palm_axis_world)
            )
            arm_base_tmat = (
                MMK2FIK.TMat_chest2lft_base
                if arm == "l"
                else MMK2FIK.TMat_chest2rgt_base
            )
            action_rot = MMK2FIK.action_rot["pick"][arm]
            rotations.append(
                mat3_mul(
                    action_rot.T,
                    mat3_mul(arm_base_tmat[:3, :3].T, endpoint_world_rot),
                )
            )
        return rotations[0], rotations[1]

    left_grip_rot, right_grip_rot = make_grip_rotations(preferred_into_cabinet_turn_deg)

    class MyAlgorithmNode(MMK2TaskBase):
        def __init__(self, config):
            self._arm_ik_solver = None
            super().__init__(config)
            self._arm_ik_solver = StableAirbotPlayIK()
            if "head_cam" in self.camera_names:
                self.cam_id = self.camera_names.index("head_cam")
                self.config.obs_rgb_cam_id = [self.cam_id]
                print("render camera: head_cam", "id=", self.cam_id)
            elif self.camera_names:
                self.cam_id = 0
                self.config.obs_rgb_cam_id = [0]
                print("render camera:", self.camera_names[0], "id= 0")
            else:
                self.cam_id = -1
                self.config.obs_rgb_cam_id = [-1]
                print("render camera: free")

        def solveArmEndTarget(self, target_pose, arm_action, arm, q_ref, a_rot):
            rotation = mat3_mul(MMK2FIK.action_rot[arm_action][arm], a_rot)
            position = target_pose[:3, 3] if target_pose.shape == (4, 4) else target_pose
            chest_pos = np.array([0.02371, 0.0, 1.311 - self.tctr_slide[0]])
            arm_base_tmat = (
                MMK2FIK.TMat_chest2lft_base if arm == "l" else MMK2FIK.TMat_chest2rgt_base
            )
            arm_base_pos = chest_pos + arm_base_tmat[:3, 3]
            delta = np.asarray(position, dtype=float) - arm_base_pos
            rot = arm_base_tmat[:3, :3]
            position_local = np.array([
                rot[0, 0] * delta[0] + rot[1, 0] * delta[1] + rot[2, 0] * delta[2],
                rot[0, 1] * delta[0] + rot[1, 1] * delta[1] + rot[2, 1] * delta[2],
                rot[0, 2] * delta[0] + rot[1, 2] * delta[1] + rot[2, 2] * delta[2],
            ])
            return self._arm_ik_solver.properIK(position_local, rotation, q_ref)

        def setArmEndTarget(self, target_pose, arm_action, arm, q_ref, a_rot):
            rq = self.solveArmEndTarget(target_pose, arm_action, arm, q_ref, a_rot)
            if arm == "l":
                self.tctr_left_arm[:] = rq
                self.set_left_arm_new_target = True
            else:
                self.tctr_right_arm[:] = rq
                self.set_right_arm_new_target = True
            return rq

        def post_physics_step(self):
            pass

        def getChangedObjectPose(self):
            return {}

        def checkTerminated(self):
            return False

        def getObservation(self):
            return super().getObservation()

        def getPrivilegedObservation(self):
            return self.obs

        def getReward(self):
            return 0.0

        def check_success(self):
            if not all(hasattr(self, name) for name in ("box_start_z", "cabinet_front_x")):
                return False
            box_pos = get_body_tmat(self.mj_data, target_body_name)[:3, 3]
            outside_ok = box_pos[0] <= self.cabinet_front_x - 0.05
            not_dropped = box_pos[2] >= self.box_start_z - 0.03
            physical_transport_ok = bool(
                getattr(self, "physical_transport_completed", False)
            )
            print(
                "success check:",
                f"box_x={box_pos[0]:.3f}",
                f"front_x={self.cabinet_front_x:.3f}",
                f"box_z={box_pos[2]:.3f}",
                f"start_z={self.box_start_z:.3f}",
                f"physical_transport={physical_transport_ok}",
            )
            return bool(outside_ok and not_dropped and physical_transport_ok)

        def box_gripper_contact_sides(self):
            """Return which grippers currently contact the target package."""
            box_body_id = int(self.mj_model.body(target_body_name).id)
            sides = set()
            for contact_id in range(int(self.mj_data.ncon)):
                contact = self.mj_data.contact[contact_id]
                geom1 = int(contact.geom1)
                geom2 = int(contact.geom2)
                body1 = int(self.mj_model.geom_bodyid[geom1])
                body2 = int(self.mj_model.geom_bodyid[geom2])
                if body1 == box_body_id:
                    other_body = body2
                elif body2 == box_body_id:
                    other_body = body1
                else:
                    continue
                other_name = self.mj_model.body(other_body).name or ""
                if other_name.startswith("lft_finger"):
                    sides.add("left")
                elif other_name.startswith("rgt_finger"):
                    sides.add("right")
            return sides

        def box_gripper_contact_report(self):
            """Summarize package contacts by arm, force, and world position."""
            box_body_id = int(self.mj_model.body(target_body_name).id)
            report = {
                "left": {"force": 0.0, "positions": []},
                "right": {"force": 0.0, "positions": []},
            }
            contact_force = np.zeros(6, dtype=float)
            for contact_id in range(int(self.mj_data.ncon)):
                contact = self.mj_data.contact[contact_id]
                geom1, geom2 = int(contact.geom1), int(contact.geom2)
                body1 = int(self.mj_model.geom_bodyid[geom1])
                body2 = int(self.mj_model.geom_bodyid[geom2])
                if body1 == box_body_id:
                    other_body = body2
                elif body2 == box_body_id:
                    other_body = body1
                else:
                    continue
                other_name = self.mj_model.body(other_body).name or ""
                side = None
                if other_name.startswith("lft_finger"):
                    side = "left"
                elif other_name.startswith("rgt_finger"):
                    side = "right"
                if side is None:
                    continue
                contact_force[:] = 0.0
                mujoco.mj_contactForce(
                    self.mj_model, self.mj_data, contact_id, contact_force
                )
                report[side]["force"] += max(0.0, float(contact_force[0]))
                report[side]["positions"].append(
                    np.asarray(contact.pos, dtype=float).copy()
                )
            return report

        def print_gripper_geometry(self, label):
            """Print endpoint/finger collision geometry for wall-grasp calibration."""
            print(f">>> gripper geometry at {label}:")
            for arm, site_name, camera_site_name, prefix in (
                ("left", "lft_endpoint", "left_cam", "lft_finger"),
                ("right", "rgt_endpoint", "right_cam", "rgt_finger"),
            ):
                site = self.mj_data.site(site_name)
                camera_site = self.mj_data.site(camera_site_name)
                site_rot = np.asarray(site.xmat, dtype=float).reshape(3, 3)
                print(
                    f"    {arm} endpoint={np.array2string(np.asarray(site.xpos), precision=4)} "
                    f"camera={np.array2string(np.asarray(camera_site.xpos), precision=4)} "
                    f"axes_x/y/z={np.array2string(site_rot, precision=3)}"
                )
                for body_id in range(self.mj_model.nbody):
                    body_name = self.mj_model.body(body_id).name or ""
                    if not body_name.startswith(prefix):
                        continue
                    geom_start = int(self.mj_model.body_geomadr[body_id])
                    geom_num = int(self.mj_model.body_geomnum[body_id])
                    geom_positions = [
                        np.asarray(self.mj_data.geom_xpos[g], dtype=float).copy()
                        for g in range(geom_start, geom_start + geom_num)
                    ]
                    print(
                        f"      {body_name}: body={np.array2string(np.asarray(self.mj_data.xpos[body_id]), precision=4)} "
                        f"geoms={[np.round(p, 4).tolist() for p in geom_positions]}"
                    )

        def finger_geom_centers(self, data=None):
            data = self.mj_data if data is None else data
            centers = {}
            for body_id in range(self.mj_model.nbody):
                body_name = self.mj_model.body(body_id).name or ""
                if not (
                    body_name.startswith("lft_finger")
                    or body_name.startswith("rgt_finger")
                ):
                    continue
                geom_start = int(self.mj_model.body_geomadr[body_id])
                geom_num = int(self.mj_model.body_geomnum[body_id])
                pad_geom_ids = [
                    geom_id
                    for geom_id in range(geom_start, geom_start + geom_num)
                    if "_pad_" in (self.mj_model.geom(geom_id).name or "")
                ]
                if pad_geom_ids:
                    centers[body_name] = np.mean(
                        np.asarray(data.geom_xpos[pad_geom_ids], dtype=float), axis=0
                    )
            return centers

        def wall_grasp_report(self, data=None):
            """Report contact force for each of the four individual fingers."""
            data = self.mj_data if data is None else data
            box_body_id = int(self.mj_model.body(target_body_name).id)
            names = (
                "lft_finger_left_link",
                "lft_finger_right_link",
                "rgt_finger_left_link",
                "rgt_finger_right_link",
            )
            forces = {name: 0.0 for name in names}
            positions = {name: [] for name in names}
            nonfinger_contacts = set()
            nonfinger_positions = {}
            tolerated_nonfinger_contacts = {"lft_arm_link6", "rgt_arm_link6"}
            contact_details = []
            contact_force = np.zeros(6, dtype=float)
            for contact_id in range(int(data.ncon)):
                contact = data.contact[contact_id]
                geom1, geom2 = int(contact.geom1), int(contact.geom2)
                body1 = int(self.mj_model.geom_bodyid[geom1])
                body2 = int(self.mj_model.geom_bodyid[geom2])
                if body1 == box_body_id:
                    other_body = body2
                elif body2 == box_body_id:
                    other_body = body1
                else:
                    continue
                other_name = self.mj_model.body(other_body).name or ""
                geom1_name = self.mj_model.geom(geom1).name or f"geom_{geom1}"
                geom2_name = self.mj_model.geom(geom2).name or f"geom_{geom2}"
                detail = {
                    "body": other_name,
                    "geom_pair": (geom1_name, geom2_name),
                    "position": np.asarray(contact.pos, dtype=float).copy(),
                    "distance": float(contact.dist),
                }
                if other_name in forces:
                    contact_force[:] = 0.0
                    mujoco.mj_contactForce(
                        self.mj_model, data, contact_id, contact_force
                    )
                    forces[other_name] += max(0.0, float(contact_force[0]))
                    positions[other_name].append(
                        np.asarray(contact.pos, dtype=float).copy()
                    )
                    detail["normal_force"] = max(0.0, float(contact_force[0]))
                    detail["tangent_force"] = float(
                        np.linalg.norm(contact_force[1:3])
                    )
                    detail["contact_normal"] = np.asarray(
                        contact.frame, dtype=float
                    ).reshape(3, 3)[0].copy()
                    detail["effective_friction"] = float(contact.friction[0])
                    contact_details.append(detail)
                elif other_name.startswith(("lft_", "rgt_")):
                    if other_name not in tolerated_nonfinger_contacts:
                        nonfinger_contacts.add(other_name)
                        nonfinger_positions.setdefault(other_name, []).append(
                            np.asarray(contact.pos, dtype=float).copy()
                        )
                    contact_details.append(detail)
            return {
                "forces": forces,
                "positions": positions,
                "nonfinger_contacts": nonfinger_contacts,
                "nonfinger_positions": nonfinger_positions,
                "contact_details": contact_details,
            }

    cfg = MMK2Cfg()
    cfg.mjcf_file_path = str(mjcf_path)
    cfg.use_gaussian_renderer = False
    visual_enabled = visual_dataset_dir is not None or visual_model_path is not None
    cfg.headless = headless
    cfg.enable_render = (not headless) or visual_enabled
    cfg.sync = not headless
    cfg.render_set = {
        "fps": 30,
        "width": 320 if visual_enabled and headless else 1280,
        "height": 240 if visual_enabled and headless else 720,
        "window_title": "DISCOVERSE dual-side grasp + collision-aware extraction",
    }
    cfg.obs_rgb_cam_id = [0] if visual_enabled else None
    cfg.obs_depth_cam_id = None
    cfg.init_state = MMK2Cfg.init_state.copy()
    cfg.init_state["base_position"] = [0.58, 0.715, 0.0]
    cfg.init_state["base_orientation"] = [1.0, 0.0, 0.0, 0.0]
    cfg.init_state["head_qpos"] = [0.0, head_pitch]
    # init_state values are raw finger-joint positions, while runtime controls
    # use the [0, 1] tendon coordinate.
    cfg.init_state["lft_gripper_qpos"] = [grip_initial / 25.0]
    cfg.init_state["rgt_gripper_qpos"] = [grip_initial / 25.0]

    sim_node = MyAlgorithmNode(cfg)
    obs = sim_node.reset()
    # Success is only armed after the package has been transported by MuJoCo
    # contacts.  Never infer a successful grasp merely from the box pose.
    sim_node.physical_transport_completed = False
    sim_node.physical_transport_verified = False
    box_body_id_physics = int(sim_node.mj_model.body(target_body_name).id)
    box_geom_start_physics = int(
        sim_node.mj_model.body_geomadr[box_body_id_physics]
    )
    box_geom_count_physics = int(
        sim_node.mj_model.body_geomnum[box_body_id_physics]
    )
    box_geom_ids_physics = np.arange(
        box_geom_start_physics,
        box_geom_start_physics + box_geom_count_physics,
        dtype=int,
    )
    nominal_box_mass_kg = 0.50
    sim_node.mj_model.body_mass[box_body_id_physics] = nominal_box_mass_kg
    # The included visual/collision asset places its body origin at the
    # package bottom.  Its stock inertial element was also at that origin,
    # which makes the free box rotate as if all mass were concentrated on the
    # floor.  Put the COM at the geometric mid-height for realistic transport.
    sim_node.mj_model.body_ipos[box_body_id_physics] = [0.0, 0.0, 0.095]
    # Approximate inertia of a 240 x 164 x 190 mm thin packaging carton/bin.
    half_dims = np.asarray([0.12, 0.082, 0.095], dtype=float)
    sim_node.mj_model.body_inertia[box_body_id_physics] = (
        nominal_box_mass_kg
        / 3.0
        * np.asarray(
            [
                half_dims[1] ** 2 + half_dims[2] ** 2,
                half_dims[0] ** 2 + half_dims[2] ** 2,
                half_dims[0] ** 2 + half_dims[1] ** 2,
            ]
        )
    )
    # Cardboard/contact-compliance proxy: permit a few millimetres of damped
    # compression instead of treating the visible wall as infinitely rigid.
    sim_node.mj_model.geom_solref[box_geom_ids_physics] = [0.015, 1.0]
    sim_node.mj_model.geom_solimp[box_geom_ids_physics] = [
        0.82, 0.95, 0.0025, 0.5, 2.0
    ]
    # Smooth plastic/carton bottom on a painted shelf.  Keep this separate
    # from the rubber finger pads (mu=1.2): the former must slide while the
    # latter must transmit the pulling force without an artificial weld.
    sim_node.mj_model.geom_friction[box_geom_ids_physics, 0] = 0.18
    # The stock MMK2 gripper actuator (kp=3, force +/-1) cannot hold the
    # fingers open after rotating the wrist for wall clamping.  Raise it to a
    # still-compliant level; contact feedback below stops closing as soon as
    # all four fingers engage, rather than relying on penetration.
    gripper_actuator_ids = []
    for actuator_name in ("lft_gripper", "rgt_gripper"):
        actuator_id = int(sim_node.mj_model.actuator(actuator_name).id)
        gripper_actuator_ids.append(actuator_id)
        sim_node.mj_model.actuator_gainprm[actuator_id, 0] = 30.0
        sim_node.mj_model.actuator_biasprm[actuator_id, 1] = -30.0
        # The tendon has mechanical advantage, so +/-4 actuator units already
        # produce useful pad loads.  Keeping this bounded avoids an unrealistically
        # rigid crush grip while still holding the fingers open against gravity.
        sim_node.mj_model.actuator_forcerange[actuator_id] = [-2.5, 2.5]
    action = sim_node.init_joint_ctrl.copy()
    sync_reset_pose(sim_node, action, mujoco)
    base_lock_x = float(cfg.init_state["base_position"][0])
    base_lock_y = float(cfg.init_state["base_position"][1])

    scene_rng = np.random.default_rng(int(scene_seed))
    scene_randomization = {
        "enabled": bool(randomize_scene),
        "seed": int(scene_seed),
        "box_dx": 0.0,
        "box_dy": 0.0,
        "box_yaw_deg": 0.0,
        "mass_scale": 1.0,
        "mass_kg": nominal_box_mass_kg,
        "friction_scale": 1.0,
        "friction_coefficient": 0.18,
        "target_dx_error": 0.0,
        "target_dz_error": 0.0,
    }
    if randomize_scene:
        box_body_id_random = int(sim_node.mj_model.body(target_body_name).id)
        box_joint_id_random = int(sim_node.mj_model.body_jntadr[box_body_id_random])
        box_qpos_adr_random = int(
            sim_node.mj_model.jnt_qposadr[box_joint_id_random]
        )
        scene_randomization.update({
            "box_dx": 0.0,
            "box_dy": 0.0,
            "box_yaw_deg": 0.0,
            "mass_kg": float(scene_rng.uniform(0.35, 0.80)),
            "friction_coefficient": float(scene_rng.uniform(0.15, 0.25)),
            "target_dx_error": 0.0,
            "target_dz_error": 0.0,
        })
        sim_node.mj_data.qpos[box_qpos_adr_random] += scene_randomization["box_dx"]
        sim_node.mj_data.qpos[box_qpos_adr_random + 1] += scene_randomization["box_dy"]
        yaw = np.deg2rad(scene_randomization["box_yaw_deg"])
        # MuJoCo free-joint quaternion order is w, x, y, z.
        sim_node.mj_data.qpos[box_qpos_adr_random + 3:box_qpos_adr_random + 7] = [
            np.cos(0.5 * yaw), 0.0, 0.0, np.sin(0.5 * yaw)
        ]
        scene_randomization["mass_scale"] = (
            scene_randomization["mass_kg"] / nominal_box_mass_kg
        )
        scene_randomization["friction_scale"] = (
            scene_randomization["friction_coefficient"] / 0.18
        )
        sim_node.mj_model.body_mass[box_body_id_random] = scene_randomization["mass_kg"]
        sim_node.mj_model.body_inertia[box_body_id_random] = (
            scene_randomization["mass_kg"]
            / nominal_box_mass_kg
            * sim_node.mj_model.body_inertia[box_body_id_random]
        )
        geom_start = int(sim_node.mj_model.body_geomadr[box_body_id_random])
        geom_num = int(sim_node.mj_model.body_geomnum[box_body_id_random])
        sim_node.mj_model.geom_friction[
            geom_start:geom_start + geom_num, 0
        ] = scene_randomization["friction_coefficient"]
        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
        print(
            ">>> randomized scene:",
            ", ".join(
                f"{key}={value:.4f}" if isinstance(value, float) else f"{key}={value}"
                for key, value in scene_randomization.items()
            ),
        )

    tmat_box = get_body_tmat(sim_node.mj_data, target_body_name)
    box_center = tmat_box[:3, 3].copy()
    side_axis = tmat_box[:3, 1].copy()
    side_axis[2] = 0.0
    if np.linalg.norm(side_axis) < 1e-6:
        side_axis = np.array([0.0, 1.0, 0.0])
    side_axis /= np.linalg.norm(side_axis)
    box_half_width_y = get_box_half_extent_y(sim_node.mj_model, target_body_name)
    cabinet_front_x = float(box_center[0] - 0.15)
    planned_slide = float(np.clip(1.22 - 1.08 * box_center[2], 0.0, 0.08))

    sim_node.box_start_z = float(box_center[2])
    sim_node.box_start_pos = np.asarray(box_center, dtype=float).copy()
    sim_node.cabinet_front_x = cabinet_front_x
    sim_node.tctr_head[1] = head_pitch
    sim_node.tctr_lft_gripper[:] = grip_initial
    sim_node.tctr_rgt_gripper[:] = grip_initial
    action[:] = sim_node.target_control[:]
    sync_reset_pose(sim_node, action, mujoco, preserve_free_objects=randomize_scene)

    targets = compute_dual_box_pick_targets(
        box_center=box_center,
        cabinet_front_x=cabinet_front_x,
        box_half_width_y=box_half_width_y,
        grasp_clearance=-0.016,
        side_axis=side_axis,
    )
    if randomize_scene:
        # Model bounded perception/calibration error. Candidate branch planning
        # can recover it using real MuJoCo feedback instead of privileged truth.
        for target_name in (
            "wall_slot_front_left", "wall_slot_front_right",
            "wall_slot_left", "wall_slot_right",
        ):
            targets[target_name] = np.asarray(targets[target_name], dtype=float).copy()
            targets[target_name][0] += scene_randomization["target_dx_error"]
            targets[target_name][2] += scene_randomization["target_dz_error"]

    grip_turn_candidates = (0.0,)
    selected_left_grip_turn_deg = preferred_into_cabinet_turn_deg
    selected_right_grip_turn_deg = preferred_into_cabinet_turn_deg

    def world_to_base(point_world):
        base_tmat = get_body_tmat(sim_node.mj_data, "mmk2")
        base_rot = base_tmat[:3, :3]
        base_pos = base_tmat[:3, 3]
        return base_rot.T @ (np.asarray(point_world, dtype=float) - base_pos)
    def solve_world_pair_with_turn_search(
        left_world, right_world, left_ref, right_ref, stage_name="dual target"
    ):
        nonlocal left_grip_rot, right_grip_rot
        nonlocal selected_left_grip_turn_deg, selected_right_grip_turn_deg
        left_base = world_to_base(left_world)
        right_base = world_to_base(right_world)

        def arm_solutions(base_target, arm, q_ref, selected_turn):
            solutions = []
            last_error = None
            ordered_turns = sorted(
                grip_turn_candidates,
                key=lambda deg: (
                    abs(float(deg) - float(selected_turn)),
                    -abs(float(deg)),
                ),
            )
            for turn_deg in ordered_turns:
                cand_left_rot, cand_right_rot = make_grip_rotations(turn_deg)
                candidate_rot = cand_left_rot if arm == "l" else cand_right_rot
                try:
                    q = sim_node.solveArmEndTarget(
                        base_target, sim_node.arm_action, arm, q_ref, candidate_rot
                    )
                except ValueError as exc:
                    # A deep front-wall descent can leave the current analytic
                    # elbow branch while another valid branch still exists.
                    # Retry without the continuity preference; paired Cartesian
                    # interpolation below will still reject collisions/jumps.
                    try:
                        q = sim_node.solveArmEndTarget(
                            base_target, sim_node.arm_action, arm, None, candidate_rot
                        )
                    except ValueError:
                        last_error = exc
                        continue
                solutions.append(
                    (float(turn_deg), np.asarray(q, dtype=float), candidate_rot)
                )
            return solutions, last_error

        left_solutions, left_error = arm_solutions(
            left_base, "l", left_ref, selected_left_grip_turn_deg
        )
        right_solutions, right_error = arm_solutions(
            right_base, "r", right_ref, selected_right_grip_turn_deg
        )
        if not left_solutions or not right_solutions:
            failed_sides = []
            if not left_solutions:
                failed_sides.append("left")
            if not right_solutions:
                failed_sides.append("right")
            last_error = left_error if not left_solutions else right_error
            raise ValueError(
                f"{stage_name}: IK has no solution for {', '.join(failed_sides)} arm; "
                f"left_target={np.round(np.asarray(left_world), 4)}, "
                f"right_target={np.round(np.asarray(right_world), 4)}, "
                f"wrist turns={grip_turn_candidates}"
            ) from last_error

        # The two arms are not exact mirror images in their analytic IK branches.
        # Permit separate wrist turns, preferring a symmetric/continuous pair.
        left_choice, right_choice = min(
            ((left, right) for left in left_solutions for right in right_solutions),
            key=lambda pair: (
                abs(pair[0][0] - pair[1][0]),
                abs(pair[0][0] - selected_left_grip_turn_deg)
                + abs(pair[1][0] - selected_right_grip_turn_deg),
                abs(pair[0][0] - preferred_into_cabinet_turn_deg)
                + abs(pair[1][0] - preferred_into_cabinet_turn_deg),
            ),
        )
        selected_left_grip_turn_deg, left_q, left_grip_rot = left_choice
        selected_right_grip_turn_deg, right_q, right_grip_rot = right_choice
        if "alpha=" not in stage_name:
            print(
                f">>> {stage_name}: selected wrist turns "
                f"left={selected_left_grip_turn_deg:.1f}deg, "
                f"right={selected_right_grip_turn_deg:.1f}deg"
            )
        return left_q, right_q

    try:
        left_start_q, right_start_q = solve_world_pair_with_turn_search(
            targets["outside_left"],
            targets["outside_right"],
            action[5:11].copy(),
            action[12:18].copy(),
            stage_name="initial outside",
        )
        action[5:11] = np.asarray(left_start_q, dtype=float)
        action[12:18] = np.asarray(right_start_q, dtype=float)
        action[2] = 0.0
        action[3:5] = [0.0, head_pitch]
        action[11] = grip_initial
        action[18] = grip_initial
        sync_reset_pose(sim_node, action, mujoco, preserve_free_objects=randomize_scene)
        print(
            ">>> initial arms snapped to outside grasp-ready pose:",
            f"turns=({selected_left_grip_turn_deg:.1f}, "
            f"{selected_right_grip_turn_deg:.1f})deg",
            "left=", np.array2string(action[5:11], precision=3),
            "right=", np.array2string(action[12:18], precision=3),
        )
    except ValueError as exc:
        print(f">>> initial outside pose IK failed; using default arm pose: {exc}")
    obstacles = build_cabinet_obstacles(box_center)

    if not Path(urdf_path).exists():
        raise FileNotFoundError(f"URDF file does not exist: {urdf_path}")
    planner_model = pin.buildModelFromUrdf(str(urdf_path))
    planner_data = planner_model.createData()
    active_q_indices, active_v_indices = joint_indices(planner_model, ACTIVE_JOINT_NAMES)

    def update_joint_move_ratio():
        dif = np.abs(action - sim_node.target_control)
        sim_node.joint_move_ratio = dif / (np.max(dif) + 1e-6)
        sim_node.joint_move_ratio[2] *= 0.35
        sim_node.joint_move_ratio[5:11] *= 0.45
        sim_node.joint_move_ratio[12:18] *= 0.45

    def solve_world_pair(left_world, right_world, left_ref, right_ref, stage_name="dual target"):
        return solve_world_pair_with_turn_search(
            left_world, right_world, left_ref, right_ref, stage_name=stage_name
        )

    def solve_world_pair_relaxed(
        left_world,
        right_world,
        left_ref,
        right_ref,
        previous_offsets=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        stage_name="transport",
        max_orientation_relax_deg=8.0,
    ):
        """Solve fixed XYZ targets while allowing small wrist rotations.

        This is used only after the box is clamped.  The left/right Cartesian
        targets remain rigidly translated together; only each wrist orientation
        may deviate slightly from its nominal grasp orientation.
        """
        left_base = world_to_base(left_world)
        right_base = world_to_base(right_world)

        def solve_one(base_target, arm, q_ref, nominal_rot, previous_offset):
            last_error = None
            for candidate_rot, offset in relaxed_grip_rotation_candidates(
                nominal_rot,
                previous_offset_deg=previous_offset,
                max_angle_deg=max_orientation_relax_deg,
                step_deg=2.0,
            ):
                try:
                    q = sim_node.solveArmEndTarget(
                        base_target, sim_node.arm_action, arm, q_ref, candidate_rot
                    )
                    return np.asarray(q, dtype=float), offset
                except ValueError as exc:
                    last_error = exc
            side = "left" if arm == "l" else "right"
            raise ValueError(
                f"{stage_name}: {side} arm IK failed even with "
                f"±{max_orientation_relax_deg:.1f} deg wrist relaxation; "
                f"target={np.round(np.asarray(base_target)[:3], 4)}"
            ) from last_error

        left_q, left_offset = solve_one(
            left_base, "l", left_ref, left_grip_rot, previous_offsets[0]
        )
        right_q, right_offset = solve_one(
            right_base, "r", right_ref, right_grip_rot, previous_offsets[1]
        )
        return left_q, right_q, (left_offset, right_offset)

    def full_config_from_arms(left_q, right_q):
        q_full = make_full_configuration(
            planner_model, cfg.init_state["base_position"], planned_slide
        )
        q_full[active_q_indices[:6]] = left_q
        q_full[active_q_indices[6:]] = right_q
        return q_full

    def plan_rrt_stage(q_current_full, left_target, right_target, stage_name):
        left_ref = q_current_full[active_q_indices[:6]].copy()
        right_ref = q_current_full[active_q_indices[6:]].copy()
        left_goal, right_goal = solve_world_pair(
            left_target, right_target, left_ref, right_ref, stage_name=stage_name
        )
        q_goal_full = full_config_from_arms(left_goal, right_goal)
        if in_collision(planner_model, planner_data, q_goal_full, obstacles):
            raise RuntimeError(f"{stage_name}: IK goal is in cabinet collision")

        q_start_active = extract_active_config(q_current_full, active_q_indices)
        q_goal_active = extract_active_config(q_goal_full, active_q_indices)
        segment = rrt_plan_active(
            planner_model,
            planner_data,
            q_current_full,
            active_q_indices,
            q_start_active,
            q_goal_active,
            obstacles,
            max_iter=9000,
            step_size=0.10,
            goal_sample_rate=0.30,
        )
        segment = smooth_path_active(
            planner_model,
            planner_data,
            q_current_full,
            active_q_indices,
            segment,
            obstacles,
            attempts=60,
        )
        segment = interpolate_active_path(segment, max_step=0.035)
        print(f"planned {stage_name}: {len(segment)} joint samples")
        return q_goal_full, segment

    def plan_synchronized_pair_stage(
        q_current_full,
        left_start,
        right_start,
        left_goal,
        right_goal,
        stage_name,
        cartesian_step=0.006,
    ):
        """Move both end-effectors through the same Cartesian progress alpha.

        RRT is appropriate for reaching the cabinet, but not for squeezing: an
        RRT path may move one arm almost completely before moving the other.
        Here every path sample advances both arms by the same fraction toward
        the package center.
        """
        left_start = np.asarray(left_start, dtype=float)
        right_start = np.asarray(right_start, dtype=float)
        left_delta = np.asarray(left_goal, dtype=float) - left_start
        right_delta = np.asarray(right_goal, dtype=float) - right_start
        distance = max(float(np.linalg.norm(left_delta)), float(np.linalg.norm(right_delta)))
        samples = max(2, int(math.ceil(distance / cartesian_step)) + 1)
        q_prev = q_current_full.copy()
        active_path = [extract_active_config(q_prev, active_q_indices)]

        for alpha in np.linspace(0.0, 1.0, samples)[1:]:
            left_target = left_start + alpha * left_delta
            right_target = right_start + alpha * right_delta
            left_ref = q_prev[active_q_indices[:6]].copy()
            right_ref = q_prev[active_q_indices[6:]].copy()
            left_q, right_q = solve_world_pair(
                left_target,
                right_target,
                left_ref,
                right_ref,
                stage_name=f"{stage_name} alpha={alpha:.2f}",
            )
            q_next = full_config_from_arms(left_q, right_q)
            if in_collision(planner_model, planner_data, q_next, obstacles):
                raise RuntimeError(
                    f"{stage_name}: synchronized pose collides at alpha={alpha:.2f}"
                )
            if edge_in_collision(
                planner_model, planner_data, q_prev, q_next, obstacles, step=0.035
            ):
                raise RuntimeError(
                    f"{stage_name}: synchronized edge collides at alpha={alpha:.2f}"
                )
            active_path.append(extract_active_config(q_next, active_q_indices))
            q_prev = q_next

        print(f"planned {stage_name}: {len(active_path)} synchronized samples")
        return q_prev, active_path

    def plan_rigid_transport_stage(
        q_current_full,
        left_start,
        right_start,
        left_goal,
        right_goal,
        stage_name,
        orientation_offsets=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        cartesian_step=0.015,
    ):
        left_delta = np.asarray(left_goal) - np.asarray(left_start)
        right_delta = np.asarray(right_goal) - np.asarray(right_start)
        if not np.allclose(left_delta, right_delta, atol=1e-9):
            raise RuntimeError(f"{stage_name}: left/right transport is not a rigid translation")

        distance = float(np.linalg.norm(left_delta))
        samples = max(2, int(math.ceil(distance / cartesian_step)) + 1)
        q_prev = q_current_full.copy()
        active_path = [extract_active_config(q_prev, active_q_indices)]

        for alpha in np.linspace(0.0, 1.0, samples)[1:]:
            left_target = np.asarray(left_start) + alpha * left_delta
            right_target = np.asarray(right_start) + alpha * right_delta
            left_ref = q_prev[active_q_indices[:6]].copy()
            right_ref = q_prev[active_q_indices[6:]].copy()
            previous_offsets = orientation_offsets
            left_q, right_q, orientation_offsets = solve_world_pair_relaxed(
                left_target,
                right_target,
                left_ref,
                right_ref,
                previous_offsets=previous_offsets,
                stage_name=stage_name,
            )
            if orientation_offsets != previous_offsets:
                print(
                    f"{stage_name} alpha={alpha:.2f}: wrist relax "
                    f"L={orientation_offsets[0]} deg, R={orientation_offsets[1]} deg"
                )
            q_next = full_config_from_arms(left_q, right_q)
            if in_collision(planner_model, planner_data, q_next, obstacles):
                raise RuntimeError(
                    f"{stage_name}: constrained grasp pose collides at alpha={alpha:.2f}"
                )
            if edge_in_collision(
                planner_model, planner_data, q_prev, q_next, obstacles, step=0.035
            ):
                raise RuntimeError(
                    f"{stage_name}: constrained transport edge collides at alpha={alpha:.2f}"
                )
            active_path.append(extract_active_config(q_next, active_q_indices))
            q_prev = q_next

        print(
            f"planned {stage_name}: {len(active_path)} constrained samples; "
            f"final wrist offsets L={orientation_offsets[0]} deg, "
            f"R={orientation_offsets[1]} deg"
        )
        return q_prev, active_path, orientation_offsets

    # Build one execution plan. The approach uses RRT; the grasped part uses
    # synchronized Cartesian waypoints so the two hands keep the same relative
    # geometry while carrying the box out of the cabinet.
    execution_steps = []
    try:
        q_current = full_config_from_arms(
            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
        )

        execution_steps.append(
            {
                "kind": "slide",
                "name": "slide_ready",
                "target": planned_slide,
                "speed": 8.0,
            }
        )

        approach_stages = [
            ("mouth", targets["mouth_left"], targets["mouth_right"]),
            ("inside_high", targets["inside_high_left"], targets["inside_high_right"]),
        ]
        for stage_name, left_target, right_target in approach_stages:
            q_current, active_path = plan_rrt_stage(
                q_current, left_target, right_target, stage_name
            )
            # The controller interpolates between samples; retaining every
            # fourth collision-checked point removes long visual pauses while
            # preserving the exact final waypoint.
            if len(active_path) > 2:
                active_path = active_path[::4] + [active_path[-1]]
            execution_steps.append(
                {
                    "kind": "joint_path",
                    "name": stage_name,
                    "path": active_path,
                    "grip": grip_initial,
                    # RRT intermediate samples may be time-limited, but the
                    # final sample must physically settle before the next
                    # Cartesian stage starts.
                    "require_final_reached": True,
                    "final_point_timeout": 1.5,
                    "position_tolerance": 0.12,
                    # The low-level arm controller commonly settles around
                    # 0.06-0.12 rad from the analytical IK target at the deep
                    # cabinet pose.  That is still a safe spread pose; let the
                    # following timed Cartesian squeeze correct it gradually.
                    "accept_timeout_error": 0.45,
                }
            )

        # First align laterally while staying at the high, reachable 12-degree
        # approach orientation.  Separating this motion prevents joint-space
        # wrist reorientation from dipping the broad link-6 housing through
        # the package rim.
        q_current, high_align_path = plan_synchronized_pair_stage(
            q_current,
            targets["inside_high_left"],
            targets["inside_high_right"],
            targets["wall_slot_front_left"],
            targets["wall_slot_front_right"],
            "wall_slot_high_alignment",
        )
        execution_steps.append(
            {
                "kind": "timed_joint_path",
                "name": "wall_slot_high_alignment",
                "path": high_align_path,
                "grip": grip_open,
                "duration": max(0.55, 0.10 * max(1, len(high_align_path) - 1)),
                "settle_duration": 0.35,
                "require_settle": True,
                "settle_error": 0.100,
                "settle_timeout": 2.5,
                "monitor_wall_safety": True,
                "stop_on_finger_contact": False,
            }
        )

        # The large mirrored toe-in requested for the final side grasp is not
        # analytically reachable at the cabinet mouth.  Once both wrists are
        # inside and high, search it again at the actual wall targets.  This
        # creates a staged wrist rotation: reachable 12 deg approach, then the
        # widest collision-clearing grasp orientation the robot can solve.
        approach_toe_deg = float(side_grip_toe_in_deg)
        grasp_toe_selected = approach_toe_deg
        grasp_orientation_found = False
        chosen_front_left_q = None
        chosen_front_right_q = None
        # Keep exactly the same outward-facing wrist orientation before and
        # after entering the shelf; closed grippers do not reorient near the
        # package.
        for candidate_toe in (approach_toe_deg,):
            candidate_left_rot = make_grip_rotations(
                selected_left_grip_turn_deg, candidate_toe
            )[0]
            candidate_right_rot = make_grip_rotations(
                selected_right_grip_turn_deg, candidate_toe
            )[1]
            try:
                left_ref = q_current[active_q_indices[:6]].copy()
                right_ref = q_current[active_q_indices[6:]].copy()
                for target_index, (left_target, right_target) in enumerate((
                    (targets["wall_slot_front_left"], targets["wall_slot_front_right"]),
                    (targets["wall_slot_left"], targets["wall_slot_right"]),
                )):
                    left_ref = np.asarray(
                        sim_node.solveArmEndTarget(
                            world_to_base(left_target),
                            sim_node.arm_action,
                            "l",
                            left_ref,
                            candidate_left_rot,
                        ),
                        dtype=float,
                    )
                    right_ref = np.asarray(
                        sim_node.solveArmEndTarget(
                            world_to_base(right_target),
                            sim_node.arm_action,
                            "r",
                            right_ref,
                            candidate_right_rot,
                        ),
                        dtype=float,
                    )
                    if target_index == 0:
                        candidate_front_left_q = left_ref.copy()
                        candidate_front_right_q = right_ref.copy()
            except ValueError:
                continue
            left_grip_rot = candidate_left_rot
            right_grip_rot = candidate_right_rot
            grasp_toe_selected = float(candidate_toe)
            chosen_front_left_q = candidate_front_left_q
            chosen_front_right_q = candidate_front_right_q
            grasp_orientation_found = True
            break
        if not grasp_orientation_found:
            raise ValueError("no reachable wrist-outside orientation at side walls")
        # Subsequent synchronized interpolation invokes the normal turn-search
        # solver, whose orientation factory reads this value.  Switch its
        # default only after the approach has been planned.
        side_grip_toe_in_deg = grasp_toe_selected
        print(
            ">>> staged side-grasp wrist orientation: "
            f"approach={approach_toe_deg:.1f}deg, "
            f"wall_grasp={grasp_toe_selected:.1f}deg"
        )

        # Reorient on the continuous IK branch found above.  Calling RRT here
        # can jump to a second valid elbow branch and make the wrist dip below
        # the rim even though both endpoints are the same.  Small direct joint
        # increments preserve the high wrist position and outward cameras.
        q_orientation_goal = full_config_from_arms(
            chosen_front_left_q, chosen_front_right_q
        )
        start_active = extract_active_config(q_current, active_q_indices)
        goal_active = extract_active_config(q_orientation_goal, active_q_indices)
        orientation_samples = max(
            2, int(math.ceil(float(np.max(np.abs(goal_active - start_active))) / 0.035)) + 1
        )
        orientation_path = [
            start_active + alpha * (goal_active - start_active)
            for alpha in np.linspace(0.0, 1.0, orientation_samples)
        ]
        q_current = q_orientation_goal
        print(
            f"planned wall_slot_front_alignment: {len(orientation_path)} "
            "continuous-branch joint samples"
        )
        execution_steps.append(
            {
                "kind": "joint_path",
                "name": "wall_slot_front_alignment",
                "path": orientation_path,
                "grip": grip_open,
                "require_final_reached": True,
                "final_point_timeout": 3.0,
                "position_tolerance": 0.030,
                "accept_timeout_error": 0.200,
            }
        )

        wall_insertion_stages = [
            (
                "wall_slot_insert",
                targets["wall_slot_front_left"],
                targets["wall_slot_front_right"],
                targets["wall_slot_left"],
                targets["wall_slot_right"],
            ),
        ]
        for stage_name, left_start, right_start, left_goal, right_goal in wall_insertion_stages:
            q_current, active_path = plan_synchronized_pair_stage(
                q_current,
                left_start,
                right_start,
                left_goal,
                right_goal,
                stage_name,
            )
            execution_steps.append(
                {
                    "kind": "timed_joint_path",
                    "name": stage_name,
                    "path": active_path,
                    "grip": grip_open,
                    # Both arms share the same normalized time alpha.  This
                    # keeps the squeeze visibly synchronized even when their
                    # low-level controllers have different steady-state error.
                    "duration": max(0.45, 0.10 * max(1, len(active_path) - 1)),
                    "settle_duration": 0.40,
                    "require_settle": stage_name == "wall_slot_insert",
                    "settle_error": 0.180,
                    "settle_timeout": 3.0,
                    # The closed pads approach real box side walls. Stop at
                    # the first palm/arm contact or appreciable box motion.
                    "monitor_wall_safety": stage_name != "wall_slot_insert",
                    # During vertical insertion, touching the top rim with a
                    # fingertip is expected; continue downward while the box
                    # remains stationary and no palm/arm contact occurs.
                    # Rim contact during the descent is expected.  Do not treat
                    # it as completion: continue until the pads are below the
                    # rim so they clamp the vertical face rather than pinching
                    # the upper lip.
                    "stop_on_finger_contact": False,
                }
            )

        execution_steps.append(
            {
                "kind": "closed_pair_clamp",
                "name": "closed dual-side friction clamp",
                "timeout": 12.0,
            }
        )
        print(
            ">>> fast closed-gripper side-clamp plan ready; both outward-facing "
            "wrists keep the same orientation through shelf entry"
        )
    except Exception as exc:
        print(">>> box_pick planning failed; holding the same grasp window open")
        print(f">>> failure: {type(exc).__name__}: {exc}")
        execution_steps = [
            {"kind": "hold", "name": "planning failed - inspect scene", "duration": 1.0e9}
        ]

    step_index = 0
    path_index = 0
    step_enter_time = sim_node.mj_data.time
    point_enter_time = sim_node.mj_data.time
    current_step_name = None
    bilateral_contact_streak = 0
    four_finger_contact_streak = 0
    closed_pair_contact_streak = 0
    closed_pair_targets_world = None
    closed_pair_last_update = -1.0e9
    wall_align_target_active = None
    wall_align_target_world = None
    wall_align_last_update = -1.0e9
    wall_alignment_streak = 0
    wall_align_pending = False
    wall_align_pending_since = -1.0e9
    clamp_seat_targets_world = None
    clamp_seat_last_update = -1.0e9
    transport_contact_loss_streak = 0
    physical_grasp_validated = False
    final_front_wall_mode = False
    box_body_id = int(sim_node.mj_model.body(target_body_name).id)
    box_joint_id = int(sim_node.mj_model.body_jntadr[box_body_id])
    box_qpos_adr = int(sim_node.mj_model.jnt_qposadr[box_joint_id])
    box_dof_adr = int(sim_node.mj_model.jnt_dofadr[box_joint_id])
    wam_recorder = WAMCriticRecorder(wam_dataset_path)
    wam_critic = wam_critic_preloaded
    wam_action_critic = wam_action_critic_preloaded
    visual_recorder = VisualWAMRecorder(visual_dataset_dir)
    visual_critic = visual_critic_preloaded
    wam_stage_ids = {}
    wam_last_sample_time = -1.0e9
    wam_last_shadow_time = -1.0e9
    visual_last_shadow_time = -1.0e9
    wam_samples_recorded = 0
    wam_dataset_flushed = False
    force_grip_targets = np.asarray([grip_close, grip_close], dtype=float)
    force_loop_last_time = float(sim_node.mj_data.time)
    force_settle_centers_world = None
    force_settle_last_center_time = -1.0e9
    force_settle_last_center_errors = np.zeros(2, dtype=float)
    force_settle_last_balance_updates = np.zeros(2, dtype=float)
    physical_grip_target_load = float(
        np.clip(
            2.3 * float(sim_node.mj_model.body_mass[box_body_id_physics]) * 9.81
            / max(0.35, float(sim_node.mj_model.geom_friction[box_geom_ids_physics[0], 0])),
            18.0,
            28.0,
        )
    )

    finger_force_actuators = {}
    finger_closing_sign = {}
    independent_finger_mode = False
    independent_force_control_enabled = False
    independent_force_last_time = float(sim_node.mj_data.time)

    def enable_differential_finger_compliance():
        """Release rigid finger coupling and hand force control to four pads."""
        nonlocal independent_finger_mode, independent_force_control_enabled
        nonlocal independent_force_last_time
        if independent_finger_mode:
            return
        finger_joint_ids = {
            int(sim_node.mj_model.joint("lft_finger_left_joint").id),
            int(sim_node.mj_model.joint("lft_finger_right_joint").id),
            int(sim_node.mj_model.joint("rgt_finger_left_joint").id),
            int(sim_node.mj_model.joint("rgt_finger_right_joint").id),
        }
        for equality_id in range(sim_node.mj_model.neq):
            if (
                int(sim_node.mj_model.eq_obj1id[equality_id]) in finger_joint_ids
                or int(sim_node.mj_model.eq_obj2id[equality_id]) in finger_joint_ids
            ):
                sim_node.mj_data.eq_active[equality_id] = False
        for actuator_id in gripper_actuator_ids:
            sim_node.mj_model.actuator_gainprm[actuator_id, 0] = 0.0
            sim_node.mj_model.actuator_biasprm[actuator_id, 1] = 0.0
        independent_finger_mode = True
        independent_force_control_enabled = True
        independent_force_last_time = float(sim_node.mj_data.time)
        print(">>> differential finger compliance enabled; rigid finger coupling released")

    def update_independent_finger_forces(report, now):
        """Bounded per-pad force feedback; no pose attachment is used."""
        nonlocal independent_force_last_time
        dt = float(np.clip(now - independent_force_last_time, 0.0, 0.03))
        independent_force_last_time = float(now)
        target_per_pad = 0.5 * physical_grip_target_load
        commands = {}
        for name, actuator_id in finger_force_actuators.items():
            measured = float(report["forces"][name])
            error = target_per_pad - measured
            magnitude = float(
                np.clip(
                    target_per_pad + 0.20 * error,
                    1.5,
                    12.0,
                )
            )
            sim_node.mj_data.ctrl[actuator_id] = finger_closing_sign[name] * magnitude
            commands[name] = magnitude
        return commands

    def update_force_grip_targets(report, now):
        """Compliant per-arm grip-force loop; 0 closes and 1 opens."""
        nonlocal force_loop_last_time
        dt = float(np.clip(now - force_loop_last_time, 0.0, 0.03))
        force_loop_last_time = float(now)
        arm_names = (
            ("lft_finger_left_link", "lft_finger_right_link"),
            ("rgt_finger_left_link", "rgt_finger_right_link"),
        )
        target_load = physical_grip_target_load
        for arm_index, names in enumerate(arm_names):
            loads = [float(report["forces"][name]) for name in names]
            total_load = sum(loads)
            if min(loads) < 0.20:
                rate = -0.12
            else:
                # Positive error opens the gripper and releases wall pressure.
                rate = float(np.clip(0.018 * (total_load - target_load), -0.10, 0.28))
            force_grip_targets[arm_index] = float(
                np.clip(force_grip_targets[arm_index] + rate * dt, 0.04, 0.92)
            )
        return force_grip_targets.copy()

    def wall_slot_metrics(data=None):
        """Return rim margins and true 3-D readiness of both open slots."""
        data = sim_node.mj_data if data is None else data
        box_now = np.asarray(data.xpos[box_body_id], dtype=float)
        rim_z = float(box_now[2] + DEFAULT_BOX_HEIGHT)
        centers = sim_node.finger_geom_centers(data)
        arm_names = (
            ("lft_finger_left_link", "lft_finger_right_link"),
            ("rgt_finger_left_link", "rgt_finger_right_link"),
        )
        margins = []
        for names in arm_names:
            projections = sorted(float(centers[name][2]) for name in names)
            margins.append(min(rim_z - projections[0], projections[1] - rim_z))
        left_endpoint = np.asarray(data.site("lft_endpoint").xpos, dtype=float)
        right_endpoint = np.asarray(data.site("rgt_endpoint").xpos, dtype=float)
        desired_x = float(box_now[0] - 0.045)
        desired_y = np.asarray(
            [box_now[1] + box_half_width_y, box_now[1] - box_half_width_y],
            dtype=float,
        )
        endpoint_x_error = max(
            abs(float(left_endpoint[0]) - desired_x),
            abs(float(right_endpoint[0]) - desired_x),
        )
        endpoint_y_error = max(
            abs(float(left_endpoint[1]) - desired_y[0]),
            abs(float(right_endpoint[1]) - desired_y[1]),
        )
        slot_ready = bool(
            min(margins) >= 0.010
            and endpoint_x_error <= 0.070
            and endpoint_y_error <= 0.100
        )
        return np.asarray(margins, dtype=float), slot_ready

    def wam_feature_vector(
        step,
        now,
        report,
        data=None,
        control=None,
        stage_progress_override=None,
        grasp_validated_override=None,
    ):
        data = sim_node.mj_data if data is None else data
        control = action if control is None else np.asarray(control, dtype=float)
        stage_name = str(step.get("name", step.get("kind", "unknown")))
        if stage_name not in wam_stage_ids:
            wam_stage_ids[stage_name] = len(wam_stage_ids) + 1
        duration = float(step.get("duration", step.get("timeout", 1.0)))
        progress = float(np.clip((now - step_enter_time) / max(duration, 1.0e-6), 0.0, 1.0))
        if stage_progress_override is not None:
            progress = float(stage_progress_override)
        box_now = np.asarray(data.xpos[box_body_id], dtype=float)
        left_endpoint = np.asarray(data.site("lft_endpoint").xpos, dtype=float)
        right_endpoint = np.asarray(data.site("rgt_endpoint").xpos, dtype=float)
        centers = sim_node.finger_geom_centers(data)
        left_mid = 0.5 * (
            centers["lft_finger_left_link"] + centers["lft_finger_right_link"]
        )
        right_mid = 0.5 * (
            centers["rgt_finger_left_link"] + centers["rgt_finger_right_link"]
        )
        rim_z = float(box_now[2] + DEFAULT_BOX_HEIGHT)
        forces = list(report["forces"].values())
        return np.asarray(
            [
                wam_stage_ids[stage_name] / 16.0,
                progress,
                *(np.asarray(box_now) - np.asarray(sim_node.box_start_pos)),
                *(left_endpoint - np.asarray(box_now)),
                *(right_endpoint - np.asarray(box_now)),
                float(np.linalg.norm(np.asarray(data.qpos[12:18]) - control[5:11])),
                float(np.linalg.norm(np.asarray(data.qpos[20:26]) - control[12:18])),
                abs(float(data.qpos[18])) * 25.0,
                abs(float(data.qpos[26])) * 25.0,
                0.5 * float(control[11] + control[18]),
                abs(float(data.qpos[9]) - float(control[2])),
                float(left_mid[2] - rim_z),
                float(right_mid[2] - rim_z),
                float(np.linalg.norm(left_endpoint - right_endpoint)),
                float(
                    physical_grasp_validated or final_front_wall_mode
                    if grasp_validated_override is None
                    else grasp_validated_override
                ),
            ],
            dtype=np.float32,
        )

    def wam_observe(step, now, force=False):
        nonlocal wam_last_sample_time, wam_last_shadow_time
        nonlocal visual_last_shadow_time, wam_samples_recorded
        if (
            wam_dataset_path is None
            and wam_critic is None
            and visual_dataset_dir is None
            and visual_critic is None
        ):
            return
        if not force and now - wam_last_sample_time < 0.20:
            return
        report = sim_node.wall_grasp_report()
        features = wam_feature_vector(step, now, report)
        forces = np.asarray(list(report["forces"].values()), dtype=float)
        safe = not bool(report["nonfinger_contacts"])
        all_four = bool(np.all(forces >= 0.10))
        bilateral = bool(
            forces[0] + forces[1] >= 0.20 and forces[2] + forces[3] >= 0.20
        )
        tracking_ok = bool(features[11] < 0.35 and features[12] < 0.35)
        grasp_validated = bool(physical_grasp_validated or final_front_wall_mode)
        # `transport_ready` means a real contact grasp has been validated.
        # Merely observing four instantaneous contacts is not sufficient: it
        # was the source of false-positive labels when transport used a
        # kinematic attachment in older datasets.
        transport_ready = bool(
            safe and tracking_ok and grasp_validated
            and sim_node.physical_transport_verified
        )
        _, slot_ready = wall_slot_metrics()
        wam_recorder.add(
            features,
            (safe, all_four, transport_ready, slot_ready),
            {
                "time": round(float(now), 4),
                "stage": str(step.get("name", step.get("kind", "unknown"))),
                "source": "mujoco",
            },
        )
        wam_samples_recorded += 1
        visual_image = None
        if visual_enabled and sim_node.cam_id in sim_node.img_rgb_obs_s:
            visual_image = sim_node.img_rgb_obs_s[sim_node.cam_id]
        visual_labels = (safe, all_four, transport_ready, slot_ready)
        visual_recorder.add(
            visual_image,
            features,
            visual_labels,
            {
                "time": round(float(now), 4),
                "stage": str(step.get("name", step.get("kind", "unknown"))),
                "scene_seed": int(scene_seed),
                "scene_randomization": scene_randomization,
            },
        )
        wam_last_sample_time = now
        if wam_critic is not None and (force or now - wam_last_shadow_time >= 1.0):
            scores = wam_critic.predict(features)
            print(
                ">>> WAM shadow:",
                f"stage={step.get('name', step.get('kind'))}",
                f"safe={scores['safe']:.3f}",
                f"four_contact={scores['four_finger_contact']:.3f}",
                f"transport_ready={scores['transport_ready']:.3f}",
                f"slot_ready={scores.get('slot_ready', float('nan')):.3f}",
            )
            wam_last_shadow_time = now
        if visual_critic is not None and visual_image is not None and (
            force or now - visual_last_shadow_time >= 1.0
        ):
            visual_scores = visual_critic.predict(visual_image, features)
            print(
                ">>> Visual WAM shadow:",
                f"stage={step.get('name', step.get('kind'))}",
                f"safe={visual_scores['safe']:.3f}",
                f"transport_ready={visual_scores['transport_ready']:.3f}",
                f"slot_ready={visual_scores['slot_ready']:.3f}",
            )
            visual_last_shadow_time = now

    def plan_final_front_wall_regrasp():
        """Build a true two-point front-wall clamp after shelf extraction."""
        nonlocal left_grip_rot, right_grip_rot
        nonlocal selected_left_grip_turn_deg, selected_right_grip_turn_deg
        box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3].copy()
        grasp_x = float(box_now[0] - 0.040)
        box_top = float(box_now[2] + DEFAULT_BOX_HEIGHT)
        hover_z = box_top + 0.130
        clamp_z = box_top + 0.045
        left_wall_y = float(box_now[1] + box_half_width_y)
        right_wall_y = float(box_now[1] - box_half_width_y)
        left_hover = np.array([grasp_x, left_wall_y, hover_z])
        right_hover = np.array([grasp_x, right_wall_y, hover_z])
        left_clamp = np.array([grasp_x, left_wall_y, clamp_z])
        right_clamp = np.array([grasp_x, right_wall_y, clamp_z])

        left_grip_rot, right_grip_rot = make_front_wall_grip_rotations()
        selected_left_grip_turn_deg = 0.0
        selected_right_grip_turn_deg = 0.0

        def solve_front_pair(left_world, right_world, left_ref, right_ref, stage_name):
            try:
                left_q = sim_node.solveArmEndTarget(
                    world_to_base(left_world),
                    sim_node.arm_action,
                    "l",
                    left_ref,
                    left_grip_rot,
                )
                right_q = sim_node.solveArmEndTarget(
                    world_to_base(right_world),
                    sim_node.arm_action,
                    "r",
                    right_ref,
                    right_grip_rot,
                )
            except ValueError as exc:
                raise ValueError(
                    f"{stage_name}: true front-wall pose is unreachable; "
                    f"left={np.round(left_world, 4)}, right={np.round(right_world, 4)}"
                ) from exc
            return np.asarray(left_q, dtype=float), np.asarray(right_q, dtype=float)

        q_actual = full_config_from_arms(
            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
        )
        left_hover_q, right_hover_q = solve_front_pair(
            left_hover,
            right_hover,
            q_actual[active_q_indices[:6]],
            q_actual[active_q_indices[6:]],
            stage_name="front-wall hover",
        )
        q_hover = full_config_from_arms(left_hover_q, right_hover_q)
        left_clamp_q, right_clamp_q = solve_front_pair(
            left_clamp,
            right_clamp,
            left_hover_q,
            right_hover_q,
            stage_name="front-wall descend",
        )
        q_clamp = full_config_from_arms(left_clamp_q, right_clamp_q)
        hover_path = interpolate_active_path(
            [
                extract_active_config(q_actual, active_q_indices),
                extract_active_config(q_hover, active_q_indices),
            ],
            max_step=0.045,
        )
        descend_path = interpolate_active_path(
            [
                extract_active_config(q_hover, active_q_indices),
                extract_active_config(q_clamp, active_q_indices),
            ],
            max_step=0.035,
        )
        print(
            ">>> planned final true front-wall regrasp:",
            f"hover={len(hover_path)} samples, descend={len(descend_path)} samples",
        )
        return [
            {
                "kind": "regrasp_joint_path",
                "name": "release temporary grasp and move above front wall",
                "path": hover_path,
                "duration": 2.6,
                "settle_timeout": 5.0,
            },
            {
                "kind": "regrasp_joint_path",
                "name": "insert one finger inside and one outside",
                "path": descend_path,
                "duration": 2.2,
                "settle_timeout": 5.0,
            },
            {
                "kind": "final_front_wall_align",
                "name": "verify front wall inside both finger slots",
                "timeout": 2.0,
                "tolerance": 0.012,
            },
            {
                "kind": "final_front_wall_clamp",
                "name": "clamp front wall at two points",
                "duration": 1.0,
            },
            {
                "kind": "hold",
                "name": "hold final true wall grasp",
                "duration": float(hold_seconds),
            },
        ]

    def plan_transport_from_actual_grasp(preload_offset):
        """Replan transport from the measured bilateral-contact arm pose."""
        q_actual = full_config_from_arms(
            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
        )
        # Pinocchio's URDF root convention is not identical to the active
        # MuJoCo free-joint/base convention.  Its frame translations must not
        # be fed back through get_tmat_wrt_mmk2base as MuJoCo world points.
        # Read the actual endpoint sites directly from the running simulation.
        left_start = np.asarray(
            sim_node.mj_data.site("lft_endpoint").xpos, dtype=float
        ).copy()
        right_start = np.asarray(
            sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float
        ).copy()
        print(
            ">>> measured contact endpoints:",
            "left=", np.array2string(left_start, precision=4),
            "right=", np.array2string(right_start, precision=4),
        )

        lift_delta = np.array([0.0, 0.0, 0.030])
        mouth_delta = np.array([
            targets["transport_mouth_left"][0] - targets["grasp_left"][0],
            0.0,
            0.030,
        ])
        outside_delta = np.array([
            targets["transport_outside_left"][0] - targets["grasp_left"][0],
            0.0,
            0.030,
        ])
        left_lift, right_lift = left_start + lift_delta, right_start + lift_delta
        left_mouth, right_mouth = left_start + mouth_delta, right_start + mouth_delta
        left_outside = left_start + outside_delta
        right_outside = right_start + outside_delta
        transport_specs = [
            ("rigid_lift", left_start, right_start, left_lift, right_lift),
            ("rigid_to_mouth", left_lift, right_lift, left_mouth, right_mouth),
            ("rigid_outside", left_mouth, right_mouth, left_outside, right_outside),
        ]
        steps = []
        q_transport = q_actual
        offsets = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        for stage_name, left0, right0, left1, right1 in transport_specs:
            q_transport, active_path, offsets = plan_rigid_transport_stage(
                q_transport,
                left0,
                right0,
                left1,
                right1,
                stage_name,
                orientation_offsets=offsets,
            )
            steps.append(
                {
                    "kind": "timed_transport_path",
                    "name": stage_name,
                    "path": active_path,
                    "grip": grip_close,
                    "preload_offset": np.asarray(preload_offset, dtype=float).copy(),
                    "duration": max(1.5, 0.55 * max(1, len(active_path) - 1)),
                    "settle_duration": 0.6,
                }
            )
        steps.append(
            {"kind": "hold", "name": "hold outside cabinet", "duration": float(hold_seconds)}
        )
        return steps

    def plan_horizontal_transport_from_actual_grasp():
        """Plan only the horizontal extraction after the slide has lifted."""
        q_actual = full_config_from_arms(
            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
        )
        left_start = np.asarray(
            sim_node.mj_data.site("lft_endpoint").xpos, dtype=float
        ).copy()
        right_start = np.asarray(
            sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float
        ).copy()
        mouth_dx = float(
            targets["transport_mouth_left"][0] - targets["grasp_left"][0]
        )
        outside_dx = float(
            targets["transport_outside_left"][0] - targets["grasp_left"][0]
        )
        left_mouth = left_start + np.array([mouth_dx, 0.0, 0.0])
        right_mouth = right_start + np.array([mouth_dx, 0.0, 0.0])
        left_outside = left_start + np.array([outside_dx, 0.0, 0.0])
        right_outside = right_start + np.array([outside_dx, 0.0, 0.0])
        specs = [
            ("rigid_to_mouth", left_start, right_start, left_mouth, right_mouth),
            ("rigid_outside", left_mouth, right_mouth, left_outside, right_outside),
        ]
        steps = []
        q_transport = q_actual
        offsets = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        for stage_name, left0, right0, left1, right1 in specs:
            q_transport, active_path, offsets = plan_rigid_transport_stage(
                q_transport,
                left0,
                right0,
                left1,
                right1,
                stage_name,
                orientation_offsets=offsets,
            )
            steps.append(
                {
                    "kind": "timed_transport_path",
                    "name": stage_name,
                    "path": active_path,
                    "grip": grip_close,
                    "preload_offset": np.zeros(12, dtype=float),
                    "duration": max(1.5, 0.55 * max(1, len(active_path) - 1)),
                    "settle_duration": 0.6,
                }
            )
        steps.append(
            {"kind": "hold", "name": "hold outside cabinet", "duration": float(hold_seconds)}
        )
        return steps

    wam_branch_selection_done = False

    def branch_robot_environment_contacts(data):
        """Return arm contact pairs that are not the intended box contact."""
        box_id = box_body_id
        contact_pairs = set()
        for contact_id in range(int(data.ncon)):
            contact = data.contact[contact_id]
            body1 = int(sim_node.mj_model.geom_bodyid[int(contact.geom1)])
            body2 = int(sim_node.mj_model.geom_bodyid[int(contact.geom2)])
            name1 = sim_node.mj_model.body(body1).name or ""
            name2 = sim_node.mj_model.body(body2).name or ""
            arm1 = name1.startswith(("lft_", "rgt_"))
            arm2 = name2.startswith(("lft_", "rgt_"))
            if not (arm1 or arm2):
                continue
            if (body1 == box_id and "finger" in name2) or (
                body2 == box_id and "finger" in name1
            ):
                continue
            # Adjacent links within the same kinematic arm can be in benign
            # self contact in the stock model; the hard gate is for an arm
            # touching the cabinet, box with a non-finger link, or other arm.
            same_arm = (
                name1.startswith("lft_") and name2.startswith("lft_")
            ) or (
                name1.startswith("rgt_") and name2.startswith("rgt_")
            )
            if not same_arm:
                contact_pairs.add(tuple(sorted((name1, name2))))
        return contact_pairs

    def choose_wam_branch_candidate():
        """Try bounded insertion corrections on copied MuJoCo states."""
        nonlocal wam_samples_recorded
        nonlocal left_grip_rot, right_grip_rot
        nonlocal selected_left_grip_turn_deg, selected_right_grip_turn_deg
        candidate_offsets = (
            ("nominal", 0.000, 0.000, 0.000),
            ("shallow_6mm", -0.006, 0.000, 0.000),
            ("deep_4mm", 0.004, 0.000, 0.000),
            ("both_down_4mm", 0.000, -0.004, -0.004),
            ("both_up_4mm", 0.000, 0.004, 0.004),
            ("left_down_6mm", 0.000, -0.006, 0.000),
            ("right_down_6mm", 0.000, 0.000, -0.006),
            ("left_up_6mm", 0.000, 0.006, 0.000),
            ("right_up_6mm", 0.000, 0.000, 0.006),
            ("both_down_30mm", 0.000, -0.030, -0.030),
            ("both_down_45mm", 0.000, -0.045, -0.045),
        )
        results = []
        baseline_left_rot = np.asarray(left_grip_rot, dtype=float).copy()
        baseline_right_rot = np.asarray(right_grip_rot, dtype=float).copy()
        baseline_turns = (
            float(selected_left_grip_turn_deg),
            float(selected_right_grip_turn_deg),
        )
        start_box = np.asarray(sim_node.mj_data.xpos[box_body_id], dtype=float).copy()
        baseline_robot_contacts = branch_robot_environment_contacts(sim_node.mj_data)
        baseline_nonfinger = set(
            sim_node.wall_grasp_report(sim_node.mj_data)["nonfinger_contacts"]
        )
        q_ref_left = np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float)
        q_ref_right = np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float)
        branch_step = {
            "kind": "wam_candidate",
            "name": "wam_slot_candidate_rollout",
            "duration": float(wam_rollout_horizon),
        }
        pre_report = sim_node.wall_grasp_report()
        pre_state_features = wam_feature_vector(
            branch_step,
            now,
            pre_report,
            stage_progress_override=0.0,
            grasp_validated_override=False,
        )
        for name, dx, left_dz, right_dz in candidate_offsets:
            left_grip_rot = baseline_left_rot.copy()
            right_grip_rot = baseline_right_rot.copy()
            selected_left_grip_turn_deg, selected_right_grip_turn_deg = baseline_turns
            left_front = np.asarray(targets["wall_slot_front_left"], dtype=float).copy()
            right_front = np.asarray(targets["wall_slot_front_right"], dtype=float).copy()
            left_goal = np.asarray(targets["wall_slot_left"], dtype=float).copy()
            right_goal = np.asarray(targets["wall_slot_right"], dtype=float).copy()
            left_front += np.array([dx, 0.0, left_dz])
            right_front += np.array([dx, 0.0, right_dz])
            left_goal += np.array([dx, 0.0, left_dz])
            right_goal += np.array([dx, 0.0, right_dz])
            try:
                left_front_q, right_front_q = solve_world_pair(
                    left_front,
                    right_front,
                    q_ref_left,
                    q_ref_right,
                    stage_name=f"WAM branch front {name}",
                )
                left_q, right_q = solve_world_pair(
                    left_goal,
                    right_goal,
                    left_front_q,
                    right_front_q,
                    stage_name=f"WAM branch {name}",
                )
                candidate_left_rot = np.asarray(left_grip_rot, dtype=float).copy()
                candidate_right_rot = np.asarray(right_grip_rot, dtype=float).copy()
                candidate_turns = (
                    float(selected_left_grip_turn_deg),
                    float(selected_right_grip_turn_deg),
                )
            except Exception as exc:
                results.append({
                    "name": name,
                    "offset": (dx, left_dz, right_dz),
                    "score": -1.0e9,
                    "hard_safe": False,
                    "reason": f"IK: {exc}",
                })
                continue

            branch_data = mujoco.MjData(sim_node.mj_model)
            mujoco.mj_copyData(branch_data, sim_node.mj_model, sim_node.mj_data)
            branch_action = np.asarray(action, dtype=float).copy()
            branch_target = branch_action.copy()
            branch_target[11] = grip_open
            branch_target[18] = grip_open
            branch_target[2] = float(sim_node.tctr_slide[0])
            branch_arm_start = np.r_[q_ref_left, q_ref_right]
            branch_arm_front = np.r_[left_front_q, right_front_q]
            branch_arm_goal = np.r_[left_q, right_q]
            hard_safe = True
            rejection_reason = ""
            maximum_box_shift = 0.0
            observed_nonfinger = set()
            observed_robot_contacts = set()
            control_sequence = []
            steps = max(
                1,
                int(float(wam_rollout_horizon) / max(float(sim_node.delta_t), 1.0e-6)),
            )
            for rollout_step in range(steps):
                rollout_progress = float(rollout_step + 1) / float(steps)
                if rollout_progress <= 0.55:
                    phase = rollout_progress / 0.55
                    branch_arm_target = (
                        (1.0 - phase) * branch_arm_start
                        + phase * branch_arm_front
                    )
                else:
                    phase = (rollout_progress - 0.55) / 0.45
                    branch_arm_target = (
                        (1.0 - phase) * branch_arm_front
                        + phase * branch_arm_goal
                    )
                branch_target[5:11] = branch_arm_target[:6]
                branch_target[12:18] = branch_arm_target[6:]
                for control_id in range(2, sim_node.njctrl):
                    rate = 0.65
                    if 5 <= control_id < 11 or 12 <= control_id < 18:
                        rate *= 0.45
                    branch_action[control_id] = step_func(
                        branch_action[control_id],
                        branch_target[control_id],
                        rate * float(sim_node.delta_t),
                    )
                branch_action[0:2] = 0.0
                control_sequence.append(branch_action.copy())
                branch_data.ctrl[:sim_node.njctrl] = branch_action[:sim_node.njctrl]
                for _ in range(int(sim_node.decimation)):
                    mujoco.mj_step(sim_node.mj_model, branch_data)
                branch_data.qpos[0] = base_lock_x
                branch_data.qpos[1] = base_lock_y
                branch_data.qvel[0:2] = 0.0
                mujoco.mj_forward(sim_node.mj_model, branch_data)
                maximum_box_shift = max(
                    maximum_box_shift,
                    float(
                        np.linalg.norm(
                            np.asarray(branch_data.xpos[box_body_id][:2])
                            - start_box[:2]
                        )
                    ),
                )
                report_now = sim_node.wall_grasp_report(branch_data)
                new_nonfinger = (
                    set(report_now["nonfinger_contacts"]) - baseline_nonfinger
                )
                new_robot_contacts = (
                    branch_robot_environment_contacts(branch_data)
                    - baseline_robot_contacts
                )
                observed_nonfinger.update(new_nonfinger)
                observed_robot_contacts.update(new_robot_contacts)
                if maximum_box_shift > 0.030:
                    hard_safe = False
                    rejection_reason = (
                        f"absolute_box_shift={maximum_box_shift:.4f} > 0.0300"
                    )
                    break

            pre_clamp_slot_margins, pre_clamp_slot_ready = wall_slot_metrics(
                branch_data
            )
            insertion_control_count = len(control_sequence)
            if hard_safe:
                settle_steps = max(
                    1, int(0.8 / max(float(sim_node.delta_t), 1.0e-6))
                )
                for _ in range(settle_steps):
                    control_sequence.append(branch_action.copy())
                    branch_data.ctrl[:sim_node.njctrl] = branch_action[:sim_node.njctrl]
                    for _ in range(int(sim_node.decimation)):
                        mujoco.mj_step(sim_node.mj_model, branch_data)
                    branch_data.qpos[0] = base_lock_x
                    branch_data.qpos[1] = base_lock_y
                    branch_data.qvel[0:2] = 0.0
                    mujoco.mj_forward(sim_node.mj_model, branch_data)
            # Predict the consequence that matters for this task, not merely
            # an open-slot pose: keep the selected arm pose and close both
            # grippers in the copied state, then measure four-finger contact.
            achieved_all_four = False
            if hard_safe:
                clamp_steps = max(1, int(2.2 / max(float(sim_node.delta_t), 1.0e-6)))
                for _ in range(clamp_steps):
                    branch_target[11] = grip_close
                    branch_target[18] = grip_close
                    for control_id in (11, 18):
                        branch_action[control_id] = step_func(
                            branch_action[control_id],
                            branch_target[control_id],
                            0.65 * float(sim_node.delta_t),
                        )
                    control_sequence.append(branch_action.copy())
                    branch_data.ctrl[:sim_node.njctrl] = branch_action[:sim_node.njctrl]
                    for _ in range(int(sim_node.decimation)):
                        mujoco.mj_step(sim_node.mj_model, branch_data)
                    branch_data.qpos[0] = base_lock_x
                    branch_data.qpos[1] = base_lock_y
                    branch_data.qvel[0:2] = 0.0
                    mujoco.mj_forward(sim_node.mj_model, branch_data)
                    maximum_box_shift = max(
                        maximum_box_shift,
                        float(np.linalg.norm(
                            np.asarray(branch_data.xpos[box_body_id][:2]) - start_box[:2]
                        )),
                    )
                    if maximum_box_shift > 0.030:
                        hard_safe = False
                        rejection_reason = (
                            f"clamp_box_shift={maximum_box_shift:.4f} > 0.0300"
                        )
                        break
                    clamp_report = sim_node.wall_grasp_report(branch_data)
                    achieved_all_four = achieved_all_four or all(
                        force >= 0.10 for force in clamp_report["forces"].values()
                    )

            report = sim_node.wall_grasp_report(branch_data)
            slot_margins = pre_clamp_slot_margins
            slot_ready = pre_clamp_slot_ready
            features = wam_feature_vector(
                branch_step,
                now,
                report,
                data=branch_data,
                control=branch_target,
                stage_progress_override=1.0,
                grasp_validated_override=False,
            )
            forces = np.asarray(list(report["forces"].values()), dtype=float)
            all_four = bool(achieved_all_four or np.all(forces >= 0.10))
            tracking_ok = bool(features[11] < 0.35 and features[12] < 0.35)
            scores = wam_critic.predict(features) if wam_critic is not None else {}
            action_scores = (
                wam_action_critic.predict(
                    pre_state_features,
                    (dx, left_dz, right_dz),
                    (
                        scene_randomization["mass_scale"],
                        scene_randomization["friction_scale"],
                    ),
                )
                if wam_action_critic is not None
                else {}
            )
            critic_safe = float(scores.get("safe", 1.0 if hard_safe else 0.0))
            critic_slot = float(scores.get("slot_ready", 1.0 if slot_ready else 0.0))
            predicted_action_safe = float(action_scores.get("safe", critic_safe))
            predicted_action_slot = float(action_scores.get("slot_ready", critic_slot))
            # Hard physics checks retain veto power. The learned term ranks
            # only candidates that survived collision and displacement gates.
            score = (
                1.5 * critic_slot
                + 0.75 * critic_safe
                + 1.5 * predicted_action_slot
                + 0.75 * predicted_action_safe
                + 40.0 * float(min(slot_margins))
                - 1.5 * float(features[11] + features[12])
                - 80.0 * maximum_box_shift
                - 0.03 * (abs(dx) + abs(left_dz) + abs(right_dz)) * 1000.0
            ) if hard_safe else -1.0e9
            results.append({
                "name": name,
                "offset": (dx, left_dz, right_dz),
                "score": score,
                "hard_safe": hard_safe,
                "slot_ready": slot_ready,
                "slot_margin": float(min(slot_margins)),
                "box_shift": maximum_box_shift,
                "final_box_pos": np.asarray(
                    branch_data.xpos[box_body_id], dtype=float
                ).copy(),
                "scores": scores,
                "action_scores": action_scores,
                "reason": rejection_reason,
                "observed_nonfinger": observed_nonfinger,
                "observed_robot_contacts": observed_robot_contacts,
                "features": features,
                "all_four": all_four,
                "tracking_ok": tracking_ok,
                "metadata": {
                    "time": round(float(now), 4),
                    "stage": branch_step["name"],
                    "source": "mujoco_branch_rollout",
                    "candidate": name,
                    "action_offset_m": [dx, left_dz, right_dz],
                    "maximum_box_shift": maximum_box_shift,
                    "pre_state_features": pre_state_features.tolist(),
                    "scene_seed": int(scene_seed),
                    "scene_randomization": scene_randomization,
                },
                "left_grip_rot": candidate_left_rot,
                "right_grip_rot": candidate_right_rot,
                "wrist_turns": candidate_turns,
                "branch_arm_start": branch_arm_start.copy(),
                "branch_arm_front": branch_arm_front.copy(),
                "branch_arm_goal": branch_arm_goal.copy(),
                "control_sequence": control_sequence,
                "insertion_control_count": insertion_control_count,
            })

        left_grip_rot = baseline_left_rot.copy()
        right_grip_rot = baseline_right_rot.copy()
        selected_left_grip_turn_deg, selected_right_grip_turn_deg = baseline_turns
        viable = [result for result in results if result["hard_safe"]]
        if not viable:
            print(">>> WAM branch planner: no safe candidate; retaining nominal plan")
            for result in results:
                print(
                    f"    {result['name']}: REJECTED; "
                    f"{result.get('reason', '')}"
                )
            return None
        nominal_result = next(
            (result for result in viable if result["name"] == "nominal"), None
        )
        if nominal_result is not None:
            nominal_shift = float(nominal_result["box_shift"])
            nominal_nonfinger = set(nominal_result["observed_nonfinger"])
            nominal_contacts = set(nominal_result["observed_robot_contacts"])
            for result in viable:
                branch_delta = float(
                    np.linalg.norm(
                        np.asarray(result["final_box_pos"])
                        - np.asarray(nominal_result["final_box_pos"])
                    )
                )
                result["branch_delta"] = branch_delta
                if branch_delta > 0.006:
                    result["hard_safe"] = False
                    result["reason"] = (
                        f"relative_box_delta={branch_delta:.4f} > 0.0060"
                    )
                    result["score"] = -1.0e9
                    continue
                extra_nonfinger = (
                    set(result["observed_nonfinger"]) - nominal_nonfinger
                )
                extra_contacts = (
                    set(result["observed_robot_contacts"]) - nominal_contacts
                )
                if extra_nonfinger or extra_contacts:
                    result["hard_safe"] = False
                    result["reason"] = (
                        f"new_nonfinger={sorted(extra_nonfinger)}, "
                        f"new_robot_contact={sorted(extra_contacts)}"
                    )
                    result["score"] = -1.0e9
                    continue
                excess_shift = max(0.0, float(result["box_shift"]) - nominal_shift)
                result["score"] -= 120.0 * excess_shift
        viable = [result for result in results if result["hard_safe"]]
        if not viable:
            print(">>> WAM branch planner: all candidates diverged from nominal dynamics")
            return None
        for result in results:
            if "features" not in result:
                continue
            final_safe = bool(result["hard_safe"])
            # A clamp-only branch has not yet demonstrated free-body motion.
            final_transport = False
            result["metadata"]["hard_gate_reason"] = result.get("reason", "")
            wam_recorder.add(
                result["features"],
                (
                    final_safe,
                    result["all_four"],
                    final_transport,
                    result["slot_ready"],
                ),
                result["metadata"],
            )
            if wam_dataset_path is not None:
                wam_samples_recorded += 1
        contact_viable = [result for result in viable if result["all_four"]]
        slot_ready_viable = [result for result in viable if result["slot_ready"]]
        selection_pool = (
            contact_viable
            if contact_viable
            else slot_ready_viable if slot_ready_viable else viable
        )
        selected = max(selection_pool, key=lambda result: result["score"])
        print(f">>> WAM branch planner evaluated {len(results)} candidates:")
        for result in results:
            if not result["hard_safe"]:
                print(
                    f"    {result['name']}: REJECTED by hard physics gate; "
                    f"{result.get('reason', '')}"
                )
                continue
            print(
                f"    {result['name']}: score={result['score']:.3f}, "
                f"slot_margin={result['slot_margin']:+.4f} m, "
                f"box_shift={result['box_shift']:.4f} m, "
                f"critic_slot={result['scores'].get('slot_ready', float('nan')):.3f}"
                f", action_slot={result['action_scores'].get('slot_ready', float('nan')):.3f}, "
                f"four_contact={result['all_four']}"
            )
        print(
            f">>> WAM selected candidate: {selected['name']}; "
            f"offset(dx,left_dz,right_dz)={selected['offset']}; "
            f"slot_ready={selected['slot_ready']}; "
            f"four_contact={selected['all_four']}"
        )
        return selected

    def apply_wam_candidate(selected):
        """Rebuild the two insertion stages around the selected correction."""
        nonlocal execution_steps
        nonlocal left_grip_rot, right_grip_rot
        nonlocal selected_left_grip_turn_deg, selected_right_grip_turn_deg
        left_grip_rot = np.asarray(selected["left_grip_rot"], dtype=float).copy()
        right_grip_rot = np.asarray(selected["right_grip_rot"], dtype=float).copy()
        selected_left_grip_turn_deg, selected_right_grip_turn_deg = selected[
            "wrist_turns"
        ]
        print(
            ">>> restoring selected WAM wrist pose:",
            f"left={selected_left_grip_turn_deg:.1f}deg, "
            f"right={selected_right_grip_turn_deg:.1f}deg",
        )
        dx, left_dz, right_dz = selected["offset"]
        left_front = np.asarray(targets["wall_slot_front_left"], dtype=float).copy()
        right_front = np.asarray(targets["wall_slot_front_right"], dtype=float).copy()
        left_insert = np.asarray(targets["wall_slot_left"], dtype=float).copy()
        right_insert = np.asarray(targets["wall_slot_right"], dtype=float).copy()
        correction_left = np.array([dx, 0.0, left_dz])
        correction_right = np.array([dx, 0.0, right_dz])
        left_front += correction_left
        right_front += correction_right
        left_insert += correction_left
        right_insert += correction_right
        controls = [
            np.asarray(value, dtype=float).copy()
            for value in selected["control_sequence"][
                :int(selected["insertion_control_count"])
            ]
        ]
        execution_steps[step_index] = {
            "kind": "wam_control_replay",
            "name": f"replay validated WAM candidate {selected['name']}",
            "controls": controls,
        }
        # Replace both original insertion stages with the single validated
        # low-level rollout. This preserves the exact predicted control trace.
        if step_index + 1 < len(execution_steps):
            del execution_steps[step_index + 1]
        print(
            f">>> planned exact WAM control replay: {len(controls)} cycles, "
            f"duration={len(controls) * float(sim_node.delta_t):.2f}s"
        )

    while sim_node.running:
        direct_action_this_step = False
        drive_base_this_step = False
        now = sim_node.mj_data.time
        if max_seconds is not None and now >= max_seconds:
            print(">>> preview time limit reached")
            break
        if step_index >= len(execution_steps):
            break

        step = execution_steps[step_index]
        if current_step_name != step["name"]:
            current_step_name = step["name"]
            step_enter_time = now
            point_enter_time = now
            path_index = 0
            print(f">>> execute: {current_step_name}")

        if (
            wam_branch_planning
            and not wam_branch_selection_done
            and step["name"] == "wall_slot_front_alignment"
        ):
            selected = choose_wam_branch_candidate()
            if selected is not None and selected["name"] != "nominal":
                apply_wam_candidate(selected)
                step = execution_steps[step_index]
            elif selected is not None:
                print(">>> WAM nominal candidate selected; preserving verified trajectory")
            wam_branch_selection_done = True

        wam_observe(step, now)

        if step["kind"] == "wam_control_replay":
            controls = step["controls"]
            control_index = min(path_index, len(controls) - 1)
            action[:] = controls[control_index]
            sim_node.target_control[:] = action
            direct_action_this_step = True
            path_index += 1
            if path_index >= len(controls):
                step_index += 1
                current_step_name = None

        elif step["kind"] == "joint_path":
            sim_node.tctr_lft_gripper[:] = step["grip"]
            sim_node.tctr_rgt_gripper[:] = step["grip"]
            path = step["path"]
            target_active = np.asarray(path[min(path_index, len(path) - 1)], dtype=float)
            sim_node.tctr_left_arm[:] = target_active[:6]
            sim_node.tctr_right_arm[:] = target_active[6:]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()

            left_err = float(np.linalg.norm(sim_node.sensor_lft_arm_qpos - target_active[:6]))
            right_err = float(np.linalg.norm(sim_node.sensor_rgt_arm_qpos - target_active[6:]))
            point_elapsed = now - point_enter_time
            position_tolerance = float(step.get("position_tolerance", 0.045))
            both_reached = (
                left_err < position_tolerance and right_err < position_tolerance
            )
            is_final_point = path_index >= len(path) - 1
            must_reach = bool(step.get("require_both_reached", False)) or (
                is_final_point and bool(step.get("require_final_reached", False))
            )
            point_timeout = float(
                step.get("final_point_timeout", 6.0)
                if is_final_point and step.get("require_final_reached", False)
                else step.get("point_timeout", 0.55)
            )
            if both_reached or (
                point_elapsed > point_timeout
                and not must_reach
            ):
                path_index += 1
                point_enter_time = now
                if path_index >= len(path):
                    step_index += 1
                    current_step_name = None
            elif point_elapsed > point_timeout:
                accept_timeout_error = step.get("accept_timeout_error")
                if (
                    is_final_point
                    and accept_timeout_error is not None
                    and max(left_err, right_err) <= float(accept_timeout_error)
                ):
                    print(
                        f">>> {current_step_name} settled with controller offset; "
                        f"continuing to synchronized correction: "
                        f"left_err={left_err:.3f}, right_err={right_err:.3f}"
                    )
                    step_index += 1
                    current_step_name = None
                else:
                    print(
                        f">>> DUAL-ARM MOVE FAILED at {current_step_name} "
                        f"sample {path_index + 1}/{len(path)}: "
                        f"left_err={left_err:.3f}, right_err={right_err:.3f}"
                    )
                    execution_steps = [
                        {
                            "kind": "hold",
                            "name": "dual-arm move failed - inspect scene",
                            "duration": 1.0e9,
                        }
                    ]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "timed_joint_path":
            sim_node.tctr_lft_gripper[:] = step["grip"]
            sim_node.tctr_rgt_gripper[:] = step["grip"]
            path = step["path"]
            duration = float(step["duration"])
            settle_duration = float(step.get("settle_duration", 0.8))
            elapsed = now - step_enter_time
            progress = min(1.0, elapsed / max(duration, 1.0e-6))

            if len(path) == 1:
                target_active = np.asarray(path[0], dtype=float)
            else:
                path_position = progress * (len(path) - 1)
                lower_index = min(int(math.floor(path_position)), len(path) - 2)
                local_alpha = path_position - lower_index
                q0 = np.asarray(path[lower_index], dtype=float)
                q1 = np.asarray(path[lower_index + 1], dtype=float)
                target_active = (1.0 - local_alpha) * q0 + local_alpha * q1

            # The exact same progress value selects both halves of the paired
            # joint sample, so neither arm can advance to a later squeeze point.
            sim_node.tctr_left_arm[:] = target_active[:6]
            sim_node.tctr_right_arm[:] = target_active[6:]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()

            if step.get("monitor_wall_safety", False):
                safety_report = sim_node.wall_grasp_report()
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                box_shift = float(
                    np.linalg.norm(
                        np.asarray(box_now[:2], dtype=float)
                        - np.asarray(sim_node.box_start_pos[:2], dtype=float)
                    )
                )
                left_entry_force = max(
                    safety_report["forces"]["lft_finger_left_link"],
                    safety_report["forces"]["lft_finger_right_link"],
                )
                right_entry_force = max(
                    safety_report["forces"]["rgt_finger_left_link"],
                    safety_report["forces"]["rgt_finger_right_link"],
                )
                first_finger_force = max(left_entry_force, right_entry_force)
                if (
                    step.get("stop_on_finger_contact", False)
                    and left_entry_force >= 0.08
                    and right_entry_force >= 0.08
                ):
                    print(
                        ">>> open-slot insertion stopped after both hands contact; "
                        f"progress={progress:.2f}, box_xy_shift={box_shift:.4f} m, "
                        f"entry_forces=({left_entry_force:.2f}, "
                        f"{right_entry_force:.2f}) N"
                    )
                    # Freeze both wrists at the contact pose.  The next stage
                    # verifies that each wall is geometrically between its own
                    # two fingers before allowing either gripper to close.
                    step_index += 1
                    current_step_name = None
                    continue
                if safety_report["nonfinger_contacts"] or box_shift > 0.004:
                    force_text = ", ".join(
                        f"{name}={force:.2f}"
                        for name, force in safety_report["forces"].items()
                    )
                    print(
                        f">>> WALL INSERTION SAFETY STOP at {current_step_name}: "
                        f"nonfinger={sorted(safety_report['nonfinger_contacts'])}; "
                        f"box_xy_shift={box_shift:.4f} m; "
                        f"delta_xy={np.round(np.asarray(box_now[:2]) - np.asarray(sim_node.box_start_pos[:2]), 4)}; "
                        f"forces=({force_text}) N; "
                        f"nonfinger_pos={{{', '.join(f'{name}: {np.round(points, 4).tolist()}' for name, points in safety_report['nonfinger_positions'].items())}}}"
                    )
                    print(
                        ">>> arm tracking at safety stop:",
                        f"left_sensor={np.round(sim_node.sensor_lft_arm_qpos, 3)}",
                        f"left_target={np.round(sim_node.tctr_left_arm, 3)}",
                        f"left_action={np.round(action[5:11], 3)}",
                        f"right_sensor={np.round(sim_node.sensor_rgt_arm_qpos, 3)}",
                        f"right_target={np.round(sim_node.tctr_right_arm, 3)}",
                        f"right_action={np.round(action[12:18], 3)}",
                    )
                    sim_node.print_gripper_geometry(
                        f"{current_step_name} safety stop"
                    )
                    execution_steps = [
                        {
                            "kind": "hold",
                            "name": "unsafe wall insertion - inspect scene",
                            "duration": 1.0e9,
                        }
                    ]
                    step_index = 0
                    current_step_name = None
                    continue

            left_err = float(
                np.linalg.norm(sim_node.sensor_lft_arm_qpos - target_active[:6])
            )
            right_err = float(
                np.linalg.norm(sim_node.sensor_rgt_arm_qpos - target_active[6:])
            )
            settled = max(left_err, right_err) <= float(step.get("settle_error", 1.0e9))
            settle_wait_exhausted = elapsed >= (
                duration + float(step.get("settle_timeout", settle_duration))
            )
            if (
                elapsed >= duration + settle_duration
                and (not step.get("require_settle", False) or settled)
            ):
                print(
                    f">>> synchronized stage complete: {current_step_name}; "
                    f"left_err={left_err:.3f}, right_err={right_err:.3f}"
                )
                if current_step_name == "wall_slot_insert":
                    print(
                        ">>> pre-clamp gripper state:",
                        f"target=({float(sim_node.tctr_lft_gripper[0]):.3f}, "
                        f"{float(sim_node.tctr_rgt_gripper[0]):.3f})",
                        f"action=({float(action[11]):.3f}, {float(action[18]):.3f})",
                        f"tendon=({float(sim_node.sensor_lft_gripper_qpos[0]):.3f}, "
                        f"{float(sim_node.sensor_rgt_gripper_qpos[0]):.3f})",
                        f"raw_q=({np.array2string(sim_node.mj_data.qpos[18:20], precision=4)}, "
                        f"{np.array2string(sim_node.mj_data.qpos[26:28], precision=4)})",
                    )
                    sim_node.print_gripper_geometry("wall slots centered before clamp")
                step_index += 1
                current_step_name = None
            elif step.get("require_settle", False) and settle_wait_exhausted:
                failed_settle_report = sim_node.wall_grasp_report()
                print(
                    f">>> SYNCHRONIZED SETTLE FAILED at {current_step_name}: "
                    f"left_err={left_err:.3f}, right_err={right_err:.3f}; "
                    f"nonfinger={sorted(failed_settle_report['nonfinger_contacts'])}; "
                    f"endpoints=(L{np.round(sim_node.mj_data.site('lft_endpoint').xpos, 4)}, "
                    f"R{np.round(sim_node.mj_data.site('rgt_endpoint').xpos, 4)})"
                )
                execution_steps = [
                    {"kind": "hold", "name": "wall slot settle failed", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None

        elif step["kind"] == "closed_pair_clamp":
            if wall_pinch_mode:
                if "center_targets" not in step:
                    step["center_targets"] = [
                        np.asarray(
                            sim_node.mj_data.site("lft_endpoint").xpos, dtype=float
                        ).copy(),
                        np.asarray(
                            sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float
                        ).copy(),
                    ]
                    step["last_center_update"] = float(now)
                    step["pinch_targets"] = [float(grip_open), float(grip_open)]
                pinch_report = sim_node.wall_grasp_report()
                pinch_forces = pinch_report["forces"]
                safe_contact = not pinch_report["nonfinger_contacts"]
                lft_inner = float(pinch_forces["lft_finger_left_link"]) >= 0.10
                lft_outer = float(pinch_forces["lft_finger_right_link"]) >= 0.10
                rgt_inner = float(pinch_forces["rgt_finger_right_link"]) >= 0.10
                rgt_outer = float(pinch_forces["rgt_finger_left_link"]) >= 0.10
                left_seated = lft_inner and lft_outer
                right_seated = rgt_inner and rgt_outer
                # The low-level controller leaves a mirrored ~2 cm lateral
                # offset.  Recenter both open grippers in small synchronized
                # steps while they close, using contact to stop each side.
                if now - float(step["last_center_update"]) >= 0.10:
                    step["last_center_update"] = float(now)
                    # Close only while a wall is not yet touching either jaw.
                    # With one-sided contact, hold opening and translate the
                    # wrist so the opposite jaw approaches without crushing.
                    if not (lft_inner or lft_outer):
                        step["pinch_targets"][0] = max(
                            grip_close, float(step["pinch_targets"][0]) - 0.025
                        )
                    if not (rgt_inner or rgt_outer):
                        step["pinch_targets"][1] = max(
                            grip_close, float(step["pinch_targets"][1]) - 0.025
                        )
                    if lft_inner and not lft_outer:
                        step["center_targets"][0][1] -= 0.001
                    elif lft_outer and not lft_inner:
                        step["center_targets"][0][1] += 0.001
                    if rgt_inner and not rgt_outer:
                        step["center_targets"][1][1] += 0.001
                    elif rgt_outer and not rgt_inner:
                        step["center_targets"][1][1] -= 0.001
                    try:
                        if not left_seated:
                            sim_node.tctr_left_arm[:] = sim_node.solveArmEndTarget(
                                world_to_base(step["center_targets"][0]),
                                sim_node.arm_action,
                                "l",
                                np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                                left_grip_rot,
                            )
                            sim_node.set_left_arm_new_target = True
                        if not right_seated:
                            sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                                world_to_base(step["center_targets"][1]),
                                sim_node.arm_action,
                                "r",
                                np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                                right_grip_rot,
                            )
                            sim_node.set_right_arm_new_target = True
                        update_joint_move_ratio()
                    except ValueError as exc:
                        print(f">>> wall-pinch centering IK stopped: {exc}")
                sim_node.tctr_lft_gripper[:] = float(step["pinch_targets"][0])
                sim_node.tctr_rgt_gripper[:] = float(step["pinch_targets"][1])
                all_four = left_seated and right_seated
                pinch_compression = max(
                    [-float(d["distance"]) for d in pinch_report["contact_details"]]
                    or [0.0]
                )
                closed_pair_contact_streak = (
                    closed_pair_contact_streak + 1
                    if all_four and safe_contact and pinch_compression <= 0.005
                    else 0
                )
                if not safe_contact:
                    print(
                        ">>> WALL PINCH SAFETY STOP: nonfinger=",
                        sorted(pinch_report["nonfinger_contacts"]),
                    )
                    execution_steps = [
                        {"kind": "hold", "name": "wall pinch collision stop", "duration": 1.0e9}
                    ]
                    step_index = 0
                    current_step_name = None
                    continue
                if pinch_compression > 0.008:
                    print(
                        ">>> WALL PINCH COMPRESSION STOP: "
                        f"compression={pinch_compression * 1000:.2f}mm"
                    )
                    execution_steps = [
                        {"kind": "hold", "name": "wall pinch compression stop", "duration": 1.0e9}
                    ]
                    step_index = 0
                    current_step_name = None
                    continue
                if closed_pair_contact_streak >= 20:
                    print(
                        ">>> four-face wall pinch acquired; "
                        f"forces={ {k: round(v, 2) for k, v in pinch_forces.items()} }; "
                        f"compression={pinch_compression * 1000:.2f}mm"
                    )
                    physical_grasp_validated = True
                    execution_steps[step_index + 1:] = [
                        {
                            "kind": "grip_base_retreat",
                            "name": "physical extraction with both side walls pinched",
                            "distance": 0.22,
                            "duration": 3.8,
                            "left_arm_q": np.asarray(sim_node.tctr_left_arm, dtype=float).copy(),
                            "right_arm_q": np.asarray(sim_node.tctr_right_arm, dtype=float).copy(),
                        },
                        {"kind": "physical_success", "name": "verify wall-pinch extraction"},
                    ]
                    step_index += 1
                    current_step_name = None
                elif now - step_enter_time >= float(step["timeout"]):
                    print(
                        ">>> WALL PINCH FAILED: four physical finger contacts not reached; "
                        f"forces={ {k: round(v, 2) for k, v in pinch_forces.items()} }"
                    )
                    execution_steps = [
                        {"kind": "hold", "name": "wall pinch failed", "duration": 1.0e9}
                    ]
                    step_index = 0
                    current_step_name = None
                continue
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            closed_report = sim_node.wall_grasp_report()
            left_load = float(
                closed_report["forces"]["lft_finger_left_link"]
                + closed_report["forces"]["lft_finger_right_link"]
            )
            right_load = float(
                closed_report["forces"]["rgt_finger_left_link"]
                + closed_report["forces"]["rgt_finger_right_link"]
            )
            safe_contact = not closed_report["nonfinger_contacts"]
            max_closed_compression = max(
                [-float(detail["distance"]) for detail in closed_report["contact_details"]]
                or [0.0]
            )
            if not safe_contact:
                print(
                    ">>> CLOSED CLAMP SAFETY STOP: nonfinger=",
                    sorted(closed_report["nonfinger_contacts"]),
                )
                execution_steps = [
                    {"kind": "hold", "name": "closed clamp collision stop", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None
                continue
            # Do not start extraction on first touch.  After both sides first
            # engage, command another 4 mm of symmetric arm travel.  The arm
            # servo deflection creates clamp preload; MuJoCo contact compliance
            # limits actual wall compression independently.
            left_travel = float(step.get("left_inward_travel", 0.0))
            right_travel = float(step.get("right_inward_travel", 0.0))
            if "left_first_contact" not in step and left_load >= 0.5:
                step["left_first_contact"] = left_travel
            if "right_first_contact" not in step and right_load >= 0.5:
                step["right_first_contact"] = right_travel
            left_preload = left_travel - float(
                step.get("left_first_contact", left_travel)
            )
            right_preload = right_travel - float(
                step.get("right_first_contact", right_travel)
            )
            left_ready = (
                "left_first_contact" in step
                and left_preload >= 0.0035
                and left_load >= 12.0
            )
            right_ready = (
                "right_first_contact" in step
                and right_preload >= 0.0035
                and right_load >= 12.0
            )
            preload_travel = min(left_preload, right_preload)
            closed_pair_contact_streak = (
                closed_pair_contact_streak + 1
                if (
                    left_ready
                    and right_ready
                    and max_closed_compression <= 0.005
                )
                else 0
            )
            if closed_pair_contact_streak >= 20:
                print(
                    ">>> bilateral closed-gripper clamp acquired; "
                    f"loads=({left_load:.2f}, {right_load:.2f}) N; "
                    f"preload_travel={preload_travel * 1000:.1f}mm; "
                    f"compression={max_closed_compression * 1000:.2f}mm; "
                    f"arm_effort_L={np.round(sim_node.mj_data.actuator_force[5:11], 2)}, "
                    f"arm_effort_R={np.round(sim_node.mj_data.actuator_force[12:18], 2)}"
                )
                print(
                    ">>> physical contact points:",
                    [
                        (
                            detail["body"],
                            detail.get("geom_pair", ("", "")),
                            np.round(detail["position"], 4).tolist(),
                            np.round(detail.get("contact_normal", np.zeros(3)), 3).tolist(),
                            round(float(detail.get("effective_friction", 0.0)), 3),
                            round(float(detail.get("tangent_force", 0.0)), 3),
                        )
                        for detail in closed_report["contact_details"]
                    ],
                )
                physical_grasp_validated = True
                # First lift the *end effectors themselves* by 5 cm while the
                # bilateral preload is preserved.  Raising only the torso slide
                # can be visually cancelled by the arm controller; a Cartesian
                # endpoint lift guarantees that both hands and the free box are
                # commanded upward before any base retreat begins.
                execution_steps[step_index + 1:] = [
                    {
                        "kind": "closed_pair_cartesian_lift",
                        "name": "lift clamped package 5cm before retreat",
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
                        "kind": "grip_base_retreat",
                        "name": "fast physical extraction after 5cm lift",
                        "distance": 0.28,
                        "duration": 12.0,
                        # These values are replaced with the measured/commanded
                        # lifted grasp state when the Cartesian lift completes.
                        "left_arm_q": np.asarray(sim_node.tctr_left_arm, dtype=float).copy(),
                        "right_arm_q": np.asarray(sim_node.tctr_right_arm, dtype=float).copy(),
                        "left_endpoint_target": np.asarray(
                            closed_pair_targets_world[0], dtype=float
                        ).copy(),
                        "right_endpoint_target": np.asarray(
                            closed_pair_targets_world[1], dtype=float
                        ).copy(),
                    },
                    {
                        "kind": "physical_success",
                        "name": "verify closed-gripper extraction",
                    },
                ]
                step_index += 1
                current_step_name = None
            elif now - closed_pair_last_update >= 0.12:
                closed_pair_last_update = now
                if closed_pair_targets_world is None:
                    closed_pair_targets_world = [
                        np.asarray(sim_node.mj_data.site("lft_endpoint").xpos, dtype=float).copy(),
                        np.asarray(sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float).copy(),
                    ]
                    step["left_inward_travel"] = 0.0
                    step["right_inward_travel"] = 0.0
                if not left_ready:
                    closed_pair_targets_world[0][1] -= 0.0012
                    step["left_inward_travel"] = (
                        float(step.get("left_inward_travel", 0.0)) + 0.0012
                    )
                if not right_ready:
                    closed_pair_targets_world[1][1] += 0.0012
                    step["right_inward_travel"] = (
                        float(step.get("right_inward_travel", 0.0)) + 0.0012
                    )
                try:
                    if not left_ready:
                        sim_node.tctr_left_arm[:] = sim_node.solveArmEndTarget(
                            world_to_base(closed_pair_targets_world[0]),
                            sim_node.arm_action, "l",
                            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float), left_grip_rot,
                        )
                        sim_node.set_left_arm_new_target = True
                    if not right_ready:
                        sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                            world_to_base(closed_pair_targets_world[1]),
                            sim_node.arm_action, "r",
                            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float), right_grip_rot,
                        )
                        sim_node.set_right_arm_new_target = True
                    update_joint_move_ratio()
                except ValueError as exc:
                    print(f">>> closed clamp IK stopped: {exc}")
            if (
                current_step_name is not None
                and now - step_enter_time >= float(step["timeout"])
            ):
                print(
                    ">>> CLOSED CLAMP FAILED: bilateral contact not reached; "
                    f"loads=({left_load:.2f}, {right_load:.2f}) N; "
                    f"commanded_travel=({left_travel * 1000:.1f}, {right_travel * 1000:.1f})mm; "
                    f"preload=({left_preload * 1000:.1f}, {right_preload * 1000:.1f})mm; "
                    f"compression={max_closed_compression * 1000:.2f}mm; "
                    f"ready=({left_ready}, {right_ready}); "
                    f"targets=({np.round(closed_pair_targets_world[0], 4)}, "
                    f"{np.round(closed_pair_targets_world[1], 4)}); "
                    f"actual=({np.round(sim_node.mj_data.site('lft_endpoint').xpos, 4)}, "
                    f"{np.round(sim_node.mj_data.site('rgt_endpoint').xpos, 4)})"
                )
                execution_steps = [
                    {"kind": "hold", "name": "closed clamp failed", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None

        elif step["kind"] == "contact_seek":
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            path = step["path"]
            elapsed = now - step_enter_time
            duration = float(step["duration"])
            progress = min(1.0, elapsed / max(duration, 1.0e-6))
            if len(path) == 1:
                target_active = np.asarray(path[0], dtype=float)
            else:
                path_position = progress * (len(path) - 1)
                lower_index = min(int(math.floor(path_position)), len(path) - 2)
                local_alpha = path_position - lower_index
                q0 = np.asarray(path[lower_index], dtype=float)
                q1 = np.asarray(path[lower_index + 1], dtype=float)
                target_active = (1.0 - local_alpha) * q0 + local_alpha * q1

            sim_node.tctr_left_arm[:] = target_active[:6]
            sim_node.tctr_right_arm[:] = target_active[6:]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()

            contact_sides = sim_node.box_gripper_contact_sides()
            contact_report = sim_node.box_gripper_contact_report()
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            left_positions = contact_report["left"]["positions"]
            right_positions = contact_report["right"]["positions"]
            left_on_positive_side = any(
                float(pos[1]) > float(box_now[1]) + 0.015 for pos in left_positions
            )
            right_on_negative_side = any(
                float(pos[1]) < float(box_now[1]) - 0.015 for pos in right_positions
            )
            minimum_contact_force = 0.15
            force_ok = (
                contact_report["left"]["force"] >= minimum_contact_force
                and contact_report["right"]["force"] >= minimum_contact_force
            )
            bilateral_physical_grasp = (
                contact_sides == {"left", "right"}
                and left_on_positive_side
                and right_on_negative_side
                and force_ok
            )
            if bilateral_physical_grasp:
                bilateral_contact_streak += 1
            else:
                bilateral_contact_streak = 0

            # Require persistent contact rather than accepting one transient
            # collision frame while the package is being centered.
            if bilateral_contact_streak >= 8:
                measured_active = np.concatenate([
                    np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                    np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                ])
                commanded_active = np.concatenate([
                    np.asarray(sim_node.tctr_left_arm, dtype=float),
                    np.asarray(sim_node.tctr_right_arm, dtype=float),
                ])
                preload_offset = commanded_active - measured_active
                # Keep only the modest elastic/controller preload produced by
                # the physical pinch; guard against transient tracking error.
                preload_offset = np.clip(preload_offset, -0.10, 0.10)
                print(
                    f">>> bilateral grasp acquired at seek progress={progress:.2f}; "
                    f"forces=({contact_report['left']['force']:.2f}, "
                    f"{contact_report['right']['force']:.2f}) N; "
                    f"preload_norm=({np.linalg.norm(preload_offset[:6]):.3f}, "
                    f"{np.linalg.norm(preload_offset[6:]):.3f}); "
                    "replanning transport from measured arm pose"
                )
                try:
                    transport_steps = plan_transport_from_actual_grasp(preload_offset)
                    execution_steps[step_index + 1:] = transport_steps
                    step_index += 1
                    current_step_name = None
                except Exception as exc:
                    print(">>> post-contact transport planning failed")
                    print(f">>> failure: {type(exc).__name__}: {exc}")
                    execution_steps = [
                        {
                            "kind": "hold",
                            "name": "transport replan failed - inspect grasp",
                            "duration": 1.0e9,
                        }
                    ]
                    step_index = 0
                    current_step_name = None
            elif elapsed >= duration + float(step.get("settle_duration", 0.8)):
                print(
                    ">>> GRASP FAILED after symmetric contact search; "
                    f"detected={sorted(contact_sides) or ['none']}; "
                    f"forces=({contact_report['left']['force']:.2f}, "
                    f"{contact_report['right']['force']:.2f}) N; "
                    f"opposed_sides=({left_on_positive_side}, {right_on_negative_side})"
                )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "contact search exhausted - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None

        elif step["kind"] == "timed_transport_path":
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            path = step["path"]
            elapsed = now - step_enter_time
            duration = float(step["duration"])
            progress = min(1.0, elapsed / max(duration, 1.0e-6))
            if len(path) == 1:
                target_active = np.asarray(path[0], dtype=float)
            else:
                path_position = progress * (len(path) - 1)
                lower_index = min(int(math.floor(path_position)), len(path) - 2)
                local_alpha = path_position - lower_index
                q0 = np.asarray(path[lower_index], dtype=float)
                q1 = np.asarray(path[lower_index + 1], dtype=float)
                target_active = (1.0 - local_alpha) * q0 + local_alpha * q1

            preload_offset = np.asarray(
                step.get("preload_offset", np.zeros(12)), dtype=float
            )
            target_active = target_active + preload_offset
            sim_node.tctr_left_arm[:] = target_active[:6]
            sim_node.tctr_right_arm[:] = target_active[6:]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()

            report = sim_node.box_gripper_contact_report()
            wall_transport_report = sim_node.wall_grasp_report()
            transport_four_finger = all(
                wall_transport_report["forces"][name] >= 0.05
                for name in (
                    "lft_finger_left_link",
                    "lft_finger_right_link",
                    "rgt_finger_left_link",
                    "rgt_finger_right_link",
                )
            )
            if (
                elapsed > 0.35
                and not transport_four_finger
                and current_step_name == "rigid_lift"
            ):
                print(
                    ">>> TRANSPORT SAFETY STOP: four-finger wall clamp lost "
                    f"during {current_step_name}; forces="
                    f"{ {name: round(force, 2) for name, force in wall_transport_report['forces'].items()} }"
                )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "wall clamp lost during lift - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
                continue
            if elapsed >= duration + float(step.get("settle_duration", 0.6)):
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                print(
                    f">>> transport stage complete: {current_step_name}; "
                    f"box={np.array2string(box_now, precision=4)}; "
                    f"forces=({report['left']['force']:.2f}, "
                    f"{report['right']['force']:.2f}) N"
                )
                step_index += 1
                current_step_name = None

        elif step["kind"] == "grip_slide_lift":
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.tctr_slide[0] = float(step["target"])
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            sim_node.joint_move_ratio[:] = 1.0
            sim_node.joint_move_ratio[2] = float(step.get("speed", 0.65))
            lift_report = sim_node.wall_grasp_report()
            left_load = (
                lift_report["forces"]["lft_finger_left_link"]
                + lift_report["forces"]["lft_finger_right_link"]
            )
            right_load = (
                lift_report["forces"]["rgt_finger_left_link"]
                + lift_report["forces"]["rgt_finger_right_link"]
            )
            bilateral_load = left_load >= 0.10 and right_load >= 0.10
            safe_robot_contact = not lift_report["nonfinger_contacts"]
            transport_contact_loss_streak = (
                0
                if bilateral_load and safe_robot_contact
                else transport_contact_loss_streak + 1
            )
            if now - step_enter_time > 0.35 and transport_contact_loss_streak >= 25:
                print(
                    ">>> SLIDE LIFT SAFETY STOP: bilateral wall clamp lost; "
                    f"forces={ {name: round(force, 2) for name, force in lift_report['forces'].items()} }; "
                    f"nonfinger={sorted(lift_report['nonfinger_contacts'])}"
                )
                execution_steps = [
                    {"kind": "hold", "name": "wall clamp lost during slide lift", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None
                continue
            if now - step_enter_time > float(step.get("timeout", 8.0)):
                print(
                    ">>> SLIDE LIFT FAILED: controller timeout; "
                    f"sensor={float(sim_node.sensor_slide_qpos[0]):.4f}, "
                    f"target={float(step['target']):.4f}, action={float(action[2]):.4f}"
                )
                execution_steps = [
                    {"kind": "hold", "name": "slide lift timeout", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None
                continue
            if abs(float(sim_node.sensor_slide_qpos[0]) - float(step["target"])) < 0.008:
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                if float(box_now[2]) < float(sim_node.box_start_z) + 0.008:
                    print(
                        ">>> SLIDE LIFT FAILED: package did not rise with clamps; "
                        f"box_z={box_now[2]:.4f}, start_z={sim_node.box_start_z:.4f}"
                    )
                    execution_steps = [
                        {"kind": "hold", "name": "package not lifted", "duration": 1.0e9}
                    ]
                    step_index = 0
                    current_step_name = None
                    continue
                print(
                    ">>> slide lift complete with arm joints frozen; "
                    f"box={np.round(box_now, 4)}"
                )
                execution_steps[step_index + 1:] = [
                    {
                        "kind": "grip_base_retreat",
                        "name": "base_retreat_with_frozen_wall_clamps",
                        "distance": 0.22,
                        "duration": 3.2,
                        "left_arm_q": np.asarray(
                            sim_node.sensor_lft_arm_qpos, dtype=float
                        ).copy(),
                        "right_arm_q": np.asarray(
                            sim_node.sensor_rgt_arm_qpos, dtype=float
                        ).copy(),
                    },
                    {
                        "kind": "hold",
                        "name": "hold outside cabinet",
                        "duration": float(hold_seconds),
                    },
                ]
                step_index += 1
                current_step_name = None

        elif step["kind"] == "closed_pair_cartesian_lift":
            # Keep the wheels stopped and preserve the same closed-gripper
            # preload while both Cartesian endpoint targets rise together.
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            lift_report = sim_node.wall_grasp_report()
            left_load = float(
                lift_report["forces"]["lft_finger_left_link"]
                + lift_report["forces"]["lft_finger_right_link"]
            )
            right_load = float(
                lift_report["forces"]["rgt_finger_left_link"]
                + lift_report["forces"]["rgt_finger_right_link"]
            )

            if "start_left_endpoint_target" not in step:
                step["start_left_endpoint_target"] = np.asarray(
                    step["left_endpoint_target"], dtype=float
                ).copy()
                step["start_right_endpoint_target"] = np.asarray(
                    step["right_endpoint_target"], dtype=float
                ).copy()
                step["start_left_site_z"] = float(
                    sim_node.mj_data.site("lft_endpoint").xpos[2]
                )
                step["start_right_site_z"] = float(
                    sim_node.mj_data.site("rgt_endpoint").xpos[2]
                )
                step["start_box_z"] = float(
                    get_body_tmat(sim_node.mj_data, target_body_name)[2, 3]
                )
                step["start_box_rotation"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, :3].copy()
                step["last_lift_log"] = -1.0e9
                step["loss_streak"] = 0
                step["settle_streak"] = 0
                step["max_lateral_speed"] = 0.0
                step["max_angular_speed"] = 0.0
                step["max_orientation_excursion_deg"] = 0.0
                step["lift_y_offsets"] = np.zeros(2, dtype=float)
                step["filtered_lift_loads"] = np.asarray(
                    [left_load, right_load], dtype=float
                )
                step["last_lift_force_update"] = float(now)
                print(
                    ">>> pre-retreat Cartesian lift started: "
                    f"requested={float(step['height']) * 100:.1f}cm; "
                    f"box_z={step['start_box_z']:.4f}; "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )

            elapsed = float(now - step_enter_time)
            duration = max(float(step["duration"]), 1.0e-6)
            pre_hold = max(0.0, float(step.get("pre_hold", 0.0)))
            post_hold = max(0.0, float(step.get("post_hold", 0.0)))
            motion_elapsed = max(0.0, elapsed - pre_hold)
            alpha = min(1.0, max(0.0, motion_elapsed / duration))
            # Quintic smootherstep has zero velocity and zero acceleration at
            # both ends.  The short pre-hold lets clamp transients decay before
            # the free package is lifted from the shelf.
            lift_alpha = alpha ** 3 * (10.0 - 15.0 * alpha + 6.0 * alpha ** 2)
            lift_dz = float(step["height"]) * lift_alpha

            left_target = np.asarray(
                step["start_left_endpoint_target"], dtype=float
            ).copy()
            right_target = np.asarray(
                step["start_right_endpoint_target"], dtype=float
            ).copy()
            left_target[2] += lift_dz
            right_target[2] += lift_dz

            # Once the carton begins to leave the shelf, unequal lateral
            # preload can release as a visible sideways spring.  Slowly trim
            # each arm's Y target from measured contact force; the correction
            # is bounded to 2 mm and cannot create an attachment constraint.
            filtered_loads = np.asarray(
                step.get("filtered_lift_loads", [left_load, right_load]),
                dtype=float,
            )
            filtered_loads = 0.75 * filtered_loads + 0.25 * np.asarray(
                [left_load, right_load], dtype=float
            )
            step["filtered_lift_loads"] = filtered_loads
            if now - float(step.get("last_lift_force_update", -1.0e9)) >= 0.04:
                step["last_lift_force_update"] = float(now)
                target_lift_load = 12.5
                force_deltas = np.clip(
                    0.00004 * (target_lift_load - filtered_loads),
                    -0.00020,
                    0.00020,
                )
                lift_y_offsets = np.asarray(
                    step.get("lift_y_offsets", np.zeros(2)), dtype=float
                )
                lift_y_offsets[0] -= force_deltas[0]
                lift_y_offsets[1] += force_deltas[1]
                step["lift_y_offsets"] = np.clip(
                    lift_y_offsets, -0.002, 0.002
                )
            lift_y_offsets = np.asarray(step["lift_y_offsets"], dtype=float)
            left_target[1] += lift_y_offsets[0]
            right_target[1] += lift_y_offsets[1]

            try:
                corrected_left_q = sim_node.solveArmEndTarget(
                    world_to_base(left_target),
                    sim_node.arm_action,
                    "l",
                    np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                    left_grip_rot,
                )
                corrected_right_q = sim_node.solveArmEndTarget(
                    world_to_base(right_target),
                    sim_node.arm_action,
                    "r",
                    np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                    right_grip_rot,
                )
                sim_node.tctr_left_arm[:] = corrected_left_q
                sim_node.tctr_right_arm[:] = corrected_right_q
                sim_node.set_left_arm_new_target = True
                sim_node.set_right_arm_new_target = True
                update_joint_move_ratio()
            except ValueError as exc:
                print(f">>> PRE-RETREAT CARTESIAN LIFT IK FAILED: {exc}")
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "5cm Cartesian lift IK failed - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
                continue

            current_left_z = float(sim_node.mj_data.site("lft_endpoint").xpos[2])
            current_right_z = float(sim_node.mj_data.site("rgt_endpoint").xpos[2])
            box_tmat = get_body_tmat(sim_node.mj_data, target_body_name)
            box_now = box_tmat[:3, 3]
            left_rise = current_left_z - float(step["start_left_site_z"])
            right_rise = current_right_z - float(step["start_right_site_z"])
            box_rise = float(box_now[2] - step["start_box_z"])
            # Diagnostic only.  Matrix rotation comparison can trigger a native
            # linalg crash in this Windows/MuJoCo stack, so do not gate motion on it.
            orientation_excursion_deg = 0.0
            box_velocity = np.asarray(
                sim_node.mj_data.qvel[box_dof_adr:box_dof_adr + 6], dtype=float
            )
            lateral_speed = float(np.linalg.norm(box_velocity[:2]))
            angular_speed = float(np.linalg.norm(box_velocity[3:6]))
            step["max_lateral_speed"] = max(
                float(step["max_lateral_speed"]), lateral_speed
            )
            step["max_angular_speed"] = max(
                float(step["max_angular_speed"]), angular_speed
            )
            step["max_orientation_excursion_deg"] = max(
                float(step["max_orientation_excursion_deg"]),
                orientation_excursion_deg,
            )

            bilateral_contact = left_load >= 1.0 and right_load >= 1.0
            step["loss_streak"] = (
                0 if bilateral_contact else int(step.get("loss_streak", 0)) + 1
            )
            if elapsed > 0.45 and int(step["loss_streak"]) >= 25:
                print(
                    ">>> PRE-RETREAT LIFT SAFETY STOP: bilateral clamp lost; "
                    f"normal=({left_load:.2f}, {right_load:.2f})N; "
                    f"box_rise={box_rise * 100:.1f}cm"
                )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "clamp lost during 5cm Cartesian lift",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
                continue

            if now - float(step.get("last_lift_log", -1.0e9)) >= 0.40:
                step["last_lift_log"] = float(now)
                print(
                    ">>> pre-retreat lift: "
                    f"progress={alpha:.2f}, "
                    f"endpoint_rise=({left_rise * 100:.1f}, {right_rise * 100:.1f})cm, "
                    f"box_rise={box_rise * 100:.1f}cm, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N, "
                    f"lateral_v={lateral_speed * 100:.2f}cm/s, "
                    f"angular_v={angular_speed:.3f}rad/s"
                )

            # Do not advance on the command alone.  Require both physical
            # endpoints to have risen about 5 cm.  This closed side-clamp does
            # not reliably lift the free box vertically before retreat, so only
            # reject clear downward slip instead of demanding a 4 cm box rise.
            endpoints_up = left_rise >= 0.045 and right_rise >= 0.045
            box_up = box_rise >= -0.010
            dynamically_settled = lateral_speed <= 0.012 and angular_speed <= 0.20
            step["settle_streak"] = (
                int(step.get("settle_streak", 0)) + 1
                if alpha >= 1.0 and dynamically_settled
                else 0
            )
            post_hold_complete = motion_elapsed - duration >= post_hold
            if (
                alpha >= 1.0
                and post_hold_complete
                and int(step["settle_streak"]) >= 12
                and endpoints_up
                and box_up
                and bilateral_contact
            ):
                final_left_target = np.asarray(
                    step["start_left_endpoint_target"], dtype=float
                ).copy()
                final_right_target = np.asarray(
                    step["start_right_endpoint_target"], dtype=float
                ).copy()
                final_left_target[2] += float(step["height"])
                final_right_target[2] += float(step["height"])

                # Feed the lifted state into the retreat stage so it cannot
                # snap back down when the wheels begin moving.
                if step_index + 1 < len(execution_steps):
                    retreat_step = execution_steps[step_index + 1]
                    if retreat_step.get("kind") == "grip_base_retreat":
                        retreat_step["left_arm_q"] = np.asarray(
                            sim_node.tctr_left_arm, dtype=float
                        ).copy()
                        retreat_step["right_arm_q"] = np.asarray(
                            sim_node.tctr_right_arm, dtype=float
                        ).copy()
                        retreat_step["left_endpoint_target"] = final_left_target.copy()
                        retreat_step["right_endpoint_target"] = final_right_target.copy()

                print(
                    ">>> pre-retreat 5cm Cartesian lift complete; "
                    f"endpoint_rise=({left_rise * 100:.1f}, {right_rise * 100:.1f})cm; "
                    f"box_rise={box_rise * 100:.1f}cm; "
                    f"normal=({left_load:.2f}, {right_load:.2f})N; "
                    f"settled_lateral_v={lateral_speed * 100:.2f}cm/s; "
                    f"settled_angular_v={angular_speed:.3f}rad/s; "
                    f"max_lateral_v={float(step['max_lateral_speed']) * 100:.2f}cm/s; "
                    f"max_angular_v={float(step['max_angular_speed']):.3f}rad/s; "
                    f"max_orientation_excursion="
                    f"{float(step['max_orientation_excursion_deg']):.2f}deg"
                )
                step_index += 1
                current_step_name = None
                continue

            if elapsed >= pre_hold + duration + float(step.get("settle_timeout", 3.0)):
                print(
                    ">>> PRE-RETREAT LIFT FAILED: endpoints did not settle before retreat; "
                    f"endpoint_rise=({left_rise * 100:.1f}, {right_rise * 100:.1f})cm; "
                    f"box_rise={box_rise * 100:.1f}cm; "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "5cm Cartesian lift incomplete - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
                continue

        elif step["kind"] == "grip_base_retreat":
            drive_base_this_step = True
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            if "start_x" not in step:
                step["start_x"] = float(base_lock_x)
                step["start_box"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, 3].copy()
                step["start_base_x"] = float(sim_node.sensor_base_position[0])
                step["start_slide"] = float(sim_node.sensor_slide_qpos[0])
                step["loss_streak"] = 0
                step["start_left_endpoint_target"] = np.asarray(
                    step.get(
                        "left_endpoint_target",
                        sim_node.mj_data.site("lft_endpoint").xpos,
                    ),
                    dtype=float,
                ).copy()
                step["start_right_endpoint_target"] = np.asarray(
                    step.get(
                        "right_endpoint_target",
                        sim_node.mj_data.site("rgt_endpoint").xpos,
                    ),
                    dtype=float,
                ).copy()
                print(
                    ">>> physical base retreat started: package pose is free; "
                    "motion depends only on finger contact, clamp force, and friction"
                )
            elapsed = now - step_enter_time
            actual_retreat = max(
                0.0,
                float(step["start_base_x"] - sim_node.sensor_base_position[0]),
            )
            progress = min(1.0, actual_retreat / max(float(step["distance"]), 1.0e-6))
            # Keep the pad height fixed until the package has been extracted.
            # This prevents an upper-wall grasp from climbing over the rim.
            retreat_lift = 0.0
            sim_node.tctr_slide[0] = float(
                np.clip(
                    step["start_slide"] - retreat_lift,
                    sim_node.mj_model.actuator_ctrlrange[2, 0],
                    sim_node.mj_model.actuator_ctrlrange[2, 1],
                )
            )
            sim_node.joint_move_ratio[2] = 2.5
            # Drive the real wheel joints.  Equal wheel speeds command straight
            # motion; the small yaw feedback prevents one clamp from leading.
            cruise_speed = -float(step["distance"]) / max(float(step["duration"]), 1.0e-6)
            ramp_alpha = min(1.0, max(0.0, elapsed / 0.8))
            speed_ramp = ramp_alpha * ramp_alpha * (3.0 - 2.0 * ramp_alpha)
            box_for_speed = get_body_tmat(
                sim_node.mj_data, target_body_name
            )[:3, 3]
            tracking_lag = float(
                box_for_speed[0]
                - (float(step["start_box"][0]) - actual_retreat)
            )
            # Real slip feedback: slow the mobile base when the free package
            # lags behind the pads, and pull more gently before the finite
            # visible pad length can slide off the wall.  The angled clamp
            # continues to pull through physical contact while the base waits.
            slip_speed_scale = float(
                np.clip((0.032 - tracking_lag) / 0.030, 0.08, 1.0)
            )
            linear_speed = (
                cruise_speed * speed_ramp * slip_speed_scale
                if progress < 1.0
                else 0.0
            )
            quat = np.asarray(sim_node.sensor_base_orientation, dtype=float)
            yaw = math.atan2(
                2.0 * (quat[0] * quat[3] + quat[1] * quat[2]),
                1.0 - 2.0 * (quat[2] ** 2 + quat[3] ** 2),
            )
            angular_speed = -1.5 * yaw
            wheel_target = np.asarray(
                [
                    (linear_speed - angular_speed * sim_node.wheel_distance)
                    / sim_node.wheel_radius,
                    (linear_speed + angular_speed * sim_node.wheel_distance)
                    / sim_node.wheel_radius,
                ],
                dtype=float,
            )
            wheel_error = np.clip(
                wheel_target - np.asarray(sim_node.sensor_wheel_qvel, dtype=float),
                -2.5,
                2.5,
            )
            action[:2] = np.clip(
                7.5 * wheel_error,
                sim_node.mj_model.actuator_ctrlrange[:2, 0],
                sim_node.mj_model.actuator_ctrlrange[:2, 1],
            )
            retreat_report = sim_node.wall_grasp_report()
            if simple_closed_gripper_mode:
                sim_node.tctr_lft_gripper[:] = grip_close
                sim_node.tctr_rgt_gripper[:] = grip_close
            elif independent_finger_mode and independent_force_control_enabled:
                update_independent_finger_forces(retreat_report, now)
            else:
                force_targets = update_force_grip_targets(retreat_report, now)
                sim_node.tctr_lft_gripper[:] = force_targets[0]
                sim_node.tctr_rgt_gripper[:] = force_targets[1]
            left_load = (
                retreat_report["forces"]["lft_finger_left_link"]
                + retreat_report["forces"]["lft_finger_right_link"]
            )
            right_load = (
                retreat_report["forces"]["rgt_finger_left_link"]
                + retreat_report["forces"]["rgt_finger_right_link"]
            )
            retreat_compression = max(
                [-float(d["distance"]) for d in retreat_report["contact_details"]]
                or [0.0]
            )
            if simple_closed_gripper_mode and (
                now - float(step.get("last_preload_update", -1.0e9)) >= 0.04
            ):
                step["last_preload_update"] = float(now)
                # Start from the unloaded IK targets that created the clamp
                # preload, never from the contact-deflected measured sites.
                # The latter would turn elastic servo deflection into the new
                # setpoint and release the grasp on the first feedback update.
                left_endpoint = np.asarray(
                    step.get(
                        "left_endpoint_target", step["start_left_endpoint_target"]
                    ),
                    dtype=float,
                ).copy()
                right_endpoint = np.asarray(
                    step.get(
                        "right_endpoint_target", step["start_right_endpoint_target"]
                    ),
                    dtype=float,
                ).copy()
                left_endpoint[0] = float(
                    step["start_left_endpoint_target"][0] - actual_retreat
                )
                right_endpoint[0] = float(
                    step["start_right_endpoint_target"][0] - actual_retreat
                )
                if tracking_lag > 0.0:
                    tow_offset = float(np.clip(0.20 * tracking_lag, 0.0, 0.010))
                    left_endpoint[0] -= tow_offset
                    right_endpoint[0] -= tow_offset
                left_endpoint[2] = float(
                    step["start_left_endpoint_target"][2] + retreat_lift
                )
                right_endpoint[2] = float(
                    step["start_right_endpoint_target"][2] + retreat_lift
                )
                # Maintain normal force while adding a little more preload
                # when the package starts to lag behind the retreat.
                target_retreat_load = 14.5 + float(
                    np.clip(90.0 * max(0.0, tracking_lag - 0.010), 0.0, 3.5)
                )
                if retreat_compression > 0.0048 or max(left_load, right_load) > 18.0:
                    left_endpoint[1] += 0.0003
                    right_endpoint[1] -= 0.0003
                else:
                    if left_load < target_retreat_load:
                        left_endpoint[1] -= 0.0005
                    if right_load < target_retreat_load:
                        right_endpoint[1] += 0.0005
                try:
                    corrected_left_q = sim_node.solveArmEndTarget(
                        world_to_base(left_endpoint),
                        sim_node.arm_action,
                        "l",
                        np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                        left_grip_rot,
                    )
                    corrected_right_q = sim_node.solveArmEndTarget(
                        world_to_base(right_endpoint),
                        sim_node.arm_action,
                        "r",
                        np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                        right_grip_rot,
                    )
                    sim_node.tctr_left_arm[:] = corrected_left_q
                    sim_node.tctr_right_arm[:] = corrected_right_q
                    # Persist the force-loop correction.  Otherwise the fixed
                    # retreat target at the top of this state overwrites it on
                    # the next simulation step and silently disables feedback.
                    step["left_arm_q"] = np.asarray(corrected_left_q, dtype=float).copy()
                    step["right_arm_q"] = np.asarray(corrected_right_q, dtype=float).copy()
                    step["left_endpoint_target"] = left_endpoint.copy()
                    step["right_endpoint_target"] = right_endpoint.copy()
                    sim_node.set_left_arm_new_target = True
                    sim_node.set_right_arm_new_target = True
                    update_joint_move_ratio()
                except ValueError as exc:
                    print(f">>> retreat preload IK stopped: {exc}")
            bilateral = left_load >= 0.05 and right_load >= 0.05
            safe_contact = not retreat_report["nonfinger_contacts"]
            step["loss_streak"] = (
                0 if bilateral and safe_contact else int(step["loss_streak"]) + 1
            )
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            if now - float(step.get("last_physics_diagnostic", -1.0e9)) >= 0.75:
                step["last_physics_diagnostic"] = float(now)
                total_tangent = sum(
                    float(detail.get("tangent_force", 0.0))
                    for detail in retreat_report["contact_details"]
                    if detail.get("body", "").startswith(("lft_finger", "rgt_finger"))
                )
                box_dof_adr = int(
                    sim_node.mj_model.jnt_dofadr[
                        sim_node.mj_model.body_jntadr[box_body_id_physics]
                    ]
                )
                print(
                    ">>> retreat physics: "
                    f"progress={progress:.2f}, normal=({left_load:.2f}, {right_load:.2f})N, "
                    f"pad_tangent={total_tangent:.2f}N, "
                    f"box_v={np.round(sim_node.mj_data.qvel[box_dof_adr:box_dof_adr + 3], 4)}"
                )
            expected_box_x = float(
                step["start_box"][0] - actual_retreat
            )
            pull_lag = float(box_now[0] - expected_box_x)
            lateral_slip = abs(float(box_now[1] - step["start_box"][1]))
            vertical_drop = float(step["start_box"][2] - box_now[2])
            # Slip outer loop: increase pad force only when the carton begins
            # to settle after leaving the shelf.  This preserves a gentle
            # nominal grip but supplies a higher friction margin under load.
            if vertical_drop > 0.004:
                physical_grip_target_load = float(
                    np.clip(
                        max(
                            physical_grip_target_load,
                            18.0 + 190.0 * (vertical_drop - 0.004),
                        ),
                        18.0,
                        28.0,
                    )
                )
            physical_grasp_validated = bool(
                bilateral
                and safe_contact
                and pull_lag <= 0.090
                and lateral_slip <= 0.035
                and vertical_drop <= 0.125
            )
            if physical_grasp_validated and actual_retreat >= 0.040:
                sim_node.physical_transport_verified = True
            fully_outside = bool(
                actual_retreat >= float(step["distance"])
                and box_now[0] <= sim_node.cabinet_front_x - 0.05
                and bilateral
                and safe_contact
                and retreat_compression <= 0.005
                and lateral_slip <= 0.035
                and vertical_drop <= 0.060
            )
            if fully_outside:
                base_lock_x = float(sim_node.sensor_base_position[0])
                action[:2] = 0.0
                sim_node.physical_transport_verified = True
                sim_node.physical_transport_completed = True
                physical_grasp_validated = True
                print(
                    ">>> physical extraction complete at measured shelf clearance; "
                    f"box={np.round(box_now, 4)}, base_retreat={actual_retreat:.4f}m, "
                    f"contact_normal=({left_load:.2f}, {right_load:.2f})N, "
                    f"compression={retreat_compression * 1000:.2f}mm"
                )
                print(
                    ">>> package extracted by physical contact and friction; "
                    "no weld, pose overwrite, or rigid-follow constraint used"
                )
                step_index += 1
                current_step_name = None
                continue
            if elapsed > 0.5 and (
                int(step["loss_streak"]) >= 300
                or pull_lag > 0.130
                or lateral_slip > 0.050
                or vertical_drop > 0.125
            ):
                print(
                    ">>> PHYSICAL RETREAT FAILED: clamp lost or package slipped; "
                    f"forces={ {name: round(force, 2) for name, force in retreat_report['forces'].items()} }; "
                    f"nonfinger={sorted(retreat_report['nonfinger_contacts'])}; "
                    f"elapsed={elapsed:.2f}, progress={progress:.2f}, "
                    f"box={np.round(box_now, 4)}; "
                    f"pull_lag={pull_lag:.4f}, lateral_slip={lateral_slip:.4f}, "
                    f"vertical_drop={vertical_drop:.4f} m"
                )
                physical_grasp_validated = False
                sim_node.physical_transport_verified = False
                sim_node.physical_transport_completed = False
                execution_steps = [
                    {"kind": "hold", "name": "physical clamp lost during retreat", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None
                continue
            if elapsed > float(step["duration"]) + 25.0 and progress < 1.0:
                print(
                    ">>> PHYSICAL RETREAT FAILED: wheel drive timeout; "
                    f"base_dx={-actual_retreat:.4f}, progress={progress:.2f}, "
                    f"wheel_qvel={np.round(sim_node.sensor_wheel_qvel, 3)}"
                )
                physical_grasp_validated = False
                sim_node.physical_transport_verified = False
                sim_node.physical_transport_completed = False
                execution_steps = [
                    {"kind": "hold", "name": "wheel retreat timeout", "duration": 1.0e9}
                ]
                step_index = 0
                current_step_name = None
                continue
            if progress >= 1.0:
                base_lock_x = float(sim_node.sensor_base_position[0])
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                expected_dx = -float(step["distance"])
                actual_dx = float(box_now[0] - step["start_box"][0])
                print(
                    ">>> physical clamp retreat complete; "
                    f"box={np.round(box_now, 4)}, dx={actual_dx:.4f} m, "
                    f"contact_normal=({left_load:.2f}, {right_load:.2f}) N, "
                    f"gripper_actuator=({float(sim_node.mj_data.actuator_force[gripper_actuator_ids[0]]):.2f}, "
                    f"{float(sim_node.mj_data.actuator_force[gripper_actuator_ids[1]]):.2f})"
                )
                if actual_dx > expected_dx + 0.12 or not physical_grasp_validated:
                    print(">>> PHYSICAL RETREAT FAILED: package did not remain clamped")
                    physical_grasp_validated = False
                    sim_node.physical_transport_verified = False
                    sim_node.physical_transport_completed = False
                    execution_steps = [
                        {"kind": "hold", "name": "package lost during retreat", "duration": 1.0e9}
                    ]
                    step_index = 0
                    current_step_name = None
                elif step.get("regrasp_after", False):
                    print(">>> supported partial extraction complete; beginning free-body regrasp")
                    execution_steps[step_index + 1:] = [
                        {"kind": "independent_release", "name": "release front-edge clamp", "duration": 0.8},
                        {"kind": "regrasp_center_move", "name": "move open fingers toward carton center", "duration": 2.2},
                        {"kind": "independent_reclamp", "name": "force-controlled center-wall reclamp", "duration": 3.0},
                        {
                            "kind": "grip_base_retreat",
                            "name": "finish extraction from centered wall grasp",
                            "distance": 0.20,
                            "duration": 4.0,
                            "left_arm_q": np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float).copy(),
                            "right_arm_q": np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float).copy(),
                        },
                        {"kind": "hold", "name": "hold outside cabinet", "duration": float(hold_seconds)},
                    ]
                    step_index += 1
                    current_step_name = None
                else:
                    print(
                        ">>> package extracted by physical contact and friction; "
                        "no weld, pose overwrite, or rigid-follow constraint used"
                    )
                    sim_node.physical_transport_completed = True
                    step_index += 1
                    current_step_name = None

        elif step["kind"] == "physical_success":
            verified_box_pose = np.asarray(
                get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3], dtype=float
            ).copy()
            verified_report = sim_node.wall_grasp_report()
            left_verified = float(
                verified_report["forces"]["lft_finger_left_link"]
                + verified_report["forces"]["lft_finger_right_link"]
            )
            right_verified = float(
                verified_report["forces"]["rgt_finger_left_link"]
                + verified_report["forces"]["rgt_finger_right_link"]
            )
            verified_max_compression = max(
                [-float(detail["distance"]) for detail in verified_report["contact_details"]]
                or [0.0]
            )
            all_four_verified = (
                all(float(force) >= 0.20 for force in verified_report["forces"].values())
                if wall_pinch_mode
                else (
                    left_verified >= 0.20 and right_verified >= 0.20
                    if simple_closed_gripper_mode
                    else all(float(force) >= 0.20 for force in verified_report["forces"].values())
                )
            )
            success = bool(
                verified_box_pose[0] <= sim_node.cabinet_front_x - 0.05
                and all_four_verified
                and not verified_report["nonfinger_contacts"]
                and verified_max_compression <= 0.005
                and sim_node.physical_transport_completed
            )
            print(
                "success check:",
                f"box_x={verified_box_pose[0]:.3f}",
                f"front_x={sim_node.cabinet_front_x:.3f}",
                f"box_z={verified_box_pose[2]:.3f}",
                f"bilateral_closed_contact={all_four_verified}",
                f"nonfinger={sorted(verified_report['nonfinger_contacts'])}",
                f"max_compression={verified_max_compression * 1000:.2f}mm",
                "physical_transport=True",
            )
            print(">>> RESULT:", "SUCCESS" if success else "FAILED")
            wam_observe(step, now, force=True)
            if success:
                execution_steps = [
                    {
                        "kind": "clamped_hover",
                        "name": "hold clamped package in air for 5s",
                        "duration": 5.0,
                    },
                    {
                        "kind": "slide_lower_before_return",
                        "name": "lower clamped package before shelf return",
                        "height": -0.01,
                        "duration": 0.2,
                    },
                    {
                        "kind": "grip_base_advance",
                        "name": "return clamped package back onto shelf",
                        "distance": 0.30,
                        "duration": 12.0,
                    },
                    {
                        "kind": "release_on_shelf",
                        "name": "release package on shelf",
                        "duration": 1.6,
                    },
                    {
                        "kind": "observe_return",
                        "name": "final hold after return-to-shelf attempt",
                        "duration": 1.0e9,
                    },
                ]
            else:
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "final hold after failed extraction",
                        "duration": 1.0e9,
                    }
                ]
            step_index = 0
            current_step_name = None
            continue

        elif step["kind"] == "clamped_hover":
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if "left_arm_q" not in step:
                step["left_arm_q"] = np.asarray(
                    sim_node.tctr_left_arm, dtype=float
                ).copy()
                step["right_arm_q"] = np.asarray(
                    sim_node.tctr_right_arm, dtype=float
                ).copy()
                step["start_box"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, 3].copy()
                step["last_hover_log"] = -1.0e9
                print(
                    f">>> {float(step['duration']):.0f}s clamped hover started; "
                    f"box={np.round(step['start_box'], 4)}"
                )
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()
            hover_report = sim_node.wall_grasp_report()
            left_load = float(
                hover_report["forces"]["lft_finger_left_link"]
                + hover_report["forces"]["lft_finger_right_link"]
            )
            right_load = float(
                hover_report["forces"]["rgt_finger_left_link"]
                + hover_report["forces"]["rgt_finger_right_link"]
            )
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            if now - float(step.get("last_hover_log", -1.0e9)) >= 5.0:
                step["last_hover_log"] = float(now)
                print(
                    ">>> hover check: "
                    f"elapsed={now - step_enter_time:.1f}s, "
                    f"box={np.round(box_now, 4)}, "
                    f"drop={float(step['start_box'][2] - box_now[2]):.4f}m, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
            if now - step_enter_time >= float(step["duration"]):
                print(
                    f">>> {float(step['duration']):.0f}s clamped hover complete; "
                    f"box={np.round(box_now, 4)}, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
                step_index += 1
                current_step_name = None
                continue

        elif step["kind"] == "closed_pair_cartesian_lower":
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if "start_left_endpoint_target" not in step:
                step["start_left_endpoint_target"] = np.asarray(
                    sim_node.mj_data.site("lft_endpoint").xpos, dtype=float
                ).copy()
                step["start_right_endpoint_target"] = np.asarray(
                    sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float
                ).copy()
                step["start_box"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, 3].copy()
                step["last_lower_log"] = -1.0e9
                initial_lower_report = sim_node.wall_grasp_report()
                step["filtered_lower_loads"] = np.asarray(
                    [
                        initial_lower_report["forces"]["lft_finger_left_link"]
                        + initial_lower_report["forces"]["lft_finger_right_link"],
                        initial_lower_report["forces"]["rgt_finger_left_link"]
                        + initial_lower_report["forces"]["rgt_finger_right_link"],
                    ],
                    dtype=float,
                )
                step["lower_y_offsets"] = np.zeros(2, dtype=float)
                step["last_lower_force_update"] = float(now)
                print(
                    ">>> lowering clamped package before return; "
                    f"requested={float(step['height']) * 100:.1f}cm, "
                    f"box={np.round(step['start_box'], 4)}"
                )
            elapsed = float(now - step_enter_time)
            alpha = min(1.0, max(0.0, elapsed / float(step["duration"])))
            lower_alpha = alpha * alpha * (3.0 - 2.0 * alpha)
            lower_dz = float(step["height"]) * lower_alpha
            left_target = np.asarray(
                step["start_left_endpoint_target"], dtype=float
            ).copy()
            right_target = np.asarray(
                step["start_right_endpoint_target"], dtype=float
            ).copy()
            left_target[2] -= lower_dz
            right_target[2] -= lower_dz

            filtered_loads = np.asarray(
                step.get("filtered_lower_loads", [12.0, 12.0]), dtype=float
            )
            if now - float(step.get("last_lower_force_update", -1.0e9)) >= 0.04:
                step["last_lower_force_update"] = float(now)
                target_lower_load = 13.0
                force_deltas = np.clip(
                    0.00005 * (target_lower_load - filtered_loads),
                    -0.00020,
                    0.00035,
                )
                lower_y_offsets = np.asarray(
                    step.get("lower_y_offsets", np.zeros(2)), dtype=float
                )
                lower_y_offsets[0] -= force_deltas[0]
                lower_y_offsets[1] += force_deltas[1]
                step["lower_y_offsets"] = np.clip(
                    lower_y_offsets, -0.004, 0.004
                )
            lower_y_offsets = np.asarray(step["lower_y_offsets"], dtype=float)
            left_target[1] += lower_y_offsets[0]
            right_target[1] += lower_y_offsets[1]

            try:
                sim_node.tctr_left_arm[:] = sim_node.solveArmEndTarget(
                    world_to_base(left_target),
                    sim_node.arm_action,
                    "l",
                    np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                    left_grip_rot,
                )
                sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                    world_to_base(right_target),
                    sim_node.arm_action,
                    "r",
                    np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                    right_grip_rot,
                )
                sim_node.set_left_arm_new_target = True
                sim_node.set_right_arm_new_target = True
                update_joint_move_ratio()
            except ValueError as exc:
                print(f">>> return lowering IK stopped: {exc}")
            lower_report = sim_node.wall_grasp_report()
            left_load = float(
                lower_report["forces"]["lft_finger_left_link"]
                + lower_report["forces"]["lft_finger_right_link"]
            )
            right_load = float(
                lower_report["forces"]["rgt_finger_left_link"]
                + lower_report["forces"]["rgt_finger_right_link"]
            )
            filtered_loads = 0.75 * filtered_loads + 0.25 * np.asarray(
                [left_load, right_load], dtype=float
            )
            step["filtered_lower_loads"] = filtered_loads
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            if now - float(step.get("last_lower_log", -1.0e9)) >= 0.8:
                step["last_lower_log"] = float(now)
                print(
                    ">>> return lower: "
                    f"progress={alpha:.2f}, "
                    f"box={np.round(box_now, 4)}, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
            lower_force_ok = left_load >= 8.0 and right_load >= 8.0
            lower_timeout = elapsed >= float(step["duration"]) + 1.2
            if alpha >= 1.0 and (lower_force_ok or lower_timeout):
                print(
                    ">>> clamped package lowered for shelf return; "
                    f"box={np.round(box_now, 4)}, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N, "
                    f"force_ok={lower_force_ok}"
                )
                step_index += 1
                current_step_name = None
                continue

        elif step["kind"] == "slide_lower_before_return":
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if "start_slide" not in step:
                step["start_slide"] = float(sim_node.sensor_slide_qpos[0])
                step["left_arm_q"] = np.asarray(
                    sim_node.tctr_left_arm, dtype=float
                ).copy()
                step["right_arm_q"] = np.asarray(
                    sim_node.tctr_right_arm, dtype=float
                ).copy()
                step["start_box"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, 3].copy()
                step["last_slide_lower_log"] = -1.0e9
                print(
                    ">>> slide-lowering clamped package before return; "
                    f"requested={float(step['height']) * 100:.1f}cm, "
                    f"box={np.round(step['start_box'], 4)}"
                )
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            elapsed = float(now - step_enter_time)
            alpha = min(1.0, max(0.0, elapsed / float(step["duration"])))
            lower_alpha = alpha * alpha * (3.0 - 2.0 * alpha)
            # Positive slide qpos moves the arm base downward in this MJCF.
            sim_node.tctr_slide[0] = float(
                np.clip(
                    float(step["start_slide"]) + float(step["height"]) * lower_alpha,
                    sim_node.mj_model.actuator_ctrlrange[2, 0],
                    sim_node.mj_model.actuator_ctrlrange[2, 1],
                )
            )
            sim_node.joint_move_ratio[:] = 1.0
            sim_node.joint_move_ratio[2] = 0.35
            lower_report = sim_node.wall_grasp_report()
            left_load = float(
                lower_report["forces"]["lft_finger_left_link"]
                + lower_report["forces"]["lft_finger_right_link"]
            )
            right_load = float(
                lower_report["forces"]["rgt_finger_left_link"]
                + lower_report["forces"]["rgt_finger_right_link"]
            )
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            if now - float(step.get("last_slide_lower_log", -1.0e9)) >= 0.6:
                step["last_slide_lower_log"] = float(now)
                print(
                    ">>> return slide-lower: "
                    f"progress={alpha:.2f}, "
                    f"slide={float(sim_node.sensor_slide_qpos[0]):.4f}, "
                    f"box={np.round(box_now, 4)}, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
            if alpha >= 1.0:
                print(
                    ">>> clamped package slide-lowered for shelf return; "
                    f"box={np.round(box_now, 4)}, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
                step_index += 1
                current_step_name = None
                continue

        elif step["kind"] == "grip_base_advance":
            drive_base_this_step = True
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if "start_x" not in step:
                step["start_x"] = float(sim_node.sensor_base_position[0])
                step["start_box"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, 3].copy()
                step["left_arm_q"] = np.asarray(
                    sim_node.tctr_left_arm, dtype=float
                ).copy()
                step["right_arm_q"] = np.asarray(
                    sim_node.tctr_right_arm, dtype=float
                ).copy()
                step["last_return_log"] = -1.0e9
                print(
                    ">>> return-to-shelf base advance started; "
                    f"box_start={np.round(step['start_box'], 4)}, "
                    f"distance={float(step['distance']):.3f}m"
                )
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()
            elapsed = float(now - step_enter_time)
            actual_advance = max(
                0.0,
                float(sim_node.sensor_base_position[0] - step["start_x"]),
            )
            progress = min(
                1.0,
                actual_advance / max(float(step["distance"]), 1.0e-6),
            )
            cruise_speed = float(step["distance"]) / max(
                float(step["duration"]), 1.0e-6
            )
            ramp_alpha = min(1.0, max(0.0, elapsed / 1.0))
            end_ramp_alpha = min(1.0, max(0.25, (1.0 - progress) / 0.08))
            speed_ramp = ramp_alpha * ramp_alpha * (3.0 - 2.0 * ramp_alpha)
            speed_ramp *= end_ramp_alpha * end_ramp_alpha * (
                3.0 - 2.0 * end_ramp_alpha
            )
            linear_speed = cruise_speed * speed_ramp if progress < 1.0 else 0.0
            quat = np.asarray(sim_node.sensor_base_orientation, dtype=float)
            yaw = math.atan2(
                2.0 * (quat[0] * quat[3] + quat[1] * quat[2]),
                1.0 - 2.0 * (quat[2] ** 2 + quat[3] ** 2),
            )
            angular_speed = -1.5 * yaw
            wheel_target = np.asarray(
                [
                    (linear_speed - angular_speed * sim_node.wheel_distance)
                    / sim_node.wheel_radius,
                    (linear_speed + angular_speed * sim_node.wheel_distance)
                    / sim_node.wheel_radius,
                ],
                dtype=float,
            )
            wheel_error = np.clip(
                wheel_target - np.asarray(sim_node.sensor_wheel_qvel, dtype=float),
                -2.5,
                2.5,
            )
            action[:2] = np.clip(
                7.5 * wheel_error,
                sim_node.mj_model.actuator_ctrlrange[:2, 0],
                sim_node.mj_model.actuator_ctrlrange[:2, 1],
            )
            return_report = sim_node.wall_grasp_report()
            left_load = float(
                return_report["forces"]["lft_finger_left_link"]
                + return_report["forces"]["lft_finger_right_link"]
            )
            right_load = float(
                return_report["forces"]["rgt_finger_left_link"]
                + return_report["forces"]["rgt_finger_right_link"]
            )
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            if now - float(step.get("last_return_log", -1.0e9)) >= 1.5:
                step["last_return_log"] = float(now)
                print(
                    ">>> return advance: "
                    f"progress={progress:.2f}, "
                    f"base_advance={actual_advance:.3f}m, "
                    f"box={np.round(box_now, 4)}, "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
            if progress >= 0.985 or (
                elapsed >= float(step["duration"]) + 2.0 and progress >= 0.94
            ):
                action[:2] = 0.0
                base_lock_x = float(sim_node.sensor_base_position[0])
                print(
                    ">>> return-to-shelf base advance complete; "
                    f"box={np.round(box_now, 4)}, "
                    f"base_advance={actual_advance:.3f}m"
                )
                step_index += 1
                current_step_name = None
                continue

        elif step["kind"] == "release_on_shelf":
            action[:2] = 0.0
            if "left_arm_q" not in step:
                step["left_arm_q"] = np.asarray(
                    sim_node.tctr_left_arm, dtype=float
                ).copy()
                step["right_arm_q"] = np.asarray(
                    sim_node.tctr_right_arm, dtype=float
                ).copy()
                step["start_box"] = get_body_tmat(
                    sim_node.mj_data, target_body_name
                )[:3, 3].copy()
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            release_alpha = min(
                1.0,
                max(0.0, (now - step_enter_time) / float(step["duration"])),
            )
            gripper_target = grip_close + (release_open - grip_close) * release_alpha
            sim_node.tctr_lft_gripper[:] = gripper_target
            sim_node.tctr_rgt_gripper[:] = gripper_target
            if release_alpha >= 1.0:
                box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
                print(
                    ">>> released package on shelf; "
                    f"box={np.round(box_now, 4)}, "
                    f"drop_after_return={float(step['start_box'][2] - box_now[2]):.4f}m"
                )
                step_index += 1
                current_step_name = None
                continue

        elif step["kind"] == "observe_return":
            action[:2] = 0.0
            sim_node.tctr_lft_gripper[:] = release_open
            sim_node.tctr_rgt_gripper[:] = release_open
            if "left_arm_q" not in step:
                step["left_arm_q"] = np.asarray(
                    sim_node.tctr_left_arm, dtype=float
                ).copy()
                step["right_arm_q"] = np.asarray(
                    sim_node.tctr_right_arm, dtype=float
                ).copy()
                step["last_observe_log"] = -1.0e9
            sim_node.tctr_left_arm[:] = step["left_arm_q"]
            sim_node.tctr_right_arm[:] = step["right_arm_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            if now - float(step.get("last_observe_log", -1.0e9)) >= 5.0:
                step["last_observe_log"] = float(now)
                print(
                    ">>> return observe: "
                    f"elapsed={now - step_enter_time:.1f}s, "
                    f"box={np.round(box_now, 4)}, "
                    f"gripper_target=({float(sim_node.tctr_lft_gripper[0]):.3f}, "
                    f"{float(sim_node.tctr_rgt_gripper[0]):.3f})"
                )

        elif step["kind"] == "post_extract_lift":
            lift_report = sim_node.wall_grasp_report()
            update_independent_finger_forces(lift_report, now)
            if "start_slide" not in step:
                step["start_slide"] = float(sim_node.sensor_slide_qpos[0])
                step["start_box_z"] = float(
                    get_body_tmat(sim_node.mj_data, target_body_name)[2, 3]
                )
            alpha = min(1.0, (now - step_enter_time) / float(step["duration"]))
            sim_node.tctr_slide[0] = float(
                np.clip(
                    step["start_slide"] - float(step["height"]) * alpha,
                    sim_node.mj_model.actuator_ctrlrange[2, 0],
                    sim_node.mj_model.actuator_ctrlrange[2, 1],
                )
            )
            sim_node.joint_move_ratio[2] = 2.5
            if alpha >= 1.0:
                verified_box_pose = np.asarray(
                    get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3],
                    dtype=float,
                ).copy()
                box_z = float(verified_box_pose[2])
                rise = box_z - float(step["start_box_z"])
                print(
                    ">>> post-extraction friction lift complete; "
                    f"box_rise={rise:.4f} m, box_z={box_z:.4f}"
                )
                if rise >= 0.050:
                    physical_grasp_validated = True
                    success = bool(
                        float(verified_box_pose[0]) <= sim_node.cabinet_front_x - 0.05
                        and box_z >= sim_node.box_start_z - 0.03
                        and sim_node.physical_transport_completed
                    )
                    print(
                        "success check:",
                        f"box_x={verified_box_pose[0]:.3f}",
                        f"front_x={sim_node.cabinet_front_x:.3f}",
                        f"box_z={box_z:.3f}",
                        f"start_z={sim_node.box_start_z:.3f}",
                        "physical_transport=True",
                    )
                    print(">>> RESULT:", "SUCCESS" if success else "FAILED")
                    wam_observe(step, now, force=True)
                    # End on the last verified finite state.  Continuing to
                    # integrate a completed task while four independent slide
                    # fingers sit on their joint limits can create a purely
                    # numerical QPOS blow-up and overwrite the valid result.
                    break
                else:
                    physical_grasp_validated = False
                    sim_node.physical_transport_completed = False
                    execution_steps = [{"kind": "hold", "name": "post-extraction lift failed", "duration": 1.0e9}]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "independent_release":
            independent_force_control_enabled = False
            for name, actuator_id in finger_force_actuators.items():
                sim_node.mj_data.ctrl[actuator_id] = -finger_closing_sign[name] * 10.0
            if now - step_enter_time >= float(step["duration"]):
                step_index += 1
                current_step_name = None

        elif step["kind"] == "regrasp_center_move":
            independent_force_control_enabled = False
            for name, actuator_id in finger_force_actuators.items():
                sim_node.mj_data.ctrl[actuator_id] = -finger_closing_sign[name] * 8.0
            if "left_q" not in step:
                box_now = np.asarray(get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3], dtype=float)
                left_target = np.asarray(sim_node.mj_data.site("lft_endpoint").xpos, dtype=float).copy()
                right_target = np.asarray(sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float).copy()
                # The pads are already near the carton centre in X.  The
                # destabilising offset is vertical: the temporary clamp sits
                # at the rim.  Keep wrist clearance in X and lower the clamp
                # line toward the free body's centre of mass after partial
                # extraction has cleared the shelf lip.
                centered_x = 0.5 * (float(left_target[0]) + float(right_target[0]))
                left_target[0] = centered_x
                right_target[0] = centered_x
                centered_z = float(box_now[2] + 0.035)
                left_target[2] = centered_z
                right_target[2] = centered_z
                step["left_q"] = sim_node.solveArmEndTarget(
                    world_to_base(left_target), sim_node.arm_action, "l",
                    np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float), left_grip_rot,
                )
                step["right_q"] = sim_node.solveArmEndTarget(
                    world_to_base(right_target), sim_node.arm_action, "r",
                    np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float), right_grip_rot,
                )
                print(
                    f">>> center-wall regrasp target x={centered_x:.4f}, "
                    f"z={centered_z:.4f}"
                )
            sim_node.tctr_left_arm[:] = step["left_q"]
            sim_node.tctr_right_arm[:] = step["right_q"]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()
            if now - step_enter_time >= float(step["duration"]):
                step_index += 1
                current_step_name = None

        elif step["kind"] == "independent_reclamp":
            if not independent_force_control_enabled:
                independent_force_control_enabled = True
                independent_force_last_time = now
            reclamp_report = sim_node.wall_grasp_report()
            update_independent_finger_forces(reclamp_report, now)
            if now - step_enter_time >= float(step["duration"]):
                forces = reclamp_report["forces"]
                valid = (
                    not reclamp_report["nonfinger_contacts"]
                    and all(float(force) >= 1.0 for force in forces.values())
                )
                print(
                    ">>> center-wall reclamp:",
                    {name: round(force, 2) for name, force in forces.items()},
                    f"nonfinger={sorted(reclamp_report['nonfinger_contacts'])}",
                )
                if valid:
                    next_step = execution_steps[step_index + 1]
                    next_step["left_arm_q"] = np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float).copy()
                    next_step["right_arm_q"] = np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float).copy()
                    step_index += 1
                    current_step_name = None
                else:
                    physical_grasp_validated = False
                    execution_steps = [{"kind": "hold", "name": "center-wall reclamp failed", "duration": 1.0e9}]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "regrasp_joint_path":
            # The temporary real grasp has already extracted the package. Keep
            # its validated pose fixed only during the hand-off, then release
            # this stabilization as soon as all four final finger contacts exist.
            sim_node.tctr_lft_gripper[:] = grip_open
            sim_node.tctr_rgt_gripper[:] = grip_open
            path = step["path"]
            elapsed = now - step_enter_time
            progress = min(1.0, elapsed / max(float(step["duration"]), 1.0e-6))
            if len(path) == 1:
                target_active = np.asarray(path[0], dtype=float)
            else:
                path_position = progress * (len(path) - 1)
                lower_index = min(int(math.floor(path_position)), len(path) - 2)
                alpha = path_position - lower_index
                target_active = (
                    (1.0 - alpha) * np.asarray(path[lower_index], dtype=float)
                    + alpha * np.asarray(path[lower_index + 1], dtype=float)
                )
            sim_node.tctr_left_arm[:] = target_active[:6]
            sim_node.tctr_right_arm[:] = target_active[6:]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()
            if progress >= 1.0:
                left_err = float(np.linalg.norm(sim_node.sensor_lft_arm_qpos - target_active[:6]))
                right_err = float(np.linalg.norm(sim_node.sensor_rgt_arm_qpos - target_active[6:]))
                settle_tolerance = 0.20 if "above front wall" in current_step_name else 0.33
                if max(left_err, right_err) < settle_tolerance:
                    print(
                        f">>> regrasp stage settled: {current_step_name}; "
                        f"errors=({left_err:.3f}, {right_err:.3f})"
                    )
                    step_index += 1
                    current_step_name = None
                elif now - step_enter_time >= float(step["duration"]) + float(step["settle_timeout"]):
                    print(
                        f">>> REGRASP MOVE FAILED: {current_step_name}; "
                        f"errors=({left_err:.3f}, {right_err:.3f})"
                    )
                    execution_steps = [{"kind": "hold", "name": "regrasp tracking failed", "duration": 1.0e9}]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "final_front_wall_align":
            sim_node.tctr_lft_gripper[:] = grip_open
            sim_node.tctr_rgt_gripper[:] = grip_open
            centers = sim_node.finger_geom_centers()
            box_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            left_wall_y = float(box_now[1] + box_half_width_y)
            right_wall_y = float(box_now[1] - box_half_width_y)
            left_x = [float(centers[n][1]) for n in ("lft_finger_left_link", "lft_finger_right_link")]
            right_x = [float(centers[n][1]) for n in ("rgt_finger_left_link", "rgt_finger_right_link")]
            margin = 0.006
            left_ok = min(left_x) < left_wall_y - margin and max(left_x) > left_wall_y + margin
            right_ok = min(right_x) < right_wall_y - margin and max(right_x) > right_wall_y + margin
            report = sim_node.wall_grasp_report()
            if report["nonfinger_contacts"]:
                print(">>> FINAL WALL ALIGN SAFETY STOP:", sorted(report["nonfinger_contacts"]))
                sim_node.print_gripper_geometry("unsafe final front-wall alignment")
                execution_steps = [{"kind": "hold", "name": "unsafe final regrasp", "duration": 1.0e9}]
                step_index = 0
                current_step_name = None
            elif left_ok and right_ok:
                print(">>> final front wall is inside both finger slots")
                step_index += 1
                current_step_name = None
            elif now - step_enter_time >= float(step["timeout"]):
                print(
                    ">>> FINAL WALL ALIGN FAILED:",
                    f"wall_y=({left_wall_y:.4f}, {right_wall_y:.4f}), "
                    f"left={left_x}, right={right_x}",
                )
                sim_node.print_gripper_geometry("final front-wall alignment failure")
                execution_steps = [{"kind": "hold", "name": "final wall align failed", "duration": 1.0e9}]
                step_index = 0
                current_step_name = None

        elif step["kind"] == "final_front_wall_clamp":
            alpha = min(1.0, (now - step_enter_time) / float(step["duration"]))
            target = grip_open + (grip_close - grip_open) * alpha
            sim_node.tctr_lft_gripper[:] = target
            sim_node.tctr_rgt_gripper[:] = target
            sim_node.joint_move_ratio[11] = 1.0
            sim_node.joint_move_ratio[18] = 1.0
            report = sim_node.wall_grasp_report()
            all_four = all(force >= 0.10 for force in report["forces"].values())
            if all_four and not report["nonfinger_contacts"]:
                final_front_wall_mode = True
                physical_grasp_validated = True
                print(">>> FINAL TRUE FRONT-WALL GRASP ACQUIRED by physical contact")
                print(">>> final forces:", {name: round(force, 2) for name, force in report["forces"].items()})
                sim_node.print_gripper_geometry("final true front-wall grasp")
                step_index += 1
                current_step_name = None
            elif now - step_enter_time >= float(step["duration"]) + 3.0:
                print(">>> FINAL FRONT-WALL GRASP FAILED:", {name: round(force, 2) for name, force in report["forces"].items()})
                sim_node.print_gripper_geometry("final front-wall clamp failure")
                execution_steps = [{"kind": "hold", "name": "final front-wall clamp failed", "duration": 1.0e9}]
                step_index = 0
                current_step_name = None

        elif step["kind"] == "wall_align":
            sim_node.tctr_lft_gripper[:] = grip_open
            sim_node.tctr_rgt_gripper[:] = grip_open
            report = sim_node.wall_grasp_report()
            box_align_now = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
            box_align_shift = float(
                np.linalg.norm(
                    np.asarray(box_align_now[:2], dtype=float)
                    - np.asarray(sim_node.box_start_pos[:2], dtype=float)
                )
            )
            if report["nonfinger_contacts"] or box_align_shift > 0.012:
                print(
                    ">>> WALL ALIGN FAILED: unsafe pre-clamp contact/motion; "
                    f"bodies={sorted(report['nonfinger_contacts'])}; "
                    f"box_xy_shift={box_align_shift:.4f} m"
                )
                for detail in report["contact_details"]:
                    print(
                        "    contact:",
                        f"body={detail['body']}",
                        f"geoms={detail['geom_pair']}",
                        f"pos={np.round(detail['position'], 4)}",
                        f"dist={detail['distance']:.6f}",
                        f"normal={detail.get('normal_force', float('nan')):.3f}"
                    )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "unsafe wall alignment - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
            else:
                if wall_align_target_world is None:
                    wall_align_target_world = [
                        np.asarray(sim_node.mj_data.site("lft_endpoint").xpos, dtype=float).copy(),
                        np.asarray(sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float).copy(),
                    ]

                box_tmat_now = get_body_tmat(sim_node.mj_data, target_body_name)
                box_pos_now = np.asarray(box_tmat_now[:3, 3], dtype=float)
                centers = sim_node.finger_geom_centers()
                required_names = (
                    "lft_finger_left_link",
                    "lft_finger_right_link",
                    "rgt_finger_left_link",
                    "rgt_finger_right_link",
                )
                if not all(name in centers for name in required_names):
                    raise RuntimeError("finger collision geometry is incomplete")

                left_mid = 0.5 * (
                    centers["lft_finger_left_link"]
                    + centers["lft_finger_right_link"]
                )
                right_mid = 0.5 * (
                    centers["rgt_finger_left_link"]
                    + centers["rgt_finger_right_link"]
                )
                # True side-wall clamp: each horizontal finger pair must place
                # one visible pad inside and one outside its Y-side wall.
                left_wall_y = float(box_pos_now[1] + box_half_width_y)
                right_wall_y = float(box_pos_now[1] - box_half_width_y)
                # The shared tendon shifts each slot centre inward by roughly
                # 10 mm while closing under load. Pre-compensate in the open
                # state so the *closed* visible pads centre on the wall.
                closure_center_bias = 0.0
                left_desired = left_wall_y + closure_center_bias
                right_desired = right_wall_y - closure_center_bias
                left_error = left_desired - float(left_mid[1])
                right_error = right_desired - float(right_mid[1])

                left_finger_projections = [
                    float(centers[name][1])
                    for name in ("lft_finger_left_link", "lft_finger_right_link")
                ]
                right_finger_projections = [
                    float(centers[name][1])
                    for name in ("rgt_finger_left_link", "rgt_finger_right_link")
                ]
                slot_margin = 0.010
                left_straddles = (
                    min(left_finger_projections) < left_wall_y - slot_margin
                    and max(left_finger_projections) > left_wall_y + slot_margin
                )
                right_straddles = (
                    min(right_finger_projections) < right_wall_y - slot_margin
                    and max(right_finger_projections) > right_wall_y + slot_margin
                )
                # A thin wall need not be exactly at the geometric midpoint of
                # the fully opened slot.  The safe prerequisite for closing is
                # that each wall lies strictly between its own two fingers;
                # the four individual contact forces below validate the clamp.
                alignment_tolerance = float(step.get("tolerance", 0.012))
                aligned = bool(
                    left_straddles
                    and right_straddles
                    and abs(left_error) <= alignment_tolerance
                    and abs(right_error) <= alignment_tolerance
                )
                wall_alignment_streak = wall_alignment_streak + 1 if aligned else 0

                if wall_alignment_streak >= 8:
                    print(
                        ">>> both package walls safely inside finger slots; "
                        f"errors=({left_error:.4f}, {right_error:.4f}) m"
                    )
                    step_index += 1
                    current_step_name = None
                elif step.get("auto_correct", False) and wall_align_pending:
                    left_joint_error = float(
                        np.linalg.norm(
                            sim_node.sensor_lft_arm_qpos - sim_node.tctr_left_arm
                        )
                    )
                    right_joint_error = float(
                        np.linalg.norm(
                            sim_node.sensor_rgt_arm_qpos - sim_node.tctr_right_arm
                        )
                    )
                    if (
                        max(left_joint_error, right_joint_error) < 0.08
                        or now - wall_align_pending_since > 1.5
                    ):
                        wall_align_pending = False
                elif (
                    step.get("auto_correct", False)
                    and now - wall_align_last_update >= 0.20
                ):
                    wall_align_last_update = now
                    corrections = (
                        float(np.clip(left_error, -0.008, 0.008)),
                        float(np.clip(right_error, -0.008, 0.008)),
                    )
                    wall_align_target_world[0][1] += corrections[0]
                    wall_align_target_world[1][1] += corrections[1]
                    left_base = world_to_base(wall_align_target_world[0])
                    right_base = world_to_base(wall_align_target_world[1])
                    try:
                        left_q = sim_node.solveArmEndTarget(
                            left_base,
                            sim_node.arm_action,
                            "l",
                            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                            left_grip_rot,
                        )
                        right_q = sim_node.solveArmEndTarget(
                            right_base,
                            sim_node.arm_action,
                            "r",
                            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                            right_grip_rot,
                        )
                        sim_node.tctr_left_arm[:] = left_q
                        sim_node.tctr_right_arm[:] = right_q
                        sim_node.set_left_arm_new_target = True
                        sim_node.set_right_arm_new_target = True
                        update_joint_move_ratio()
                        wall_align_pending = True
                        wall_align_pending_since = now
                    except ValueError as exc:
                        print(f">>> WALL ALIGN IK FAILED: {exc}")
                        execution_steps = [
                            {
                                "kind": "hold",
                                "name": "wall alignment IK failed - inspect scene",
                                "duration": 1.0e9,
                            }
                        ]
                        step_index = 0
                        current_step_name = None

                if (
                    current_step_name is not None
                    and now - step_enter_time >= float(step["timeout"])
                ):
                    print(
                        ">>> WALL ALIGN FAILED: timeout; "
                        f"errors=({left_error:.4f}, {right_error:.4f}) m; "
                        f"straddles=({left_straddles}, {right_straddles})"
                    )
                    sim_node.print_gripper_geometry("wall alignment timeout")
                    execution_steps = [
                        {
                            "kind": "hold",
                            "name": "wall alignment timeout - inspect scene",
                            "duration": 1.0e9,
                        }
                    ]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "wall_clamp":
            clamp_alpha = min(1.0, (now - step_enter_time) / float(step["duration"]))
            # Use the stock shared tendon only to reach its normal zero pose.
            # Beyond zero, independent per-finger forces below provide the
            # adaptive over-close without making both fingers drift together.
            gripper_target = max(
                0.0, grip_open + (grip_close - grip_open) * clamp_alpha
            )
            # Do not inherit near-zero gripper speed ratios from the preceding
            # arm-only path.  Both finger pairs must physically track the
            # closing command before contact can be evaluated.
            sim_node.joint_move_ratio[11] = 1.0
            sim_node.joint_move_ratio[18] = 1.0
            wall_report = sim_node.wall_grasp_report()
            if clamp_alpha < 1.0 and not all(
                force >= 0.20 for force in wall_report["forces"].values()
            ):
                force_grip_targets[:] = gripper_target
            else:
                force_grip_targets[:] = update_force_grip_targets(
                    wall_report, now
                )
            sim_node.tctr_lft_gripper[:] = force_grip_targets[0]
            sim_node.tctr_rgt_gripper[:] = force_grip_targets[1]
            if clamp_seat_targets_world is None:
                clamp_seat_targets_world = [
                    np.asarray(sim_node.mj_data.site("lft_endpoint").xpos, dtype=float).copy(),
                    np.asarray(sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float).copy(),
                ]
            minimum_finger_force = 0.10
            all_four = all(
                wall_report["forces"][name] >= minimum_finger_force
                for name in (
                    "lft_finger_left_link",
                    "lft_finger_right_link",
                    "rgt_finger_left_link",
                    "rgt_finger_right_link",
                )
            )
            safe_contact = not wall_report["nonfinger_contacts"]
            if not safe_contact:
                print(
                    ">>> WALL CLAMP SAFETY STOP: non-finger robot/package "
                    f"contact={sorted(wall_report['nonfinger_contacts'])}"
                )
                for detail in wall_report["contact_details"]:
                    if detail["body"] in wall_report["nonfinger_contacts"]:
                        print(
                            "    unsafe contact:",
                            f"body={detail['body']}",
                            f"geoms={detail['geom_pair']}",
                            f"pos={np.round(detail['position'], 4)}",
                            f"dist={detail['distance']:.6f}"
                        )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "unsafe wall clamp - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
                continue

            # Once mostly closed, independently centre each vertical finger
            # pair on its wall rim. If only the lower finger touches, lower
            # that hand; if only the upper finger touches, raise it. The step
            # is intentionally small and non-finger contact remains a hard stop.
            if (
                step.get("enable_seating", False)
                and
                clamp_alpha >= 1.0
                and now - step_enter_time >= float(step["duration"]) + 0.5
                and not all_four
                and now - clamp_seat_last_update >= 0.18
            ):
                clamp_seat_last_update = now
                force_pairs = (
                    (
                        wall_report["forces"]["lft_finger_left_link"],
                        wall_report["forces"]["lft_finger_right_link"],
                    ),
                    (
                        wall_report["forces"]["rgt_finger_left_link"],
                        wall_report["forces"]["rgt_finger_right_link"],
                    ),
                )
                # Determine upper/lower by current measured geometry rather
                # than relying on mirrored link naming.
                centers_now = sim_node.finger_geom_centers()
                arm_names = (
                    ("lft_finger_left_link", "lft_finger_right_link"),
                    ("rgt_finger_left_link", "rgt_finger_right_link"),
                )
                dz_updates = []
                for arm_index, names in enumerate(arm_names):
                    upper_name = max(names, key=lambda name: centers_now[name][2])
                    lower_name = min(names, key=lambda name: centers_now[name][2])
                    upper_force = wall_report["forces"][upper_name]
                    lower_force = wall_report["forces"][lower_name]
                    dz = 0.0
                    if lower_force >= minimum_finger_force and upper_force < minimum_finger_force:
                        dz = -0.002
                    elif upper_force >= minimum_finger_force and lower_force < minimum_finger_force:
                        dz = 0.002
                    clamp_seat_targets_world[arm_index][2] += dz
                    dz_updates.append(dz)
                if any(abs(dz) > 0.0 for dz in dz_updates):
                    try:
                        left_base = world_to_base(clamp_seat_targets_world[0])
                        right_base = world_to_base(clamp_seat_targets_world[1])
                        sim_node.tctr_left_arm[:] = sim_node.solveArmEndTarget(
                            left_base, sim_node.arm_action, "l",
                            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float), left_grip_rot,
                        )
                        sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                            right_base, sim_node.arm_action, "r",
                            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float), right_grip_rot,
                        )
                        sim_node.set_left_arm_new_target = True
                        sim_node.set_right_arm_new_target = True
                        update_joint_move_ratio()
                        print(
                            ">>> seating wall clamps: "
                            f"dz=({dz_updates[0]:+.3f}, {dz_updates[1]:+.3f}) m"
                        )
                    except ValueError as exc:
                        print(f">>> wall clamp seating IK skipped: {exc}")
            four_finger_contact_streak = (
                four_finger_contact_streak + 1 if all_four and safe_contact else 0
            )
            if four_finger_contact_streak >= 8:
                force_text = ", ".join(
                    f"{name}={wall_report['forces'][name]:.2f}"
                    for name in wall_report["forces"]
                )
                print(f">>> four-finger wall grasp acquired; {force_text} N")
                print(
                    ">>> force-control grip targets:",
                    np.round(force_grip_targets, 3),
                    f"desired_load={physical_grip_target_load:.1f} N/arm",
                )
                enable_differential_finger_compliance()
                physical_grasp_validated = True
                sim_node.print_gripper_geometry("temporary extraction grasp acquired")
                # Plan and execute directly from the measured wall-clamp pose.
                # The old opposing-arm squeeze used a joint preload offset;
                # applying it here would tilt the two independently seated
                # rim clamps and release their finger contacts.
                preload_offset = np.zeros(12, dtype=float)
                try:
                    transport_steps = [
                        {
                            "kind": "force_grip_settle",
                            "name": "settle compliant wall clamp",
                            "duration": 4.0,
                            "left_arm_q": np.asarray(action[5:11], dtype=float).copy(),
                            "right_arm_q": np.asarray(action[12:18], dtype=float).copy(),
                        },
                        {
                            "kind": "grip_base_retreat",
                            "name": "pull_box_with_two_front_wall_clamps",
                            "distance": 0.26,
                            "duration": 5.0,
                            "left_arm_q": np.asarray(
                                action[5:11], dtype=float
                            ).copy(),
                            "right_arm_q": np.asarray(
                                action[12:18], dtype=float
                            ).copy(),
                        },
                        {
                            "kind": "physical_success",
                            "name": "verify free-body extraction and four-pad contact",
                        },
                    ]
                    execution_steps[step_index + 1:] = transport_steps
                    step_index += 1
                    current_step_name = None
                except Exception as exc:
                    print(">>> wall-grasp transport planning failed")
                    print(f">>> failure: {type(exc).__name__}: {exc}")
                    execution_steps = [
                        {
                            "kind": "hold",
                            "name": "wall transport replan failed - inspect grasp",
                            "duration": 1.0e9,
                        }
                    ]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "force_grip_settle":
            if force_settle_centers_world is None:
                sim_node.tctr_left_arm[:] = step["left_arm_q"]
                sim_node.tctr_right_arm[:] = step["right_arm_q"]
                sim_node.set_left_arm_new_target = True
                sim_node.set_right_arm_new_target = True
            settle_report = sim_node.wall_grasp_report()
            if independent_finger_mode:
                independent_commands = update_independent_finger_forces(
                    settle_report, now
                )
                settle_targets = np.asarray(
                    [
                        0.5 * (
                            independent_commands["lft_finger_left_link"]
                            + independent_commands["lft_finger_right_link"]
                        ),
                        0.5 * (
                            independent_commands["rgt_finger_left_link"]
                            + independent_commands["rgt_finger_right_link"]
                        ),
                    ],
                    dtype=float,
                )
            else:
                settle_targets = update_force_grip_targets(settle_report, now)
                sim_node.tctr_lft_gripper[:] = settle_targets[0]
                sim_node.tctr_rgt_gripper[:] = settle_targets[1]
            loads = np.asarray(
                [
                    settle_report["forces"]["lft_finger_left_link"]
                    + settle_report["forces"]["lft_finger_right_link"],
                    settle_report["forces"]["rgt_finger_left_link"]
                    + settle_report["forces"]["rgt_finger_right_link"],
                ],
                dtype=float,
            )
            if force_settle_centers_world is None:
                force_settle_centers_world = [
                    np.asarray(sim_node.mj_data.site("lft_endpoint").xpos, dtype=float).copy(),
                    np.asarray(sim_node.mj_data.site("rgt_endpoint").xpos, dtype=float).copy(),
                ]
            if (not independent_finger_mode) and now - force_settle_last_center_time >= 0.20:
                force_settle_last_center_time = now
                box_now = np.asarray(
                    get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3],
                    dtype=float,
                )
                centers_now = sim_node.finger_geom_centers()
                left_mid_y = 0.5 * (
                    centers_now["lft_finger_left_link"][1]
                    + centers_now["lft_finger_right_link"][1]
                )
                right_mid_y = 0.5 * (
                    centers_now["rgt_finger_left_link"][1]
                    + centers_now["rgt_finger_right_link"][1]
                )
                force_settle_last_center_errors = np.asarray(
                    [
                        box_now[1] + box_half_width_y - left_mid_y,
                        box_now[1] - box_half_width_y - right_mid_y,
                    ],
                    dtype=float,
                )
                arm_names = (
                    ("lft_finger_left_link", "lft_finger_right_link"),
                    ("rgt_finger_left_link", "rgt_finger_right_link"),
                )
                force_balance_updates = []
                for arm_index, names in enumerate(arm_names):
                    low_name, high_name = sorted(
                        names, key=lambda name: centers_now[name][1]
                    )
                    force_difference = float(
                        settle_report["forces"][high_name]
                        - settle_report["forces"][low_name]
                    )
                    # Translate away from the stronger pad.  For a wall held
                    # between two fingers this unloads the compressed inner
                    # pad and seats the weak outer pad against the visible wall.
                    dy = float(np.clip(-0.00004 * force_difference, -0.0010, 0.0010))
                    force_settle_centers_world[arm_index][1] += dy
                    force_balance_updates.append(dy)
                force_settle_last_balance_updates = np.asarray(
                    force_balance_updates, dtype=float
                )
                try:
                    sim_node.tctr_left_arm[:] = sim_node.solveArmEndTarget(
                        world_to_base(force_settle_centers_world[0]),
                        sim_node.arm_action,
                        "l",
                        np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                        left_grip_rot,
                    )
                    sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                        world_to_base(force_settle_centers_world[1]),
                        sim_node.arm_action,
                        "r",
                        np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
                        right_grip_rot,
                    )
                    sim_node.set_left_arm_new_target = True
                    sim_node.set_right_arm_new_target = True
                    update_joint_move_ratio()
                except ValueError as exc:
                    print(f">>> force-balance centering IK skipped: {exc}")
            real_pad_contacts = all(
                "_pad_" in geom_name
                for detail in settle_report["contact_details"]
                if detail["body"] in settle_report["forces"]
                for geom_name in detail["geom_pair"]
                if geom_name.startswith(("lft_", "rgt_"))
            )
            max_compression = max(
                [-float(detail["distance"]) for detail in settle_report["contact_details"]]
                or [0.0]
            )
            if now - step_enter_time >= float(step["duration"]):
                valid = bool(
                    not settle_report["nonfinger_contacts"]
                    and all(force >= 0.20 for force in settle_report["forces"].values())
                    and np.all(loads >= 0.60 * physical_grip_target_load)
                    and real_pad_contacts
                    and max_compression <= 0.005
                )
                print(
                    ">>> compliant grip settle:",
                    f"loads={np.round(loads, 2)} N",
                    f"finger_forces={ {name: round(force, 2) for name, force in settle_report['forces'].items()} }",
                    f"center_error={np.round(force_settle_last_center_errors, 4)} m",
                    f"force_balance_dy={np.round(force_settle_last_balance_updates, 4)} m",
                    f"nonfinger={sorted(settle_report['nonfinger_contacts'])}",
                    f"targets={np.round(settle_targets, 3)}",
                    f"max_compression={max_compression * 1000:.2f} mm",
                    f"real_pads={real_pad_contacts}",
                )
                if valid:
                    step_index += 1
                    current_step_name = None
                else:
                    print(">>> COMPLIANT GRIP FAILED: force/contact gate not satisfied")
                    physical_grasp_validated = False
                    execution_steps = [
                        {"kind": "hold", "name": "compliant grip validation failed", "duration": 1.0e9}
                    ]
                    step_index = 0
                    current_step_name = None
            elif now - step_enter_time >= float(step["duration"]) + 4.0:
                force_text = ", ".join(
                    f"{name}={wall_report['forces'][name]:.2f}"
                    for name in wall_report["forces"]
                )
                position_text = ", ".join(
                    f"{name}={np.round(points, 4).tolist()}"
                    for name, points in wall_report["positions"].items()
                    if points
                )
                print(
                    f">>> WALL GRASP FAILED: four-finger contact missing; {force_text} N; "
                    f"nonfinger={sorted(wall_report['nonfinger_contacts'])}; "
                    f"contact_positions=({position_text}); "
                    f"gripper_q=({float(sim_node.sensor_lft_gripper_qpos[0]):.3f}, "
                    f"{float(sim_node.sensor_rgt_gripper_qpos[0]):.3f}); "
                    f"target=({float(sim_node.tctr_lft_gripper[0]):.3f}, "
                    f"{float(sim_node.tctr_rgt_gripper[0]):.3f}); "
                    f"action=({float(action[11]):.3f}, {float(action[18]):.3f}); "
                    f"mj_ctrl=({float(sim_node.mj_data.ctrl[11]):.3f}, "
                    f"{float(sim_node.mj_data.ctrl[18]):.3f}); "
                    f"raw_q=({np.round(sim_node.mj_data.qpos[18:20], 4)}, "
                    f"{np.round(sim_node.mj_data.qpos[26:28], 4)})"
                )
                sim_node.print_gripper_geometry("after wall clamp failure")
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "four-finger wall grasp failed - inspect scene",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None

        elif step["kind"] == "slide":
            sim_node.tctr_slide[0] = float(step["target"])
            sim_node.joint_move_ratio[:] = 1.0
            sim_node.joint_move_ratio[2] = float(step.get("speed", 4.0))
            if abs(float(sim_node.sensor_slide_qpos[0]) - float(step["target"])) < 0.01:
                step_index += 1
                current_step_name = None

        elif step["kind"] == "clamp":
            clamp_alpha = min(1.0, (now - step_enter_time) / step["duration"])
            gripper_target = grip_open + (grip_close - grip_open) * clamp_alpha
            sim_node.tctr_lft_gripper[:] = gripper_target
            sim_node.tctr_rgt_gripper[:] = gripper_target
            if clamp_alpha >= 1.0:
                sim_node.tctr_lft_gripper[:] = grip_close
                sim_node.tctr_rgt_gripper[:] = grip_close
                contact_sides = sim_node.box_gripper_contact_sides()
                if now - step_enter_time > step["duration"] + 0.6:
                    print(
                        ">>> clamp complete; starting symmetric contact search; "
                        f"initial contacts={sorted(contact_sides) or ['none']}"
                    )
                    step_index += 1
                    current_step_name = None

        elif step["kind"] == "hold":
            hold_report = sim_node.wall_grasp_report()
            if simple_closed_gripper_mode:
                sim_node.tctr_lft_gripper[:] = grip_close
                sim_node.tctr_rgt_gripper[:] = grip_close
            elif physical_grasp_validated:
                if independent_finger_mode:
                    update_independent_finger_forces(hold_report, now)
                else:
                    hold_targets = update_force_grip_targets(hold_report, now)
                    sim_node.tctr_lft_gripper[:] = hold_targets[0]
                    sim_node.tctr_rgt_gripper[:] = hold_targets[1]
            else:
                sim_node.tctr_lft_gripper[:] = grip_close
                sim_node.tctr_rgt_gripper[:] = grip_close
            if now - step_enter_time >= step["duration"]:
                success = sim_node.check_success()
                print(">>> RESULT:", "SUCCESS" if success else "FAILED")
                wam_observe(step, now, force=True)
                if not wam_dataset_flushed:
                    flushed = wam_recorder.flush(success)
                    visual_flushed = visual_recorder.flush(success)
                    wam_dataset_flushed = True
                    if flushed:
                        print(
                            f">>> WAM dataset: wrote {flushed} real MuJoCo samples "
                            f"to {Path(wam_dataset_path).resolve()}"
                        )
                    if visual_flushed:
                        print(
                            f">>> Visual WAM dataset: wrote {visual_flushed} frame-pair samples "
                            f"to {Path(visual_dataset_dir).resolve()}"
                        )
                step_index += 1
                current_step_name = None

        if not direct_action_this_step:
            for i in range(2, sim_node.njctrl):
                action[i] = step_func(
                    action[i],
                    sim_node.target_control[i],
                    1.30 * sim_node.joint_move_ratio[i] * sim_node.delta_t,
                )
        if not drive_base_this_step:
            action[0] = 0.0
            action[1] = 0.0
        obs, _, _, _, _ = sim_node.step(action)
        # MMK2Base consumes only its stock 19-element action. Differential
        # pad-force actuators are appended to the MJCF, so refresh them after
        # each step's stock-control update and before the next physics step.
        if independent_finger_mode and independent_force_control_enabled:
            update_independent_finger_forces(sim_node.wall_grasp_report(), float(sim_node.mj_data.time))

        # Manipulation is planned for a fixed base. Prevent contact forces from
        # making the mobile base drift and invalidating the collision plan.
        # During physical extraction the wheel dynamics must remain untouched,
        # otherwise MuJoCo cannot generate tangential pull at the finger pads.
        if not drive_base_this_step:
            sim_node.mj_data.qpos[0] = base_lock_x
            sim_node.mj_data.qpos[1] = base_lock_y
            sim_node.mj_data.qvel[0] = 0.0
            sim_node.mj_data.qvel[1] = 0.0
            mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)

    if wam_dataset_path is not None and not wam_dataset_flushed:
        success = bool(sim_node.check_success())
        flushed = wam_recorder.flush(success)
        visual_flushed = visual_recorder.flush(success)
        if flushed:
            print(
                f">>> WAM dataset: wrote {flushed} partial-episode samples "
                f"to {Path(wam_dataset_path).resolve()}"
            )
        if visual_flushed:
            print(
                f">>> Visual WAM dataset: wrote {visual_flushed} partial samples "
                f"to {Path(visual_dataset_dir).resolve()}"
            )
    elif visual_dataset_dir is not None and not wam_dataset_flushed:
        success = bool(sim_node.check_success())
        visual_flushed = visual_recorder.flush(success)
        if visual_flushed:
            print(
                f">>> Visual WAM dataset: wrote {visual_flushed} partial samples "
                f"to {Path(visual_dataset_dir).resolve()}"
            )

def fk_position(model, data, frame_id, q):
    pin.forwardKinematics(model, data, q)
    pin.updateFramePlacements(model, data)
    return data.oMf[frame_id].translation.copy()


def frame_position(model, data, frame_name):
    if not model.existFrame(frame_name):
        return None
    return data.oMf[model.getFrameId(frame_name)].translation.copy()


def clamp_to_limits(model, q):
    lower = model.lowerPositionLimit.copy()
    upper = model.upperPositionLimit.copy()
    invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
    lower[invalid] = -math.pi
    upper[invalid] = math.pi
    return np.clip(q, lower, upper)


def joint_indices(model, joint_names):
    q_indices = []
    v_indices = []
    for name in joint_names:
        jid = model.getJointId(name)
        if jid == 0:
            raise ValueError(f"joint not found: {name}")
        joint = model.joints[jid]
        if joint.nq != 1 or joint.nv != 1:
            raise ValueError(f"joint {name} is not 1-DoF, nq={joint.nq}, nv={joint.nv}")
        q_indices.append(joint.idx_q)
        v_indices.append(joint.idx_v)
    return np.array(q_indices, dtype=int), np.array(v_indices, dtype=int)


def make_full_configuration(model, base_position, slide_value=0.2):
    q = pin.neutral(model)
    if model.nq >= 7:
        q[0:3] = np.asarray(base_position, dtype=float)
        # Pinocchio free-flyer quaternion order is x, y, z, w.
        q[3:7] = np.array([0.0, 0.0, 0.0, 1.0])

    for joint_name in ("lft_wheel_joint", "rgt_wheel_joint"):
        jid = model.getJointId(joint_name)
        if jid != 0:
            q[model.joints[jid].idx_q : model.joints[jid].idx_q + 2] = 0.0

    if model.getJointId("slide_joint") != 0:
        sid = model.getJointId("slide_joint")
        q[model.joints[sid].idx_q] = slide_value

    return clamp_to_limits(model, q)


def extract_active_config(q_full, active_q_indices):
    return q_full[active_q_indices].copy()


def segment_hits_aabb(p0, p1, box, samples=16):
    for alpha in np.linspace(0.0, 1.0, samples):
        p = (1.0 - alpha) * p0 + alpha * p1
        if np.all(p >= box.minimum) and np.all(p <= box.maximum):
            return True
    return False


def chain_points(model, data, q, frame_names):
    pin.forwardKinematics(model, data, q)
    pin.updateFramePlacements(model, data)
    points = []
    for name in frame_names:
        if model.existFrame(name):
            points.append(data.oMf[model.getFrameId(name)].translation.copy())
    return [p for p in points if p is not None]


def robot_chains(model, data, q):
    chains = []
    left_chain = [
        "left_base_link",
        "left_link1",
        "left_link2",
        "left_link3",
        "left_link4",
        "left_link5",
        "left_link6",
        "left_flange",
    ]
    right_chain = [
        "right_base_link",
        "right_link1",
        "right_link2",
        "right_link3",
        "right_link4",
        "right_link5",
        "right_link6",
        "right_flange",
    ]
    body_chain = ["floating_base", "underboard_link", "skin_link", "agv_link"]

    for frame_names in (body_chain, left_chain, right_chain):
        pts = chain_points(model, data, q, frame_names)
        if len(pts) >= 2:
            chains.append(pts)
    return chains


def in_collision(model, data, q, obstacles, robot_radius=0.015):
    inflated_obstacles = [obstacle.inflated(robot_radius) for obstacle in obstacles]
    for chain in robot_chains(model, data, q):
        for p0, p1 in zip(chain[:-1], chain[1:]):
            for obstacle in inflated_obstacles:
                if segment_hits_aabb(p0, p1, obstacle):
                    return True
    return False


def edge_in_collision(model, data, q0, q1, obstacles, step=0.05):
    distance = np.linalg.norm(q1 - q0)
    steps = max(2, int(math.ceil(distance / step)))
    for alpha in np.linspace(0.0, 1.0, steps):
        q = (1.0 - alpha) * q0 + alpha * q1
        if in_collision(model, data, q, obstacles):
            return True
    return False


def solve_damped_least_squares_3d(jacobian, error, damping):
    rows = jacobian.tolist()
    err = error.tolist()

    a = [[0.0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            a[i][j] = sum(rows[i][k] * rows[j][k] for k in range(len(rows[i])))
        a[i][i] += damping

    b = err[:]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-10:
            return np.zeros(jacobian.shape[1])
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            b[col], b[pivot] = b[pivot], b[col]

        pivot_value = a[col][col]
        for j in range(col, 3):
            a[col][j] /= pivot_value
        b[col] /= pivot_value

        for row in range(3):
            if row == col:
                continue
            factor = a[row][col]
            for j in range(col, 3):
                a[row][j] -= factor * a[col][j]
            b[row] -= factor * b[col]

    dq = []
    for joint_col in range(len(rows[0])):
        dq.append(sum(rows[row][joint_col] * b[row] for row in range(3)))
    return np.array(dq, dtype=float)


def solve_arm_position_ik(
    model,
    data,
    frame_id,
    arm_q_indices,
    arm_v_indices,
    q_seed,
    target_pos,
    max_iter=400,
    tolerance=0.01,
):
    damping = 1e-4
    lower = model.lowerPositionLimit[arm_q_indices].copy()
    upper = model.upperPositionLimit[arm_q_indices].copy()
    invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
    lower[invalid] = -math.pi
    upper[invalid] = math.pi

    seeds = [q_seed.copy()]
    for scale in (0.03, 0.06, 0.10):
        for _ in range(3):
            q_try = q_seed.copy()
            q_try[arm_q_indices] += np.random.uniform(-scale, scale, size=len(arm_q_indices))
            q_try = clamp_to_limits(model, q_try)
            seeds.append(q_try)
    for _ in range(35):
        q_try = q_seed.copy()
        q_try[arm_q_indices] = np.random.uniform(lower, upper)
        seeds.append(q_try)

    for q_start in seeds:
        q = q_start.copy()
        for _ in range(max_iter):
            pin.forwardKinematics(model, data, q)
            pin.computeJointJacobians(model, data, q)
            pin.updateFramePlacements(model, data)

            ee_pos = data.oMf[frame_id].translation.copy()
            error = target_pos - ee_pos
            if np.linalg.norm(error) < tolerance:
                return clamp_to_limits(model, q), True

            full_jacobian = pin.computeFrameJacobian(
                model,
                data,
                q,
                frame_id,
                pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
            )
            jacobian = np.asarray(full_jacobian[:3, :][:, arm_v_indices], dtype=float).copy()

            dq = solve_damped_least_squares_3d(jacobian, error, damping)
            dq = np.clip(dq, -0.06, 0.06)

            for idx, delta in zip(arm_q_indices, dq):
                q[idx] += delta
            q = clamp_to_limits(model, q)

    return q_seed.copy(), False


def solve_dual_position_ik(
    model,
    data,
    left_frame_id,
    right_frame_id,
    active_q_indices,
    active_v_indices,
    q_seed,
    left_target,
    right_target,
    left_q_indices,
    left_v_indices,
    right_q_indices,
    right_v_indices,
    obstacles=None,
    max_sweeps=5,
    max_attempts=25,
):
    for attempt in range(max_attempts):
        q = q_seed.copy()
        if attempt > 0:
            q[active_q_indices] = random_active_configuration(model, active_q_indices)

        for _ in range(max_sweeps):
            q, left_ok = solve_arm_position_ik(
                model,
                data,
                left_frame_id,
                left_q_indices,
                left_v_indices,
                q,
                left_target,
                max_iter=240,
                tolerance=0.012,
            )
            q, right_ok = solve_arm_position_ik(
                model,
                data,
                right_frame_id,
                right_q_indices,
                right_v_indices,
                q,
                right_target,
                max_iter=240,
                tolerance=0.012,
            )
            if not (left_ok and right_ok):
                continue

            q = clamp_to_limits(model, q)
            if obstacles is None or not in_collision(model, data, q, obstacles):
                return q, True

    return q_seed.copy(), False


def nearest_node(nodes, q):
    distances = [np.linalg.norm(node - q) for node in nodes]
    return int(np.argmin(distances))


def steer(q_from, q_to, step_size):
    direction = q_to - q_from
    distance = np.linalg.norm(direction)
    if distance <= step_size:
        return q_to.copy()
    return q_from + direction / distance * step_size


def reconstruct_path(nodes, parents, goal_index):
    path = []
    index = goal_index
    while index is not None:
        path.append(nodes[index])
        index = parents[index]
    path.reverse()
    return path


def clamp_active(model, active_q, active_q_indices):
    q = pin.neutral(model)[active_q_indices]
    q[:] = active_q
    lower = model.lowerPositionLimit[active_q_indices].copy()
    upper = model.upperPositionLimit[active_q_indices].copy()
    invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
    lower[invalid] = -math.pi
    upper[invalid] = math.pi
    return np.clip(active_q, lower, upper)


def random_active_configuration(model, active_q_indices):
    lower = model.lowerPositionLimit[active_q_indices].copy()
    upper = model.upperPositionLimit[active_q_indices].copy()
    invalid = ~np.isfinite(lower) | ~np.isfinite(upper) | (upper - lower > 20.0)
    lower[invalid] = -math.pi
    upper[invalid] = math.pi
    return np.random.uniform(lower, upper)


def active_to_full(q_template, q_active, active_q_indices):
    q = q_template.copy()
    q[active_q_indices] = q_active
    return q


def rrt_plan_active(
    model,
    data,
    q_template,
    active_q_indices,
    q_start_active,
    q_goal_active,
    obstacles,
    max_iter=7000,
    step_size=0.12,
    goal_sample_rate=0.22,
):
    q_start_full = active_to_full(q_template, q_start_active, active_q_indices)
    q_goal_full = active_to_full(q_template, q_goal_active, active_q_indices)
    if in_collision(model, data, q_start_full, obstacles):
        raise ValueError("q_start is in collision")
    if in_collision(model, data, q_goal_full, obstacles):
        raise ValueError("q_goal is in collision")
    if not edge_in_collision(model, data, q_start_full, q_goal_full, obstacles):
        return [q_start_active.copy(), q_goal_active.copy()]

    nodes = [q_start_active.copy()]
    parents = [None]

    for _ in range(max_iter):
        q_rand = q_goal_active if random.random() < goal_sample_rate else random_active_configuration(model, active_q_indices)
        nearest_index = nearest_node(nodes, q_rand)
        q_new = steer(nodes[nearest_index], q_rand, step_size)
        q_new = clamp_active(model, q_new, active_q_indices)

        q_near_full = active_to_full(q_template, nodes[nearest_index], active_q_indices)
        q_new_full = active_to_full(q_template, q_new, active_q_indices)
        if edge_in_collision(model, data, q_near_full, q_new_full, obstacles):
            continue

        nodes.append(q_new)
        parents.append(nearest_index)
        new_index = len(nodes) - 1

        if np.linalg.norm(q_new - q_goal_active) < step_size:
            q_new_full = active_to_full(q_template, q_new, active_q_indices)
            if not edge_in_collision(model, data, q_new_full, q_goal_full, obstacles):
                nodes.append(q_goal_active.copy())
                parents.append(new_index)
                return reconstruct_path(nodes, parents, len(nodes) - 1)

    raise RuntimeError("RRT failed to find a collision-free path")


def smooth_path_active(model, data, q_template, active_q_indices, path, obstacles, attempts=120):
    path = [q.copy() for q in path]
    if len(path) <= 2:
        return path

    for _ in range(attempts):
        if len(path) <= 2:
            break
        i, j = sorted(random.sample(range(len(path)), 2))
        if j <= i + 1:
            continue
        q_i_full = active_to_full(q_template, path[i], active_q_indices)
        q_j_full = active_to_full(q_template, path[j], active_q_indices)
        if not edge_in_collision(model, data, q_i_full, q_j_full, obstacles):
            path = path[: i + 1] + path[j:]
    return path


def interpolate_active_path(path, max_step=0.03):
    dense_path = []
    for q0, q1 in zip(path[:-1], path[1:]):
        distance = np.linalg.norm(q1 - q0)
        steps = max(2, int(math.ceil(distance / max_step)))
        for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
            dense_path.append((1.0 - alpha) * q0 + alpha * q1)
    dense_path.append(path[-1].copy())
    return dense_path


def build_cabinet_obstacles(box_center):
    """Return the code-2 cabinet approximation used by the collision planner."""
    box_center = np.asarray(box_center, dtype=float)
    cabinet_center = np.array([box_center[0], box_center[1], 0.0])
    return [
        AABB(
            "cabinet_left_side",
            cabinet_center + np.array([-0.15, 0.39, 0.00]),
            cabinet_center + np.array([0.15, 0.41, 2.03]),
        ),
        AABB(
            "cabinet_right_side",
            cabinet_center + np.array([-0.15, -0.41, 0.00]),
            cabinet_center + np.array([0.15, -0.39, 2.03]),
        ),
        AABB(
            "cabinet_back",
            cabinet_center + np.array([0.13, -0.40, 0.00]),
            cabinet_center + np.array([0.15, 0.40, 2.03]),
        ),
        AABB(
            "lower_shelf",
            cabinet_center + np.array([-0.15, -0.40, 0.72]),
            cabinet_center + np.array([0.15, 0.40, 0.74]),
        ),
        AABB(
            "upper_shelf",
            cabinet_center + np.array([-0.15, -0.40, 1.05]),
            cabinet_center + np.array([0.15, 0.40, 1.07]),
        ),
    ]


def compute_dual_box_pick_targets(
    box_center,
    box_yaw=0.0,
    cabinet_front_x=0.48,
    box_half_width_y=DEFAULT_BOX_HALF_WIDTH_Y,
    pre_clearance=0.050,
    grasp_clearance=0.000,
    lift_delta=0.030,
    side_axis=None,
):
    """Build approach targets and rigid post-grasp transport targets.

    The approach now enters from the front low lip of the box at equal left/right
    depth, then closes on the two short-side walls. After grasping, *both hands
    receive exactly the same XYZ translation*, so their separation vector and
    grasp geometry are preserved.
    """
    box_center = np.asarray(box_center, dtype=float)
    if side_axis is None:
        axis = np.array([-math.sin(box_yaw), math.cos(box_yaw), 0.0], dtype=float)
    else:
        axis = np.asarray(side_axis, dtype=float).copy()
        axis[2] = 0.0
    if np.linalg.norm(axis) < 1e-6:
        axis = np.array([0.0, 1.0, 0.0])
    axis /= np.linalg.norm(axis)

    outside_x = cabinet_front_x - 0.16
    mouth_x = cabinet_front_x - 0.035
    inside_x = box_center[0] - DEFAULT_BOX_HALF_DEPTH_X - 0.030
    # Keep the wrist housing in front of the package.  Only the visible pad
    # segments extend past the front plane and along the side walls.
    # With the reachable wrist-outside pose, the visible fingers extend roughly
    # 35-40 mm toward the robot from the endpoint.  Put the endpoint deeper so
    # the resulting contact patch lies on the vertical side-wall face, not on
    # the front rim/corner where it cannot generate an opposing clamp.
    # Horizontal-entry experiment: move the endpoint 105 mm behind the front
    # face while locking vertical wrist pitch to 0 deg in grip_turn_candidates.
    grasp_x = box_center[0] - DEFAULT_BOX_HALF_DEPTH_X + 0.105
    wall_slot_front_x = grasp_x
    retreat_x = cabinet_front_x - 0.20

    box_bottom_z = float(box_center[2])
    box_top_z = box_bottom_z + DEFAULT_BOX_HEIGHT
    # First center the open slot above the visible rim, then descend vertically.
    # Lateral motion at wall height would make the inner pad collide with the
    # outside face before it can enter the box.
    # Keep the broad wrist housing above the rim; the opened finger meshes
    # extend down around each wall and perform the actual pinch.
    grasp_z = box_top_z + 0.005
    slot_align_z = box_top_z + 0.055
    approach_z = slot_align_z + 0.025
    inside_z = approach_z
    approach_lateral = float(box_half_width_y + pre_clearance)
    grasp_lateral = float(box_half_width_y + grasp_clearance)

    def side_pair(x, z, lateral, left_inset=0.0, right_inset=0.0):
        center = np.array([x, box_center[1], z], dtype=float)
        point_a = center + axis * (lateral - float(left_inset))
        point_b = center - axis * (lateral - float(right_inset))
        if point_a[1] >= point_b[1]:
            left_point, right_point = point_a, point_b
        else:
            left_point, right_point = point_b, point_a
        return left_point, right_point

    outside_left, outside_right = side_pair(
        outside_x, approach_z, approach_lateral
    )
    mouth_left, mouth_right = side_pair(
        mouth_x, approach_z, approach_lateral
    )
    inside_high_left, inside_high_right = side_pair(
        inside_x, inside_z, box_half_width_y + pre_clearance
    )
    # Enter deeply while still spread safely outside the package sides.  Only
    # after this waypoint do the two arms squeeze laterally toward contact.
    deep_entry_left, deep_entry_right = side_pair(
        grasp_x, grasp_z, box_half_width_y + pre_clearance
    )
    squeeze_approach_left, squeeze_approach_right = side_pair(
        grasp_x, grasp_z, box_half_width_y + 0.006
    )
    squeeze_contact_left, squeeze_contact_right = side_pair(
        grasp_x, grasp_z, box_half_width_y - 0.002
    )
    grasp_left, grasp_right = side_pair(
        grasp_x,
        grasp_z,
        grasp_lateral,
    )
    # The mirrored toe-in lets the fingertips reach the wall while the wrist
    # bodies remain about 3 cm farther out.  The feedback clamp handles the
    # final millimetres symmetrically from this collision-free starting pose.
    wall_slot_left, wall_slot_right = side_pair(
        grasp_x,
        grasp_z,
        box_half_width_y + 0.020,
    )
    wall_slot_front_left, wall_slot_front_right = side_pair(
        wall_slot_front_x,
        slot_align_z,
        box_half_width_y + 0.045,
    )
    # Feedback-controlled fallback target.  Execution stops as soon as both
    # grippers have persistent package contact, so this is a maximum symmetric
    # inward travel rather than a pose that must always be reached.
    contact_seek_left, contact_seek_right = side_pair(
        grasp_x,
        grasp_z,
        max(0.020, grasp_lateral - 0.035),
    )

    inside_mid_left = (mouth_left + inside_high_left) * 0.5
    inside_mid_right = (mouth_right + inside_high_right) * 0.5

    # Once the grippers close, all subsequent target pairs are generated by
    # applying the same translation to the original grasp pair.
    lift_translation = np.array([0.0, 0.0, lift_delta])
    mouth_translation = np.array([mouth_x - grasp_x, 0.0, lift_delta])
    outside_translation = np.array([retreat_x - grasp_x, 0.0, lift_delta])

    transport_lift_left = grasp_left + lift_translation
    transport_lift_right = grasp_right + lift_translation
    transport_mouth_left = grasp_left + mouth_translation
    transport_mouth_right = grasp_right + mouth_translation
    transport_outside_left = grasp_left + outside_translation
    transport_outside_right = grasp_right + outside_translation

    return {
        "outside_left": outside_left,
        "outside_right": outside_right,
        "mouth_left": mouth_left,
        "mouth_right": mouth_right,
        "inside_mid_left": inside_mid_left,
        "inside_mid_right": inside_mid_right,
        "inside_high_left": inside_high_left,
        "inside_high_right": inside_high_right,
        "deep_entry_left": deep_entry_left,
        "deep_entry_right": deep_entry_right,
        "squeeze_approach_left": squeeze_approach_left,
        "squeeze_approach_right": squeeze_approach_right,
        "squeeze_contact_left": squeeze_contact_left,
        "squeeze_contact_right": squeeze_contact_right,
        "grasp_left": grasp_left,
        "grasp_right": grasp_right,
        "wall_slot_left": wall_slot_left,
        "wall_slot_right": wall_slot_right,
        "wall_slot_front_left": wall_slot_front_left,
        "wall_slot_front_right": wall_slot_front_right,
        "contact_seek_left": contact_seek_left,
        "contact_seek_right": contact_seek_right,
        "transport_lift_left": transport_lift_left,
        "transport_lift_right": transport_lift_right,
        "transport_mouth_left": transport_mouth_left,
        "transport_mouth_right": transport_mouth_right,
        "transport_outside_left": transport_outside_left,
        "transport_outside_right": transport_outside_right,
        # Backward-compatible aliases used by the optional plan visualizer.
        "lift_left": transport_lift_left,
        "lift_right": transport_lift_right,
        "retreat_left": transport_outside_left,
        "retreat_right": transport_outside_right,
    }


def plan_dual_grasp_sequence(
    model,
    data,
    left_frame_id,
    right_frame_id,
    q_start_full,
    active_q_indices,
    active_v_indices,
    left_q_indices,
    left_v_indices,
    right_q_indices,
    right_v_indices,
    stage_targets,
    obstacles,
):
    q_path_full = [q_start_full.copy()]
    q_current_full = q_start_full.copy()
    stage_configs = []
    pin.forwardKinematics(model, data, q_current_full)
    pin.updateFramePlacements(model, data)
    prev_left_target = data.oMf[left_frame_id].translation.copy()
    prev_right_target = data.oMf[right_frame_id].translation.copy()

    for name, left_target, right_target in stage_targets:
        q_goal_full, ik_ok = solve_dual_position_ik(
            model,
            data,
            left_frame_id,
            right_frame_id,
            active_q_indices,
            active_v_indices,
            q_current_full,
            left_target,
            right_target,
            left_q_indices,
            left_v_indices,
            right_q_indices,
            right_v_indices,
            obstacles=obstacles,
        )
        if not ik_ok:
            raise RuntimeError(
                f"failed to solve dual IK for stage {name}: "
                f"left={np.round(left_target, 3)}, right={np.round(right_target, 3)}"
            )

        q_start_active = extract_active_config(q_current_full, active_q_indices)
        q_goal_active = extract_active_config(q_goal_full, active_q_indices)
        try:
            segment_active = rrt_plan_active(
                model,
                data,
                q_current_full,
                active_q_indices,
                q_start_active,
                q_goal_active,
                obstacles,
                max_iter=9000,
                step_size=0.10,
                goal_sample_rate=0.30,
            )
            segment_active = smooth_path_active(
                model,
                data,
                q_current_full,
                active_q_indices,
                segment_active,
                obstacles,
                attempts=50,
            )
        except RuntimeError:
            print(f"RRT fallback: split Cartesian segment for stage {name}")
            segment_active = [q_start_active.copy()]
            q_bridge = q_current_full.copy()
            for alpha in np.linspace(0.2, 1.0, 5):
                left_mid = (1.0 - alpha) * prev_left_target + alpha * left_target
                right_mid = (1.0 - alpha) * prev_right_target + alpha * right_target
                q_next, bridge_ok = solve_dual_position_ik(
                    model,
                    data,
                    left_frame_id,
                    right_frame_id,
                    active_q_indices,
                    active_v_indices,
                    q_bridge,
                    left_mid,
                    right_mid,
                    left_q_indices,
                    left_v_indices,
                    right_q_indices,
                    right_v_indices,
                    obstacles=obstacles,
                    max_attempts=30,
                )
                if not bridge_ok or edge_in_collision(model, data, q_bridge, q_next, obstacles):
                    raise
                segment_active.append(extract_active_config(q_next, active_q_indices))
                q_bridge = q_next

        q_path_full.extend(
            [active_to_full(q_current_full, q_active, active_q_indices) for q_active in segment_active[1:]]
        )
        q_current_full = q_goal_full
        prev_left_target = left_target.copy()
        prev_right_target = right_target.copy()
        stage_configs.append((name, q_goal_full.copy(), left_target.copy(), right_target.copy()))
        print(f"stage {name}: left={np.round(left_target, 3)}, right={np.round(right_target, 3)}")

    return q_path_full, stage_configs


def arm_chain_points(model, data, q, side):
    if side == "left":
        frame_names = [
            "left_base_link",
            "left_link1",
            "left_link2",
            "left_link3",
            "left_link4",
            "left_link5",
            "left_link6",
            "left_flange",
        ]
    else:
        frame_names = [
            "right_base_link",
            "right_link1",
            "right_link2",
            "right_link3",
            "right_link4",
            "right_link5",
            "right_link6",
            "right_flange",
        ]
    return chain_points(model, data, q, frame_names)


def add_aabb_trace(fig, obstacle):
    mn = obstacle.minimum
    mx = obstacle.maximum
    x = [mn[0], mx[0], mx[0], mn[0], mn[0], mn[0], mx[0], mx[0], mn[0], mn[0], mx[0], mx[0], mx[0], mx[0], mn[0], mn[0]]
    y = [mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mn[1], mn[1], mn[1], mx[1], mx[1], mx[1], mx[1]]
    z = [mn[2], mn[2], mn[2], mn[2], mn[2], mx[2], mx[2], mx[2], mx[2], mx[2], mx[2], mn[2], mn[2], mx[2], mx[2], mn[2]]
    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines",
            line=dict(color="#4A5568", width=4),
            name=obstacle.name,
        )
    )


def visualize_trajectory(
    model,
    data,
    left_frame_id,
    right_frame_id,
    q_path,
    left_points,
    right_points,
    obstacles,
    stage_configs,
):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=left_points[:, 0],
            y=left_points[:, 1],
            z=left_points[:, 2],
            mode="lines+markers",
            line=dict(color="#2563EB", width=6),
            marker=dict(size=3, color="#2563EB", opacity=0.6),
            name="left ee path",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=right_points[:, 0],
            y=right_points[:, 1],
            z=right_points[:, 2],
            mode="lines+markers",
            line=dict(color="#EF4444", width=6),
            marker=dict(size=3, color="#EF4444", opacity=0.6),
            name="right ee path",
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[left_points[0, 0]],
            y=[left_points[0, 1]],
            z=[left_points[0, 2]],
            mode="markers",
            marker=dict(size=8, color="#10B981"),
            name="left start",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[right_points[0, 0]],
            y=[right_points[0, 1]],
            z=[right_points[0, 2]],
            mode="markers",
            marker=dict(size=8, color="#14B8A6"),
            name="right start",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[left_points[-1, 0]],
            y=[left_points[-1, 1]],
            z=[left_points[-1, 2]],
            mode="markers",
            marker=dict(size=8, color="#B91C1C"),
            name="left goal",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[right_points[-1, 0]],
            y=[right_points[-1, 1]],
            z=[right_points[-1, 2]],
            mode="markers",
            marker=dict(size=8, color="#7F1D1D"),
            name="right goal",
        )
    )

    for obstacle in obstacles:
        add_aabb_trace(fig, obstacle)

    for name, _q, left_target, right_target in stage_configs:
        fig.add_trace(
            go.Scatter3d(
                x=[left_target[0], right_target[0]],
                y=[left_target[1], right_target[1]],
                z=[left_target[2], right_target[2]],
                mode="markers+text",
                marker=dict(size=5, color="#111827"),
                text=[f"{name}-L", f"{name}-R"],
                textposition="top center",
                name=f"stage: {name}",
            )
        )

    snapshot_count = min(8, len(q_path))
    snapshot_indices = np.linspace(0, len(q_path) - 1, snapshot_count, dtype=int)
    for trace_idx, path_idx in enumerate(snapshot_indices):
        left_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "left"))
        right_chain = np.array(arm_chain_points(model, data, q_path[path_idx], "right"))
        if len(left_chain) >= 2:
            fig.add_trace(
                go.Scatter3d(
                    x=left_chain[:, 0],
                    y=left_chain[:, 1],
                    z=left_chain[:, 2],
                    mode="lines+markers",
                    line=dict(color="#1E293B", width=5),
                    marker=dict(size=3, color="#1E293B"),
                    opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
                    name="left arm snapshots" if trace_idx == 0 else None,
                    showlegend=trace_idx == 0,
                )
            )
        if len(right_chain) >= 2:
            fig.add_trace(
                go.Scatter3d(
                    x=right_chain[:, 0],
                    y=right_chain[:, 1],
                    z=right_chain[:, 2],
                    mode="lines+markers",
                    line=dict(color="#374151", width=5),
                    marker=dict(size=3, color="#374151"),
                    opacity=0.18 + 0.5 * trace_idx / max(1, snapshot_count - 1),
                    name="right arm snapshots" if trace_idx == 0 else None,
                    showlegend=trace_idx == 0,
                )
            )

    fig.update_layout(
        title="Dual-arm collision-aware grasp motion planning",
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)",
            aspectmode="data",
            camera=dict(eye=dict(x=1.9, y=1.8, z=1.25)),
        ),
        width=1000,
        height=760,
        margin=dict(l=0, r=0, t=50, b=0),
    )
    fig.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--urdf", default=DEFAULT_URDF_PATH)
    parser.add_argument(
        "--mjcf",
        default=DEFAULT_MJCF_FILE_PATH,
        help="DISCOVERSE MJCF scene file to display",
    )
    parser.add_argument(
        "--discoverse-root",
        default=DEFAULT_DISCOVERSE_ROOT,
        help="local DISCOVERSE source root used to open the MJCF task window",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="run the offline Pinocchio/RRT trajectory visualizer instead of MuJoCo execution",
    )
    parser.add_argument(
        "--headless-preview-seconds",
        type=float,
        default=None,
        help="run the MJCF auto-motion preview without a window for this many seconds",
    )
    parser.add_argument("--left-frame", default=LEFT_EEF_FRAME)
    parser.add_argument("--right-frame", default=RIGHT_EEF_FRAME)
    parser.add_argument("--base-position", nargs=3, type=float, default=[0.80, 0.238, 0.0])
    parser.add_argument("--slide", type=float, default=0.3)
    parser.add_argument("--box-center", nargs=3, type=float, default=[1.23, 0.238, 0.82])
    parser.add_argument("--box-yaw", type=float, default=0.0)
    parser.add_argument(
        "--wam-dataset",
        default=None,
        help="append compact MuJoCo state/action/outcome samples to this JSONL file",
    )
    parser.add_argument(
        "--wam-model",
        default=None,
        help="load a trained WAM critic and print predictions",
    )
    parser.add_argument(
        "--wam-branch-planning",
        action="store_true",
        help="evaluate bounded insertion candidates in copied MuJoCo states",
    )
    parser.add_argument(
        "--wam-rollout-horizon",
        type=float,
        default=1.8,
        help="simulated seconds per WAM branch candidate (default: 1.8)",
    )
    parser.add_argument(
        "--train-wam-critic",
        action="store_true",
        help="train the stage-1 critic from --wam-dataset and save to --wam-model",
    )
    parser.add_argument("--randomize-scene", action="store_true")
    parser.add_argument("--scene-seed", type=int, default=0)
    parser.add_argument("--wam-action-model", default=None)
    parser.add_argument("--train-wam-action", action="store_true")
    parser.add_argument("--visual-dataset-dir", default=None)
    parser.add_argument("--visual-model", default=None)
    parser.add_argument("--train-visual-wam", action="store_true")
    args = parser.parse_args()

    if args.train_wam_critic:
        if not args.wam_dataset or not args.wam_model:
            parser.error("--train-wam-critic requires --wam-dataset and --wam-model")
        from wam_critic import train_critic

        train_critic(args.wam_dataset, args.wam_model, epochs=800)
        return
    if args.train_wam_action:
        if not args.wam_dataset or not args.wam_action_model:
            parser.error("--train-wam-action requires --wam-dataset and --wam-action-model")
        from action_wam import train_action_critic

        train_action_critic(args.wam_dataset, args.wam_action_model)
        return
    if args.train_visual_wam:
        if not args.visual_dataset_dir or not args.visual_model:
            parser.error("--train-visual-wam requires --visual-dataset-dir and --visual-model")
        from visual_wam import train_visual_critic

        train_visual_critic(args.visual_dataset_dir, args.visual_model)
        return

    if not args.plan:
        run_box_pick_grasp_scene(
            args.mjcf,
            args.discoverse_root,
            urdf_path=args.urdf,
            headless=args.headless_preview_seconds is not None,
            max_seconds=args.headless_preview_seconds,
            wam_dataset_path=args.wam_dataset,
            wam_model_path=args.wam_model,
            wam_branch_planning=args.wam_branch_planning,
            wam_rollout_horizon=args.wam_rollout_horizon,
            randomize_scene=args.randomize_scene,
            scene_seed=args.scene_seed,
            wam_action_model_path=args.wam_action_model,
            visual_dataset_dir=args.visual_dataset_dir,
            visual_model_path=args.visual_model,
        )
        return

    global pin, go
    import pinocchio as pin
    import plotly.graph_objects as go

    if not Path(args.urdf).exists():
        raise FileNotFoundError(f"URDF file does not exist: {args.urdf}")

    model = pin.buildModelFromUrdf(args.urdf)
    data = model.createData()

    if not model.existFrame(args.left_frame):
        raise ValueError(f"Left frame not found: {args.left_frame}")
    if not model.existFrame(args.right_frame):
        raise ValueError(f"Right frame not found: {args.right_frame}")

    left_frame_id = model.getFrameId(args.left_frame)
    right_frame_id = model.getFrameId(args.right_frame)
    active_q_indices, active_v_indices = joint_indices(model, ACTIVE_JOINT_NAMES)
    left_q_indices = active_q_indices[:6]
    left_v_indices = active_v_indices[:6]
    right_q_indices = active_q_indices[6:]
    right_v_indices = active_v_indices[6:]

    print("model loaded")
    print(f"urdf: {args.urdf}")
    print(f"left frame: {args.left_frame}")
    print(f"right frame: {args.right_frame}")
    print(f"nq: {model.nq}, nv: {model.nv}")
    print(f"active joints: {ACTIVE_JOINT_NAMES}")

    q_start = make_full_configuration(model, args.base_position, args.slide)

    box_center = np.array(args.box_center, dtype=float)
    obstacles = build_cabinet_obstacles(box_center)
    pick_targets = compute_dual_box_pick_targets(
        box_center=box_center,
        box_yaw=args.box_yaw,
        cabinet_front_x=box_center[0] - 0.15,
    )
    stage_targets = [
        ("pregrasp", pick_targets["outside_left"], pick_targets["outside_right"]),
        ("mouth", pick_targets["mouth_left"], pick_targets["mouth_right"]),
        ("grasp_down", pick_targets["grasp_left"], pick_targets["grasp_right"]),
        ("lift", pick_targets["lift_left"], pick_targets["lift_right"]),
        ("retreat", pick_targets["retreat_left"], pick_targets["retreat_right"]),
    ]

    q_path, stage_configs = plan_dual_grasp_sequence(
        model,
        data,
        left_frame_id,
        right_frame_id,
        q_start,
        active_q_indices,
        active_v_indices,
        left_q_indices,
        left_v_indices,
        right_q_indices,
        right_v_indices,
        stage_targets,
        obstacles,
    )
    q_path = [q.copy() for q in q_path]
    q_path_dense = []
    for q0, q1 in zip(q_path[:-1], q_path[1:]):
        distance = np.linalg.norm(q1[active_q_indices] - q0[active_q_indices])
        steps = max(2, int(math.ceil(distance / 0.03)))
        for alpha in np.linspace(0.0, 1.0, steps, endpoint=False):
            q_path_dense.append((1.0 - alpha) * q0 + alpha * q1)
    q_path_dense.append(q_path[-1].copy())

    left_points = []
    right_points = []
    for q in q_path_dense:
        pin.forwardKinematics(model, data, q)
        pin.updateFramePlacements(model, data)
        left_points.append(data.oMf[left_frame_id].translation.copy())
        right_points.append(data.oMf[right_frame_id].translation.copy())

    left_points = np.array(left_points)
    right_points = np.array(right_points)

    print(f"planned joint samples: {len(q_path_dense)}")
    print(f"left ee start: {left_points[0]}")
    print(f"left ee goal:  {left_points[-1]}")
    print(f"right ee start: {right_points[0]}")
    print(f"right ee goal:  {right_points[-1]}")

    visualize_trajectory(
        model,
        data,
        left_frame_id,
        right_frame_id,
        q_path_dense,
        left_points,
        right_points,
        obstacles,
        stage_configs,
    )


if __name__ == "__main__":
    main()
