import requests
from PIL import Image, ImageOps
import numpy as np
import csv
import io
import time
import sys


## download DMR 

# digitalni model reliefa je interpolacija reliefa na osnovi točk OTR, 
# ki je zapisana v pravilno mrežo 1 m × 1 m. Shranjen je v ASCI datoteki.
# Podatki so razdeljeni v kvadrate velikosti 1km² (1000 x 10000)
# YXZ format

# Podatki se izdajajo v ASCII zapisu (y, x, H). Primer izhodnega formata:

# Lidar data fishnet in D96TM projection(1km2) 
# Area: b_22
# Name of the fishnet: 511_122
# 511000.00;122000
# 511999.00;122999.00
# vrbensko jezero

csv_url = 'http://gis.arso.gov.si/lidar/dmr1/b_22/D96TM/TM1_511_122.txt'
dim = 1000
bytes = []   



with requests.Session() as session:
    download = session.get(csv_url)
    # open('decoded_content', 'wb').write(download.content)
    decoded_content = download.content.decode('ascii')
    csvreader = csv.reader(decoded_content.splitlines(), delimiter=';')
    my_list = list(csvreader)
    # np.savetxt('data.csv', (my_list), delimiter=',')


    for yxh in my_list:
        height =  z = yxh[2]
        z = int(float(z) * 100) # *100 not nesser
        bytes.append((z >> 16) & 255)
        bytes.append((z >> 8) & 255)
        bytes.append(z & 255)
    
    pixels = np.reshape(bytes, (dim, dim, 3))
    pixels = np.rot90(pixels)
    pixels = pixels.astype(np.uint8, copy=False)

    im = Image.fromarray(pixels, mode='RGB')
    gray_image = ImageOps.grayscale(im)
    gray_image.save('slike/heightmap' + '.png')

#uncomment for smaller sizes
    # Save smaller versions of the image for later concatination
    # for i in range(10, 0, -1):
    #     im = Image.fromarray(pixels, mode='RGB')
    #     gray_image = ImageOps.grayscale(im)

    #     # im.save('../%s/%s_%s.png' % (i, 'xname', 'yname'), 'PNG')
    #     gray_image.save('slike/' + str(i) + '.png')
    #     pixels = pixels[::2, ::2]

