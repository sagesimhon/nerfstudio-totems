# Copyright 2022 The Nerfstudio Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Ray generator.
"""
import torch
from torch import nn
from torchtyping import TensorType

from nerfstudio.cameras.camera_optimizers import CameraOptimizer
from nerfstudio.cameras.cameras import Cameras
from nerfstudio.cameras.rays import RayBundle

import numpy as np

class RayGenerator(nn.Module):
    """torch.nn Module for generating rays.
    This class is the interface between the scene's cameras/camera optimizer and the ray sampler.

    Args:
        cameras: Camera objects containing camera info.
        pose_optimizer: pose optimization module, for optimizing noisy camera intrisics/extrinsics.
    """

    def __init__(self, cameras: Cameras, pose_optimizer: CameraOptimizer) -> None:
        super().__init__()
        self.cameras = cameras
        self.pose_optimizer = pose_optimizer
        self.image_coords = nn.Parameter(cameras.get_image_coords(), requires_grad=False)

    def reshape_rays_to_image_dimensions(self, ray_d, dims):
        h, w, = dims #960 x 540
        return torch.reshape(ray_d, (h,w,3))

    def forward(self, ray_indices: TensorType["num_rays", 3]) -> RayBundle:
        """Index into the cameras to generate the rays.

        Args:
            ray_indices: Contains camera, row, and col indicies for target rays.
        """
        c = ray_indices[:, 0]  # camera indices
        y = ray_indices[:, 1]  # row indices
        x = ray_indices[:, 2]  # col indices
        # import pdb; pdb.set_trace()
        #hardcoding for debugging coordiante systems
        # c = torch.Tensor(np.zeros((960*540,), dtype=np.int8))
        # c = torch.Tensor(np.repeat(1, 960*540))
        c = np.repeat(1, 960*540)

        xx, yy = np.meshgrid(np.arange(0, 540), np.arange(0, 960))
        xx = np.reshape(xx, (960*540,))
        yy = np.reshape(yy, (960*540,))
        coords = self.image_coords[yy, xx] #torch.Size([960*540,2]) (flattened image in row-major order)

        camera_opt_to_camera = self.pose_optimizer(c)

        c = torch.Tensor(c)
        ray_bundle = self.cameras.generate_rays(
            camera_indices=c.unsqueeze(-1),
            coords=coords,
            camera_opt_to_camera=camera_opt_to_camera,
        )
        # import pdb; pdb.set_trace()
        reshaped_d = self.reshape_rays_to_image_dimensions(ray_bundle.directions, (960, 540))
        np.save("reshaped_d", reshaped_d.cpu().detach().numpy())
        return ray_bundle
