from pyproj import Transformer
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageOps
import numpy as np
import csv
import io
import time
import sys


xMin_ = 511000.00
yMin_ = 122000.00
xMax_ = 511999.00
yMax_ = 122999.00

transformer = Transformer.from_crs("epsg:3794", "epsg:4326")
xMin, yMin = transformer.transform(xMin_, yMin_)
xMax, yMax = transformer.transform(xMax_, yMax_)

print(xMin, yMin)
print(xMax, yMax )

with open('floveg.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            lat = float(row[21])
            lon = float(row[22])
            # print(lat, lon)
            # print(xMin, lat, xMax)
            if (xMin < lat):
                if (lat < xMax):
                    print ('joj')
            # print(row)
        
            # print(row[22])
            #lat
            # print(row[21])
            # #lon
            # print(row[22])


            line_count += 1
    print(f'Processed {line_count} lines.')
