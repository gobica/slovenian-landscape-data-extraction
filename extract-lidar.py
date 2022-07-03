import numpy as np
import cv2

import laspy

# import open3d as o3d
DIMENSION = 1000
LAS_FILE = 'TM_511_122.laz'
#classes
#ground: 2
#low vegetation 3
#medium vegetation 4
#high vegetation 5
#building 6
xMin_ = 511000
yMin_ = 122000
xMax_ = 511999
yMax_ = 122999


def returnXY(points):
    points_XY =  np.vstack((points.x, points.y)).transpose()
    points_XY[:, 0] -= xMin_
    points_XY[:, 1] -= yMin_ 
    points_XY_floored = np.floor(points_XY)
    points_XY_floored[points_XY_floored < 0] = 0
    points_XY_floored[points_XY_floored > 999] = 999
    return points_XY_floored

def sample_points(points):
    points_xy = returnXY(points)
    sampled_points, counts  = np.unique(points_xy, axis=0, return_counts=True)
    return (sampled_points, counts)

def saveToPng(points, PNG_NAME):
    image = np.zeros([DIMENSION, DIMENSION])
    sampled_points, counts = sample_points(points)
    for i, point in enumerate(sampled_points):
        x = round(point[0])
        y = round(point[1])
        if (counts[i] > 5):
            image[x][y] = 255
        else: 
            image[x][y] = 0

    rotated_image= np.rot90(image)
    cv2.imwrite(PNG_NAME, rotated_image)

with laspy.open(LAS_FILE) as fh:
    las = fh.read()
    high_vegetation_points = las.points[las.classification == 5]
    saveToPng(high_vegetation_points, 'slike/high_vegetation_points.png')
    medium_vegetation_points = las.points[las.classification == 4]
    saveToPng(medium_vegetation_points, 'slike/medium_vegetation_points.png')
    low_vegetation_points = las.points[las.classification == 3]
    saveToPng(low_vegetation_points, 'slike/low_vegetation_points.png')



     