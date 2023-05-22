import dev.cam_creation as cam_creation
import dev.stab_and_piv as stab_and_piv
import dev.mask_and_plot_piv as mask_and_plot_piv
import dev.transect as transect
import pyorc
import cv2
import xarray as xr

# todo add load_cam Flag parameter whether to create or load a cam_config fil
# todo if load_cam, add a folder interface to load the desired cam_config json file
# todo same as above but for the load_piv Flag, folder interface to load desired piv file

# todo add interface to select start and end time to get the timing window to process for PIV analysis
# todo add user input to get the frequency n, -ie use one frame on n for PIV analysis (reduce process time)
# todo add user input whether to stabilize or not the video -> in stabilization flag variable

if __name__ == "__main__":

    directory = "examples/data/VGC1/"
    video_filepath = directory + "VGC1.mp4"
    bathy_file = directory + "bathy_format_riverApp.txt"
    # step at which to start the process
    # 1 = cam creation, 2 = piv process, 3 = mask application, 4 = transect choice
    step = 1

    start_second = 25
    end_second = 30
    freq = 1

    # get fps of the video
    video = cv2.VideoCapture(video_filepath)
    fps = video.get(cv2.CAP_PROP_FPS)

    # convert seconds in frames
    start_frame = round(start_second * fps)
    end_frame = round(end_second * fps)

    # whether to stabilize the frames first
    flag_stabilization = False

    video = pyorc.Video(video_filepath, start_frame=start_frame, end_frame=end_frame,
                        stabilize="fixed" if flag_stabilization else None, freq=freq, h_a=0.44)

    if step == 1:
        cam_config = cam_creation.cam_create(video, directory)
    else:
        cam_config = pyorc.load_camera_config(directory + "cam_config.json")

    video.camera_config = cam_config

    if step <= 2:
        stab_and_piv.process_piv(directory, video)

    if step <= 3:
        ds = xr.open_dataset(directory + "piv.nc")
        mask_and_plot_piv.mask_and_plot(directory, ds, video)

    if step <= 4:
        ds = xr.open_dataset(directory + "piv_masked.nc")
        transect.transect(ds, video, directory, bathy_file)


