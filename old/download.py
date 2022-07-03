import requests
from PIL import Image
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





csv_url = 'http://gis.arso.gov.si/lidar/dmr1/b_22/D96TM/TM1_514_123.txt'


with requests.Session() as session:
    download = session.get(csv_url)

    decoded_content = download.content.decode('ascii')

    csvreader = csv.reader(decoded_content.splitlines(), delimiter=';')
    my_list = list(csvreader)

    dim = 1000

    for row in range(dim):
        for column in range(dim):
            # print(csvreader);
            print(next(csvreader))
    # for row in my_list:
        # print(row)



# xname = sys.argv[1]
# yname = sys.argv[2]

# start = time.time()

# dim = 1000
# bytes = []


# csvreader = csv.reader(dmr_file, delimiter=';')
# with open('./TM1_%s_%s.asc' % (xname, yname), 'r') as ascfile:
#     for row in range(dim):
#         for column in range(dim):
#             yxh = next(csvreader)
#             print(yxh)
        # z = yxh[2]
        # z = int(float(z) * 100) # why 100

        # bytes.append((z >> 16) & 255)
        # bytes.append((z >> 8) & 255)
        # bytes.append(z & 255)

# with open('./TM1_%s_%s.asc' % (xname, yname), 'r') as ascfile:
#     csvreader = csv.reader(ascfile, delimiter=';')

#     for x in range(dim):
#         row = ()
#         for y in range(dim):
#             xyz = next(csvreader)

#             z = xyz[2]

#             z = int(float(z) * 100)

#             bytes.append((z >> 16) & 255)
#             bytes.append((z >> 8) & 255)
#             bytes.append(z & 255)

#     pixels = np.reshape(bytes, (dim, dim, 3))
#     pixels = np.rot90(pixels)
#     pixels = pixels.astype(np.uint8, copy=False)

#     # Save smaller versions of the image for later concatination
#     for i in range(10, 0, -1):
#         im = Image.fromarray(pixels, mode='RGB')
#         im.save('../%s/%s_%s.png' % (i, xname, yname), 'PNG')

#         pixels = pixels[::2, ::2]

#     end = time.time()
# print(end - start)

# sys.exit()
