
import ee
# Initialize the Earth Engine module.
ee.Initialize()

def getNDVI (image):
    # return image.normalizedDifference(['B4', 'B3'])
    return image.normalizedDifference(['B4', 'B3'])


#LOOK WHAT IS THIS, MORŠ PRAVO NAJDET
# image = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')
l8 = ee.ImageCollection('VITO/PROBAV/C1/S1_TOC_100M')
point = ee.Geometry.Point([15.5778, 50.2256])


image = ee.Image(
  l8.filterBounds(point)
    .filterDate('2018-03-01', '2018-04-01')
    .sort('CLOUD_COVER')
    .first()
)
#COMPUTE NDVI FROM THE SCENE
# ndvi1 = getNDVI(image)

ndvi1 = image.select('NDVI')

# ndviParams = {'palette': ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9efb8', '#a6d96a',
# '#66bd63', '#1a9850']}
ndviParams = {min: -1, max: 1, 'palette': ['blue', 'white', 'green']}

# Import the Folium library.  
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
# Create a folium map object.T
my_map = folium.Map(location= [36,-121], zoom_start = 6)  

my_map.add_ee_layer(ndvi1, ndviParams, 'NDVI')
my_map.add_child(folium.LayerControl())

my_map.save("map.html")
