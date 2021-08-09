import numpy as np
import pykitti
import cv2

from visual_odometry import PinholeCamera, VisualOdometry

kitti_odom_dir = "/home/swimming/Documents/Dataset/dataset"
kitti_odom_sequence = "05"

dataset = pykitti.odometry(kitti_odom_dir, kitti_odom_sequence)
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
            gt_pose[0][3],
            gt_pose[1][3],
            gt_pose[2][3],
        ]
        for gt_pose in dataset.poses
    ]
)

vo = VisualOdometry(cam, ground_truth=gt_trajectory_xyz)
traj = np.zeros((600, 600, 3), dtype=np.uint8)
img_id = 0

try:
    while True:

        PIL_Image = dataset.get_cam0(img_id)
        color_img = cv2.cvtColor(np.asarray(PIL_Image), cv2.COLOR_RGB2BGR)
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)

        vo.update(gray_img, img_id)
        print(img_id)

        cur_t = vo.cur_t
        if img_id > 2:
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
        else:
            x, y, z = 0.0, 0.0, 0.0
        draw_x, draw_y = int(x) + 290, int(z) + 90
        true_x, true_y = int(vo.trueX) + 290, int(vo.trueZ) + 90

        img_id += 1

        # cv2.circle(img, center, radian, color, thickness)
        cv2.circle(traj, (draw_x, draw_y), 1, (0, 255, 0), 1)
        cv2.circle(traj, (true_x, true_y), 1, (0, 0, 255), 1)
        # cv2.rectangle(img, start, end, color, thickness)
        cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)
        text = "Coordinates: x=%2fm y=%2fm z=%2fm" % (x, y, z)
        cv2.putText(
            traj, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
        )

        cv2.imshow("Road facing camera", gray_img)
        cv2.imshow("Trajectory", traj)
        cv2.waitKey(1)
except IndexError:
    print("IndexError, Traverse Done")
except Exception as e:
    print(e)
finally:
    cv2.imwrite("map.png", traj)
