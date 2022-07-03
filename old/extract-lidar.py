import numpy as np
import cv2
import laspy
DIMENSION = 1000
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

with laspy.open('TM_511_122.laz') as fh:
    print('Points from Header:', fh.header.point_count)
    las = fh.read()
    # print(set(list(las.classification)))
    # print('Points from data:', len(las.points))
    high_points = las.points[las.classification == 5]
    # print(len(ground_pts.x))
    # print(len(las.y))
    # print(len(set(list(las.y))))

    # coords = np.vstack((las.x, las.y, las.z)).transpose()
    coordsNot = np.vstack((high_points.x, high_points.y)).transpose()
    # print('coordsNot', coordsNot)

    coordsNot[:, 0] -= xMin_
    coordsNot[:, 1] -= yMin_ 

    # print(coordsNot)
    # new = coordsNot.round(decimals=0)
    new = np.floor(coordsNot)
    new[new < 0] = 0

    # print(new)

    # print(np.shape(new))
    # print(np.shape(np.unique(new, axis=0)))
    print(new)
    points, counts  = np.unique(new, axis=0, return_counts=True)

    coordinates_1000_1000 = np.zeros([DIMENSION+1, DIMENSION+1])



    print(points)
    # print(len(counts))

    
    for i, point in enumerate(points):
        # print(point)
        x = round(point[0])
        y = round(point[1])
        # print(x)
        # print(y)
        if (counts[i] > 10):
            coordinates_1000_1000[x][y] = counts[i]
        else: 
            coordinates_1000_1000[x][y] =0

    high_veg= np.rot90(coordinates_1000_1000)
    cv2.imwrite('slike/high_vegetation.png', high_veg)

        

    # values
    # a = values.transpose()[0] - xMin_
    # b = values.transpose()[1] - yMin_

    # print(a)
    # for i in range(DIMENSION):
    #     for j in range(DIMENSION):
            

    # newX = new[0].round(decimals=0)
    # print(newX)
    # newY = new[1].round(decimals=0)
    # print(newY)
    

    # unique, counts = np.unique(newX, return_counts=True)
    # print(dict(zip(unique, counts)))




    # print(np.shape(coords))
    # # for i in range (1000):
    # print (las.x)
    # print (las.y)



    # con = np.stack((las.x, las.y), axis=1)

    # print(con[0])

    # print(np.shape(scaled_x))
    # ground_points_xyz = np.array((ground_pts['point']['X'],
    #                             ground_pts['point']['Y'],
    #                             ground_pts['point']['Z'])).transpose()
    # for i in range(len(coords)):
    # for i in range(xMin_, xMax_):
    #     for j in range(yMin_, yMax_):
    #         print(i,j)
            # coordinates_1000_1000[i][j] = 
            # nonzero = np.count_nonzero(
            #     (i < las.x) & (las.x < i+1) & (j < las.y) & (las.y< j+1))
            # if (nonzero > 10): 
            #     print(nonzero)

    # for x in range(len(las.x)):
    #     for y in range(len(las.y)):
    #         number = int(str(x)[-3:])
    #         # print(number)
    # new = coords.round(decimals=0)
    # print(new)
    # newX = las.x.round(decimals=0)
    # print(newX)
    # newY = las.y.round(decimals=0)
    # print(newY)
    # print(newX, newY )
    # unique, counts = np.unique(new, return_counts=True)
    # print(dict(zip(unique, counts)))
    # for point in con:
    #     print(round (point[0]))
        # new_ids = [f'{x%1000:03}' for x in point[0]]  # Pad the remainder with 0s
        # new_ids = [f'{x:03}'[-3:] for x in point[0]]

    #         number = int(str(x)[-3:])


    # a = np.histogram(las.x, bins=1000, range=None, normed=None, weights=None, density=None)
    # import matplotlib.pyplot as plt


    # _ = plt.hist(a, bins=1000)  # arguments are passed to np.histogram
    # plt.title("Histogram with 'auto' bins")
    # plt.show()
    # print(scaled_x)
    # # for i in range(xMin_, xMax_):
    #         # coordinates_1000_1000[i][j] = 

    # for i in range(xMin_, xMax_):
    #     # nonzero = np.count_nonzero((i < scaled_x) & (scaled_x < i+1))
    #     print(i)
    #     # if (nonzero < 1000): 
    #     #     print(nonzero)




    # print(ground_points_xyz)

# geom = o3d.geometry.PointCloud()
# geom.points = o3d.utility.Vector3dVector(ground_pts)
# o3d.visualization.draw_geometries([geom])

    # bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
    # print('Ground Point Return Number distribution:')
    # for r,c in zip(bins,counts):
    #     print('    {}:{}'.format(r,c))

        