
##D96/TM v nadmorskih višinah: TM1_eee_nnn.asc, kjer je eee kilometer v e koordinati in nnn kilometer v n koordinati spodnjega levega vogala kvadrata oz. km2
import ee
from pyproj import Transformer
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

# Initialize the Earth Engine module.
ee.Initialize()
def addNDVI (image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)


# 511355.61
# 122095.07
xMin_ = 511000.00
yMin_ = 122000.00
xMax_ = 511999.00
yMax_ = 122999.00

transformer = Transformer.from_crs("epsg:3794", "epsg:4326")
xMin, yMin = transformer.transform(xMin_, yMin_)
xMax, yMax = transformer.transform(xMax_, yMax_)

print(xMin, yMin)
print(xMax, yMax )


#pretvorjene koordinate

rectangleBounds = ee.Geometry.Rectangle(
  [yMin, xMin, yMax, xMax]
)
print(rectangleBounds)
 


# S2_SR = ee.ImageCollection('COPERNICUS/S2_SR')
S2_SR = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(rectangleBounds) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))


S2_NDVI = S2_SR.map(addNDVI)
recent_S2 = ee.Image(S2_NDVI.sort('system:time_start', False).first())
s2NDVI = recent_S2.select('NDVI').clip(rectangleBounds)


ndviVis = {
    min: -1, max: 1, 
  'palette': ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901', '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01', '012E01', '011D01', '011301']
}
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
my_map = folium.Map(location= [xMin, yMin], zoom_start = 15)  


# Map.addLayer(reprojected, {min: 0.15, max: 0.7}, 'Reprojected');
#add to map
# my_map.add_ee_layer(s2, rgbVis, 'Sentinel')
my_map.add_ee_layer(s2NDVI, ndviVis, 'NDVI')

my_map.add_child(folium.LayerControl())

my_map.save("map.html")
palette = ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901', '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01', '012E01', '011D01', '011301']
# var imageRGB = image.visualize({bands: ['B5', 'B4', 'B3'], max: 0.5});
# ndwiRGB = s2NDVI.visualize({
#   min: 0,
#   max: 1,
#   palette: palette
# })

#has to be saved to drive than download
thumbnail_ndvi_image = s2NDVI.getThumbURL({
  'min': 0,
  'max': 1,
  # 'palette': palette,
  'region': rectangleBounds,
  'dimensions': [1000, 1000],
  'crs': 'EPSG:4326'
})
print('url', thumbnail_ndvi_image)

import requests
img_data = requests.get(thumbnail_ndvi_image).content
with open('slike/ndvi_image.jpg', 'wb') as handler:
  handler.write(img_data)


# ndvi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
# ndvi_landsat_class = np.digitize(thumbnail_ndvi_image, ndvi_class_bins)
# ndvi_landsat_class = np.ma.masked_where(
#     np.ma.getmask(thumbnail_ndvi_image), ndvi_landsat_class
# )
# np.unique(ndvi_landsat_class)

# ##
# # Plot Classified NDVI With Categorical Legend
# # --------------------------------------------
# #
# # You can plot the classified NDVI with a categorical legend using the
# # ``draw_legend`` function from the ``earthpy.plot`` module.

# # Define color map
# nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
# nbr_cmap = ListedColormap(nbr_colors)

# fig, ax = plt.subplots(figsize=(12, 12))

# im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

# # Get list of classes
# classes = np.unique(ndvi_landsat_class)
# classes = classes.tolist()

# # ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)

# ax.set_title(
#     "Landsat 8 - Normalized Difference Vegetation Index (NDVI) Classes",
#     fontsize=14,
# )
# ax.set_axis_off()

# # Auto adjust subplot to fit figure size
# plt.tight_layout()