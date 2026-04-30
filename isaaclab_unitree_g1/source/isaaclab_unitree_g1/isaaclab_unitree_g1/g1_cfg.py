# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg

G1_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path="ros2_ws/src/g1_description/urdf/robot.urdf",
        fix_base=False,
        self_collision=True,
        collider_type="convex_hull",
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.74),
        joint_pos={
            ".*_hip_pitch_joint": 0.0,
            ".*_hip_roll_joint": 0.0,
            ".*_hip_yaw_joint": 0.0,
            ".*_knee_joint": 0.0,
            ".*_ankle_pitch_joint": 0.0,
            ".*_ankle_roll_joint": 0.0,
            "waist_yaw_joint": 0.0,
            ".*_shoulder_pitch_joint": 0.0,
            ".*_shoulder_roll_joint": 0.0,
            ".*_shoulder_yaw_joint": 0.0,
            ".*_elbow_joint": 0.0,
            ".*_wrist_roll_joint": 0.0,
        },
    ),
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names=[".*_hip_.*", ".*_knee_.*", ".*_ankle_.*"],
            effort_limit=88.0,
            velocity_limit=32.0,
            stiffness=40.0,
            damping=1.0,
        ),
        "upper_body": ImplicitActuatorCfg(
            joint_names=["waist_yaw_joint", ".*_shoulder_.*", ".*_elbow_.*", ".*_wrist_.*"],
            effort_limit=25.0,
            velocity_limit=37.0,
            stiffness=20.0,
            damping=1.0,
        ),
    },
)
