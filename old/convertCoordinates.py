import ee
# Initialize the Earth Engine module.
ee.Initialize()

# Lidar data fishnet in D96TM projection(1km2) 
# Area: b_22
# Name of the fishnet: 511_122
# 511000.00;122000
# 511999.00;122999.00
# vrbensko jezero

point = ee.Geometry.Point(51.100, 12.2000)
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
my_map = folium.Map(location= [51.1000, 12.2000], zoom_start = 20)  
my_map.add_child(folium.LayerControl())
my_map.save("map.html")
