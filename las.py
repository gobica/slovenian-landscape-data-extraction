import laspy
import open3d as o3d
import numpy as np

las = laspy.read('data/TM_402_40.laz')
print(las)