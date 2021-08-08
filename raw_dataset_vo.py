import numpy as np
import pykitti
import cv2

from visual_odometry import PinholeCamera, VisualOdometry

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
gt_trajectory_xyz = np.array(
    [
        [
            oxts_data.T_w_imu[0][3],
            oxts_data.T_w_imu[1][3],
            oxts_data.T_w_imu[2][3],
        ]
        for oxts_data in dataset.oxts
    ]
)

vo = VisualOdometry(cam, "/home/swimming/Documents/Dataset/dataset/poses/00.txt")
traj = np.zeros((600, 600, 3), dtype=np.uint8)


for img_id in range(4541):

    img = cv2.imread(
        "/home/swimming/Documents/Dataset/dataset/sequences/00/image_0/"
        + str(img_id).zfill(6)
        + ".png",
        0,
    )

    print(img_id)
    vo.update(img, img_id)

    cur_t = vo.cur_t
    if img_id > 2:
        x, y, z = cur_t[0], cur_t[1], cur_t[2]
    else:
        x, y, z = 0.0, 0.0, 0.0
    draw_x, draw_y = int(x) + 290, int(z) + 90
    true_x, true_y = int(vo.trueX) + 290, int(vo.trueZ) + 90

    # cv2.circle(img, center, radian, color, thickness)
    cv2.circle(traj, (draw_x, draw_y), 1, (0, 255, 0), 1)
    cv2.circle(traj, (true_x, true_y), 1, (0, 0, 255), 1)
    # cv2.rectangle(img, start, end, color, thickness)
    cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)
    text = "Coordinates: x=%2fm y=%2fm z=%2fm" % (x, y, z)
    cv2.putText(traj, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8)

    cv2.imshow("Road facing camera", img)
    cv2.imshow("Trajectory", traj)
    cv2.waitKey(1)

cv2.imwrite("map.png", traj)
