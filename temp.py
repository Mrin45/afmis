from flask import Flask, request, render_template, jsonify
import ee

# Initialize the Earth Engine API
ee.Initialize()

# Initialize the Flask app
app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-flood-data', methods=['POST'])
def get_flood_data():
    try:
        data = request.json
        before_dates = data.get('before')
        after_dates = data.get('after')

        if not before_dates or not after_dates:
            return jsonify({'error': 'Missing before or after dates'}), 400

        before_start = before_dates['start']
        before_end = before_dates['end']
        after_start = after_dates['start']
        after_end = after_dates['end']

        # Define Region of Interest (ROI)
        roi = ee.FeatureCollection('projects/ee-mrinmoynath1/assets/Assam')

        # Load Sentinel-1 image collection
        collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .filterBounds(roi)

        # Filter collection by before and after dates
        before = collection.filter(ee.Filter.date(before_start, before_end)).mosaic().clip(roi)
        after = collection.filter(ee.Filter.date(after_start, after_end)).mosaic().clip(roi)

        # Image preprocessing functions
        def to_natural(image):
            return ee.Image(10.0).pow(image.divide(10.0))

        def to_db(image):
            return ee.Image(image).log10().multiply(10.0)

        before_filtered = to_db(to_natural(before))
        after_filtered = to_db(to_natural(after))

        # Flood and water detection logic
        flood = before_filtered.gt(-20).And(after_filtered.lt(-20))
        flood_mask = flood.updateMask(flood.eq(1))
        water = before_filtered.lt(-20).And(after_filtered.lt(-20))
        water_mask = water.updateMask(water.eq(1))

        # Visualization parameters
        before_filtered_vis_params = {'min': -25, 'max': 0}
        after_filtered_vis_params = {'min': -25, 'max': 0}
        flood_vis_params = {'min': 0, 'max': 1, 'palette': ['yellow', 'red']}
        water_vis_params = {'min': 0, 'max': 1, 'palette': ['blue']}

        # Convert masks to single-band images for visualization
        flood_single_band = flood_mask.select(0)  # Ensure only one band is selected
        water_single_band = water_mask.select(0)  # Ensure only one band is selected

        # Get map tile URLs for each layer
        before_filtered_id = before_filtered.getMapId(before_filtered_vis_params)
        after_filtered_id = after_filtered.getMapId(after_filtered_vis_params)
        flood_map_id = flood_single_band.getMapId(flood_vis_params)
        water_map_id = water_single_band.getMapId(water_vis_params)

        before_filtered_url = before_filtered_id['tile_fetcher'].url_format
        after_filtered_url = after_filtered_id['tile_fetcher'].url_format
        flood_tile_url = flood_map_id['tile_fetcher'].url_format
        water_tile_url = water_map_id['tile_fetcher'].url_format

        return jsonify({
            'before_filtered_url': before_filtered_url,
            'after_filtered_url': after_filtered_url,
            'flood_tile_url': flood_tile_url,
            'water_tile_url': water_tile_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
