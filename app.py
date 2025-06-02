# from flask import Flask, render_template, jsonify
# import ee

# # Initialize the Earth Engine API
# ee.Initialize()

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get-false-color-image')
# def get_false_color_image():
#     # Define a fixed date range for the Sentinel-2 image (example: 2024-06-01 to 2024-06-10)
#     start_date = '2023-05-01'
#     end_date = '2024-08-10'

#     # Define the Region of Interest (ROI) as a small area (example coordinates for Goalpara, Assam)
#     roi = ee.FeatureCollection('projects/ee-mrinmoynath1/assets/Assam')

#     # Load Sentinel-2 image collection
#     image_collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
#         .filterDate(start_date, end_date) \
#         .filterBounds(roi)  # Filter by the ROI (small area)

#     # Select bands for false color composite (NIR, Red, Green)
#     false_color_image = image_collection.select(['B8', 'B4', 'B3']).median()  # NIR, Red, Green

#     # Clip the image to the ROI
#     false_color_image = false_color_image.clip(roi)

#     # Visualization parameters for false color composite
#     vis_params = {
#         'min': 500,    # Adjusted the min value to make it darker
#         'max': 2500,   # Adjusted the max value to reduce brightness
#         'bands': ['B8', 'B4', 'B3'],  # NIR, Red, Green
#         'gamma': 1.2    # Lower gamma value for a darker look
#     }

#     # Generate a map ID for the false color image
#     map_id = false_color_image.getMapId(vis_params)

#     # Extract the tile URL from the map ID
#     tile_url = map_id['tile_fetcher'].url_format

#     # Print the tile URL for debugging purposes
#     print(f"Generated Tile URL: {tile_url}")

#     # Return the tile URL to the frontend
#     return jsonify({'tile_url': tile_url})

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, jsonify
# import ee

# # Initialize the Earth Engine API
# ee.Initialize()

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get-ndvi')
# def get_ndvi():
#     # Define a fixed date range for the Sentinel-2 image (example: 2024-06-01 to 2024-06-10)
#     start_date = '2023-05-01'
#     end_date = '2023-08-10'

#     # Define the Region of Interest (ROI) as a small area (example coordinates for Goalpara, Assam)
#     roi = ee.FeatureCollection('projects/ee-mrinmoynath1/assets/Assam')

#     # Load Sentinel-2 image collection
#     image_collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
#         .filterDate(start_date, end_date) \
#         .filterBounds(roi)  # Filter by the ROI (small area)

#     # Select NIR (Band 8) and Red (Band 4) for NDVI calculation
#     image = image_collection.select(['B8', 'B4']).median()  # Using median to get a single composite image

#     # Calculate NDVI
#     ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

#     # Clip the image to the ROI
#     ndvi = ndvi.clip(roi)

#     # Visualization parameters for NDVI
#     vis_params = {
#         'min': -0.1,    # Minimum NDVI value (for bare soil or water)
#         'max': 0.8,     # Maximum NDVI value (for healthy vegetation)
#         'palette': ['green', 'white', 'blue']  # Color palette for NDVI
#     }

#     # Generate a map ID for the NDVI image
#     map_id = ndvi.getMapId(vis_params)

#     # Extract the tile URL from the map ID
#     tile_url = map_id['tile_fetcher'].url_format

#     # Print the tile URL for debugging purposes
#     print(f"Generated Tile URL: {tile_url}")

#     # Return the tile URL to the frontend
#     return jsonify({'tile_url': tile_url})

# if __name__ == '__main__':
#     app.run(debug=True)



#-------------------------------------------------------------------------------------------#
# from flask import Flask, render_template, jsonify
# import ee

# # Initialize the Earth Engine API
# ee.Initialize()

# # Initialize the Flask app
# app = Flask(__name__)

# # Define routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get-flood-data')
# def get_flood_data():
#     # Define the Region of Interest (ROI) as a small area (example: Goalpara, Assam)
#     roi = ee.FeatureCollection('projects/ee-mrinmoynath1/assets/Goalpara')

#     # Load Sentinel-1 GRD image collection
#     collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
#         .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
#         .filter(ee.Filter.eq('instrumentMode', 'IW')) \
#         .filter(ee.Filter.Or(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'),
#                              ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))) \
#         .filterBounds(roi)

#     # Filter for before and after flood dates
#     before = collection.filter(ee.Filter.date('2022-05-01', '2022-05-10')).mosaic().clip(roi)
#     after = collection.filter(ee.Filter.date('2022-05-15', '2022-05-22')).mosaic().clip(roi)

#     def to_natural(image):
#         return ee.Image(10.0).pow(image.divide(10.0))

#     def to_db(image):
#         return ee.Image(image).log10().multiply(10.0)

#     # Apply speckle filtering and convert to dB
#     before_filtered = to_db(to_natural(before))
#     after_filtered = to_db(to_natural(after))

#     # Generate flood and water masks with the same logic as JavaScript
#     flood = before_filtered.gt(-20).And(after_filtered.lt(-20))
#     flood_mask = flood.updateMask(flood.eq(1))
#     water = before_filtered.lt(-20).And(after_filtered.lt(-20))
#     water_mask = water.updateMask(water.eq(1))

#     # Visualization parameters for Sentinel-1
#     before_filtered_vis_params = {
#         'min': -25,
#         'max': 0,
#     }

#     after_filtered_vis_params = {
#         'min': -25,
#         'max': 0,
#     }

#     flood_vis_params = {
#         'min': 0,
#         'max': 1,
#         'palette': ['yellow', 'red']
#     }

#     water_vis_params = {
#         'min': 0,
#         'max': 1,
#         'palette': ['blue']
#     }

#     # Convert masks to single-band images for visualization
#     flood_single_band = flood_mask.select(0)  # Ensure only one band is selected
#     water_single_band = water_mask.select(0)  # Ensure only one band is selected

#     # Generate map IDs for the layers
#     before_filtered_id = before_filtered.getMapId(before_filtered_vis_params)
#     after_filtered_id = after_filtered.getMapId(after_filtered_vis_params)
#     flood_map_id = flood_single_band.getMapId(flood_vis_params)
#     water_map_id = water_single_band.getMapId(water_vis_params)

#     # Extract the tile URLs
#     before_filtered_url = before_filtered_id['tile_fetcher'].url_format
#     after_filtered_url = after_filtered_id['tile_fetcher'].url_format
#     flood_tile_url = flood_map_id['tile_fetcher'].url_format
#     water_tile_url = water_map_id['tile_fetcher'].url_format


#     # Print URLs for debugging
#     print(f"Flood Tile URL: {flood_tile_url}")
#     print(f"Water Tile URL: {water_tile_url}")

#     # Return tile URLs to the frontend
#     return jsonify({
#         'before_filtered_url' : before_filtered_url,
#         'after_filtered_url' : after_filtered_url,
#         'flood_tile_url': flood_tile_url,
#         'water_tile_url': water_tile_url
#     })

# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, request, render_template, jsonify
# import ee
# import os
# import json




# # Store the credentials as an environment variable in Render (or locally)
# credentials_json = os.getenv("GEE_CREDENTIALS_JSON")

# # Save the credentials JSON to a temporary file
# credentials_path = "/tmp/credentials.json"
# with open(credentials_path, "w") as f:
#     f.write(credentials_json)

# # Initialize Earth Engine with the service account credentials
# credentials = ee.ServiceAccountCredentials(None, credentials_path)
# ee.Initialize(credentials)

# print("Earth Engine Initialized Successfully")







# # Initialize the Flask app
# app = Flask(__name__)


# # Get the port from the environment variable
# port = int(os.environ.get("PORT", 5000))

# # Define routes
# @app.route('/')
# def index():
#     return render_template('index.html')



# @app.route('/get-districts', methods=['GET'])
# def get_districts():
#     try:
#         # Load ROI with district names
#         roi = ee.FeatureCollection('projects/fire-detection-429215/assets/Assam_Dist')
#         # Extract district names
#         district_names = roi.aggregate_array('NAME').getInfo()
#         return jsonify({'districts': sorted(district_names)})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/get-flood-data', methods=['POST'])
# def get_flood_data():
#     try:
#         data = request.json
#         before_dates = data.get('before')
#         after_dates = data.get('after')
#         district = data.get('district')

#         # Validate input data
#         if not before_dates or not after_dates:
#             return jsonify({'error': 'Please provide valid before and after date ranges.'}), 400
#         if not district and district != "all":  # Allow "all" to display the entire ROI
#             return jsonify({'error': 'Please specify a district or "all" for the entire ROI.'}), 400

#         before_start = before_dates['start']
#         before_end = before_dates['end']
#         after_start = after_dates['start']
#         after_end = after_dates['end']

#         # Define Region of Interest (ROI)
#         roi = ee.FeatureCollection('projects/fire-detection-429215/assets/Assam_Dist')
        
#         if district != "all":  # If specific district is selected
#             roi = roi.filter(ee.Filter.eq('NAME', district))  # Filter ROI by district

#         # Load Sentinel-1 image collection
#         collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
#             .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
#             .filter(ee.Filter.eq('instrumentMode', 'IW')) \
#             .filterBounds(roi)

#         # Check for empty collections
#         before_collection = collection.filter(ee.Filter.date(before_start, before_end))
#         after_collection = collection.filter(ee.Filter.date(after_start, after_end))

#         if before_collection.size().getInfo() == 0 or after_collection.size().getInfo() == 0:
#             return jsonify({'error': 'No data available for the selected date range or region.'}), 400

#         # Mosaic and clip
#         before = before_collection.mosaic().clip(roi)
#         after = after_collection.mosaic().clip(roi)

#         # Image preprocessing functions
#         def to_natural(image):
#             return ee.Image(10.0).pow(image.divide(10.0)).unmask(0)

#         def to_db(image):
#             return ee.Image(image).log10().multiply(10.0)

#         before_filtered = to_db(to_natural(before))
#         after_filtered = to_db(to_natural(after))


#         # Flood and water detection logic
#         flood = before_filtered.gt(-20).And(after_filtered.lt(-20))
#         flood_mask = flood.updateMask(flood.eq(1))
#         water = before_filtered.lt(-20).And(after_filtered.lt(-20))
#         water_mask = water.updateMask(water.eq(1))


#         # Load Sentinel-2 Image Collection
#         s2_collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
#             .filterBounds(roi)
#             # .filter(ee.Filter.date(before_start, before_end).Or(ee.Filter.date(after_start, after_end))) \
            
#             # .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50))

#         # Check for empty collections
#         before_collection_s2 = s2_collection.filter(ee.Filter.date(before_start, before_end))
#         after_collection_s2 = s2_collection.filter(ee.Filter.date(after_start, after_end))

#         if before_collection_s2.size().getInfo() == 0 or after_collection_s2.size().getInfo() == 0:
#             return jsonify({'error': 'No data available for the selected date range or region.'}), 400

#         # Mosaic and clip
#         before_s2 = before_collection_s2.mosaic().clip(roi)
#         after_s2 = after_collection_s2.mosaic().clip(roi)

#         # if s2_collection.size().getInfo():
#         #     return jsonify({'error': 'No Sentinel-2 data available for the selected date range or region.'}), 400

#         # s2_mosaic = s2_collection.mosaic().clip(roi)
        

#         #ndwi calculation
#         ndwi_beforeflood = before_s2.normalizedDifference(['B3', 'B8']).rename('NDWI_BEFORE')
#         ndwi_afterflood = after_s2.normalizedDifference(['B3', 'B8']).rename('NDWI_AFTER')


#         # Visualization parameters
#         # ndwi_vis = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
#         ndwi_vis = {'min': -1, 'max': 1, 'palette': ['#0000FF', '#C0C0C0', '#008000']}  # Dark Blue to Gray to Green
#         # ndwi_vis = {'min': -1, 'max': 1, 'palette': ['#0000FF', '#00FFFF', '#00FF00', '#FFFF00']}  # Blue to Cyan to Green to Yellow
        
#         before_filtered_vis_params = {'min': -25, 'max': 0, 'palette': ['black', 'white']}
#         after_filtered_vis_params = {'min': -25, 'max': 0, 'palette': ['black', 'white']}
#         flood_vis_params = {'min': 0, 'max': 1, 'palette': ['yellow', 'red']}
#         water_vis_params = {'min': 0, 'max': 1, 'palette': ['blue']}
        
        

#         # Convert masks to single-band images for visualization
#         before_filtered_single_band = before_filtered.select([0])
#         after_filtered_single_band = after_filtered.select([0])
#         flood_single_band = flood_mask.select([0])  # Ensure only one band is selected
#         water_single_band = water_mask.select([0])  # Ensure only one band is selected
#         ndwi_beforeflood_single_band = ndwi_beforeflood.select(['NDWI_BEFORE'])
#         ndwi_afterflood_single_band = ndwi_afterflood.select(['NDWI_AFTER'])
        

#         # Debug: Check number of bands in the images  
#         print("Flood image bands:", before_filtered_single_band.bandNames().getInfo())
#         print("Flood image bands:", after_filtered_single_band.bandNames().getInfo())
#         print("Flood image bands:", flood_single_band.bandNames().getInfo())
#         print("Water image bands:", water_single_band.bandNames().getInfo())
#         print("NDWI before flood bands:", ndwi_beforeflood_single_band.bandNames().getInfo())
#         print("NDWI after flood bands:", ndwi_afterflood_single_band.bandNames().getInfo())

#         # Get map tile URLs for each layer
#         try:
#             before_filtered_url = before_filtered_single_band.getMapId(before_filtered_vis_params)['tile_fetcher'].url_format
#             after_filtered_url = after_filtered_single_band.getMapId(after_filtered_vis_params)['tile_fetcher'].url_format
#             flood_tile_url = flood_single_band.getMapId(flood_vis_params)['tile_fetcher'].url_format
#             water_tile_url = water_single_band.getMapId(water_vis_params)['tile_fetcher'].url_format
#             ndwi_beforeflood_url = ndwi_beforeflood_single_band.getMapId(ndwi_vis)['tile_fetcher'].url_format
#             ndwi_afterflood_url = ndwi_afterflood_single_band.getMapId(ndwi_vis)['tile_fetcher'].url_format
#         except Exception as e:
#             return jsonify({'error': f"Error fetching map tiles: {str(e)}"}), 500

#         return jsonify({
#             'before_filtered_url': before_filtered_url,
#             'after_filtered_url': after_filtered_url,
#             'flood_tile_url': flood_tile_url,
#             'water_tile_url': water_tile_url,
#             'ndwi_beforeflood_url': ndwi_beforeflood_url,
#             'ndwi_afterflood_url': ndwi_afterflood_url
#         })
#     except ee.EEException as ee_error:
#         return jsonify({'error': f"Earth Engine Error: {str(ee_error)}"}), 500
#     except Exception as e:
#         return jsonify({'error': f"Unexpected Error: {str(e)}"}), 500



from flask import Flask, request, render_template, jsonify
import ee
import os
import json




# Store the credentials as an environment variable in Render (or locally)
credentials_json = os.getenv("GEE_CREDENTIALS_JSON")

# Save the credentials JSON to a temporary file
credentials_path = "/tmp/credentials.json"
with open(credentials_path, "w") as f:
    f.write(credentials_json)

# Initialize Earth Engine with the service account credentials
credentials = ee.ServiceAccountCredentials(None, credentials_path)
ee.Initialize(credentials)

print("Earth Engine Initialized Successfully")







# Initialize the Flask app
app = Flask(__name__)


# Get the port from the environment variable
port = int(os.environ.get("PORT", 5000))



# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-districts', methods=['GET'])
def get_districts():
    try:
        # Load ROI with district names
        roi = ee.FeatureCollection('projects/fire-detection-429215/assets/Assam_Dist')
        # Extract district names
        district_names = roi.aggregate_array('NAME').getInfo()
        return jsonify({'districts': sorted(district_names)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-flood-data', methods=['POST'])
def get_flood_data():
    try:
        data = request.json
        before_dates = data.get('before')
        after_dates = data.get('after')
        district = data.get('district')

        # Validate input data
        if not before_dates or not after_dates:
            return jsonify({'error': 'Please provide valid before and after date ranges.'}), 400
        if not district and district != "all":
            return jsonify({'error': 'Please specify a district or "all" for the entire ROI.'}), 400

        before_start = before_dates['start']
        before_end = before_dates['end']
        after_start = after_dates['start']
        after_end = after_dates['end']

        # Define Region of Interest (ROI)
        roi = ee.FeatureCollection('projects/ee-mrinmoynath/assets/Assam_Dist')
        
        if district != "all":
            roi = roi.filter(ee.Filter.eq('NAME', district))

        # Load Sentinel-1 image collection
        collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .filterBounds(roi)

        # Check for empty collections
        before_collection = collection.filter(ee.Filter.date(before_start, before_end))
        after_collection = collection.filter(ee.Filter.date(after_start, after_end))

        if before_collection.size().getInfo() == 0 or after_collection.size().getInfo() == 0:
            return jsonify({'error': 'No data available for the selected date range or region.'}), 400

        # Mosaic and clip
        before = before_collection.mosaic().clip(roi)
        after = after_collection.mosaic().clip(roi)

        # Image preprocessing functions
        def to_natural(image):
            return ee.Image(10.0).pow(image.divide(10.0)).unmask(0)

        def to_db(image):
            return ee.Image(image).log10().multiply(10.0)

        # Select VH band for flood and water detection
        before_filtered = to_db(to_natural(before)).select(['VH'])
        after_filtered = to_db(to_natural(after)).select(['VH'])

        # Flood and water detection logic
        flood = before_filtered.gt(-20).And(after_filtered.lt(-20))  # Adjusted threshold
        flood_mask = flood.updateMask(flood.eq(1)).rename('flood')  # Single band 'flood'
        water = before_filtered.lt(-20).And(after_filtered.lt(-20))  # Adjusted threshold
        water_mask = water.updateMask(water.eq(1)).rename('water')  # Single band 'water'

        # Load Sentinel-2 Image Collection
        s2_collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
            .filterBounds(roi)

        # Check for empty collections
        before_collection_s2 = s2_collection.filter(ee.Filter.date(before_start, before_end))
        after_collection_s2 = s2_collection.filter(ee.Filter.date(after_start, after_end))

        if before_collection_s2.size().getInfo() == 0 or after_collection_s2.size().getInfo() == 0:
            return jsonify({'error': 'No data available for the selected date range or region.'}), 400

        # Mosaic and clip
        before_s2 = before_collection_s2.mosaic().clip(roi)
        after_s2 = after_collection_s2.mosaic().clip(roi)

        # NDWI calculation
        ndwi_beforeflood = before_s2.normalizedDifference(['B3', 'B8']).rename('NDWI_BEFORE')
        ndwi_afterflood = after_s2.normalizedDifference(['B3', 'B8']).rename('NDWI_AFTER')

        # Calculate NDWI stats (mean, min, max)
        def calculate_stats(ndwi_image, geometry):
            mean = ndwi_image.reduceRegion(ee.Reducer.mean(), geometry)
            min_value = ndwi_image.reduceRegion(ee.Reducer.min(), geometry)
            max_value = ndwi_image.reduceRegion(ee.Reducer.max(), geometry)
            mean_info = mean.getInfo()
            min_info = min_value.getInfo()
            max_info = max_value.getInfo()
            return {
                'mean': mean_info.get('NDWI_BEFORE', mean_info.get('NDWI_AFTER', None)),
                'min': min_info.get('NDWI_BEFORE', min_info.get('NDWI_AFTER', 'No Data')),
                'max': max_info.get('NDWI_BEFORE', max_info.get('NDWI_AFTER', 'No Data'))
            }
        geometry = roi
        before_ndwi_stats = calculate_stats(ndwi_beforeflood, geometry)
        after_ndwi_stats = calculate_stats(ndwi_afterflood, geometry)

        # Load ESA WorldCover
        esa_worldcover = ee.Image('ESA/WorldCover/v200/2021').select('Map').clip(roi)
        esa_water = esa_worldcover.eq(80).rename('water')  # Single band 'water'

        # Debug: Print band names
        print("Flood mask bands:", flood_mask.bandNames().getInfo())
        print("Water mask bands:", water_mask.bandNames().getInfo())
        print("ESA water bands:", esa_water.bandNames().getInfo())

        # Calculate areas
        def calculate_area(image, geometry, band_name, scale=10):
            try:
                image = image.select([band_name])
                pixel_area = image.multiply(ee.Image.pixelArea())
                area_m2 = pixel_area.reduceRegion(
                    reducer=ee.Reducer.sum(),
                    geometry=geometry,
                    scale=scale,
                    maxPixels=1e10
                ).get(band_name, 0)
                area_ha = ee.Number(area_m2).divide(10000).getInfo()
                area_sqkm = ee.Number(area_m2).divide(1000000).getInfo()
                return {
                    'ha': area_ha if area_ha is not None else 0,
                    'sqkm': area_sqkm if area_sqkm is not None else 0
                }
            except ee.EEException as e:
                print(f"Area calculation error for band {band_name}: {str(e)}")
                return {'ha': 0, 'sqkm': 0}

        flood_area = calculate_area(flood_mask, roi, 'flood', scale=10)
        water_area = calculate_area(water_mask, roi, 'water', scale=10)
        esa_water_area = calculate_area(esa_water, roi, 'water', scale=10)

        # Debug: Print area results
        print(f"Flood area: {flood_area['ha']} Ha, {flood_area['sqkm']} sqkm")
        print(f"Water area: {water_area['ha']} Ha, {water_area['sqkm']} sqkm")
        print(f"ESA water area: {esa_water_area['ha']} Ha, {esa_water_area['sqkm']} sqkm")

        # Visualization parameters
        esa_vis_params = {
            'min': 10,
            'max': 100,
            'palette': [
                '#006400', '#ffbb22', '#ffff4c', '#f096ff', '#fa0000',
                '#b4b4b4', '#f0f0f0', '#0064c8', '#0096a0', '#00cf75', '#fae6a0'
            ]
        }
        esa_water_vis_params = {'min': 0, 'max': 1, 'palette': ['#000000', '#0064c8']}
        ndwi_vis = {'min': -1, 'max': 1, 'palette': ['#0000FF', '#C0C0C0', '#008000']}
        before_filtered_vis_params = {'min': -25, 'max': 0, 'palette': ['black', 'white']}
        after_filtered_vis_params = {'min': -25, 'max': 0, 'palette': ['black', 'white']}
        flood_vis_params = {'min': 0, 'max': 1, 'palette': ['yellow', 'red']}
        water_vis_params = {'min': 0, 'max': 1, 'palette': ['blue']}

        # Single-band images for visualization
        before_filtered_single_band = before_filtered.select(['VH'])
        after_filtered_single_band = after_filtered.select(['VH'])
        flood_single_band = flood_mask.select(['flood'])
        water_single_band = water_mask.select(['water'])
        ndwi_beforeflood_single_band = ndwi_beforeflood.select(['NDWI_BEFORE'])
        ndwi_afterflood_single_band = ndwi_afterflood.select(['NDWI_AFTER'])
        esa_worldcover_single_band = esa_worldcover.select(['Map'])
        esa_water_single_band = esa_water.select(['water'])

        # Debug: Check band names
        print("Before filtered bands:", before_filtered_single_band.bandNames().getInfo())
        print("After filtered bands:", after_filtered_single_band.bandNames().getInfo())
        print("Flood bands:", flood_single_band.bandNames().getInfo())
        print("Water bands:", water_single_band.bandNames().getInfo())
        print("NDWI before bands:", ndwi_beforeflood_single_band.bandNames().getInfo())
        print("NDWI after bands:", ndwi_afterflood_single_band.bandNames().getInfo())
        print("ESA WorldCover bands:", esa_worldcover_single_band.bandNames().getInfo())
        print("ESA water bands:", esa_water_single_band.bandNames().getInfo())

        # Get map tile URLs
        try:
            before_filtered_url = before_filtered_single_band.getMapId(before_filtered_vis_params)['tile_fetcher'].url_format
            after_filtered_url = after_filtered_single_band.getMapId(after_filtered_vis_params)['tile_fetcher'].url_format
            flood_tile_url = flood_single_band.getMapId(flood_vis_params)['tile_fetcher'].url_format
            water_tile_url = water_single_band.getMapId(water_vis_params)['tile_fetcher'].url_format
            ndwi_beforeflood_url = ndwi_beforeflood_single_band.getMapId(ndwi_vis)['tile_fetcher'].url_format
            ndwi_afterflood_url = ndwi_afterflood_single_band.getMapId(ndwi_vis)['tile_fetcher'].url_format
            esa_worldcover_url = esa_worldcover_single_band.getMapId(esa_vis_params)['tile_fetcher'].url_format
            esa_water_url = esa_water_single_band.getMapId(esa_water_vis_params)['tile_fetcher'].url_format
        except Exception as e:
            return jsonify({'error': f"Error fetching map tiles: {str(e)}"}), 500

        return jsonify({
            'before_filtered_url': before_filtered_url,
            'after_filtered_url': after_filtered_url,
            'flood_tile_url': flood_tile_url,
            'water_tile_url': water_tile_url,
            'ndwi_beforeflood_url': ndwi_beforeflood_url,
            'ndwi_afterflood_url': ndwi_afterflood_url,
            'esa_worldcover_url': esa_worldcover_url,
            'esa_water_url': esa_water_url,
            'before_ndwi_stats': before_ndwi_stats,
            'after_ndwi_stats': after_ndwi_stats,
            'flood_area_ha': flood_area['ha'],
            'flood_area_sqkm': flood_area['sqkm'],
            'water_area_ha': water_area['ha'],
            'water_area_sqkm': water_area['sqkm'],
            'esa_water_area_ha': esa_water_area['ha'],
            'esa_water_area_sqkm': esa_water_area['sqkm']
        })
    except ee.EEException as ee_error:
        return jsonify({'error': f"Earth Engine Error: {str(ee_error)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Unexpected Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)


# Run Flask app on the specified port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
