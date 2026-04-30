# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import torch

from isaaclab.assets import Articulation
from isaaclab.managers import SceneEntityCfg

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def _quat_rotate(q: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    qvec = q[:, 1:]
    v = v.unsqueeze(0).expand(qvec.shape[0], -1)
    uv = torch.cross(qvec, v, dim=1)
    uuv = torch.cross(qvec, uv, dim=1)
    return v + 2.0 * (q[:, :1] * uv + uuv)


def base_height_below(env: ManagerBasedRLEnv, min_height: float, asset_cfg: SceneEntityCfg) -> torch.Tensor:
    """Terminate when the base height drops below the threshold."""
    asset: Articulation = env.scene[asset_cfg.name]
    return asset.data.root_pos_w[:, 2] < min_height


def base_tilt_exceeded(env: ManagerBasedRLEnv, max_tilt: float, asset_cfg: SceneEntityCfg) -> torch.Tensor:
    """Terminate when the base tilt exceeds the threshold in radians."""
    asset: Articulation = env.scene[asset_cfg.name]
    base_up = _quat_rotate(asset.data.root_quat_w, torch.tensor([0.0, 0.0, 1.0], device=asset.data.root_quat_w.device))
    return base_up[:, 2] < math.cos(max_tilt)
