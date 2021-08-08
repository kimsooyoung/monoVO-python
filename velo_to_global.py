import pykitti
import numpy as np

basedir = "/home/swimming/Documents/Dataset"
date = "2011_09_30"
drive = "0033"

# The 'frames' argument is optional - default: None, which loads the whole dataset.
# Calibration, timestamps, and IMU data are read automatically. 
# Camera and velodyne data are available via properties that create generators
# when accessed, or through getter methods that provide random access.
data = pykitti.raw(basedir, date, drive)


# transform points from lidar to global frame using lidar_extrinsic_matrix
def generate_transformed_pcd_from_point_cloud(points, lidar_extrinsic_matrix):
    tps = []
    for point in points:
        transformed_points = np.matmul(lidar_extrinsic_matrix, np.array([point[0], point[1], point[2], 1], dtype=np.float32).reshape(4,1)).tolist()
        if len(point) > 3 and point[3] is not None:
            tps.append([transformed_points[0][0], transformed_points[1][0], transformed_points[2][0], point[3]])
       
    return tps

# i is frame number
i = 0
gt_pose = []

try:
    while True:
        # velodyne raw point cloud in lidar scanners own coordinate system
        points = data.get_velo(i)

        # customer computes lidar extrinsics
        lidar_extrinsic_matrix = data.oxts[i].T_w_imu

        # customer transforms points from lidar to global frame using lidar_extrinsic_matrix
        transformed_pcl = generate_transformed_pcd_from_point_cloud(points, lidar_extrinsic_matrix)
        # print(transformed_pcl)
        print(i)

        gt_pose.append(transformed_pcl)
        i += 1
except IndexError:
    print("IndexError, Traverse Done")
except Exception as e:
    print(e)
finally:
    print()