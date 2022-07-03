
import ee
# Initialize the Earth Engine module.
ee.Initialize()

##name of bands
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
        t = (t.addBands(img.select(['QA60'])).set(prop)
            .copyProperties(img,['system:time_start','system:footprint']))

        return ee.Image(t)
    
    
    s2s = s2s.map(scaleBands)
    s2s = s2s.select(inBands,outBands)
    
    return s2s


startyear = 2019
endyear = 2019

startDate = ee.Date.fromYMD(startyear,1,1)
endDate = ee.Date.fromYMD(endyear,12,31)

#gee assets to get the study area
# studyArea = ee.FeatureCollection('users/bikesbade/bankey/banke')
# point = ee.Geometry.Point([15.5778, 50.2256])
# point = ee.Geometry.Point([-122.292, 37.9018])
studyArea = ee.FeatureCollection(ee.Geometry.Point(16.37, 48.225))

# studyArea = [
#   ee.Feature(ee.Geometry.Rectangle(30.01, 59.80, 30.59, 60.15))
# ]

print("Getting images") 
s2 = importData(studyArea, startDate,endDate)

s2 = s2.median().clip(studyArea)

# get indexes
def getNDVI(image):
    
    # Normalized difference vegetation index (NDVI)
    # ndvi = image.normalizedDifference(['nir','red']).rename("ndvi")
    # image = image.addBands(ndvi)
    return image.normalizedDifference(['nir', 'B3'])

    return(image)

#get Indexes
print("getting indexes")

ndvi1 = getNDVI(s2)
# ndviParams = {min: -1, max: 1, 'palette': ['blue', 'white', 'green']}
# ndviParams = {min: -1, max: 1}
ndviParams = {'palette': ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9efb8', '#a6d96a',
'#66bd63', '#1a9850']}
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
my_map = folium.Map(location= [16.37, 48.225], zoom_start = 6)  

my_map.add_ee_layer(ndvi1, ndviParams, 'ndvi')
my_map.add_child(folium.LayerControl())

my_map.save("map.html")