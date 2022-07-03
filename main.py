import laspy
import numpy as np
import open3d as o3d

INPUT_PATH = 'TM_511_122.laz'
las = laspy.read(INPUT_PATH)
las.points = las.points[las.classification == 2]


point_data = np.stack([las.X, las.Y, las.Z], axis=0).transpose((1, 0))
print(point_data)


geom = o3d.geometry.PointCloud()
geom.points = o3d.utility.Vector3dVector(point_data)
o3d.visualization.draw_geometries([geom])

# las.write('ground.laz')
# point_cloud=las.
#  
# with laspy.open('TM_511_122.laz') as f:
#     print(f"Number of points:   {f.header.point_count}")
#     print(f"Number of vlrs:     {len(f.header.vlrs)}")

# points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
# colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(colors/65535)
# pcd.normals = o3d.utility.Vector3dVector(normals)
# o3d.visualization.draw_geometries([pcd])