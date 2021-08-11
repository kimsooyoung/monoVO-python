import matplotlib.pyplot as plt
import numpy as np
import pykitti
import cv2

from geo_transforms import lla_to_enu
from visual_odometry import PinholeCamera, VisualOdometry

# kitti_root_dir = "/home/kimsooyoung/Documents/AI_KR"
kitti_root_dir = "/home/swimming/Documents/Dataset"
kitti_date = "2011_09_30"
kitti_drive = "0033"

dataset = pykitti.raw(kitti_root_dir, kitti_date, kitti_drive)
myCam = dataset.get_cam0(0)

width = myCam.width
height = myCam.height

fx = dataset.calib.K_cam0[0][0]
fy = dataset.calib.K_cam0[1][1]
cx = dataset.calib.K_cam0[0][2]
cy = dataset.calib.K_cam0[1][2]

cam = PinholeCamera(width, height, fx, fy, cx, cy)

gt_trajectory_imu = np.array(
    [
        [
            oxts_data.T_w_imu[0][3],
            oxts_data.T_w_imu[1][3],
            oxts_data.T_w_imu[2][3],
            1,
        ]
        for oxts_data in dataset.oxts
    ]
)

# dataset.calib.T_cam0_velo
# @ np.linalg.inv(dataset.oxts[i].T_w_imu) @

cam0_xyz = np.array(
    [dataset.calib.T_cam0_imu @ gt_trajectory_imu[i] for i in range(len(dataset))]
)

gt_trajectory_lla = np.array(
    [
        [oxts_data.packet.lon, oxts_data.packet.lat, oxts_data.packet.alt]
        for oxts_data in dataset.oxts
    ]
)

gt_trajectory_lla = gt_trajectory_lla.T
origin = gt_trajectory_lla[:, 0]  # set the initial position to the origin
gt_trajectory_xyz = lla_to_enu(gt_trajectory_lla, origin).T

### test ###

print(f"cam0_xyz : {cam0_xyz.shape}")
print(f"gt_trajectory_xyz : {gt_trajectory_xyz.shape}")
xs, ys, zs = gt_trajectory_xyz.T
ix, iy, iz, _ = gt_trajectory_imu.T
cam_x, cam_y, cam_z, _ = cam0_xyz.T


# fig, ax = plt.subplots(2, 1, gridspec_kw={"height_ratios": [1, 1]}, figsize=(10, 12))
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
ax.plot(xs, ys, lw=2, label="ground-truth trajectory")
ax.plot(ix, iy, lw=2, label="imu traj")

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.grid()

plt.show()

fig2 = plt.figure(figsize=(15, 15))
ax2 = plt.axes(projection="3d")
ax2.scatter3D(xs, ys, zs, color="green")
ax2.scatter3D(ix, iy, iz, color="red")

plt.show()

fig2 = plt.figure(figsize=(15, 15))
ax2 = plt.axes(projection="3d")
ax2.scatter3D(cam_x, cam_y, cam_z, color="green")

plt.show()
