print("[INFO] Loading packages")
import dev.cam_creation as cam_creation
import dev.stab_and_piv as stab_and_piv
import dev.mask_and_plot_piv as mask_and_plot_piv
import dev.transect as transect
import pyorc
import cv2
import xarray as xr
import os.path
import numpy as np
import pandas as pd

# todo add load_cam Flag parameter whether to create or load a cam_config file
# todo if load_cam, add a folder interface to load the desired cam_config json file
# todo same as above but for the load_piv Flag, folder interface to load desired piv file



if __name__ == "__main__":

    #todo : Add a window to enable the user to set the step

    # step at which to start the process
    # 1 = cam creation, 2 = piv process, 3 = mask application, 4 = transect choice
    step = 1

    #todo : Add a window to enable the user to change these variables
    # - directory
    # - start_second
    # - end_second
    # - freq
    # - water_level
    # - video_filepath (should be in the folder 'directory')
    # - dimension_filepath (should be in the folder 'directory')
    # - bathy_filepath (should be in the folder 'directory')
    # - to_stabilize

    ###########
    # Load data file (video, dim and bathy)
    ###########

    # Data variables set by default on a good-looking example available on the git repository
    directory = "examples/riverapp_examples/VGC1/"
    start_second = 25
    end_second = 30
    freq = 1
    water_level = 0.44
    video_filepath = directory + "VGC1.mp4"
    dimension_filepath = directory + "dimension.txt"
    bathy_filepath = directory + "bathy_format_riverApp.txt"
    to_stabilize = False

    # Checking if the data files are available
    data_required = []
    data_required += [os.path.isfile(video_filepath)]
    data_required += [os.path.isfile(dimension_filepath)]
    data_required += [os.path.isfile(bathy_filepath)]
    if not all(data_required):
        print("[ERROR] - Could not load one of the following data files\n",
              "* ",video_filepath, "\n",
              "* ",dimension_filepath, "\n",
              "* ",bathy_filepath, "\n",
              "Please refer to the data format information file: \n ./examples/riverapp_examples/data_format.md \n")
        quit()

    # Loading the data from files
    print("[INFO] Loading data")
    video = cv2.VideoCapture(video_filepath)
    dimension = np.loadtxt(dimension_filepath, delimiter=",")
    bathy = pd.read_csv(bathy_filepath)

    ###########
    # Process the video file and create a Video object
    ###########
    # get fps of the video
    fps = video.get(cv2.CAP_PROP_FPS)
    # convert seconds in frames
    start_frame = round(start_second * fps)
    end_frame = round(end_second * fps)
    # create the Video object
    video = pyorc.Video(video_filepath, start_frame=start_frame, end_frame=end_frame,
                        stabilize="fixed" if to_stabilize else None, freq=freq, h_a=water_level)

    ###########
    # RiverApp processes
    ###########

    if step == 1:
        print("[INFO] Camera creation")
        cam_config = cam_creation.cam_create(video, directory, dimension,water_level)
    else:
        cam_config = pyorc.load_camera_config(directory + "cam_config.json")

    video.camera_config = cam_config

    if step <= 2:
        print("[INFO] Processing PIV")
        stab_and_piv.process_piv(directory, video)

    if step <= 3:
        print("[INFO] Applying masks and plotting results")
        ds = xr.open_dataset(directory + "piv.nc")
        mask_and_plot_piv.mask_and_plot(directory, ds, video)

    if step <= 4:
        print("[INFO] Compute transect")
        ds = xr.open_dataset(directory + "piv_masked.nc")
        transect.transect(ds, video, directory, bathy_filepath)


