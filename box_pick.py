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
    [0.0, 0.998482, 0.055072],
    [0.923880, -0.021075, 0.382103],
    [0.382683, 0.050880, -0.922477],
])
RIGHT_GRIP_ROT = np.array([
    [0.0, -0.998482, 0.055072],
    [-0.923880, -0.021075, -0.382103],
    [0.382683, -0.050880, -0.922477],
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

    for geom_id in range(geom_start, geom_start + geom_num):
        geom_type = mj_model.geom_type[geom_id]
        if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
            return float(mj_model.geom_size[geom_id, 1])
        if geom_type == mujoco.mjtGeom.mjGEOM_MESH:
            mesh_id = int(mj_model.geom_dataid[geom_id])
            vert_adr = int(mj_model.mesh_vertadr[mesh_id])
            vert_num = int(mj_model.mesh_vertnum[mesh_id])
            verts = mj_model.mesh_vert[vert_adr: vert_adr + vert_num]
            return float((verts[:, 1].max() - verts[:, 1].min()) / 2.0)

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
):
    """Run collision-aware dual-side grasp and rigid extraction in MuJoCo.

    Planning/execution policy:
      1. Read the real ``box_yellow`` pose and width from the code-2 MJCF scene.
      2. Use RRT + AABB collision checking for the ungrasped approach path.
      3. Close both grippers gradually on the two side walls.
      4. After grasping, keep the left/right grasp geometry fixed and move both
         arms through synchronized Cartesian lift/extraction waypoints.
      5. Collision-check every constrained transport segment before execution.

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

    def sync_reset_pose(sim_node, action, mujoco_module):
        """Keep qpos, controls, and sensors aligned before the first rendered step."""
        sim_node.mj_data.ctrl[:sim_node.njctrl] = action[:sim_node.njctrl]
        sim_node.target_control[:] = action[:sim_node.njctrl]
        sim_node.mj_data.qpos[:sim_node.njq] = sim_node.init_joint_pose[:]
        sim_node.mj_data.qpos[9:10] = action[2:3]
        sim_node.mj_data.qpos[10:12] = action[3:5]
        sim_node.mj_data.qpos[12:18] = action[5:11]
        sim_node.mj_data.qpos[18:20] = [action[11], -action[11]]
        sim_node.mj_data.qpos[20:26] = action[12:18]
        sim_node.mj_data.qpos[26:28] = [action[18], -action[18]]
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
    grip_close = 0.0
    grip_open = 0.16
    head_pitch = -0.25
    clamp_duration = 1.6
    outward_grip_angle = np.deg2rad(0.0)
    into_cabinet_turn_angle = np.deg2rad(0.0)
    downward_insert_angle = np.deg2rad(0.0)
    horizontal_finger_roll = np.deg2rad(0.0)

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

    left_grip_rot = mat3_mul(
        mat3_mul(
            mat3_mul(LEFT_GRIP_ROT, rot_z(into_cabinet_turn_angle + outward_grip_angle)),
            rot_x(horizontal_finger_roll),
        ),
        rot_y(-downward_insert_angle),
    )
    right_grip_rot = mat3_mul(
        mat3_mul(
            mat3_mul(RIGHT_GRIP_ROT, rot_z(-into_cabinet_turn_angle - outward_grip_angle)),
            rot_x(-horizontal_finger_roll),
        ),
        rot_y(-downward_insert_angle),
    )

    class MyAlgorithmNode(MMK2TaskBase):
        def __init__(self, config):
            self._arm_ik_solver = None
            super().__init__(config)
            self._arm_ik_solver = StableAirbotPlayIK()
            self._configure_grasp_contacts()
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

        def _configure_grasp_contacts(self):
            for actuator_name in ("lft_gripper", "rgt_gripper"):
                actuator_id = int(self.mj_model.actuator(actuator_name).id)
                self.mj_model.actuator_gainprm[actuator_id, 0] = 35.0
                self.mj_model.actuator_forcelimited[actuator_id] = 1
                self.mj_model.actuator_forcerange[actuator_id, :] = [-25.0, 25.0]

            contact_bodies = {
                target_body_name,
                "lft_finger_left_link",
                "lft_finger_right_link",
                "rgt_finger_left_link",
                "rgt_finger_right_link",
            }
            for geom_id in range(self.mj_model.ngeom):
                body_name = self.mj_model.body(int(self.mj_model.geom_bodyid[geom_id])).name
                if body_name in contact_bodies:
                    self.mj_model.geom_friction[geom_id, :] = [5.0, 0.12, 0.012]
                    self.mj_model.geom_solref[geom_id, :] = [0.004, 1.0]
                    self.mj_model.geom_solimp[geom_id, :] = [0.98, 0.995, 0.001, 0.5, 2.0]
            mujoco.mj_setConst(self.mj_model, self.mj_data)
            mujoco.mj_forward(self.mj_model, self.mj_data)
            print("grasp contact friction configured")

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
            print(
                "success check:",
                f"box_x={box_pos[0]:.3f}",
                f"front_x={self.cabinet_front_x:.3f}",
                f"box_z={box_pos[2]:.3f}",
                f"start_z={self.box_start_z:.3f}",
            )
            return bool(outside_ok and not_dropped)

    cfg = MMK2Cfg()
    cfg.mjcf_file_path = str(mjcf_path)
    cfg.use_gaussian_renderer = False
    cfg.headless = headless
    cfg.enable_render = not headless
    cfg.sync = not headless
    cfg.render_set = {
        "fps": 30,
        "width": 1280,
        "height": 720,
        "window_title": "DISCOVERSE dual-side grasp + collision-aware extraction",
    }
    cfg.obs_rgb_cam_id = None
    cfg.obs_depth_cam_id = None
    cfg.init_state = MMK2Cfg.init_state.copy()
    cfg.init_state["base_position"] = [0.58, 0.715, 0.0]
    cfg.init_state["base_orientation"] = [1.0, 0.0, 0.0, 0.0]
    cfg.init_state["head_qpos"] = [0.0, head_pitch]
    cfg.init_state["lft_gripper_qpos"] = [grip_open]
    cfg.init_state["rgt_gripper_qpos"] = [grip_open]

    sim_node = MyAlgorithmNode(cfg)
    obs = sim_node.reset()
    action = sim_node.init_joint_ctrl.copy()
    sync_reset_pose(sim_node, action, mujoco)
    base_lock_x = float(cfg.init_state["base_position"][0])
    base_lock_y = float(cfg.init_state["base_position"][1])

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
    sim_node.cabinet_front_x = cabinet_front_x
    sim_node.tctr_head[1] = head_pitch
    sim_node.tctr_lft_gripper[:] = grip_open
    sim_node.tctr_rgt_gripper[:] = grip_open
    action[:] = sim_node.target_control[:]
    sync_reset_pose(sim_node, action, mujoco)

    targets = compute_dual_box_pick_targets(
        box_center=box_center,
        cabinet_front_x=cabinet_front_x,
        box_half_width_y=box_half_width_y,
        side_axis=side_axis,
    )

    def world_to_base(point_world):
        base_tmat = get_body_tmat(sim_node.mj_data, "mmk2")
        base_rot = base_tmat[:3, :3]
        base_pos = base_tmat[:3, 3]
        return base_rot.T @ (np.asarray(point_world, dtype=float) - base_pos)

    try:
        left_outside_base = world_to_base(targets["outside_left"])
        right_outside_base = world_to_base(targets["outside_right"])
        left_start_q = sim_node.solveArmEndTarget(
            left_outside_base,
            sim_node.arm_action,
            "l",
            action[5:11].copy(),
            left_grip_rot,
        )
        right_start_q = sim_node.solveArmEndTarget(
            right_outside_base,
            sim_node.arm_action,
            "r",
            action[12:18].copy(),
            right_grip_rot,
        )
        action[5:11] = np.asarray(left_start_q, dtype=float)
        action[12:18] = np.asarray(right_start_q, dtype=float)
        action[2] = 0.0
        action[3:5] = [0.0, head_pitch]
        action[11] = grip_open
        action[18] = grip_open
        sync_reset_pose(sim_node, action, mujoco)
        print(
            ">>> initial arms snapped to outside grasp-ready pose:",
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

    def solve_world_pair(left_world, right_world, left_ref, right_ref):
        left_base = world_to_base(left_world)
        right_base = world_to_base(right_world)
        left_q = sim_node.solveArmEndTarget(
            left_base, sim_node.arm_action, "l", left_ref, left_grip_rot
        )
        right_q = sim_node.solveArmEndTarget(
            right_base, sim_node.arm_action, "r", right_ref, right_grip_rot
        )
        return np.asarray(left_q, dtype=float), np.asarray(right_q, dtype=float)

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
            left_target, right_target, left_ref, right_ref
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
                "speed": 4.0,
            }
        )

        approach_stages = [
            ("mouth", targets["mouth_left"], targets["mouth_right"]),
            ("inside_high", targets["inside_high_left"], targets["inside_high_right"]),
            ("side_grasp", targets["grasp_left"], targets["grasp_right"]),
        ]
        for stage_name, left_target, right_target in approach_stages:
            q_current, active_path = plan_rrt_stage(
                q_current, left_target, right_target, stage_name
            )
            execution_steps.append(
                {"kind": "joint_path", "name": stage_name, "path": active_path, "grip": grip_open}
            )

        execution_steps.append(
            {"kind": "clamp", "name": "dual-side clamp", "duration": clamp_duration}
        )

        transport_specs = [
            (
                "rigid_lift",
                targets["grasp_left"],
                targets["grasp_right"],
                targets["transport_lift_left"],
                targets["transport_lift_right"],
            ),
            (
                "rigid_to_mouth",
                targets["transport_lift_left"],
                targets["transport_lift_right"],
                targets["transport_mouth_left"],
                targets["transport_mouth_right"],
            ),
            (
                "rigid_outside",
                targets["transport_mouth_left"],
                targets["transport_mouth_right"],
                targets["transport_outside_left"],
                targets["transport_outside_right"],
            ),
        ]
        transport_orientation_offsets = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        for stage_name, left_start, right_start, left_goal, right_goal in transport_specs:
            q_current, active_path, transport_orientation_offsets = plan_rigid_transport_stage(
                q_current,
                left_start,
                right_start,
                left_goal,
                right_goal,
                stage_name,
                orientation_offsets=transport_orientation_offsets,
            )
            execution_steps.append(
                {
                    "kind": "joint_path",
                    "name": stage_name,
                    "path": active_path,
                    "grip": grip_close,
                    "speed_scale": 0.65,
                    "err_threshold": 0.030,
                    "point_timeout": 0.75,
                }
            )

        execution_steps.append(
            {"kind": "hold", "name": "hold outside cabinet", "duration": float(hold_seconds)}
        )
        print(">>> collision-aware plan ready; executing dual-side grasp")
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
    result_reported = False

    def print_grasp_debug(label):
        box_pos_dbg = get_body_tmat(sim_node.mj_data, target_body_name)[:3, 3]
        lft_pos_dbg = get_body_tmat(sim_node.mj_data, "lft_arm_link6")[:3, 3]
        rgt_pos_dbg = get_body_tmat(sim_node.mj_data, "rgt_arm_link6")[:3, 3]
        lft_fl_dbg = get_body_tmat(sim_node.mj_data, "lft_finger_left_link")[:3, 3]
        lft_fr_dbg = get_body_tmat(sim_node.mj_data, "lft_finger_right_link")[:3, 3]
        rgt_fl_dbg = get_body_tmat(sim_node.mj_data, "rgt_finger_left_link")[:3, 3]
        rgt_fr_dbg = get_body_tmat(sim_node.mj_data, "rgt_finger_right_link")[:3, 3]
        contact_pairs_dbg = []
        interesting_bodies_dbg = {
            target_body_name,
            "lft_finger_left_link",
            "lft_finger_right_link",
            "rgt_finger_left_link",
            "rgt_finger_right_link",
        }
        for contact_idx in range(int(sim_node.mj_data.ncon)):
            contact = sim_node.mj_data.contact[contact_idx]
            geom1 = int(contact.geom1)
            geom2 = int(contact.geom2)
            body1 = sim_node.mj_model.body(
                int(sim_node.mj_model.geom_bodyid[geom1])
            ).name
            body2 = sim_node.mj_model.body(
                int(sim_node.mj_model.geom_bodyid[geom2])
            ).name
            if body1 in interesting_bodies_dbg or body2 in interesting_bodies_dbg:
                contact_pairs_dbg.append((body1, body2, round(float(contact.dist), 4)))
        print(
            f"{label}:",
            "box=", np.array2string(box_pos_dbg, precision=3),
            "left=", np.array2string(lft_pos_dbg, precision=3),
            "right=", np.array2string(rgt_pos_dbg, precision=3),
            "lfingers=",
            np.array2string(np.vstack([lft_fl_dbg, lft_fr_dbg]), precision=3),
            "rfingers=",
            np.array2string(np.vstack([rgt_fl_dbg, rgt_fr_dbg]), precision=3),
            "ncon=",
            int(sim_node.mj_data.ncon),
            "contacts=",
            contact_pairs_dbg[:16],
            "dy=",
            round(float(lft_pos_dbg[1] - rgt_pos_dbg[1]), 4),
        )

    while sim_node.running:
        now = sim_node.mj_data.time
        if max_seconds is not None and now >= max_seconds:
            print(">>> preview time limit reached")
            break
        if step_index >= len(execution_steps):
            if headless:
                break
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            action[11] = grip_close
            action[18] = grip_close
            obs, _, _, _, _ = sim_node.step(action)
            continue
            break

        step = execution_steps[step_index]
        if current_step_name != step["name"]:
            current_step_name = step["name"]
            step_enter_time = now
            point_enter_time = now
            path_index = 0
            print(f">>> execute: {current_step_name}")

        if step["kind"] == "joint_path":
            sim_node.tctr_lft_gripper[:] = step["grip"]
            sim_node.tctr_rgt_gripper[:] = step["grip"]
            path = step["path"]
            target_active = np.asarray(path[min(path_index, len(path) - 1)], dtype=float)
            sim_node.tctr_left_arm[:] = target_active[:6]
            sim_node.tctr_right_arm[:] = target_active[6:]
            sim_node.set_left_arm_new_target = True
            sim_node.set_right_arm_new_target = True
            update_joint_move_ratio()
            if "speed_scale" in step:
                speed_scale = float(step["speed_scale"])
                sim_node.joint_move_ratio[5:11] *= speed_scale
                sim_node.joint_move_ratio[12:18] *= speed_scale

            left_err = float(np.linalg.norm(sim_node.sensor_lft_arm_qpos - target_active[:6]))
            right_err = float(np.linalg.norm(sim_node.sensor_rgt_arm_qpos - target_active[6:]))
            point_elapsed = now - point_enter_time
            err_threshold = float(step.get("err_threshold", 0.045))
            point_timeout = float(step.get("point_timeout", 0.55))
            if (left_err < err_threshold and right_err < err_threshold) or point_elapsed > point_timeout:
                path_index += 1
                point_enter_time = now
                if path_index >= len(path):
                    if current_step_name in {"rigid_lift", "rigid_to_mouth", "rigid_outside"}:
                        print_grasp_debug(f"{current_step_name} debug")
                    step_index += 1
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
                print_grasp_debug("clamp debug")
                step_index += 1
                current_step_name = None

        elif step["kind"] == "hold":
            sim_node.tctr_lft_gripper[:] = grip_close
            sim_node.tctr_rgt_gripper[:] = grip_close
            if now - step_enter_time >= step["duration"] and not result_reported:
                success = sim_node.check_success()
                print(">>> RESULT:", "SUCCESS" if success else "FAILED")
                result_reported = True
                step_index += 1
                current_step_name = None

        for i in range(2, sim_node.njctrl):
            action[i] = step_func(
                action[i],
                sim_node.target_control[i],
                0.65 * sim_node.joint_move_ratio[i] * sim_node.delta_t,
            )
        action[0] = 0.0
        action[1] = 0.0
        obs, _, _, _, _ = sim_node.step(action)

        # Manipulation is planned for a fixed base. Prevent contact forces from
        # making the mobile base drift and invalidating the collision plan.
        sim_node.mj_data.qpos[0] = base_lock_x
        sim_node.mj_data.qpos[1] = base_lock_y
        sim_node.mj_data.qvel[0] = 0.0
        sim_node.mj_data.qvel[1] = 0.0
        mujoco.mj_forward(sim_node.mj_model, sim_node.mj_data)

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
    grasp_clearance=-0.025,
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
    inside_x = box_center[0] - DEFAULT_BOX_HALF_DEPTH_X - 0.010
    grasp_x = box_center[0] - DEFAULT_BOX_HALF_DEPTH_X + 0.100
    retreat_x = cabinet_front_x - 0.075

    box_bottom_z = float(box_center[2])
    box_top_z = box_bottom_z + DEFAULT_BOX_HEIGHT
    approach_z = box_top_z + 0.020
    inside_z = box_bottom_z + DEFAULT_BOX_HEIGHT * 0.84
    grasp_z = box_bottom_z + DEFAULT_BOX_HEIGHT * 0.76
    approach_lateral = float(box_half_width_y + pre_clearance)
    grasp_lateral = float(box_half_width_y + grasp_clearance)

    def side_pair(x, z, lateral):
        center = np.array([x, box_center[1], z], dtype=float)
        point_a = center + axis * lateral
        point_b = center - axis * lateral
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
        inside_x, inside_z, grasp_lateral
    )
    grasp_left, grasp_right = side_pair(
        grasp_x, grasp_z, grasp_lateral
    )

    inside_mid_left = (mouth_left + inside_high_left) * 0.5
    inside_mid_right = (mouth_right + inside_high_right) * 0.5

    # Once the grippers close, all subsequent target pairs are generated by
    # applying the same translation to the original grasp pair.
    transport_squeeze = 0.010
    transport_lateral = max(0.030, grasp_lateral - transport_squeeze)
    carry_left, carry_right = side_pair(grasp_x, grasp_z, transport_lateral)

    lift_translation = np.array([0.0, 0.0, lift_delta])
    mouth_translation = np.array([mouth_x - grasp_x, 0.0, lift_delta])
    outside_translation = np.array([retreat_x - grasp_x, 0.0, lift_delta])

    transport_lift_left = carry_left + lift_translation
    transport_lift_right = carry_right + lift_translation
    transport_mouth_left = carry_left + mouth_translation
    transport_mouth_right = carry_right + mouth_translation
    transport_outside_left = carry_left + outside_translation
    transport_outside_right = carry_right + outside_translation

    return {
        "outside_left": outside_left,
        "outside_right": outside_right,
        "mouth_left": mouth_left,
        "mouth_right": mouth_right,
        "inside_mid_left": inside_mid_left,
        "inside_mid_right": inside_mid_right,
        "inside_high_left": inside_high_left,
        "inside_high_right": inside_high_right,
        "grasp_left": grasp_left,
        "grasp_right": grasp_right,
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
    args = parser.parse_args()

    if not args.plan:
        run_box_pick_grasp_scene(
            args.mjcf,
            args.discoverse_root,
            urdf_path=args.urdf,
            headless=args.headless_preview_seconds is not None,
            max_seconds=args.headless_preview_seconds,
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
