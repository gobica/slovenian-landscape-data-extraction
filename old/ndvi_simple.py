
import ee
# Initialize the Earth Engine module.
ee.Initialize()

# Lidar data fishnet in D96TM projection(1km2) 
# Area: b_22
# Name of the fishnet: 511_122
# 511000.00;122000
# 511999.00;122999.00
# vrbensko jezero


# geometry = ee.Geometry({
#   'type': 'Polygon',
#   'proj': 'EPSG:3794',
#   'coordinates':
#     [[[51.1000, 12.2000],
#       [51.1999, 12.2000],
#       [51.1000, 12.2999],
#       [51.1999, 12.2999]]]
# })

# rectangleGeoJSON = ee.Geometry.Rectangle(
#   [
#     [10, 10],
#     [40, 90]   
#   ]
# 
# Coordinates for the bounds of a rectangle.
xMin = 51.1000
yMin = 12.2000
xMax = 51.1999
yMax = 12.2999

#Construct a rectangle from a list of GeoJSON 'point' formatted coordinates.
rectangleBounds = ee.Geometry.Rectangle(
  [xMin, yMin, xMax, yMax]
)

roi = ee.Geometry.Point([-124.0769, 40.1035]).buffer(1000)

# rectanglepoint = ee.Geometry.Point(
#   [xMin, yMin]
# )
# point = ee.Geometry.Point(51.100, 12.2000)

# Apply the area method to the Geometry object.
# geometryArea = geometry.area({'maxError': 1});

# Print the result to the console.
# print('geometry.area(...) =', geometryArea);
# // Apply the bounds method to the Geometry object.
# print(ee.Projection('EPSG:3912'));  
# print(ee.Projection('EPSG:3794'));  

# proj = ee.Projection('EPSG:3794')

# // Print the result to the console.
# print('geometry.bounds(...) =', geometryBounds);

# s2 = ee.ImageCollection('COPERNICUS/S2')
# image = ee.Image(
#   s2.filterBounds(geometry)
#     .filterDate('2018-03-01', '2018-04-01')
#     .first()
# )
def getNDVI (image):
    ndvi = image.normalizedDifference(['B8','B4']).rename("ndvi")
    image = image.addBands(ndvi)
    return image

# s2 = ee.ImageCollection('COPERNICUS/S2')
# point = ee.Geometry.Point([51.1000, 12.2000])
# s2 = ee.ImageCollection('VITO/PROBAV/C1/S1_TOC_100M').filterDate('2021-07-01', '2021-10-01').filterBounds(rectangleBounds)
# image = ee.Image('VITO/PROBAV/C1/S1_TOC_100M')
s2 = ee.ImageCollection('COPERNICUS/S2').filterDate('2019-01-01', '2019-12-30') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)).filterBounds(roi); 
s2 = s2.median()
s2 = getNDVI(s2).clip(roi)
s2NDVI = s2.select('ndvi')
print(s2)

ndviVis = {
  min: 0.0,
  max: 0.8,
  'palette': [
    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301'
  ],
}

rgbVis = {
  min: 0.0,
  max: 0.3,
  'bands': ['B4', 'B3', 'B2'],
}
# geometry = ee.Geometry.Polygon(
#     [[[-74.17301042227143, 41.01676815108097],
#       [-75.15079362539643, 40.93797200093739],
#       [-74.50260026602143, 40.3084072747414],
#       [-73.63468034414643, 40.559275861105796]]])

# landsat = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")


# area = ee.FeatureCollection(geometry);

# image = ee.Image((landsat)
#     .filterBounds(geometry)
#     .filterDate('2018-01-01', '2018-12-31')
#     .sort('CLOUD_COVER')
#     .median())

# filteredimage = image.clip(geometry)
# image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515')

# # image = ee.Image(s2.first())
# # image.clip(rectangleBounds)	
# projection = image.select('B2').projection().getInfo()
# print(projection)

# geomPoly = ee.Geometry.BBox(-121.55, 39.01, -120.57, 39.38);
# demClip = dem.clip(geomPoly);
# image = ee.Image(
#   s2.filterBounds(rectangleGeoJSON)
#     .sort('CLOUD_COVER')
#     .first()
# )

# image = ee.Image('COPERNICUS/S2/20160701T184340_20160701T221909_T11SKA')
# visParams = {'bands': ['B8', 'B4', 'B3'], max: 3048, 'gamma': 1}
# # visParams_ndvi = {min: -0.2, max: 0.8, 'palette': 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
# #     '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'}
# visParams_ndvi = {'palette': ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9efb8', '#a6d96a',
# '#66bd63', '#1a9850']}
# # image_ndvi = image.normalizedDifference(['B8','B4'])
# # print(image_ndvi)
# image_ndvi = filteredimage.select('B3')


import folium

def add_ee_layer(self, ee_image_object, vis_params, name):
    """Adds a method for displaying Earth Engine image tiles to folium map."""
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# Add Earth Engine drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer
# # Create a folium map object.T
my_map = folium.Map(location= [-124.0769, 40.1035], zoom_start = 8)  

# my_map.add_ee_layer(ndvi1, ndviParams, 'NDVI')
# my_map.add_child(folium.LayerControl())
 

# my_map.center_image(image,9)
# my_map.add_ee_layer(image,visParams,'Sentinel-2 False Color Infrared')
# my_map.add_ee_layer(image_ndvi,visParams_ndvi,'Sentinel-2 NDVI')

# # my_map.add_ee_layer(ndvi1, ndviParams, 'NDVI')
# my_map.add_child(folium.LayerControl())

# my_map.save("map.html")

#add to map
my_map.add_ee_layer(s2, rgbVis, 'Sentinel')
my_map.add_ee_layer(s2NDVI, ndviVis, 'NDVI')
my_map.add_child(folium.LayerControl())

my_map.save("map.html")

#NARDIMO PROJEKCIJO V PRAVI KOORDINACTNI SISTEM
# print(ee.Projection('EPSG:3857'));  
# print(ee.Projection('EPSG:4326'));  

# EPSG 3912 ... za »stari« referenčni koordinatni sistem z oznako D48/GK
# EPSG 3794 ... za »novi« referenčni koordinatni sistem z oznako D96/TM

# print(ee.Projection('EPSG:3912'));  
# print(ee.Projection('EPSG:3794'));  