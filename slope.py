import numpy as np
import cv2
import math 
import matplotlib.pyplot as plt

# Let V be the set of vegetable species to be distributed and 
# v a particular species in that set. Since sp is
# the position of the seed, the altitude of the seed
# can be obtained directly in meters from 
# the height-map height(sp) . The slope where a seed is situated, sp, 

# calculating slope from heightmap
import numpy as np
heightmap = cv2.imread('slike/heightmap.png')

sobelx = cv2.Sobel(heightmap,cv2.CV_64F,1,0,ksize=5)  # x
sobely = cv2.Sobel(heightmap,cv2.CV_64F,0,1,ksize=5)  # y

dst_y = cv2.convertScaleAbs(sobely)
dst_x = cv2.convertScaleAbs(sobelx)
slope_image = cv2.addWeighted(dst_x, 0.5, dst_y, 0.5, 0)

cv2.imwrite('slike/slope_image.png', slope_image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# Hopefully see some edges
# plt.imshow(sobel,cmap=plt.cm.gray)
# sobel filter - za zracun slope, to si mal poglej ce je res

# def GetSteepness(heightmap, x,y):
#     height = heightmap[x, y]
#     # print(height)
# #    Compute the differentials by stepping over 1 in both directions.
#     #    TODO: Ensure these are inside the heightmap before sampling.
#     dx = heightmap[x + 1, y] - height
#     dy = heightmap[x, y + 1] - height
# #    The "steepness" is the magnitude of the gradient vector
# #    For a faster but not as accurate computation, you can just use abs(dx) + abs(dy)
#     # return math.sqrt(dx * dx + dy * dy)
#     return abs(dx) + abs(dy)

# print(img)
# stepness = GetSteepness(img, 100, 100)
# print(stepness)



#scratch implementatcion