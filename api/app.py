import json

from flask import Flask, request, send_file
import os
from libs.pyorc import CameraConfig, Video
from src.utils import get_video_frame
from src.back.transect import transect

from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OUTPUT_FOLDER = 'outputs'


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
        piv = da_norm_proj.frames.get_piv().to_netcdf(os.path.join(OUTPUT_FOLDER, data["project_name"]+"_"+'piv.nc'))
        return 'File processed successfully', 200


@app.route('/process', methods=['GET'])
def process_transects():
    # TODO : take the project name and process the transects using the proper piv file
    return send_file(os.path.join(OUTPUT_FOLDER, 'plot_transect.jpg'), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)
