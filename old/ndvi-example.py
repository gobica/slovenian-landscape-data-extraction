import ee

# import Google earth engine module
import geetools

#Authenticate the Google earth engine with google account
ee.Initialize()

# import Google earth engine module
# Import libraries.
import folium



 # Define a method for displaying Earth Engine image tiles on a folium map.

def add_ee_layer(self, ee_object, vis_params, name):
        
    try:    
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):    
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)

        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):    
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)

        # display ee.Geometry()
        elif isinstance(ee_object, ee.geometry.Geometry):    
            folium.GeoJson(
            data = ee_object.getInfo(),
            name = name,
            overlay = True,
            control = True
            ).add_to(self)

        # display ee.FeatureCollection()
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):  
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
        
    except:
        print("Could not display {}".format(name))

        
        
 

class foliumInitialize:
    # The init method or constructor  
    def __init__(self, location,zoom_start,height):  
            
        # Instance Variable  
        self.location = location
        self.zoom_start = zoom_start
        self.height = height
    
    def Initialize(self):
        folium.Map.add_ee_layer = add_ee_layer
        return folium.Map(location=self.location, zoom_start=self.zoom_start, height=self.height)


# Class for pulgins  
class pluginsTools:     
        
    # The init method or constructor  
    def __init__(self, my_map):  
            
        # Instance Variable  
        self.my_map = my_map              
    
    # Add a layer control panel to the map.
    def addLayerControl(self):
        self.my_map.add_child(folium.LayerControl())

    #fullscreen
    def addFullscreen(self):
        plugins.Fullscreen().add_to(self.my_map)

    #GPS
    def addLocateControl(self):
        plugins.LocateControl().add_to(self.my_map)

    #mouse position
    def addMousePosition(self):
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(self.my_map)


    #Measure Tool
    def addMeasureControl(self):
        plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(self.my_map)
        

    def addDrawTool(self):
        plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(self.my_map)   
inBands = ee.List(['QA60','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12']);
outBands = ee.List(['QA60','blue','green','red','re1','re2','re3','nir','re4','waterVapor','cirrus','swir1','swir2']);
 
CloudCoverMax = 20

def importData(studyArea,startDate,endDate):
 
    # Get Sentinel-2 data
    s2s =(ee.ImageCollection('COPERNICUS/S2')
          .filterDate(startDate,endDate)
          .filterBounds(studyArea)
          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',CloudCoverMax))
          .filter(ee.Filter.lt('CLOUD_COVERAGE_ASSESSMENT',CloudCoverMax)))
    
    def scaleBands(img):
        prop = img.toDictionary()
        t = img.select(['QA60','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12']).divide(10000)
        t = t.addBands(img.select(['QA60'])).set(prop).copyProperties(img,['system:time_start','system:footprint'])
        return ee.Image(t)
    
    
    s2s = s2s.map(scaleBands)
    s2s = s2s.select(inBands,outBands)
   
    
    return s2s
# get indexes
def getNDVI(image):
    
    # Normalized difference vegetation index (NDVI)
    ndvi = image.normalizedDifference(['nir','red']).rename("ndvi")
    image = image.addBands(ndvi)
  
    return(image)
 
# Initialize the GEE
ee.Initialize()

#import data
from general.importData import importData

#manual Module
#folium
from general.myfolium import *


#indexes, topography and covariates
#from general.GetIndexes import GetIndexes
from general.GetIndexes import getNDVI

print("Initialized")

# Create a folium map object.
location=[28.5973518, 83.54495724]
mapObject = foliumInitialize(location,6,600)
my_map = mapObject.Initialize()

print('folium map Initialized')

tartyear = 2019
endyear = 2019

startDate = ee.Date.fromYMD(startyear,1,1)
endDate = ee.Date.fromYMD(endyear,12,31)

#gee assets to get the study area
studyArea = ee.FeatureCollection('users/bikesbade/bankey/banke')



print("getting images")
s2 = importData(studyArea,startDate,endDate)

s2 = s2.median().clip(studyArea)

print(str(s2.bandNames().getInfo()))

#get Indexes
print("getting indexes")
s2 = getNDVI(s2)
print(str(s2.bandNames().getInfo()))

s2 = s2.select('ndvi')
print(str(s2.bandNames().getInfo()))

ndviParams = {min: -1, max: 1, 'palette': ['blue', 'white', 'green']};
my_map.add_ee_layer(s2,ndviParams,'ndvi')
                    
print('done')

#layer control 
tools = pluginsTools(my_map)
tools.addLayerControl()

# Display the map.
display(my_map)