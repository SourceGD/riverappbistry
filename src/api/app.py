import base64
import json
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, send_file, jsonify, abort
import os
# import libs.pyorc path


from libs.pyorc import CameraConfig, Video
from src.back.transect import transect
from src.back.mask import mask_and_plot
import xarray as xr

from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OUTPUT_FOLDER = 'outputs'
load_dotenv()
required_api_key = os.getenv("API_KEY")


# TODO add tls to server

def api_key_required(api_key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.headers.get('X-API-KEY') and request.headers.get('X-API-KEY') == api_key:
                return f(*args, **kwargs)
            else:
                abort(401)

        return decorated_function

    return decorator


@app.route('/process-piv', methods=['POST'])
@api_key_required(required_api_key)
def process_piv():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = json.loads(request.files['data'].read())
        pyorc_video: Video = Video(
            # concat upload_folder+filename
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            start_frame=data["start_frame"],
            end_frame=data["end_frame"],
            freq=data["freq"],
            h_a=data["h_a"],
            camera_config=data["camera_config"]
        )
        da = pyorc_video.get_frames()
        # Apply previous steps filter here
        da_norm = da.frames.normalize()
        da_norm_proj = da_norm.frames.project()
        logging.info("Starting PIV")
        piv = da_norm_proj.frames.get_piv().to_netcdf(
            os.path.join(OUTPUT_FOLDER, data["project_name"] + "_" + 'piv.nc'))
        logging.info("PIV done")
        return 'File processed successfully', 200


@app.route('/process-transects', methods=['GET'])
@api_key_required(required_api_key)
def process_transects():
    request_data = request.get_json()
    video_path = request_data["video_name"].replace("/", "_").lstrip("_")
    pyorc_video: Video = Video(
        os.path.join(UPLOAD_FOLDER, video_path),
        start_frame=request_data["video"]["start_frame"],
        end_frame=request_data["video"]["end_frame"],
        camera_config=request_data["video"]["camera_config"]
    )
    dataset = xr.open_dataset(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + 'piv.nc')
    mask_and_plot(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_", dataset, pyorc_video)
    masked_dataset = xr.open_dataset(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + "piv_masked.nc")
    river_flow = transect(masked_dataset, pyorc_video, OUTPUT_FOLDER + "/" + request_data["project_name"] + "_",
                          request_data["bathymetry"])
    # os.remove(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_piv_masked.nc") does not have the right on every computer,
    # TODO: find a way to bypass admin permissions (windows)

    river_flow = river_flow.values.tolist()
    send_file(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + 'plot_transect.jpg', mimetype='image/jpeg')
    # converting image to base64 to send it with other responses
    with open(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + 'plot_transect.jpg', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    data = {
        "Message": "Transect processed successfully",
        "river_flow": river_flow,
        "image": encoded_string
    }
    return jsonify(data)


if __name__ == '__main__':
    from waitress import serve

    serve(app, host='0.0.0.0', port=80)
    # app.run(debug=True)
