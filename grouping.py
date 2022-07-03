
import numpy as np
import cv2
import matplotlib.pyplot as plt
import random
import math


# Load image
iregular_grid_image = cv2.imread('slike/iregular_grid_image.png')

diffusion_points = [(140, 50), (50, 400), (700, 900)]
colors = [(255, 0 ,0 ), (0, 255, 0), (0, 0, 255)]
radius = [100, 150, 200]
# Generate diffusion points rendomly - tuki naj pride pol input iz zbirk, koordinat popisa rastlin
for index, dp in enumerate(diffusion_points): 
    iregular_grid_image = cv2.rectangle(iregular_grid_image, 
        dp, dp, color=colors[index], thickness=1)


# distance_to_diffusion_point = distance(seed, diffusion_point)
# if (distance_to_diffusion_point < radius_of_diffusion_point): 
#     influance= 1 - (distance_to_diffusion_point / radius_of_diffusion_point)
# # cv2.imwrite('thresholded_img_inv.png', regular_grid_inverted)
# cv2.imwrite('resimg.png', regular_destribution_image)
# cv2.imwrite('thresholded_img.png', thresholded_img)

# Describe what a single red pixel looks like
red = np.array([255,0,0],dtype=np.uint8)
reds = np.where(np.all((iregular_grid_image==red),axis=-1))

white = np.array([255,255,255],dtype=np.uint8)
all_points = np.where(np.all((iregular_grid_image==white),axis=-1))

for index in range(len(all_points[0])):
    distances = np.empty(3)
    y = all_points[0][index]
    x = all_points[1][index]

    for di in range(len(diffusion_points)): 
        dx2 = (x - diffusion_points[di][0])**2          # (200-10)^2
        dy2 = (y - diffusion_points[di][1])**2          # (300-20)^2
        distance = math.sqrt(dx2 + dy2)
        distances[di] = distance

    index_min = np.argmin(distances)
    if (distances[index_min] < radius[di]):
        influance = 1 - (distances[index_min] / radius[di])
        print(influance)
        iregular_grid_image = cv2.rectangle(iregular_grid_image, 
        (x,y), (x,y), color=colors[index_min], thickness=1)


cv2.imwrite('slike/destribution_image.png', iregular_grid_image)

# Finally, the influence of each diffusion point set by the user for a vegetation species v has to be evaluated on a seed sp following the expression: