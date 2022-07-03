import numpy as np
import cv2
import matplotlib.pyplot as plt
import random

# Load image
img = cv2.imread('slike/ndvi_image.jpg')
high_vegetation_points = cv2.imread('slike/high_vegetation_points.png')

# #trashold values that are green ndvi; values > 0.0?
ret, thresholded_img= cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
ret_hv, thresholded_img_hv= cv2.threshold(high_vegetation_points, 100, 255, cv2.THRESH_BINARY)

#invert
thresholded_img_inv = cv2.bitwise_not(thresholded_img)
thresholded_img_hv_inv = cv2.bitwise_not(thresholded_img_hv)

# Use Numpy indexing to make alternate rows and columns black
# regular_grid_inverted[0::5,0::5] = [255,255,255]

# mask = cv2.imread('mask.png',0)
# # res = cv2.bitwise_and(thresholded_img_inv,thresholded_img_inv, thresholded_img)
# # res = regular_grid_inverted - thresholded_img_inv


#create regular destiribution
blank_image = np.zeros((1000,1000,3), np.uint8)
regular_destribution_image  = blank_image

sp = np.random.uniform(0,3,1000000)
scounter=0
for i in range(0, 1000, 5) :
    for j in range(0, 1000, 5) :
        spx = round((sp[scounter]))
        spy = round((sp[scounter+1]))
        regular_destribution_image = cv2.rectangle(regular_destribution_image, 
        (i+spx,j+spy), (i+spx,j+spy), color=(255, 255, 255), thickness=1)
        scounter = scounter+2

#        (round(i+spx[scounter]), round(j+spy[scounter])), (round(i+spx[scounter]),round(j+spy[scounter])), color=(0, 0, 255), thickness=1)

# Then, in order to break up the regular location of the seed positions, 
# the method performs a deviation of the seed positions sp,
# by modifying their (x, y) coordinates with a random value using a uniform distribution of 
# random number generator.
# This random value will always be less than half the spacing used in the generation of the grid, in order to prevent two elements from overlapping.

#substract ndwi image (where there is no vegetation) from regular grid
iregular_grid_image = cv2.subtract(regular_destribution_image,thresholded_img_inv)
iregular_grid_image_high_vegetation = cv2.subtract(regular_destribution_image,thresholded_img_hv_inv)
high_vegetation_destribution = cv2.subtract(iregular_grid_image_high_vegetation,thresholded_img_inv)

# # cv2.imwrite('thresholded_img_inv.png', regular_grid_inverted)
# cv2.imwrite('resimg.png', regular_destribution_image)
# cv2.imwrite('thresholded_img.png', thresholded_img)
cv2.imwrite('slike/iregular_grid_image.png', iregular_grid_image)
cv2.imwrite('slike/high_vegetation_destribution.png', high_vegetation_destribution)

# xvalues = np.arange(0, 1000, 5)
# yvalues = np.arange(0, 1000, 5)

# # xvalues = np.array([0, 1, 2, 3, 4])
# # yvalues = np.array([0, 1, 2, 3, 4])
# # Now, when we call meshgrid, we get the previous output automatically.

# xx, yy = np.meshgrid(xvalues, yvalues)

# # plt.plot(xx, yy, marker='.', color='k', linestyle='none')
# # plt.show()
# print(xx.shape)

# print(xx)
# # img = np.zeros([5,5,3])

# # img[:,:,0] = np.ones([5,5])*64/255.0
# #
# # img[:,:,1] = np.ones([5,5])*128/255.0
# # img[:,:,2] = np.ones([5,5])*192/255.0

# cv2.imwrite('color_img.jpg', xx)
# # cv2.imshow("image", img)
# # cv2.waitKey()


# # cv2.imwrite('color_img.jpg', xx)
# 
