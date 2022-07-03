# import Google earth engine module
import ee

# Authenticate the Google earth engine with google account
ee.Initialize()

def getNDVI(image):
    
    # Normalized difference vegetation index (NDVI)
    ndvi = image.normalizedDifference(['nir','red']).rename("ndvi")
    image = image.addBands(ndvi)
  
    return(image)
inBands = ee.List(['QA60','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12']);
outBands = ee.List(['QA60','blue','green','red','re1','re2','re3','nir','re4','waterVapor','cirrus','swir1','swir2']);
 
CloudCoverMax = 20

#function to get the data
def importData(studyArea,startDate,endDate):
 
    # Get Sentinel-2 data
    s2s =(ee.ImageCollection('COPERNICUS/S2')
          .filterDate(startDate,endDate)
          .filterBounds(studyArea)
          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',CloudCoverMax))
          .filter(ee.Filter.lt('CLOUD_COVERAGE_ASSESSMENT',CloudCoverMax)))
    
    #sentinel bands are in scale of 0.0001
    def scaleBands(img):
        prop = img.toDictionary()
        t = (img.select(['QA60','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12'])
             .divide(10000))
        t = t.addBands(img.select(['QA60'])).set(prop).copyProperties(img,['system:time_start','system:footprint'])

        return ee.Image(t)
    
    
    s2s = s2s.map(scaleBands)
    s2s = s2s.select(inBands,outBands)
    
    return s2s

startyear = 2019
endyear = 2019

startDate = ee.Date.fromYMD(startyear,1,1)
endDate = ee.Date.fromYMD(endyear,12,31)

#gee assets to get the study area
studyArea = ee.FeatureCollection('users/bikesbade/bankey/banke')

print("Getting images") 
s2 = importData(studyArea, startDate,endDate)

s2 = s2.median().clip(studyArea)

print("getting indexes")
s2 = getNDVI(s2)
print(str(s2.bandNames().getInfo()))

s2 = s2.select('ndvi')
print(str(s2.bandNames().getInfo()))

ndviParams = {min: -1, max: 1, 'palette': ['blue', 'white', 'green']}

# Create a folium map object.
location=[28.5973518, 83.54495724]



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

folium.Map.add_ee_layer = add_ee_layer
# # Create a folium map object.T
my_map = folium.Map(location= [-124.0769, 40.1035], zoom_start = 8)  

print('folium map Initialized')
my_map.add_ee_layer(s2,ndviParams,'ndvi')
                    
print('done')
my_map.save("map.html")

# Display the map.
