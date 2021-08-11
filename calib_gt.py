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

calib_matrix = np.linalg.inv(dataset.calib.T_cam0_imu @ dataset.oxts[0].T_w_imu)
new_pose_mat_list = [ calib_matrix @ dataset.calib.T_cam0_imu @ oxts.T_w_imu for oxts in dataset.oxts ]

new_gt_traj = np.array(
    [
        [oxts_data[0,3], oxts_data[1,3], oxts_data[2,3]]
        for oxts_data in new_pose_mat_list
    ]
)

xs, ys, zs = new_gt_traj.T

fig2 = plt.figure(figsize=(15, 15))
ax2 = plt.axes(projection="3d")
ax2.scatter3D(xs, ys, zs, color="green")

plt.show()