import json

from flask import Flask, request, send_file
import os
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


# TODO: check if the user connecting has the right to do so

@app.route('/process-piv', methods=['POST'])
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


@app.route('/process', methods=['GET'])
def process_transects():
    # TODO : take the project name and process the transects using the proper piv file
    # print json params
    request_data = request.get_json()
    print(request_data)
    print(request_data["video_name"])
    print("HERE")
    print("project name : " + request_data["project_name"])
    print(OUTPUT_FOLDER + request_data["video_name"])
    pyorc_video : Video = Video(
        os.path.join(OUTPUT_FOLDER, request_data["video_name"]),
        start_frame=request_data["video"]["start_frame"],
        end_frame=request_data["video"]["end_frame"],
        camera_config=request_data["video"]["camera_config"]
    )
    dataset = xr.open_dataset(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + 'piv.nc')
    print("dataset ok")
    mask_and_plot(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_", dataset, pyorc_video)
    print("mask_and_plot ok")
    masked_dataset = xr.open_dataset(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + "piv_masked.nc")
    print("masked_dataset ok")
    river_flow = transect(masked_dataset, pyorc_video, OUTPUT_FOLDER + "/"+ request_data["project_name"] + "_", request_data["bathymetry"])
    print("river_flow ok")

    # TODO: verify that it returns the value of the river flow
    # TODO: verify how the plot transect is received in the front
    # convert river_flow from DataArray to classic array
    river_flow = river_flow.values.tolist()
    print(river_flow)
    send_file(OUTPUT_FOLDER + "/" + request_data["project_name"] + "_" + 'plot_transect.jpg', mimetype='image/jpeg')
    return river_flow, 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True)
