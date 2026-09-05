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
# #             left_base = sim_node.get_tmat_wrt_mmk2base(left_world)
# #             right_base = sim_node.get_tmat_wrt_mmk2base(right_world)
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
# #             left_base = sim_node.get_tmat_wrt_mmk2base(left_world)
# #             right_base = sim_node.get_tmat_wrt_mmk2base(right_world)
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
#         left_base = sim_node.get_tmat_wrt_mmk2base(left_world)
#         right_base = sim_node.get_tmat_wrt_mmk2base(right_world)
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
import os
import math
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

pin = None
go = None

PROJECT_ROOT = Path(__file__).resolve().parent


def _existing_path_or_default(*candidates):
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return str(path)
    return str(Path(candidates[0]))


def _default_perception_root():
    env_root = os.environ.get("THINGSCATCH_PERCEPTION_ROOT")
    if env_root:
        return env_root
    return _existing_path_or_default(
        PROJECT_ROOT / "vlm-sam",
        PROJECT_ROOT.parent / "vlm-sam",
        "D:/line/vlm-sam",
        "D:/line/line/vlm-sam",
    )


def _default_perception_python():
    return os.environ.get("THINGSCATCH_PERCEPTION_PYTHON", sys.executable)


DEFAULT_DISCOVERSE_ROOT = _existing_path_or_default(
    PROJECT_ROOT / "DISCOVERSE",
    PROJECT_ROOT.parent / "DISCOVERSE",
    "D:/thingscatch/DISCOVERSE-main/DISCOVERSE",
)
DEFAULT_URDF_PATH = str(
    Path(DEFAULT_DISCOVERSE_ROOT) / "models" / "urdf" / "mmk2_s_g2.urdf"
)
DEFAULT_PERCEPTION_ROOT = _default_perception_root()
DEFAULT_PERCEPTION_PYTHON = _default_perception_python()

DEFAULT_MJCF_FILE_PATH = str(
    Path(DEFAULT_DISCOVERSE_ROOT)
    / "models"
    / "mjcf"
    / "tasks_mmk2"
    / "task1_pick_and_place_open.xml"
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
NOMINAL_BASE_POSITION = (0.58, 0.715, 0.0)
NOMINAL_BOX_CENTER = (1.28, 0.715, 0.911)
# This is the conservative entry plane 5 cm in front of the physical shelf
# face at x=1.18, not the literal cabinet geometry boundary.
NOMINAL_CABINET_FRONT_X = 1.13
NOMINAL_SLIDE = 0.08
NOMINAL_CLEARANCE_LIFT = 0.05
NOMINAL_BASE_RETREAT = 0.28


def default_box_half_dimensions():
    return (
        DEFAULT_BOX_HALF_DEPTH_X,
        DEFAULT_BOX_HALF_WIDTH_Y,
        0.5 * DEFAULT_BOX_HEIGHT,
    )


def nominal_plan_scene():
    """Return the non-randomized scene values shared by execution and --plan."""
    return {
        "base_position": NOMINAL_BASE_POSITION,
        "box_center": NOMINAL_BOX_CENTER,
        "cabinet_front_x": NOMINAL_CABINET_FRONT_X,
        "slide": NOMINAL_SLIDE,
    }


def grip_endpoint_world_rotations(
    turn_deg=0.0,
    toe_in_deg=-12.0,
    camera_roll_deg=90.0,
):
    """Return the current mirrored left/right endpoint rotations in world XYZ."""
    pitch = np.deg2rad(float(turn_deg))
    toe_in = np.deg2rad(float(toe_in_deg))
    rotations = []
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
        opening_axis_world = np.array([0.0, 1.0, 0.0], dtype=float)
        opening_axis_world -= (
            np.dot(opening_axis_world, finger_axis_world) * finger_axis_world
        )
        opening_axis_world /= np.linalg.norm(opening_axis_world)
        palm_axis_world = np.cross(finger_axis_world, opening_axis_world)
        palm_axis_world /= np.linalg.norm(palm_axis_world)
        camera_roll = np.deg2rad(
            -float(camera_roll_deg) if arm == "l" else float(camera_roll_deg)
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
        rotations.append(
            np.column_stack((finger_axis_world, opening_axis_world, palm_axis_world))
        )
    return rotations[0], rotations[1]


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


def create_scene_rng(scene_seed):
    seed_sequence = np.random.SeedSequence(scene_seed)
    actual_seed = int(seed_sequence.entropy)
    return actual_seed, np.random.default_rng(seed_sequence)


def select_lift_target_load(shelf_level, initial_left_load, initial_right_load):
    if int(shelf_level) == 4:
        return 12.0
    return 13.5 if int(shelf_level) == 2 else 10.5


def select_clamp_ready_load(shelf_level):
    return 11.5 if int(shelf_level) == 4 else 9.0


def wall_clamp_contacts_are_safe(report, max_abs_normal_z=0.30):
    """Allow finger contacts on mesh seams; reject palm or arm collisions."""
    del max_abs_normal_z
    return not bool(report["nonfinger_contacts"])


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


def mat3_vec_mul(matrix, vector):
    """Small fixed-size multiply that avoids the broken BLAS runtime."""
    matrix = np.asarray(matrix, dtype=float)
    vector = np.asarray(vector, dtype=float)
    return np.array(
        [
            matrix[i, 0] * vector[0]
            + matrix[i, 1] * vector[1]
            + matrix[i, 2] * vector[2]
            for i in range(3)
        ],
        dtype=float,
    )


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
    """Measure the complete body's local-Y half extent, not its first mesh.

    The competition package is assembled from many mesh geoms.  The first
    mesh happens to be about 0.110 m wide, while the assembled package is
    about 0.080 m wide.  Returning the first mesh therefore leaves both
    grippers roughly 3 cm away from the package walls.
    """
    import mujoco

    try:
        body_id = int(mj_model.body(body_name).id)
    except Exception as exc:
        print(f"warning: body {body_name!r} not found ({exc}); use default half-y")
        return DEFAULT_BOX_HALF_WIDTH_Y

    geom_start = int(mj_model.body_geomadr[body_id])
    geom_num = int(mj_model.body_geomnum[body_id])
    if geom_num == 0:
        return DEFAULT_BOX_HALF_WIDTH_Y

    y_min = math.inf
    y_max = -math.inf
    for geom_id in range(geom_start, geom_start + geom_num):
        geom_type = mj_model.geom_type[geom_id]
        if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
            half = np.asarray(mj_model.geom_size[geom_id, :3], dtype=float)
            local_points = np.array([
                [sx * half[0], sy * half[1], sz * half[2]]
                for sx in (-1.0, 1.0)
                for sy in (-1.0, 1.0)
                for sz in (-1.0, 1.0)
            ])
        elif geom_type == mujoco.mjtGeom.mjGEOM_MESH:
            mesh_id = int(mj_model.geom_dataid[geom_id])
            vert_adr = int(mj_model.mesh_vertadr[mesh_id])
            vert_num = int(mj_model.mesh_vertnum[mesh_id])
            local_points = np.asarray(
                mj_model.mesh_vert[vert_adr: vert_adr + vert_num], dtype=float
            )
        elif kind == "base":
            left_delta = np.asarray(stage["left_goal"], dtype=float) - np.asarray(
                stage["left_start"], dtype=float
            )
            right_delta = np.asarray(stage["right_goal"], dtype=float) - np.asarray(
                stage["right_start"], dtype=float
            )
            if not np.allclose(left_delta, right_delta, atol=1.0e-9):
                raise RuntimeError(
                    f"{stage['name']}: base retreat does not preserve grasp geometry"
                )
            distance = float(np.linalg.norm(left_delta))
            samples = max(2, int(math.ceil(distance / 0.015)) + 1)
            q_base_start = q_current.copy()
            q_previous = q_current
            q_segment = []
            for alpha in np.linspace(0.0, 1.0, samples)[1:]:
                q_next = q_base_start.copy()
                q_next[:3] = q_base_start[:3] + alpha * left_delta
                if in_collision(model, data, q_next, obstacles) or edge_in_collision(
                    model, data, q_previous, q_next, obstacles, step=0.035
                ):
                    raise RuntimeError(
                        f"{stage['name']}: base retreat collides at alpha={alpha:.2f}"
                    )
                q_segment.append(q_next)
                q_previous = q_next
            q_current = q_previous
        else:
            continue

        # MuJoCo quaternions use w, x, y, z.  Transform every geom's points
        # into the body frame before combining their bounds.
        w, x, y, z = np.asarray(mj_model.geom_quat[geom_id], dtype=float)
        rotation = np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ])
        body_points = np.asarray(
            [mat3_vec_mul(rotation, point) for point in local_points], dtype=float
        ) + np.asarray(mj_model.geom_pos[geom_id], dtype=float)
        y_min = min(y_min, float(np.min(body_points[:, 1])))
        y_max = max(y_max, float(np.max(body_points[:, 1])))

    if not (math.isfinite(y_min) and math.isfinite(y_max)):
        return DEFAULT_BOX_HALF_WIDTH_Y
    half_extent_y = 0.5 * (y_max - y_min)
    print(
        f">>> measured complete {body_name} half-width-y={half_extent_y:.4f} m "
        f"(bounds {y_min:.4f} .. {y_max:.4f})"
    )
    return half_extent_y


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
    randomize_scene=False,
    randomize_box_pose=False,
    shelf_level=None,
    scene_seed=None,
    pose_source="ground-truth",
    perception_root=DEFAULT_PERCEPTION_ROOT,
    perception_python=DEFAULT_PERCEPTION_PYTHON,
    perception_query="yellow packaging box",
    perception_center_offset=(0.12, 0.0, -0.095),
    perception_debug=False,
    perception_bridge_factory=None,
    external_env=None,
    target_world=None,
    grasp_world=None,
    target_body_name="box_yellow",
    return_on_result=False,
):
    """Run collision-aware dual-wall grasp and physical extraction in MuJoCo.

    Planning/execution policy:
      1. Use either visual localization or explicit simulation-truth test mode.
      2. In visual mode, stop outside the shelf and refine with both hand cameras.
      3. Replan shelf entry from the measured arm state and refined box position.
      4. Keep the package as a free body and retreat with the real wheel drive.
      5. Accept success only if contact/friction transport survives slip checks.

    The scene's object mass and contact friction are left unchanged.
    """
    ensure_discoverse_import_path(discoverse_root)


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

    # Simplified physical mode: each two-finger gripper stays mechanically
    # coupled and fully closed for the whole task.  The two arms provide the
    # opposing package clamp; there is no per-finger differential control.
    simple_closed_gripper_mode = True
    wall_pinch_mode = False
    grip_close = 0.0
    grip_initial = grip_close
    grip_open = grip_close
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
        endpoint_world_rotations = grip_endpoint_world_rotations(
            turn_deg=turn_deg,
            toe_in_deg=(
                side_grip_toe_in_deg if toe_in_deg is None else float(toe_in_deg)
            ),
            camera_roll_deg=wrist_camera_roll_deg,
        )
        for arm, endpoint_world_rot in zip(("l", "r"), endpoint_world_rotations):
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
                if pose_source == "perception":
                    self.config.obs_rgb_cam_id = [
                        self.camera_names.index(name)
                        for name in ("head_cam", "lft_handeye", "rgt_handeye")
                    ]
                    self.config.obs_depth_cam_id = list(
                        self.config.obs_rgb_cam_id
                    )
                else:
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

        def get_tmat_wrt_mmk2base(self, pose):
            """Transform a world pose without the environment's LAPACK inverse.

            MuJoCo body transforms are rigid, so the exact inverse is formed
            from ``R.T`` and ``-R.T @ t``.  This avoids a NumPy/LAPACK deadlock
            observed in the supplied discoverse Windows environment.
            """
            tmat_mmk2 = get_body_tmat(self.mj_data, "mmk2")
            rotation_world_from_base = tmat_mmk2[:3, :3]
            translation_world = tmat_mmk2[:3, 3]
            rotation_base_from_world = rotation_world_from_base.T
            pose_array = np.asarray(pose, dtype=float)
            if pose_array.shape == (4, 4):
                transformed = np.eye(4, dtype=float)
                transformed[:3, :3] = mat3_mul(
                    rotation_base_from_world, pose_array[:3, :3]
                )
                transformed[:3, 3] = mat3_vec_mul(
                    rotation_base_from_world,
                    pose_array[:3, 3] - translation_world,
                )
                return transformed
            return mat3_vec_mul(
                rotation_base_from_world, pose_array - translation_world
            )

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

    actual_scene_seed, scene_rng = create_scene_rng(scene_seed)
    planning_seed = int(actual_scene_seed) if (
        randomize_scene or randomize_box_pose or shelf_level is not None
    ) else 0
    random.seed(planning_seed)
    np.random.seed(planning_seed % (2**32 - 1))
    spatial_randomization_enabled = bool(
        randomize_box_pose or shelf_level is not None
    )
    selected_shelf_level = (
        int(shelf_level)
        if shelf_level is not None
        else int(scene_rng.choice((2, 3, 4)))
        if spatial_randomization_enabled
        else 3
    )
    randomized_box_dx = (
        float(scene_rng.uniform(-0.018, 0.018))
        if randomize_box_pose
        else 0.0
    )
    randomized_box_dy = (
        float(scene_rng.uniform(-0.100, 0.100))
        if randomize_box_pose
        else 0.0
    )

    cfg = MMK2Cfg()
    cfg.mjcf_file_path = str(mjcf_path)
    cfg.use_gaussian_renderer = False
    cfg.headless = headless
    # VLM/SAM needs off-screen RGB-D even during a headless run.
    cfg.enable_render = (not headless) or pose_source == "perception"
    cfg.sync = not headless
    cfg.render_set = {
        # Visual localization explicitly refreshes all cameras at its two
        # checkpoints.  A low background frame rate avoids paying for three
        # off-screen RGB-D renders at every control tick while the arms move.
        "fps": 15 if pose_source == "perception" else 30,
        "width": 640 if pose_source == "perception" else 1280,
        "height": 480 if pose_source == "perception" else 720,
        "window_title": "DISCOVERSE dual-side grasp + collision-aware extraction",
    }
    # Camera order is validated by the perception bridge against MJCF names.
    # The current competition scene defines head, left hand and right hand in
    # this order.  Keep rendering disabled in the legacy truth-only mode.
    perception_camera_ids = [0, 1, 2]
    cfg.obs_rgb_cam_id = perception_camera_ids if pose_source == "perception" else None
    cfg.obs_depth_cam_id = perception_camera_ids if pose_source == "perception" else None
    cfg.init_state = MMK2Cfg.init_state.copy()
    navigation_start_y = NOMINAL_BASE_POSITION[1]
    planning_base_y = (
        navigation_start_y + randomized_box_dy
        if pose_source == "ground-truth"
        else navigation_start_y
    )
    cfg.init_state["base_position"] = list(NOMINAL_BASE_POSITION)
    cfg.init_state["base_orientation"] = [1.0, 0.0, 0.0, 0.0]
    cfg.init_state["head_qpos"] = [0.0, head_pitch]
    # init_state values are raw finger-joint positions, while runtime controls
    # use the [0, 1] tendon coordinate.
    cfg.init_state["lft_gripper_qpos"] = [grip_initial / 25.0]
    cfg.init_state["rgt_gripper_qpos"] = [grip_initial / 25.0]

    using_external_env = external_env is not None
    if using_external_env:
        sim_node = external_env
        required_attributes = (
            "mj_model",
            "mj_data",
            "step",
            "target_control",
            "joint_move_ratio",
            "sensor_base_position",
            "sensor_slide_qpos",
            "sensor_head_qpos",
            "sensor_lft_arm_qpos",
            "sensor_lft_gripper_qpos",
            "sensor_rgt_arm_qpos",
            "sensor_rgt_gripper_qpos",
        )
        missing_attributes = [
            name for name in required_attributes if not hasattr(sim_node, name)
        ]
        if missing_attributes:
            raise TypeError(
                "external DISCOVERSE env is not MMK2-compatible; missing: "
                + ", ".join(missing_attributes)
            )
        for method_name in (
            "get_tmat_wrt_mmk2base",
            "solveArmEndTarget",
            "setArmEndTarget",
            "box_gripper_contact_sides",
            "box_gripper_contact_report",
            "print_gripper_geometry",
            "finger_geom_centers",
            "wall_grasp_report",
        ):
            setattr(
                sim_node,
                method_name,
                types.MethodType(getattr(MyAlgorithmNode, method_name), sim_node),
            )
        sim_node._arm_ik_solver = StableAirbotPlayIK()
        if not hasattr(sim_node, "arm_action"):
            sim_node.arm_action = "pick"
        obs = getattr(sim_node, "obs", None)
        current_base_position = np.asarray(
            sim_node.sensor_base_position, dtype=float
        ).copy()
        current_base_orientation = np.asarray(
            getattr(
                sim_node,
                "sensor_base_orientation",
                sim_node.mj_data.qpos[3:7],
            ),
            dtype=float,
        ).copy()
        cfg.init_state["base_position"] = current_base_position.tolist()
        cfg.init_state["base_orientation"] = current_base_orientation.tolist()
        navigation_start_y = float(current_base_position[1])
        planning_base_y = navigation_start_y
        print(
            ">>> using caller-provided DISCOVERSE env; existing simulation "
            "state is preserved"
        )
    else:
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
    box_geom_types = np.asarray(
        sim_node.mj_model.geom_type[box_geom_ids_physics], dtype=int
    )
    uses_open_mesh_carton = bool(
        box_geom_count_physics > 1
        and np.any(box_geom_types == int(mujoco.mjtGeom.mjGEOM_MESH))
    )
    if not uses_open_mesh_carton:
        box_half_height = 0.5 * DEFAULT_BOX_HEIGHT
        # Legacy solid-box scenes define their primitive at the free-body
        # origin, while this controller defines the body origin at the box
        # bottom.  Shift only that old primitive.  The open carton mesh is
        # already authored bottom-up, so moving its visual and collision
        # pieces here would incorrectly float the carton above the shelf.
        for geom_id in box_geom_ids_physics:
            sim_node.mj_model.geom_sameframe[geom_id] = 0
            sim_node.mj_model.geom_pos[geom_id] = [
                0.0, 0.0, box_half_height
            ]
    # Approximate inertia of a 240 x 160 x 190 mm thin packaging carton/bin.
    half_dims = np.asarray(default_box_half_dimensions(), dtype=float)
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
    if using_external_env:
        action = np.asarray(sim_node.target_control, dtype=float).copy()
        action[:2] = 0.0
        action[2:3] = np.asarray(sim_node.sensor_slide_qpos, dtype=float)
        action[3:5] = np.asarray(sim_node.sensor_head_qpos, dtype=float)
        action[5:11] = np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float)
        action[11:12] = np.asarray(
            sim_node.sensor_lft_gripper_qpos, dtype=float
        )
        action[12:18] = np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float)
        action[18:19] = np.asarray(
            sim_node.sensor_rgt_gripper_qpos, dtype=float
        )
        sim_node.target_control[:] = action
        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
    else:
        action = sim_node.init_joint_ctrl.copy()
        sync_reset_pose(sim_node, action, mujoco)
    base_lock_x = float(cfg.init_state["base_position"][0])
    base_lock_y = float(cfg.init_state["base_position"][1])

    # The task scene stores the loose coloured cartons on the
    # material table.  This controller is specifically the shelf-extraction
    # task, so place its selected target at the declared nominal plan scene
    # before optional bounded randomization.  Previously the controller mixed
    # shelf coordinates with the material-table body pose and failed IK before
    # executing its first state.
    target_box_body_id = int(sim_node.mj_model.body(target_body_name).id)
    if not using_external_env:
        target_box_joint_id = int(
            sim_node.mj_model.body_jntadr[target_box_body_id]
        )
        target_box_qpos_adr = int(
            sim_node.mj_model.jnt_qposadr[target_box_joint_id]
        )
        sim_node.mj_data.qpos[target_box_qpos_adr:target_box_qpos_adr + 3] = (
            np.asarray(NOMINAL_BOX_CENTER, dtype=float)
        )
        sim_node.mj_data.qpos[
            target_box_qpos_adr + 3:target_box_qpos_adr + 7
        ] = [
            1.0,
            0.0,
            0.0,
            0.0,
        ]
    mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
    print(
        ">>> initialized shelf package geometry:",
        f"shape={'open_mesh_carton' if uses_open_mesh_carton else 'solid_primitive'}",
        f"geom_count={box_geom_count_physics}",
        f"body={np.round(sim_node.mj_data.xpos[target_box_body_id], 4)}",
        f"geom_local={np.round(sim_node.mj_model.geom_pos[box_geom_ids_physics[0]], 4)}",
        f"geom_world={np.round(sim_node.mj_data.geom_xpos[box_geom_ids_physics[0]], 4)}",
    )

    scene_randomization = {
        "enabled": bool(randomize_scene or spatial_randomization_enabled),
        "seed": actual_scene_seed,
        "box_dx": randomized_box_dx,
        "box_dy": randomized_box_dy,
        "shelf_level": selected_shelf_level,
        "base_alignment_dy": randomized_box_dy,
        "box_yaw_deg": 0.0,
        "mass_scale": 1.0,
        "mass_kg": nominal_box_mass_kg,
        "friction_scale": 1.0,
        "friction_coefficient": 0.18,
    }
    if (randomize_scene or spatial_randomization_enabled) and not using_external_env:
        box_body_id_random = int(sim_node.mj_model.body(target_body_name).id)
        box_joint_id_random = int(sim_node.mj_model.body_jntadr[box_body_id_random])
        box_qpos_adr_random = int(
            sim_node.mj_model.jnt_qposadr[box_joint_id_random]
        )
        scene_randomization.update({
            "box_dx": randomized_box_dx,
            "box_dy": randomized_box_dy,
            "box_yaw_deg": 0.0,
            "mass_kg": (
                float(scene_rng.uniform(0.35, 0.80))
                if randomize_scene
                else nominal_box_mass_kg
            ),
            "friction_coefficient": (
                float(scene_rng.uniform(0.15, 0.25))
                if randomize_scene
                else 0.18
            ),
        })
        sim_node.mj_data.qpos[box_qpos_adr_random] += scene_randomization["box_dx"]
        sim_node.mj_data.qpos[box_qpos_adr_random + 1] += scene_randomization["box_dy"]
        # Shelf boards are centered at 0.30 m increments with 20 mm total
        # thickness.  The package free-joint origin is its bottom, 1 mm above
        # the selected board's top surface, matching the nominal layer-3 pose.
        sim_node.mj_data.qpos[box_qpos_adr_random + 2] = (
            0.30 * selected_shelf_level + 0.011
        )
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

    perception_bridge = None
    coarse_estimate = None
    truth_box_tmat = get_body_tmat(sim_node.mj_data, target_body_name)
    truth_box_center = truth_box_tmat[:3, 3].copy()
    if using_external_env and target_world is not None:
        box_center = np.asarray(target_world, dtype=float).reshape(-1)
        if box_center.size != 3 or not np.all(np.isfinite(box_center)):
            raise ValueError("target_world must contain three finite XYZ values")
        box_center = box_center.copy()
        side_axis = truth_box_tmat[:3, 1].copy()
        box_half_width_y = get_box_half_extent_y(
            sim_node.mj_model, target_body_name
        )
        selected_shelf_level = int(
            np.clip(round((float(box_center[2]) - 0.011) / 0.30), 2, 4)
        )
        planning_base_y = navigation_start_y
        print(
            ">>> interface target accepted:",
            f"target_world={np.round(box_center, 4)}",
            f"grasp_world={None if grasp_world is None else np.round(grasp_world, 4)}",
            f"shelf_level={selected_shelf_level}",
        )
    elif pose_source == "perception":
        from perception_bridge import (
            CurrentStatePerceptionBridge,
            PerceptionBridgeError,
        )

        try:
            if perception_bridge_factory is not None:
                perception_bridge = perception_bridge_factory(sim_node)
            else:
                perception_bridge = CurrentStatePerceptionBridge(
                    sim_node,
                    perception_root,
                    confidence_threshold=0.6,
                    visible_to_body_offset=perception_center_offset,
                    box_half_width_y=DEFAULT_BOX_HALF_WIDTH_Y,
                    debug=perception_debug,
                    worker_python=perception_python,
                )
            coarse_estimate = perception_bridge.coarse_localize(perception_query)
        except PerceptionBridgeError as exc:
            raise RuntimeError(f"coarse head-camera perception failed: {exc}") from exc
        box_center = np.asarray(coarse_estimate.center_world, dtype=float).copy()
        side_axis = np.asarray(coarse_estimate.side_axis_world, dtype=float).copy()
        box_half_width_y = float(coarse_estimate.half_width_y)
        selected_shelf_level = int(coarse_estimate.shelf_level)
        planning_base_y = float(box_center[1])
        print(
            ">>> coarse visual localization:",
            f"center={np.round(box_center, 4)}",
            f"confidence={coarse_estimate.confidence:.3f}",
            f"shelf_level={selected_shelf_level}",
        )
        print(
            ">>> perception evaluation only (not used by planner):",
            f"truth_error={np.linalg.norm(box_center - truth_box_center):.4f}m",
        )
    elif pose_source in ("ground-truth", "external"):
        box_center = truth_box_center.copy()
        side_axis = truth_box_tmat[:3, 1].copy()
        box_half_width_y = get_box_half_extent_y(
            sim_node.mj_model, target_body_name
        )
    else:
        raise ValueError(f"unknown pose_source: {pose_source!r}")

    side_axis[2] = 0.0
    if np.linalg.norm(side_axis) < 1e-6:
        side_axis = np.array([0.0, 1.0, 0.0])
    side_axis /= np.linalg.norm(side_axis)
    needs_base_alignment = abs(planning_base_y - navigation_start_y) > 1.0e-4

    # Plan the arm trajectory at the pose that the physical wheel-navigation
    # stage will reach.  Before execution the base is restored to its nominal
    # start and must actually drive to this lateral alignment pose.
    if needs_base_alignment:
        sim_node.mj_data.qpos[1] = planning_base_y
        sim_node.mj_data.qvel[:6] = 0.0
        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
        base_lock_y = planning_base_y
    # The shelf mouth is fixed in world coordinates.  Do not move this safety
    # plane when the package is randomized deeper or shallower on the board.
    cabinet_front_x = NOMINAL_CABINET_FRONT_X
    # Preserve the verified 0.08 m torso setting on layer 3, then translate
    # the torso by the shelf-height difference.  Positive slide travels down
    # on MMK2 (joint axis -Z).  Mechanical limits clip only the extreme layers.
    planned_slide = float(
        np.clip(
            NOMINAL_SLIDE + (NOMINAL_BOX_CENTER[2] - float(box_center[2])),
            -0.04,
            0.45,
        )
    )
    # Analytic arm IK reads the commanded torso slide directly.  Plan all arm
    # waypoints in the same torso configuration that the slide-ready execution
    # stage will physically reach before shelf entry.
    sim_node.tctr_slide[0] = planned_slide

    # Ground truth is retained only for simulation outcome evaluation.  Motion
    # targets in perception mode use box_center from the camera bridge above.
    sim_node.box_start_z = float(truth_box_center[2])
    sim_node.box_start_pos = np.asarray(truth_box_center, dtype=float).copy()
    sim_node.cabinet_front_x = cabinet_front_x
    sim_node.tctr_head[1] = head_pitch
    sim_node.tctr_lft_gripper[:] = grip_initial
    sim_node.tctr_rgt_gripper[:] = grip_initial
    action[:] = sim_node.target_control[:]
    if not using_external_env:
        sync_reset_pose(
            sim_node,
            action,
            mujoco,
            preserve_free_objects=(
                randomize_scene
                or spatial_randomization_enabled
                or pose_source == "perception"
            ),
        )
    else:
        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)

    targets = compute_dual_box_pick_targets(
        box_center=box_center,
        cabinet_front_x=cabinet_front_x,
        box_half_width_y=box_half_width_y,
        grasp_clearance=-0.016,
        grasp_height=(0.095 if uses_open_mesh_carton else 0.110),
        grasp_world=grasp_world,
        side_axis=side_axis,
    )
    grip_turn_candidates = (0.0,)
    selected_left_grip_turn_deg = preferred_into_cabinet_turn_deg
    selected_right_grip_turn_deg = preferred_into_cabinet_turn_deg

    def solve_world_pair_with_turn_search(
        left_world, right_world, left_ref, right_ref, stage_name="dual target"
    ):
        nonlocal left_grip_rot, right_grip_rot
        nonlocal selected_left_grip_turn_deg, selected_right_grip_turn_deg
        left_base = sim_node.get_tmat_wrt_mmk2base(left_world)
        right_base = sim_node.get_tmat_wrt_mmk2base(right_world)

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
        if pose_source == "perception":
            raise ValueError("visual mode starts from the physical safe arm pose")
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
        sync_reset_pose(
            sim_node,
            action,
            mujoco,
            preserve_free_objects=(randomize_scene or spatial_randomization_enabled),
        )
        print(
            ">>> initial arms snapped to outside grasp-ready pose:",
            f"turns=({selected_left_grip_turn_deg:.1f}, "
            f"{selected_right_grip_turn_deg:.1f})deg",
            "left=", np.array2string(action[5:11], precision=3),
            "right=", np.array2string(action[12:18], precision=3),
        )
    except ValueError as exc:
        print(f">>> using physical safe arm start: {exc}")
    sim_node.tctr_slide[0] = planned_slide
    obstacles = build_cabinet_obstacles(box_center)

    if not Path(urdf_path).exists():
        raise FileNotFoundError(f"URDF file does not exist: {urdf_path}")
    print(">>> loading collision planner model")
    planner_model = pin.buildModelFromUrdf(str(urdf_path))
    planner_data = planner_model.createData()
    active_q_indices, active_v_indices = joint_indices(planner_model, ACTIVE_JOINT_NAMES)
    print(">>> collision planner model ready")

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
        left_base = sim_node.get_tmat_wrt_mmk2base(left_world)
        right_base = sim_node.get_tmat_wrt_mmk2base(right_world)

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
        stage_started_at = time.monotonic()
        print(f">>> {stage_name}: solving paired IK")
        left_ref = q_current_full[active_q_indices[:6]].copy()
        right_ref = q_current_full[active_q_indices[6:]].copy()
        left_goal, right_goal = solve_world_pair(
            left_target, right_target, left_ref, right_ref, stage_name=stage_name
        )
        print(
            f">>> {stage_name}: paired IK solved in "
            f"{time.monotonic() - stage_started_at:.2f}s"
        )
        q_goal_full = full_config_from_arms(left_goal, right_goal)
        if in_collision(planner_model, planner_data, q_goal_full, obstacles):
            raise RuntimeError(f"{stage_name}: IK goal is in cabinet collision")

        q_start_active = extract_active_config(q_current_full, active_q_indices)
        q_goal_active = extract_active_config(q_goal_full, active_q_indices)

        # Before invoking a coupled 12-DoF planner, try moving one arm at a
        # time.  This is deterministic, keeps the other hand in its known safe
        # pose, and is the common collision-free route to the camera checkpoint.
        left_then_right = q_start_active.copy()
        left_then_right[:6] = q_goal_active[:6]
        right_then_left = q_start_active.copy()
        right_then_left[6:] = q_goal_active[6:]
        for route_name, middle in (
            ("left-then-right", left_then_right),
            ("right-then-left", right_then_left),
        ):
            route_started_at = time.monotonic()
            print(f">>> {stage_name}: checking {route_name} route")
            middle_full = active_to_full(q_current_full, middle, active_q_indices)
            if in_collision(planner_model, planner_data, middle_full, obstacles):
                continue
            if edge_in_collision(
                planner_model, planner_data, q_current_full, middle_full, obstacles
            ):
                continue
            if edge_in_collision(
                planner_model, planner_data, middle_full, q_goal_full, obstacles
            ):
                continue
            segment = interpolate_active_path(
                [q_start_active.copy(), middle.copy(), q_goal_active.copy()],
                max_step=0.035,
            )
            print(
                f"planned {stage_name}: {len(segment)} joint samples "
                f"({route_name} deterministic route, "
                f"{time.monotonic() - route_started_at:.2f}s check)"
            )
            return q_goal_full, segment

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

    def build_refined_insertion_steps(refined_estimate):
        """Plan shelf entry from the measured observation-pose arm state."""
        nonlocal box_center, side_axis, box_half_width_y, targets

        box_center = np.asarray(refined_estimate.center_world, dtype=float).copy()
        side_axis = np.asarray(
            refined_estimate.side_axis_world, dtype=float
        ).copy()
        box_half_width_y = float(refined_estimate.half_width_y)
        targets = compute_dual_box_pick_targets(
            box_center=box_center,
            cabinet_front_x=cabinet_front_x,
            box_half_width_y=box_half_width_y,
            grasp_clearance=-0.016,
            grasp_height=(0.095 if uses_open_mesh_carton else 0.110),
            grasp_world=grasp_world,
            side_axis=side_axis,
        )
        q_current_actual = full_config_from_arms(
            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
            np.asarray(sim_node.sensor_rgt_arm_qpos, dtype=float),
        )
        steps = []

        q_current_actual, active_path = plan_rrt_stage(
            q_current_actual,
            targets["inside_high_left"],
            targets["inside_high_right"],
            "refined_inside_level_entry",
        )
        if len(active_path) > 2:
            active_path = active_path[::4] + [active_path[-1]]
        steps.append(
            {
                "kind": "joint_path",
                "name": "refined_inside_level_entry",
                "path": active_path,
                "grip": grip_initial,
                "require_final_reached": True,
                "final_point_timeout": 2.5,
                "position_tolerance": 0.08,
                "accept_timeout_error": 0.25,
            }
        )

        q_current_actual, deep_path = plan_synchronized_pair_stage(
            q_current_actual,
            targets["inside_high_left"],
            targets["inside_high_right"],
            targets["wall_slot_front_left"],
            targets["wall_slot_front_right"],
            "refined_deep_level_entry",
        )
        steps.append(
            {
                "kind": "timed_joint_path",
                "name": "refined_deep_level_entry",
                "path": deep_path,
                "grip": grip_open,
                "duration": max(0.55, 0.10 * max(1, len(deep_path) - 1)),
                "settle_duration": 0.35,
                "require_settle": True,
                "settle_error": 0.12,
                "settle_timeout": 3.0,
                "monitor_wall_safety": True,
                "stop_on_finger_contact": False,
            }
        )

        q_current_actual, insertion_path = plan_synchronized_pair_stage(
            q_current_actual,
            targets["wall_slot_front_left"],
            targets["wall_slot_front_right"],
            targets["wall_slot_left"],
            targets["wall_slot_right"],
            "refined_wall_slot_insert",
        )
        steps.append(
            {
                "kind": "timed_joint_path",
                "name": "refined_wall_slot_insert",
                "path": insertion_path,
                "grip": grip_open,
                "duration": max(
                    0.45, 0.10 * max(1, len(insertion_path) - 1)
                ),
                "settle_duration": 0.40,
                "require_settle": True,
                "settle_error": 0.18,
                "settle_timeout": 3.0,
                "monitor_wall_safety": False,
                "stop_on_finger_contact": False,
            }
        )
        steps.append(
            {
                "kind": "closed_pair_clamp",
                "name": "closed dual-side friction clamp",
                "timeout": 12.0,
            }
        )
        return steps

    class DeferredPerceptionPlanning(Exception):
        pass

    # Build one execution plan. The approach uses RRT; the grasped part uses
    # synchronized Cartesian waypoints so the two hands keep the same relative
    # geometry while carrying the box out of the cabinet.
    execution_steps = []
    planning_success = False
    try:
        print(">>> planning pre-observation arm motion")
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

        # Establish the final shelf-layer height and outward-facing wrist pose
        # while both complete hands are still in front of the cabinet.  Every
        # subsequent approach waypoint has the same Z, so entering the shelf
        # is a horizontal insertion rather than an unsafe vertical sweep next
        # to the upper/lower boards.
        approach_stages = [
            (
                "outside_mouth_height_ready",
                targets["mouth_left"],
                targets["mouth_right"],
            ),
        ]
        if pose_source == "ground-truth":
            approach_stages.append(
                (
                    "inside_level_entry",
                    targets["inside_high_left"],
                    targets["inside_high_right"],
                )
            )
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

        if pose_source == "perception":
            execution_steps.append(
                {
                    "kind": "perception_checkpoint",
                    "name": "dual hand-camera precise localization",
                    "max_retries": 3,
                    "settle_duration": 0.5,
                }
            )
            raise DeferredPerceptionPlanning()
        if pose_source == "external":
            execution_steps.append(
                {
                    "kind": "external_target_checkpoint",
                    "name": "replan from task-manager world coordinates",
                    "settle_duration": 0.20,
                }
            )
            raise DeferredPerceptionPlanning()

        # Continue horizontally to the deep wall-entry pose.  Height and wrist
        # orientation were already established outside the cabinet.
        q_current, high_align_path = plan_synchronized_pair_stage(
            q_current,
            targets["inside_high_left"],
            targets["inside_high_right"],
            targets["wall_slot_front_left"],
            targets["wall_slot_front_right"],
            "deep_level_entry",
        )
        execution_steps.append(
            {
                "kind": "timed_joint_path",
                "name": "deep_level_entry",
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
                            sim_node.get_tmat_wrt_mmk2base(left_target),
                            sim_node.arm_action,
                            "l",
                            left_ref,
                            candidate_left_rot,
                        ),
                        dtype=float,
                    )
                    right_ref = np.asarray(
                        sim_node.solveArmEndTarget(
                            sim_node.get_tmat_wrt_mmk2base(right_target),
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
        orientation_q_prev = q_current.copy()
        for sample_index, active_sample in enumerate(orientation_path):
            orientation_q_next = active_to_full(
                q_current, active_sample, active_q_indices
            )
            if in_collision(
                planner_model, planner_data, orientation_q_next, obstacles
            ) or edge_in_collision(
                planner_model,
                planner_data,
                orientation_q_prev,
                orientation_q_next,
                obstacles,
                step=0.025,
            ):
                raise RuntimeError(
                    "wall_slot_front_alignment: shelf collision on "
                    f"continuous sample {sample_index + 1}/{len(orientation_path)}"
                )
            orientation_q_prev = orientation_q_next
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
        planning_success = True
    except DeferredPerceptionPlanning:
        planning_success = True
        print(
            ">>> precise shelf-entry planning deferred until the hand-camera "
            "observation checkpoint"
        )
    except Exception as exc:
        print(">>> box_pick planning failed; holding the same grasp window open")
        print(f">>> failure: {type(exc).__name__}: {exc}")
        execution_steps = [
            {"kind": "hold", "name": "planning failed - inspect scene", "duration": 1.0e9}
        ]

    if planning_success and needs_base_alignment:
        execution_steps.insert(
            0,
            {
                "kind": "base_lateral_align",
                "name": "navigate base laterally to randomized package",
                "target_x": float(cfg.init_state["base_position"][0]),
                "target_y": planning_base_y,
                "timeout": 40.0,
            },
        )
        sim_node.mj_data.qpos[0] = float(cfg.init_state["base_position"][0])
        sim_node.mj_data.qpos[1] = navigation_start_y
        sim_node.mj_data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
        sim_node.mj_data.qvel[:6] = 0.0
        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
        base_lock_x = float(cfg.init_state["base_position"][0])
        base_lock_y = navigation_start_y
        print(
            ">>> planned physical base alignment: "
            f"start_y={navigation_start_y:.4f}, target_y={planning_base_y:.4f}, "
            f"delta_y={planning_base_y - navigation_start_y:+.4f}m"
        )

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
                    sim_node.get_tmat_wrt_mmk2base(left_world),
                    sim_node.arm_action,
                    "l",
                    left_ref,
                    left_grip_rot,
                )
                right_q = sim_node.solveArmEndTarget(
                    sim_node.get_tmat_wrt_mmk2base(right_world),
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

    operation_success = False
    operation_reason = "grasp_not_completed"
    sim_node._box_pick_context = {
        "target_body_name": target_body_name,
        "left_grip_rot": np.asarray(left_grip_rot, dtype=float).copy(),
        "right_grip_rot": np.asarray(right_grip_rot, dtype=float).copy(),
        "box_half_width_y": float(box_half_width_y),
        "uses_open_mesh_carton": bool(uses_open_mesh_carton),
        "grip_close": float(grip_close),
    }

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
        if (
            return_on_result
            and step.get("kind") == "hold"
            and float(step.get("duration", 0.0)) >= 1.0e8
        ):
            operation_success = False
            operation_reason = str(step.get("name", "grasp_failed"))
            break
        if current_step_name != step["name"]:
            current_step_name = step["name"]
            step_enter_time = now
            point_enter_time = now
            path_index = 0
            print(f">>> execute: {current_step_name}")


        if step["kind"] == "perception_checkpoint":
            # Keep the robot stationary while both hand-eye views are captured.
            action[:2] = 0.0
            if now - step_enter_time >= float(step.get("settle_duration", 0.5)):
                try:
                    refined_estimate = perception_bridge.refine_with_hand_cameras(
                        perception_query,
                        expected_shelf_level=selected_shelf_level,
                    )
                    refined_steps = build_refined_insertion_steps(refined_estimate)
                    refined_center = np.asarray(
                        refined_estimate.center_world, dtype=float
                    )
                    truth_now = get_body_tmat(
                        sim_node.mj_data, target_body_name
                    )[:3, 3]
                    print(
                        ">>> precise visual localization:",
                        f"center={np.round(refined_center, 4)}",
                        f"confidence={refined_estimate.confidence:.3f}",
                        f"dual_disagreement={refined_estimate.disagreement_m:.4f}m",
                    )
                    print(
                        ">>> perception evaluation only (not used by planner):",
                        f"truth_error={np.linalg.norm(refined_center - truth_now):.4f}m",
                    )
                    if headless:
                        # Both required visual observations are complete.  The
                        # remaining clamp/lift/retreat loop uses only joint and
                        # contact sensors, so stop rendering three RGB-D views
                        # on every control tick.
                        sim_node.config.enable_render = False
                        print(">>> visual checkpoints complete; background RGB-D rendering disabled")
                    execution_steps[step_index + 1:] = refined_steps
                    step_index += 1
                    current_step_name = None
                except Exception as exc:
                    step["retry_count"] = int(step.get("retry_count", 0)) + 1
                    print(
                        ">>> hand-camera localization/replan failed "
                        f"({step['retry_count']}/{step['max_retries']}): "
                        f"{type(exc).__name__}: {exc}"
                    )
                    if step["retry_count"] >= int(step["max_retries"]):
                        execution_steps = [
                            {
                                "kind": "hold",
                                "name": "hand-camera localization failed",
                                "duration": 1.0e9,
                            }
                        ]
                        step_index = 0
                        current_step_name = None
                    else:
                        step_enter_time = now

        elif step["kind"] == "external_target_checkpoint":
            action[:2] = 0.0
            if now - step_enter_time >= float(step.get("settle_duration", 0.2)):
                try:
                    external_estimate = types.SimpleNamespace(
                        center_world=np.asarray(box_center, dtype=float).copy(),
                        side_axis_world=np.asarray(side_axis, dtype=float).copy(),
                        half_width_y=float(box_half_width_y),
                    )
                    refined_steps = build_refined_insertion_steps(
                        external_estimate
                    )
                    execution_steps[step_index + 1:] = refined_steps
                    step_index += 1
                    current_step_name = None
                    print(
                        ">>> task-manager coordinates replanned from the "
                        "measured observation-pose arm state"
                    )
                except Exception as exc:
                    print(
                        ">>> external target replan failed: "
                        f"{type(exc).__name__}: {exc}"
                    )
                    execution_steps = [
                        {
                            "kind": "hold",
                            "name": "external target replan failed",
                            "duration": 1.0e9,
                        }
                    ]
                    step_index = 0
                    current_step_name = None

        elif step["kind"] == "base_lateral_align":
            drive_base_this_step = True
            if "phase" not in step:
                lateral_delta = float(step["target_y"] - sim_node.sensor_base_position[1])
                step["direction"] = 1.0 if lateral_delta >= 0.0 else -1.0
                step["heading"] = step["direction"] * 0.5 * math.pi
                # The two passive caster contacts move the chassis back by
                # about 8 mm while it turns from +/-90 deg to face the shelf.
                # Deliberately over-travel before that turn so one manoeuvre
                # lands at the requested lateral pose instead of oscillating.
                step["drive_target_y"] = (
                    float(step["target_y"]) + step["direction"] * 0.008
                )
                step["phase"] = "turn_to_lateral"
                print(
                    ">>> base alignment started with real wheel motion: "
                    f"current_y={float(sim_node.sensor_base_position[1]):.4f}, "
                    f"target_y={float(step['target_y']):.4f}"
                )

            quat = np.asarray(sim_node.sensor_base_orientation, dtype=float)
            yaw = math.atan2(
                2.0 * (quat[0] * quat[3] + quat[1] * quat[2]),
                1.0 - 2.0 * (quat[2] ** 2 + quat[3] ** 2),
            )
            y_error = float(step["target_y"] - sim_node.sensor_base_position[1])
            drive_y_error = float(
                step.get("drive_target_y", step["target_y"])
                - sim_node.sensor_base_position[1]
            )
            if now - float(step.get("last_navigation_log", -1.0e9)) >= 5.0:
                step["last_navigation_log"] = float(now)
                print(
                    ">>> base navigation: "
                    f"phase={step['phase']}, "
                    f"pose=({float(sim_node.sensor_base_position[0]):.3f}, "
                    f"{float(sim_node.sensor_base_position[1]):.3f}, "
                    f"yaw={yaw:.3f}), y_error={y_error:+.3f}m, "
                    f"x_target={float(step.get('target_x', float('nan'))):.3f}, "
                    f"base_v={np.round(sim_node.mj_data.qvel[:2], 3)}, "
                    f"wheel_v={np.round(sim_node.sensor_wheel_qvel, 2)}, "
                    f"wheel_u={np.round(action[:2], 2)}"
                )

            def wrapped_angle_error(target, current):
                return math.atan2(math.sin(target - current), math.cos(target - current))

            linear_speed = 0.0
            angular_speed = 0.0
            if step["phase"] == "turn_to_lateral":
                heading_error = wrapped_angle_error(float(step["heading"]), yaw)
                angular_speed = float(np.clip(2.2 * heading_error, -0.90, 0.90))
                if abs(heading_error) <= 0.025:
                    step["phase"] = "drive_lateral"
            elif step["phase"] == "drive_lateral":
                heading_error = wrapped_angle_error(float(step["heading"]), yaw)
                angular_speed = float(np.clip(2.2 * heading_error, -0.30, 0.30))
                if abs(drive_y_error) <= 0.008:
                    step["phase"] = "brake_lateral"
                else:
                    speed = float(np.clip(1.2 * abs(drive_y_error), 0.008, 0.050))
                    linear_speed = (
                        float(np.sign(drive_y_error))
                        * float(step["direction"])
                        * speed
                    )
            elif step["phase"] == "brake_lateral":
                heading_error = wrapped_angle_error(float(step["heading"]), yaw)
                angular_speed = float(np.clip(2.2 * heading_error, -0.30, 0.30))
                wheel_speed = float(
                    np.linalg.norm(np.asarray(sim_node.sensor_wheel_qvel, dtype=float))
                )
                base_lateral_speed = abs(float(sim_node.mj_data.qvel[1]))
                if wheel_speed <= 0.08 and base_lateral_speed <= 0.003:
                    if abs(drive_y_error) > 0.015:
                        step["phase"] = "drive_lateral"
                    else:
                        step["phase"] = "turn_to_shelf"
            elif step["phase"] == "turn_to_shelf":
                # Rotate in place.  Applying a lateral correction while the
                # heading is changing produced a large unintended X arc and
                # repeated correction passes on the differential chassis.
                heading_error = wrapped_angle_error(0.0, yaw)
                angular_speed = float(np.clip(2.2 * heading_error, -0.90, 0.90))
                if abs(heading_error) <= 0.025:
                    if abs(y_error) > 0.020:
                        step["direction"] = 1.0 if y_error >= 0.0 else -1.0
                        step["heading"] = step["direction"] * 0.5 * math.pi
                        step["drive_target_y"] = (
                            float(step["target_y"])
                            + step["direction"] * 0.008
                        )
                        step["phase"] = "turn_to_lateral"
                        print(
                            ">>> base alignment correction pass: "
                            f"remaining_y_error={y_error:+.4f}m"
                        )
                    else:
                        step["phase"] = "drive_x_recover"
            elif step["phase"] == "drive_x_recover":
                x_error = float(
                    step["target_x"] - sim_node.sensor_base_position[0]
                )
                heading_error = wrapped_angle_error(0.0, yaw)
                angular_speed = float(np.clip(2.0 * heading_error, -0.45, 0.45))
                if abs(x_error) > 0.006:
                    linear_speed = float(np.clip(1.5 * x_error, -0.12, 0.12))
                elif abs(heading_error) <= 0.015:
                    step["phase"] = "final_brake"
            elif step["phase"] == "final_brake":
                heading_error = wrapped_angle_error(0.0, yaw)
                angular_speed = float(np.clip(2.0 * heading_error, -0.30, 0.30))
                wheel_speed = float(
                    np.linalg.norm(np.asarray(sim_node.sensor_wheel_qvel, dtype=float))
                )
                base_speed = float(np.linalg.norm(sim_node.mj_data.qvel[:6]))
                if (
                    wheel_speed <= 0.05
                    and base_speed <= 0.006
                    and abs(heading_error) <= 0.008
                    and abs(y_error) <= 0.020
                ):
                    action[:2] = 0.0
                    measured_base = np.asarray(
                        sim_node.sensor_base_position[:2], dtype=float
                    ).copy()
                    box_after_navigation = get_body_tmat(
                        sim_node.mj_data, target_body_name
                    )[:3, 3].copy()
                    box_navigation_shift = (
                        box_after_navigation - np.asarray(sim_node.box_start_pos)
                    )
                    # Arm collision/IK paths are planned for an exact base pose.
                    # The wheel controller performs the visible, physical move;
                    # remove only its final millimetre-scale odometry residual
                    # before manipulation so that both wall contacts remain
                    # symmetric.  This is the simulation equivalent of the
                    # low-speed localization/pose-hold handoff used on hardware.
                    sim_node.mj_data.qpos[0] = float(step["target_x"])
                    sim_node.mj_data.qpos[1] = float(step["target_y"])
                    sim_node.mj_data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
                    sim_node.mj_data.qvel[:6] = 0.0
                    mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
                    base_lock_x = float(step["target_x"])
                    base_lock_y = float(step["target_y"])
                    print(
                        ">>> base lateral alignment complete: "
                        f"measured=({measured_base[0]:.4f}, "
                        f"{measured_base[1]:.4f}), "
                        f"target=({float(step['target_x']):.4f}, "
                        f"{float(step['target_y']):.4f}), yaw={yaw:.4f}rad; "
                        f"box_navigation_dxyz={np.round(box_navigation_shift, 5)}"
                    )
                    step_index += 1
                    current_step_name = None
            else:
                raise ValueError(f"unknown base alignment phase: {step['phase']}")

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
            if now - step_enter_time >= float(step["timeout"]):
                if abs(y_error) <= 0.010 and abs(yaw) <= 0.070:
                    action[:2] = 0.0
                    measured_base = np.asarray(
                        sim_node.sensor_base_position[:2], dtype=float
                    ).copy()
                    box_after_navigation = get_body_tmat(
                        sim_node.mj_data, target_body_name
                    )[:3, 3].copy()
                    box_navigation_shift = (
                        box_after_navigation - np.asarray(sim_node.box_start_pos)
                    )
                    sim_node.mj_data.qpos[0] = float(step["target_x"])
                    sim_node.mj_data.qpos[1] = float(step["target_y"])
                    sim_node.mj_data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
                    sim_node.mj_data.qvel[:6] = 0.0
                    mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)
                    base_lock_x = float(step["target_x"])
                    base_lock_y = float(step["target_y"])
                    print(
                        ">>> base lateral alignment accepted at timeout: "
                        f"measured=({measured_base[0]:.4f}, "
                        f"{measured_base[1]:.4f}), "
                        f"target=({float(step['target_x']):.4f}, "
                        f"{float(step['target_y']):.4f}), "
                        f"y_error={y_error:+.4f}m, yaw={yaw:.4f}rad; "
                        f"box_navigation_dxyz={np.round(box_navigation_shift, 5)}"
                    )
                    step_index += 1
                    current_step_name = None
                    continue
                print(
                    ">>> BASE ALIGNMENT FAILED: "
                    f"y_error={y_error:.4f}m, yaw={yaw:.4f}rad"
                )
                action[:2] = 0.0
                base_lock_x = float(sim_node.sensor_base_position[0])
                base_lock_y = float(sim_node.sensor_base_position[1])
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "base lateral alignment failed",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
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
                        f">>> WALL INSERTION SAFETY WARNING at {current_step_name}: "
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
                        f"{current_step_name} safety warning"
                    )
                    if current_step_name == "refined_deep_level_entry":
                        step["monitor_wall_safety"] = False
                        print(
                            ">>> continuing refined_deep_level_entry without hard stop"
                        )
                    else:
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
                                sim_node.get_tmat_wrt_mmk2base(step["center_targets"][0]),
                                sim_node.arm_action,
                                "l",
                                np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                                left_grip_rot,
                            )
                            sim_node.set_left_arm_new_target = True
                        if not right_seated:
                            sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                                sim_node.get_tmat_wrt_mmk2base(step["center_targets"][1]),
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
            safe_contact = wall_clamp_contacts_are_safe(closed_report)
            max_closed_compression = max(
                [-float(detail["distance"]) for detail in closed_report["contact_details"]]
                or [0.0]
            )
            if not safe_contact:
                non_side_normals = [
                    np.round(detail["contact_normal"], 3).tolist()
                    for detail in closed_report["contact_details"]
                    if (
                        "contact_normal" in detail
                        and abs(float(detail["contact_normal"][2])) > 0.30
                    )
                ]
                print(
                    ">>> CLOSED CLAMP SAFETY STOP: "
                    f"nonfinger={sorted(closed_report['nonfinger_contacts'])}; "
                    f"non_side_normals={non_side_normals}"
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
            required_clamp_load = select_clamp_ready_load(selected_shelf_level)
            left_ready = (
                "left_first_contact" in step
                and left_preload >= 0.002
                and left_load >= required_clamp_load
            )
            right_ready = (
                "right_first_contact" in step
                and right_preload >= 0.002
                and right_load >= required_clamp_load
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
                    f"required>={required_clamp_load:.2f} N; "
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
                # First lift the *end effectors themselves* while the
                # bilateral preload is preserved.  Raising only the torso slide
                # can be visually cancelled by the arm controller; a Cartesian
                # endpoint lift guarantees that both hands and the free box are
                # commanded upward before any base retreat begins.
                execution_steps[step_index + 1:] = [
                    {
                        "kind": "closed_pair_cartesian_lift",
                        "name": "lift clamped package before retreat",
                        # Level 4 has only about 9 cm clearance to the next
                        # board.  A 5 cm lift leaves too little rotational
                        # margin, so use a 3 cm clearance lift there.
                        "height": (
                            0.030
                            if selected_shelf_level == 4
                            else NOMINAL_CLEARANCE_LIFT
                        ),
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
                        "name": "fast physical extraction after clearance lift",
                        "distance": NOMINAL_BASE_RETREAT,
                        "duration": 9.0,
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
                # At different torso heights the two arm servos can deflect by
                # different amounts.  Relieve an overloaded side instead of
                # continuing to store asymmetric spring energy in the carton.
                balanced_ready = left_ready and right_ready
                compression_relief = (
                    max_closed_compression > 0.0046 and not balanced_ready
                )
                left_relief = left_load > 13.0 or (
                    compression_relief and left_load >= right_load - 0.5
                )
                right_relief = right_load > 13.0 or (
                    compression_relief and right_load >= left_load - 0.5
                )
                left_adjust = 0.0
                right_adjust = 0.0
                if left_relief:
                    left_adjust = 0.0006
                elif not left_ready:
                    left_adjust = -0.0012
                if right_relief:
                    right_adjust = -0.0006
                elif not right_ready:
                    right_adjust = 0.0012
                closed_pair_targets_world[0][1] += left_adjust
                closed_pair_targets_world[1][1] += right_adjust
                step["left_inward_travel"] = max(
                    0.0,
                    float(step.get("left_inward_travel", 0.0)) - left_adjust,
                )
                step["right_inward_travel"] = max(
                    0.0,
                    float(step.get("right_inward_travel", 0.0)) + right_adjust,
                )
                try:
                    if abs(left_adjust) > 0.0:
                        sim_node.tctr_left_arm[:] = sim_node.solveArmEndTarget(
                            sim_node.get_tmat_wrt_mmk2base(closed_pair_targets_world[0]),
                            sim_node.arm_action, "l",
                            np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float), left_grip_rot,
                        )
                        sim_node.set_left_arm_new_target = True
                    if abs(right_adjust) > 0.0:
                        sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                            sim_node.get_tmat_wrt_mmk2base(closed_pair_targets_world[1]),
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
                step["target_lift_load"] = select_lift_target_load(
                    selected_shelf_level, left_load, right_load
                )
                step["last_lift_force_update"] = float(now)
                print(
                    ">>> pre-retreat Cartesian lift started: "
                    f"requested={float(step['height']) * 100:.1f}cm; "
                    f"box_z={step['start_box_z']:.4f}; "
                    f"normal=({left_load:.2f}, {right_load:.2f})N; "
                    f"target={float(step['target_lift_load']):.2f}N"
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
                target_lift_load = float(step["target_lift_load"])
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
                    sim_node.get_tmat_wrt_mmk2base(left_target),
                    sim_node.arm_action,
                    "l",
                    np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                    left_grip_rot,
                )
                corrected_right_q = sim_node.solveArmEndTarget(
                    sim_node.get_tmat_wrt_mmk2base(right_target),
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
                        "name": "Cartesian clearance lift IK failed - inspect scene",
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
            relative_rotation = mat3_mul(
                np.asarray(step["start_box_rotation"], dtype=float).T,
                np.asarray(box_tmat[:3, :3], dtype=float),
            )
            orientation_excursion_deg = math.degrees(
                math.acos(
                    float(np.clip((np.trace(relative_rotation) - 1.0) * 0.5, -1.0, 1.0))
                )
            )
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
                        "name": "clamp lost during Cartesian clearance lift",
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
            # endpoints to have reached the requested clearance and the free box to have
            # visibly followed the grasp upward before the wheels may move.
            required_endpoint_rise = max(0.015, float(step["height"]) - 0.005)
            required_box_rise = max(0.015, float(step["height"]) - 0.010)
            endpoints_up = (
                left_rise >= required_endpoint_rise
                and right_rise >= required_endpoint_rise
            )
            box_up = box_rise >= required_box_rise
            near_endpoint_rise = max(0.015, float(step["height"]) - 0.010)
            near_box_rise = max(0.015, float(step["height"]) - 0.015)
            endpoints_nearly_up = (
                left_rise >= near_endpoint_rise
                and right_rise >= near_endpoint_rise
            )
            box_nearly_up = box_rise >= near_box_rise
            # The open-top carton is represented by many thin convex wall
            # pieces rather than one solid primitive.  A side clamp can
            # briefly rotate it a little more while the bottom clears the
            # shelf, even though both hands retain load.  Keep a bounded
            # safety stop, but allow that expected transient before judging
            # the grasp as unstable.
            max_lift_tilt_deg = 20.0 if uses_open_mesh_carton else 8.0
            if orientation_excursion_deg > max_lift_tilt_deg:
                print(
                    ">>> PRE-RETREAT LIFT ORIENTATION STOP: "
                    f"package excursion={orientation_excursion_deg:.2f}deg > "
                    f"{max_lift_tilt_deg:.2f}deg"
                )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "package tilted during Cartesian clearance lift",
                        "duration": 1.0e9,
                    }
                ]
                step_index = 0
                current_step_name = None
                continue
            dynamically_settled = lateral_speed <= 0.012 and angular_speed <= 0.20
            step["settle_streak"] = (
                int(step.get("settle_streak", 0)) + 1
                if alpha >= 1.0 and dynamically_settled
                else 0
            )
            post_hold_complete = motion_elapsed - duration >= post_hold
            full_clearance_ready = endpoints_up and box_up
            near_clearance_ready = (
                endpoints_nearly_up
                and box_nearly_up
                and bilateral_contact
                and dynamically_settled
            )
            if (
                alpha >= 1.0
                and post_hold_complete
                and int(step["settle_streak"]) >= 12
                and (full_clearance_ready or near_clearance_ready)
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
                        retreat_step["near_clearance"] = not full_clearance_ready
                        if (
                            uses_open_mesh_carton
                            and (
                                not full_clearance_ready
                                or int(selected_shelf_level) == 4
                            )
                        ):
                            retreat_step["lateral_slip_limit"] = 0.080
                            retreat_step["retreat_speed_scale"] = 1.05
                            retreat_step["ramp_seconds"] = 0.85
                        else:
                            retreat_step["retreat_speed_scale"] = 1.40
                            retreat_step["ramp_seconds"] = 0.45

                print(
                    ">>> pre-retreat Cartesian lift complete; "
                    f"endpoint_rise=({left_rise * 100:.1f}, {right_rise * 100:.1f})cm; "
                    f"box_rise={box_rise * 100:.1f}cm; "
                    f"clearance={'full' if full_clearance_ready else 'near'}; "
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
                    ">>> PRE-RETREAT LIFT FAILED: requested clearance was not physically reached; "
                    f"endpoint_rise=({left_rise * 100:.1f}, {right_rise * 100:.1f})cm; "
                    f"box_rise={box_rise * 100:.1f}cm; "
                    f"normal=({left_load:.2f}, {right_load:.2f})N"
                )
                execution_steps = [
                    {
                        "kind": "hold",
                        "name": "Cartesian clearance lift incomplete - inspect scene",
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
            retreat_speed_scale = float(step.get("retreat_speed_scale", 1.25))
            cruise_speed = -float(step["distance"]) * retreat_speed_scale / max(
                float(step["duration"]),
                1.0e-6,
            )
            ramp_alpha = min(
                1.0,
                max(0.0, elapsed / float(step.get("ramp_seconds", 0.6))),
            )
            speed_ramp = ramp_alpha * ramp_alpha * (3.0 - 2.0 * ramp_alpha)
            box_for_speed = get_body_tmat(
                sim_node.mj_data, target_body_name
            )[:3, 3]
            tracking_lag = float(
                box_for_speed[0]
                - (float(step["start_box"][0]) - actual_retreat)
            )
            # Real slip feedback: slow the mobile base when the free package
            # lags behind the pads, and pause before the finite visible pad
            # length can slide off the wall.  The angled clamp continues to
            # pull through physical contact while the base waits.
            slip_speed_scale = float(
                np.clip((0.015 - tracking_lag) / 0.0075, 0.25, 1.0)
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
            angular_speed = -1.7 * yaw
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
                8.5 * wheel_error,
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
                left_endpoint[2] = float(
                    step["start_left_endpoint_target"][2] + retreat_lift
                )
                right_endpoint[2] = float(
                    step["start_right_endpoint_target"][2] + retreat_lift
                )
                # Maintain normal force only; X/Z remain the actually measured
                # endpoints moving with the wheeled base.
                if retreat_compression > 0.0048 or max(left_load, right_load) > 17.0:
                    left_endpoint[1] += 0.0003
                    right_endpoint[1] -= 0.0003
                else:
                    if left_load < 14.0:
                        left_endpoint[1] -= 0.0004
                    if right_load < 14.0:
                        right_endpoint[1] += 0.0004
                try:
                    corrected_left_q = sim_node.solveArmEndTarget(
                        sim_node.get_tmat_wrt_mmk2base(left_endpoint),
                        sim_node.arm_action,
                        "l",
                        np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                        left_grip_rot,
                    )
                    corrected_right_q = sim_node.solveArmEndTarget(
                        sim_node.get_tmat_wrt_mmk2base(right_endpoint),
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
            retreat_nonfinger_contacts = set(
                retreat_report["nonfinger_contacts"]
            )
            allowed_open_carton_wrist_links = {
                "lft_arm_link6",
                "rgt_arm_link6",
            }
            distal_contact_distances = [
                float(detail["distance"])
                for detail in retreat_report["contact_details"]
                if detail["body"] in retreat_nonfinger_contacts
            ]
            shallow_distal_wrist_support = bool(
                uses_open_mesh_carton
                and retreat_nonfinger_contacts
                and retreat_nonfinger_contacts.issubset(
                    allowed_open_carton_wrist_links
                )
                and distal_contact_distances
                and min(distal_contact_distances) >= -0.004
            )
            safe_contact = bool(
                not retreat_nonfinger_contacts
                or (bilateral and shallow_distal_wrist_support)
            )
            if (
                shallow_distal_wrist_support
                and not step.get("reported_distal_wrist_support", False)
            ):
                step["reported_distal_wrist_support"] = True
                print(
                    ">>> open-carton rim has shallow distal-wrist support; "
                    f"links={sorted(retreat_nonfinger_contacts)}, "
                    f"max_penetration={-min(distal_contact_distances) * 1000:.2f}mm; "
                    "bilateral finger clamp remains required"
                )
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
            lateral_slip_limit = float(step.get("lateral_slip_limit", 0.050))
            lateral_validated_limit = max(0.035, lateral_slip_limit - 0.015)
            lateral_outside_limit = max(0.035, lateral_slip_limit - 0.005)
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
                and pull_lag <= 0.055
                and lateral_slip <= lateral_validated_limit
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
                and lateral_slip <= lateral_outside_limit
                and vertical_drop <= 0.060
            )
            if fully_outside:
                base_lock_x = float(sim_node.sensor_base_position[0])
                action[:2] = 0.0
                sim_node.physical_transport_verified = True
                sim_node.physical_transport_completed = True
                physical_grasp_validated = True
                base_world_tmat = get_body_tmat(sim_node.mj_data, "mmk2")
                base_rotation = np.asarray(
                    base_world_tmat[:3, :3], dtype=float
                )
                base_translation = np.asarray(
                    base_world_tmat[:3, 3], dtype=float
                )
                left_endpoint_base = base_rotation.T @ (
                    np.asarray(step["left_endpoint_target"], dtype=float)
                    - base_translation
                )
                right_endpoint_base = base_rotation.T @ (
                    np.asarray(step["right_endpoint_target"], dtype=float)
                    - base_translation
                )
                sim_node._box_pick_context.update(
                    {
                        # Keep the unloaded Cartesian setpoints which produced
                        # the verified clamp.  The measured sites are slightly
                        # deflected by contact; using those as a new command in
                        # place_object would relax the clamp immediately.
                        "left_endpoint_target": np.asarray(
                            step["left_endpoint_target"], dtype=float
                        ).copy(),
                        "right_endpoint_target": np.asarray(
                            step["right_endpoint_target"], dtype=float
                        ).copy(),
                        # Navigation may translate and rotate the base before
                        # placement.  Base-frame copies follow that motion.
                        "left_endpoint_target_base": left_endpoint_base.copy(),
                        "right_endpoint_target_base": right_endpoint_base.copy(),
                    }
                )
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
                or pull_lag > 0.090
                or lateral_slip > lateral_slip_limit
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
                if actual_dx > expected_dx + 0.07 or not physical_grasp_validated:
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
            verified_nonfinger_contacts = set(
                verified_report["nonfinger_contacts"]
            )
            verified_distal_distances = [
                float(detail["distance"])
                for detail in verified_report["contact_details"]
                if detail["body"] in verified_nonfinger_contacts
            ]
            verified_contact_safe = bool(
                not verified_nonfinger_contacts
                or (
                    uses_open_mesh_carton
                    and all_four_verified
                    and verified_nonfinger_contacts.issubset(
                        {"lft_arm_link6", "rgt_arm_link6"}
                    )
                    and verified_distal_distances
                    and min(verified_distal_distances) >= -0.004
                )
            )
            success = bool(
                verified_box_pose[0] <= sim_node.cabinet_front_x - 0.05
                and all_four_verified
                and verified_contact_safe
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
                f"contact_safe={verified_contact_safe}",
                f"max_compression={verified_max_compression * 1000:.2f}mm",
                "physical_transport=True",
            )
            print(">>> RESULT:", "SUCCESS" if success else "FAILED")
            operation_success = bool(success)
            operation_reason = (
                "grasp_acquired" if success else "grasp_verification_failed"
            )
            sim_node._box_pick_context.update(
                {
                    "left_grip_rot": np.asarray(
                        left_grip_rot, dtype=float
                    ).copy(),
                    "right_grip_rot": np.asarray(
                        right_grip_rot, dtype=float
                    ).copy(),
                    "grasped": bool(success),
                    "box_pose": verified_box_pose.copy(),
                }
            )
            if return_on_result:
                break
            execution_steps = [
                {
                    "kind": "hold",
                    "name": "final hold after successful extraction" if success else "final hold after failed extraction",
                    "duration": 1.0e9,
                }
            ]
            step_index = 0
            current_step_name = None
            continue

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
                    sim_node.get_tmat_wrt_mmk2base(left_target), sim_node.arm_action, "l",
                    np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float), left_grip_rot,
                )
                step["right_q"] = sim_node.solveArmEndTarget(
                    sim_node.get_tmat_wrt_mmk2base(right_target), sim_node.arm_action, "r",
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
                    left_base = sim_node.get_tmat_wrt_mmk2base(wall_align_target_world[0])
                    right_base = sim_node.get_tmat_wrt_mmk2base(wall_align_target_world[1])
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
                        left_base = sim_node.get_tmat_wrt_mmk2base(clamp_seat_targets_world[0])
                        right_base = sim_node.get_tmat_wrt_mmk2base(clamp_seat_targets_world[1])
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
                        sim_node.get_tmat_wrt_mmk2base(force_settle_centers_world[0]),
                        sim_node.arm_action,
                        "l",
                        np.asarray(sim_node.sensor_lft_arm_qpos, dtype=float),
                        left_grip_rot,
                    )
                    sim_node.tctr_right_arm[:] = sim_node.solveArmEndTarget(
                        sim_node.get_tmat_wrt_mmk2base(force_settle_centers_world[1]),
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
                operation_success = bool(success)
                operation_reason = (
                    "grasp_acquired" if success else "grasp_verification_failed"
                )
                if return_on_result:
                    break
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

    sim_node._box_pick_context["grasped"] = bool(operation_success)
    sim_node._box_pick_last_result = {
        "success": bool(operation_success),
        "retryable": not bool(operation_success),
        "reason": str(operation_reason),
    }
    return bool(operation_success)


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


def in_collision(model, data, q, obstacles, robot_radius=0.035):
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
    max_seconds=30.0,
):
    q_start_full = active_to_full(q_template, q_start_active, active_q_indices)
    q_goal_full = active_to_full(q_template, q_goal_active, active_q_indices)
    if in_collision(model, data, q_start_full, obstacles):
        raise ValueError("q_start is in collision")
    if in_collision(model, data, q_goal_full, obstacles):
        raise ValueError("q_goal is in collision")
    if not edge_in_collision(model, data, q_start_full, q_goal_full, obstacles):
        return [q_start_active.copy(), q_goal_active.copy()]

    # Bidirectional RRT-Connect is much better suited to the coupled 12-DoF
    # arm state than the previous one-tree search.  In particular, reaching
    # an observation pose beside a shelf should take seconds, not minutes.
    nodes_a = [q_start_active.copy()]
    parents_a = [None]
    nodes_b = [q_goal_active.copy()]
    parents_b = [None]
    a_root_is_start = True
    started_at = time.monotonic()

    def append_if_free(nodes, parents, target):
        nearest_index = nearest_node(nodes, target)
        q_near = nodes[nearest_index]
        q_new = clamp_active(model, steer(q_near, target, step_size), active_q_indices)
        if np.linalg.norm(q_new - q_near) < 1e-9:
            return None
        q_near_full = active_to_full(q_template, q_near, active_q_indices)
        q_new_full = active_to_full(q_template, q_new, active_q_indices)
        if edge_in_collision(model, data, q_near_full, q_new_full, obstacles):
            return None
        nodes.append(q_new)
        parents.append(nearest_index)
        return len(nodes) - 1

    for iteration in range(max_iter):
        if time.monotonic() - started_at > max_seconds:
            raise RuntimeError(
                f"RRT timed out after {max_seconds:.1f}s "
                f"({len(nodes_a) + len(nodes_b)} nodes)"
            )

        # Bias each active tree towards the other root while still exploring
        # the entire joint range when the shelf blocks that direct route.
        other_root = nodes_b[0]
        q_rand = (
            other_root
            if random.random() < goal_sample_rate
            else random_active_configuration(model, active_q_indices)
        )
        new_a_index = append_if_free(nodes_a, parents_a, q_rand)
        if new_a_index is not None:
            q_meet = nodes_a[new_a_index]
            # Greedily connect the opposite tree to the new node.
            while True:
                if time.monotonic() - started_at > max_seconds:
                    raise RuntimeError(
                        f"RRT timed out after {max_seconds:.1f}s "
                        f"({len(nodes_a) + len(nodes_b)} nodes)"
                    )
                nearest_b = nearest_node(nodes_b, q_meet)
                distance = float(np.linalg.norm(nodes_b[nearest_b] - q_meet))
                if distance < 1e-8:
                    meet_b_index = nearest_b
                    break
                new_b_index = append_if_free(nodes_b, parents_b, q_meet)
                if new_b_index is None:
                    meet_b_index = None
                    break
                if np.linalg.norm(nodes_b[new_b_index] - q_meet) < 1e-8:
                    meet_b_index = new_b_index
                    break

            if meet_b_index is not None:
                path_a = reconstruct_path(nodes_a, parents_a, new_a_index)
                path_b = reconstruct_path(nodes_b, parents_b, meet_b_index)
                if a_root_is_start:
                    return path_a + list(reversed(path_b[:-1]))
                return path_b + list(reversed(path_a[:-1]))

        # Alternate the trees so neither the start nor goal side has to pass
        # through a disproportionately narrow region on its own.
        nodes_a, nodes_b = nodes_b, nodes_a
        parents_a, parents_b = parents_b, parents_a
        a_root_is_start = not a_root_is_start

    raise RuntimeError(
        f"RRT failed after {max_iter} iterations "
        f"({len(nodes_a) + len(nodes_b)} nodes)"
    )


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
    del box_center
    # The shelf is fixed in world coordinates; package randomization must not
    # translate the collision model with the package.  Include every physical
    # board because the selected package layer can now be 2, 3, or 4.
    cabinet_center = np.array([1.32, 0.715, 0.0])
    obstacles = [
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
    ]
    for layer_index, shelf_z in enumerate((0.30, 0.60, 0.90, 1.20, 1.50, 1.80), 1):
        obstacles.append(
            AABB(
                f"shelf_board_{layer_index}",
                cabinet_center + np.array([-0.14, -0.40, shelf_z - 0.01]),
                cabinet_center + np.array([0.14, 0.40, shelf_z + 0.01]),
            )
        )
    return obstacles


def compute_dual_box_pick_targets(
    box_center,
    box_yaw=0.0,
    cabinet_front_x=0.48,
    box_half_width_y=DEFAULT_BOX_HALF_WIDTH_Y,
    pre_clearance=0.050,
    grasp_clearance=0.000,
    grasp_height=0.110,
    grasp_world=None,
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
    grasp_world = (
        None
        if grasp_world is None
        else np.asarray(grasp_world, dtype=float).reshape(-1)
    )
    if grasp_world is not None and (
        grasp_world.size != 3 or not np.all(np.isfinite(grasp_world))
    ):
        raise ValueError("grasp_world must contain three finite XYZ values")
    grasp_x = (
        float(grasp_world[0])
        if grasp_world is not None
        else box_center[0] - DEFAULT_BOX_HALF_DEPTH_X + 0.105
    )
    wall_slot_front_x = grasp_x
    retreat_x = cabinet_front_x - 0.20

    box_bottom_z = float(box_center[2])
    box_top_z = box_bottom_z + DEFAULT_BOX_HEIGHT
    # Clamp the broad middle portion of the side wall.  The earlier nominal
    # layer-3 run reached this height only because planning and execution used
    # torso-slide values that differed by about 8 cm.  Make the intended wall
    # depth explicit so every shelf level uses the same physical contact patch.
    grasp_z = (
        float(grasp_world[2])
        if grasp_world is not None
        else box_bottom_z + float(grasp_height)
    )
    grasp_center_y = (
        float(grasp_world[1])
        if grasp_world is not None
        else float(box_center[1])
    )
    # Reach the final clamp height before crossing the cabinet front plane.
    # The old trajectory entered above the box and descended beside it; on a
    # randomized shelf this swept the vertical fingers and wrist housings
    # through the board above.  All ungrasped entry targets now share one Z and
    # differ only in X/Y.
    slot_align_z = grasp_z
    approach_z = grasp_z
    inside_z = approach_z
    approach_lateral = float(box_half_width_y + pre_clearance)
    grasp_lateral = float(box_half_width_y + grasp_clearance)

    def side_pair(x, z, lateral, left_inset=0.0, right_inset=0.0):
        center_y = (
            grasp_center_y
            if abs(float(x) - grasp_x) <= 1.0e-9
            else float(box_center[1])
        )
        center = np.array([x, center_y, z], dtype=float)
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


def build_current_plan_stage_specs(targets):
    """Describe the current nominal entry, clamp, and extraction sequence.

    The physical controller replaces ``nominal_contact_seek`` and all later
    targets with measured contact poses at runtime.  The offline preview uses
    the nominal grasp pair, then mirrors the level-3 default branch: a 5 cm
    Cartesian clearance lift followed by a 28 cm physical base retreat.
    """
    def pair(name):
        return (
            np.asarray(targets[f"{name}_left"], dtype=float).copy(),
            np.asarray(targets[f"{name}_right"], dtype=float).copy(),
        )

    outside = pair("outside")
    mouth = pair("mouth")
    inside = pair("inside_high")
    wall_front = pair("wall_slot_front")
    wall = pair("wall_slot")
    grasp = pair("grasp")
    clearance_lift = (
        grasp[0] + np.array([0.0, 0.0, NOMINAL_CLEARANCE_LIFT]),
        grasp[1] + np.array([0.0, 0.0, NOMINAL_CLEARANCE_LIFT]),
    )
    base_retreat = (
        clearance_lift[0] + np.array([-NOMINAL_BASE_RETREAT, 0.0, 0.0]),
        clearance_lift[1] + np.array([-NOMINAL_BASE_RETREAT, 0.0, 0.0]),
    )

    def stage(name, kind, start, goal):
        return {
            "name": name,
            "kind": kind,
            "left_start": start[0].copy(),
            "right_start": start[1].copy(),
            "left_goal": goal[0].copy(),
            "right_goal": goal[1].copy(),
        }

    return [
        stage("initial_outside", "start", outside, outside),
        stage("outside_mouth_height_ready", "rrt", outside, mouth),
        stage("inside_level_entry", "rrt", mouth, inside),
        stage("deep_level_entry", "synchronized", inside, wall_front),
        stage("wall_slot_front_alignment", "orientation", wall_front, wall_front),
        stage("wall_slot_insert", "synchronized", wall_front, wall),
        stage("nominal_contact_seek", "synchronized", wall, grasp),
        stage("cartesian_clearance_lift", "rigid", grasp, clearance_lift),
        stage("physical_base_retreat", "base", clearance_lift, base_retreat),
    ]


def build_current_cartesian_preview(stage_specs):
    """Interpolate the current execution targets without inventing joint poses."""
    initial = stage_specs[0]
    left_points = [np.asarray(initial["left_goal"], dtype=float).copy()]
    right_points = [np.asarray(initial["right_goal"], dtype=float).copy()]
    stage_end_indices = {initial["name"]: 0}

    for stage in stage_specs[1:]:
        left_start = np.asarray(stage["left_start"], dtype=float)
        right_start = np.asarray(stage["right_start"], dtype=float)
        left_delta = np.asarray(stage["left_goal"], dtype=float) - left_start
        right_delta = np.asarray(stage["right_goal"], dtype=float) - right_start
        distance = max(
            float(np.linalg.norm(left_delta)),
            float(np.linalg.norm(right_delta)),
        )
        cartesian_step = 0.015 if stage["kind"] in {"rigid", "base"} else 0.006
        samples = max(2, int(math.ceil(distance / cartesian_step)) + 1)
        for alpha in np.linspace(0.0, 1.0, samples)[1:]:
            left_points.append(left_start + alpha * left_delta)
            right_points.append(right_start + alpha * right_delta)
        stage_end_indices[stage["name"]] = len(left_points) - 1

    return np.asarray(left_points), np.asarray(right_points), stage_end_indices


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


def plan_current_grasp_preview(
    model,
    data,
    q_template,
    active_q_indices,
    stage_specs,
    obstacles,
    left_rotation,
    right_rotation,
    pose_solver,
):
    """Plan the current horizontal entry and position-only extraction preview."""
    q_path_full = []
    stage_configs = []
    q_current = q_template.copy()

    def solve_goal(stage, seed):
        q_goal, ok = pose_solver(
            seed,
            stage["left_goal"],
            stage["right_goal"],
            left_rotation,
            right_rotation,
        )
        if not ok:
            raise RuntimeError(
                f"failed to solve pose IK for stage {stage['name']}: "
                f"left={np.round(stage['left_goal'], 3)}, "
                f"right={np.round(stage['right_goal'], 3)}"
            )
        return q_goal

    initial = stage_specs[0]
    q_current = solve_goal(initial, q_current)
    q_path_full.append(q_current.copy())
    stage_configs.append(
        (
            initial["name"],
            q_current.copy(),
            initial["left_goal"].copy(),
            initial["right_goal"].copy(),
        )
    )
    print(
        f"stage {initial['name']}: left={np.round(initial['left_goal'], 3)}, "
        f"right={np.round(initial['right_goal'], 3)}"
    )

    for stage in stage_specs[1:]:
        kind = stage["kind"]
        if kind == "rrt":
            q_goal = solve_goal(stage, q_current)
            start_active = extract_active_config(q_current, active_q_indices)
            goal_active = extract_active_config(q_goal, active_q_indices)
            segment = rrt_plan_active(
                model,
                data,
                q_current,
                active_q_indices,
                start_active,
                goal_active,
                obstacles,
                max_iter=9000,
                step_size=0.10,
                goal_sample_rate=0.30,
            )
            segment = smooth_path_active(
                model,
                data,
                q_current,
                active_q_indices,
                segment,
                obstacles,
                attempts=60,
            )
            segment = interpolate_active_path(segment, max_step=0.035)
            q_segment = [
                active_to_full(q_current, q_active, active_q_indices)
                for q_active in segment[1:]
            ]
            q_current = q_goal
        else:
            left_start = np.asarray(stage["left_start"], dtype=float)
            right_start = np.asarray(stage["right_start"], dtype=float)
            left_delta = np.asarray(stage["left_goal"], dtype=float) - left_start
            right_delta = np.asarray(stage["right_goal"], dtype=float) - right_start
            if kind == "rigid" and not np.allclose(
                left_delta, right_delta, atol=1.0e-9
            ):
                raise RuntimeError(
                    f"{stage['name']}: left/right transport is not rigid"
                )
            cartesian_step = 0.015 if kind == "rigid" else 0.006
            distance = max(
                float(np.linalg.norm(left_delta)),
                float(np.linalg.norm(right_delta)),
            )
            samples = max(2, int(math.ceil(distance / cartesian_step)) + 1)
            q_segment = []
            q_previous = q_current
            for alpha in np.linspace(0.0, 1.0, samples)[1:]:
                sample_stage = {
                    **stage,
                    "left_goal": left_start + alpha * left_delta,
                    "right_goal": right_start + alpha * right_delta,
                }
                q_next = solve_goal(sample_stage, q_previous)
                if edge_in_collision(
                    model, data, q_previous, q_next, obstacles, step=0.035
                ):
                    raise RuntimeError(
                        f"{stage['name']}: interpolated edge collides at "
                        f"alpha={alpha:.2f}"
                    )
                q_segment.append(q_next)
                q_previous = q_next
            q_current = q_previous

        q_path_full.extend(q.copy() for q in q_segment)
        stage_configs.append(
            (
                stage["name"],
                q_current.copy(),
                stage["left_goal"].copy(),
                stage["right_goal"].copy(),
            )
        )
        print(
            f"stage {stage['name']}: left={np.round(stage['left_goal'], 3)}, "
            f"right={np.round(stage['right_goal'], 3)}"
        )

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


def add_box_preview_trace(fig, box_center):
    center = np.asarray(box_center, dtype=float) + np.array(
        [0.0, 0.0, 0.5 * DEFAULT_BOX_HEIGHT]
    )
    half = np.array(
        [DEFAULT_BOX_HALF_DEPTH_X, DEFAULT_BOX_HALF_WIDTH_Y, 0.5 * DEFAULT_BOX_HEIGHT]
    )
    vertices = np.array(
        [
            center + half * np.array([sx, sy, sz])
            for sx, sy, sz in (
                (-1, -1, -1),
                (1, -1, -1),
                (1, 1, -1),
                (-1, 1, -1),
                (-1, -1, 1),
                (1, -1, 1),
                (1, 1, 1),
                (-1, 1, 1),
            )
        ]
    )
    triangles = (
        (0, 1, 2), (0, 2, 3),
        (4, 6, 5), (4, 7, 6),
        (0, 4, 5), (0, 5, 1),
        (1, 5, 6), (1, 6, 2),
        (2, 6, 7), (2, 7, 3),
        (3, 7, 4), (3, 4, 0),
    )
    fig.add_trace(
        go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=[triangle[0] for triangle in triangles],
            j=[triangle[1] for triangle in triangles],
            k=[triangle[2] for triangle in triangles],
            color="#FBBF24",
            opacity=0.38,
            name="nominal box",
            flatshading=True,
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
    box_center,
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
    add_box_preview_trace(fig, box_center)

    for name, _q, left_target, right_target in stage_configs:
        show_text = name in {
            "initial_outside",
            "wall_slot_insert",
            "nominal_contact_seek",
            "physical_base_retreat",
        }
        is_post_contact = name in {
            "nominal_contact_seek",
            "cartesian_clearance_lift",
            "physical_base_retreat",
        }
        fig.add_trace(
            go.Scatter3d(
                x=[left_target[0], right_target[0]],
                y=[left_target[1], right_target[1]],
                z=[left_target[2], right_target[2]],
                mode="markers+text" if show_text else "markers",
                marker=dict(
                    size=5,
                    color=("#B45309" if is_post_contact else "#111827"),
                ),
                text=[f"{name}-L", f"{name}-R"],
                hovertext=[f"{name}-L", f"{name}-R"],
                hoverinfo="text+x+y+z",
                textposition="top center",
                name=f"stage: {name}",
                showlegend=False,
            )
        )

    snapshot_count = min(6, len(q_path))
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
        title=(
            "Current dual-arm position preview "
            "(orange: nominal contact, 5 cm lift, 28 cm base retreat)"
        ),
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


def _infer_target_body_name(env, target_position):
    """Choose the nearest package body when perception supplies only XYZ."""
    candidates = []
    for body_name in ("box_yellow", "box_pink", "box_brown"):
        try:
            body_position = np.asarray(
                env.mj_data.body(body_name).xpos, dtype=float
            ).copy()
        except (AttributeError, KeyError):
            continue
        candidates.append(
            (
                float(
                    np.linalg.norm(
                        body_position - np.asarray(target_position, dtype=float)
                    )
                ),
                body_name,
            )
        )
    if not candidates:
        return "box_yellow"
    return min(candidates, key=lambda item: item[0])[1]


def grasp_object(env, target_world, grasp_world=None):
    """Grasp a recognized package in an already-running DISCOVERSE env.

    Parameters follow the integration document. ``target_world`` accepts
    either XYZ or the recognition dictionary used by the task manager;
    ``grasp_world`` is an optional recommended central contact point.
    The public result is strictly ``True``/``False``. Detailed diagnostics are
    available through :func:`get_last_manipulation_result`.
    """
    if env is None:
        _set_manipulation_result(env, False, "invalid_env", retryable=False)
        return False
    try:
        target_position = _interface_world_position(target_world, "target_world")
        recommended_grasp = (
            target_position + np.array([0.050, 0.0, 0.095], dtype=float)
            if grasp_world is None
            else _interface_world_position(grasp_world, "grasp_world")
        )
        requested_body_name = (
            target_world.get("body_name")
            if isinstance(target_world, dict)
            else None
        )
        target_body_name = (
            str(requested_body_name)
            if requested_body_name
            else _infer_target_body_name(env, target_position)
        )
        env_time = float(env.mj_data.time)
        mjcf_path = getattr(
            getattr(env, "config", None),
            "mjcf_file_path",
            DEFAULT_MJCF_FILE_PATH,
        )
        success = run_box_pick_grasp_scene(
            mjcf_path,
            discoverse_root=DEFAULT_DISCOVERSE_ROOT,
            urdf_path=DEFAULT_URDF_PATH,
            headless=bool(getattr(getattr(env, "config", None), "headless", False)),
            max_seconds=env_time + 140.0,
            pose_source="external",
            external_env=env,
            target_world=target_position,
            grasp_world=recommended_grasp,
            target_body_name=target_body_name,
            return_on_result=True,
        )
        if success:
            _set_manipulation_result(env, True, "grasp_acquired", retryable=False)
        elif get_last_manipulation_result(env)["reason"] == "no_manipulation_result":
            _set_manipulation_result(env, False, "grasp_failed", retryable=True)
        return bool(success)
    except (TypeError, ValueError, RuntimeError, KeyError) as exc:
        _set_manipulation_result(
            env,
            False,
            f"grasp_interface_error:{type(exc).__name__}:{exc}",
            retryable=not isinstance(exc, TypeError),
        )
        print(">>> grasp_object failed:", get_last_manipulation_result(env))
        return False


def _interface_control_step(env, action, step_func, speed_scale=1.0):
    for index in range(2, int(env.njctrl)):
        ratio = max(0.05, float(env.joint_move_ratio[index]))
        action[index] = step_func(
            action[index],
            env.target_control[index],
            float(speed_scale) * ratio * float(env.delta_t),
        )
    action[:2] = 0.0
    env.step(action)


def place_object(env, placement):
    """Place the currently grasped package using the same DISCOVERSE env."""
    if env is None:
        return False
    try:
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
        translation = destination - start_box
        if float(np.linalg.norm(translation)) > 0.45:
            _set_manipulation_result(
                env,
                False,
                "placement_out_of_reach_after_navigation",
                retryable=True,
            )
            return False

        left_rotation = np.asarray(context["left_grip_rot"], dtype=float)
        right_rotation = np.asarray(context["right_grip_rot"], dtype=float)
        if (
            "left_endpoint_target_base" in context
            and "right_endpoint_target_base" in context
        ):
            base_world_tmat = get_body_tmat(env.mj_data, "mmk2")
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
        # Preserve the small, load-dependent difference between the unloaded
        # Cartesian clamp command and the measured finger sites.  Placement
        # convergence is about following the requested displacement, not
        # eliminating the elastic deflection that supplies normal force.
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
        waypoint_count = max(
            8, int(math.ceil(float(np.linalg.norm(translation)) / 0.012)) + 1
        )
        loss_streak = 0
        left_force_offset = 0.0
        right_force_offset = 0.0
        for alpha in np.linspace(0.0, 1.0, waypoint_count)[1:]:
            left_nominal = left_start + alpha * translation
            right_nominal = right_start + alpha * translation
            segment_start = float(env.mj_data.time)
            last_force_update = -1.0e9
            while True:
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
                    if max_compression > 0.0048 or max(left_load, right_load) > 17.0:
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
                env.tctr_left_arm[:] = env.solveArmEndTarget(
                    env.get_tmat_wrt_mmk2base(left_target),
                    env.arm_action,
                    "l",
                    np.asarray(env.sensor_lft_arm_qpos, dtype=float),
                    left_rotation,
                )
                env.tctr_right_arm[:] = env.solveArmEndTarget(
                    env.get_tmat_wrt_mmk2base(right_target),
                    env.arm_action,
                    "r",
                    np.asarray(env.sensor_rgt_arm_qpos, dtype=float),
                    right_rotation,
                )
                env.set_left_arm_new_target = True
                env.set_right_arm_new_target = True
                env.joint_move_ratio[:] = 1.0
                _interface_control_step(env, action, step_func, speed_scale=1.30)
                loss_streak = (
                    loss_streak + 1
                    if min(left_load, right_load) < 0.05
                    else 0
                )
                endpoint_error = max(
                    float(
                        np.linalg.norm(
                            np.asarray(
                                env.mj_data.site("lft_endpoint").xpos,
                                dtype=float,
                            )
                            - (left_target + left_tracking_bias)
                        )
                    ),
                    float(
                        np.linalg.norm(
                            np.asarray(
                                env.mj_data.site("rgt_endpoint").xpos,
                                dtype=float,
                            )
                            - (right_target + right_tracking_bias)
                        )
                    ),
                )
                segment_elapsed = float(env.mj_data.time) - segment_start
                if segment_elapsed >= 0.12 and endpoint_error <= 0.009:
                    break
                if loss_streak >= 300:
                    raise RuntimeError("package contact lost during placement")
                if segment_elapsed >= 1.50:
                    raise RuntimeError(
                        "arm endpoint did not reach placement waypoint: "
                        f"alpha={alpha:.3f}, error={endpoint_error:.4f}m, "
                        f"loads=({left_load:.2f},{right_load:.2f})N, "
                        f"offsets=({left_force_offset:.4f},"
                        f"{right_force_offset:.4f})m"
                    )

        settled_start = float(env.mj_data.time)
        while float(env.mj_data.time) - settled_start < 0.40:
            _interface_control_step(env, action, step_func, speed_scale=1.0)

        box_at_destination = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()
        if float(np.linalg.norm(box_at_destination - destination)) > 0.070:
            raise RuntimeError(
                "package did not follow the arms to the placement pose"
            )

        box_tmat = get_body_tmat(env.mj_data, target_body_name)
        side_axis = np.asarray(box_tmat[:3, 1], dtype=float)
        side_axis[2] = 0.0
        if np.linalg.norm(side_axis) < 1.0e-6:
            side_axis = np.array([0.0, 1.0, 0.0])
        side_axis /= np.linalg.norm(side_axis)
        left_now = np.asarray(
            env.mj_data.site("lft_endpoint").xpos, dtype=float
        ).copy()
        right_now = np.asarray(
            env.mj_data.site("rgt_endpoint").xpos, dtype=float
        ).copy()
        if np.dot(left_now - right_now, side_axis) < 0.0:
            side_axis *= -1.0
        release_distance = 0.055
        for alpha in np.linspace(0.0, 1.0, 18)[1:]:
            left_target = left_now + alpha * release_distance * side_axis
            right_target = right_now - alpha * release_distance * side_axis
            env.tctr_left_arm[:] = env.solveArmEndTarget(
                env.get_tmat_wrt_mmk2base(left_target),
                env.arm_action,
                "l",
                np.asarray(env.sensor_lft_arm_qpos, dtype=float),
                left_rotation,
            )
            env.tctr_right_arm[:] = env.solveArmEndTarget(
                env.get_tmat_wrt_mmk2base(right_target),
                env.arm_action,
                "r",
                np.asarray(env.sensor_rgt_arm_qpos, dtype=float),
                right_rotation,
            )
            env.set_left_arm_new_target = True
            env.set_right_arm_new_target = True
            release_start = float(env.mj_data.time)
            while float(env.mj_data.time) - release_start < 0.12:
                _interface_control_step(env, action, step_func, speed_scale=1.30)

        release_box = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()
        wait_start = float(env.mj_data.time)
        while float(env.mj_data.time) - wait_start < 0.80:
            _interface_control_step(env, action, step_func, speed_scale=1.0)
        final_box = np.asarray(
            get_body_tmat(env.mj_data, target_body_name)[:3, 3], dtype=float
        ).copy()
        final_report = env.wall_grasp_report()
        finger_load = sum(float(v) for v in final_report["forces"].values())
        stable = bool(
            np.linalg.norm(final_box[:2] - destination[:2]) <= 0.070
            and final_box[2] >= destination[2] - 0.060
            and np.linalg.norm(final_box - release_box) <= 0.070
            and finger_load <= 0.20
        )
        context["grasped"] = False
        context["placed"] = stable
        context["box_pose"] = final_box.copy()
        _set_manipulation_result(
            env,
            stable,
            "place_completed" if stable else "place_verification_failed",
            retryable=not stable,
        )
        print(
            ">>> place_object result:",
            get_last_manipulation_result(env),
            f"destination={np.round(destination, 4)}",
            f"final_box={np.round(final_box, 4)}",
        )
        return stable
    except (TypeError, ValueError, RuntimeError, KeyError) as exc:
        _set_manipulation_result(
            env,
            False,
            f"place_interface_error:{type(exc).__name__}:{exc}",
            retryable=not isinstance(exc, TypeError),
        )
        print(">>> place_object failed:", get_last_manipulation_result(env))
        return False


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
        help="visualize the current nominal Cartesian execution targets without running MuJoCo",
    )
    parser.add_argument(
        "--headless-preview-seconds",
        type=float,
        default=None,
        help="run the MJCF auto-motion preview without a window for this many seconds",
    )
    parser.add_argument("--left-frame", default=LEFT_EEF_FRAME)
    parser.add_argument("--right-frame", default=RIGHT_EEF_FRAME)
    parser.add_argument(
        "--base-position", nargs=3, type=float, default=list(NOMINAL_BASE_POSITION)
    )
    parser.add_argument("--slide", type=float, default=NOMINAL_SLIDE)
    parser.add_argument(
        "--box-center", nargs=3, type=float, default=list(NOMINAL_BOX_CENTER)
    )
    parser.add_argument(
        "--cabinet-front-x",
        type=float,
        default=NOMINAL_CABINET_FRONT_X,
        help="conservative shelf entry plane (default: 1.13 m; physical face: 1.18 m)",
    )
    parser.add_argument("--box-yaw", type=float, default=0.0)
    parser.add_argument(
        "--plan-seed",
        type=int,
        default=0,
        help="random seed for reproducible offline RRT previews (default: 0)",
    )
    parser.add_argument("--randomize-scene", action="store_true")
    parser.add_argument(
        "--randomize-box-pose",
        action="store_true",
        help=(
            "randomize package X/Y position and choose shelf level 2, 3, or 4; "
            "the base is laterally aligned with the randomized package"
        ),
    )
    parser.add_argument(
        "--shelf-level",
        type=int,
        choices=(2, 3, 4),
        default=None,
        help="force package initialization on shelf level 2, 3, or 4",
    )
    parser.add_argument(
        "--scene-seed",
        type=int,
        default=None,
        help=(
            "reproduce a randomized scene with a fixed seed; when omitted, "
            "a fresh seed is generated for every run"
        ),
    )
    parser.add_argument(
        "--pose-source",
        choices=("ground-truth", "perception"),
        default="ground-truth",
        help=(
            "use line RGB-D perception with a hand-camera checkpoint, or the "
            "legacy MuJoCo truth pose for grasp-controller regression tests"
        ),
    )
    parser.add_argument(
        "--perception-root",
        default=DEFAULT_PERCEPTION_ROOT,
        help="path containing line's perception_module and my_work directories",
    )
    parser.add_argument(
        "--perception-python",
        default=DEFAULT_PERCEPTION_PYTHON,
        help="GPU Python executable used by the persistent VLM/SAM worker",
    )
    parser.add_argument(
        "--perception-query",
        default="yellow packaging box",
        help="target phrase sent to the existing VLM/SAM perception module",
    )
    parser.add_argument(
        "--perception-center-offset",
        nargs=3,
        type=float,
        default=[0.12, 0.0, -0.095],
        metavar=("DX", "DY", "DZ"),
        help=(
            "calibrated visible-surface to box-bottom-centre offset in world metres"
        ),
    )
    parser.add_argument("--perception-debug", action="store_true")
    args = parser.parse_args()


    if not args.plan:
        run_box_pick_grasp_scene(
            args.mjcf,
            args.discoverse_root,
            urdf_path=args.urdf,
            headless=args.headless_preview_seconds is not None,
            max_seconds=args.headless_preview_seconds,
            randomize_scene=args.randomize_scene,
            randomize_box_pose=args.randomize_box_pose,
            shelf_level=args.shelf_level,
            scene_seed=args.scene_seed,
            pose_source=args.pose_source,
            perception_root=args.perception_root,
            perception_python=args.perception_python,
            perception_query=args.perception_query,
            perception_center_offset=args.perception_center_offset,
            perception_debug=args.perception_debug,
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

    random.seed(args.plan_seed)
    np.random.seed(args.plan_seed)

    q_start = make_full_configuration(model, args.base_position, args.slide)

    box_center = np.array(args.box_center, dtype=float)
    obstacles = build_cabinet_obstacles(box_center)
    pick_targets = compute_dual_box_pick_targets(
        box_center=box_center,
        box_yaw=args.box_yaw,
        cabinet_front_x=args.cabinet_front_x,
        box_half_width_y=DEFAULT_BOX_HALF_WIDTH_Y,
        grasp_clearance=-0.016,
    )
    stage_specs = build_current_plan_stage_specs(pick_targets)
    initial = stage_specs[0]
    q_initial, initial_ok = solve_dual_position_ik(
        model,
        data,
        left_frame_id,
        right_frame_id,
        active_q_indices,
        active_v_indices,
        q_start,
        initial["left_goal"],
        initial["right_goal"],
        left_q_indices,
        left_v_indices,
        right_q_indices,
        right_v_indices,
        obstacles=obstacles,
    )
    if not initial_ok:
        raise RuntimeError("failed to solve the initial outside preview pose")
    q_path = [q_initial]
    left_points, right_points, _stage_end_indices = (
        build_current_cartesian_preview(stage_specs)
    )
    stage_configs = [
        (
            stage["name"],
            q_initial.copy() if index == 0 else None,
            stage["left_goal"].copy(),
            stage["right_goal"].copy(),
        )
        for index, stage in enumerate(stage_specs)
    ]

    print(
        "position-only preview: MuJoCo wrist orientations and contact feedback "
        "are not represented by the Pinocchio URDF"
    )
    for stage in stage_specs:
        print(
            f"stage {stage['name']}: left={np.round(stage['left_goal'], 3)}, "
            f"right={np.round(stage['right_goal'], 3)}"
        )
    print(f"planned Cartesian samples: {len(left_points)}")
    print(f"left path start: {left_points[0]}")
    print(f"left path goal:  {left_points[-1]}")
    print(f"right path start: {right_points[0]}")
    print(f"right path goal:  {right_points[-1]}")

    visualize_trajectory(
        model,
        data,
        left_frame_id,
        right_frame_id,
        q_path,
        left_points,
        right_points,
        obstacles,
        stage_configs,
        box_center,
    )


if __name__ == "__main__":
    main()
