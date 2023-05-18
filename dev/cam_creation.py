import pyorc
import math
import cv2

###################
"""
module where we create all the camera setup/configuration necessary 
to compute the PIV process
"""


###################


# todo add interface to get start_second, the second timing of the video to get the
#  frame used to place markers to create cam_config
# personal suggestion: add a slider that goes from first to last frame and show the frame indicated by the slider
# allows the user to truly see which frame will by used to point the src and corner points --> user-friendly
# see 01_Camera_Configuration_single_video notebook in example folder to see example of plots to show
# the user where he placed to points
def load_init_frame(filepath):
    # get fps of the video
    video = cv2.VideoCapture(filepath)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_second = 25
    frame = round(frame_second * fps)
    # we just need one frame in order to place our markers
    video = pyorc.Video(filepath, start_frame=frame, end_frame=frame + 1)
    return video.get_frame(0, method="rgb")


# convert distances points to the local referential
def convert_dist_to_dest_points(L):
    # Points coordinates computation
    # We consider first that P1 and P4 are vertically aligned and P4 as the  origin
    P1, P4 = [0, L[3]], [0, 0]

    # Then we compute other coordinates using cosine law
    alpha = math.acos((L[3] ** 2 + L[5] ** 2 - L[0] ** 2) / (2 * L[3] * L[5]))
    P2 = [L[5] * math.sin(alpha), L[5] * math.cos(alpha)]
    beta = math.acos((L[3] ** 2 + L[2] ** 2 - L[4] ** 2) / (2 * L[3] * L[2]))
    P3 = [L[2] * math.sin(beta), L[2] * math.cos(beta)]

    return [[P2[0], P2[1]], [P3[0], P3[1]], [P4[0], P4[1]], [P1[0], P1[1]]]


# todo add interface showing init_frame to get the four src points
# todo add pictures to show/explain to what correspond the L array containing distances
# todo add interface showing init_frame to get the four corner points
# todo interface to get z_0, resolution, window_size parameters
# todo add user input to get resolution and window_size parameters
#  (greatly influence process speed and results of PIV)
def cam_create(video, directory):
    init_frame = video.get_frame(0, method = "rgb")

    # src points, in the image referential
    src = [[1523, 117], [1455, 748], [203, 650], [768, 155]]

    # Distances between the fours points of reference ABCD (A top left corner then clockwise order)
    #  in the following order [L_AB, L_BC, L_CD, L_DA, L_AC, L_DB]
    L = [6.65, 7.60, 6.69, 7.82, 10.29, 10.10]
    dst = convert_dist_to_dest_points(L)

    # build the gcps dictionary
    gcps = {"src": src, "dst": dst}
    # # if we would use this video as survey in video, the lines below are also needed,
    # # and proper values need to be filled in. They are now commented out.
    # gcps["h_ref"] = <your locally measured water level during survey in>
    #gcps["h_ref"] = 0.44
    # water level in the local referential
    gcps["z_0"] = 0.44

    # set the height and width
    height, width = init_frame.shape[0:2]

    # now we use everything to make a camera configuration note that the lens_position does not seem to be used for
    # the process but has to be indicated to avoid error/warnings
    cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps, lens_position=[7, -2, 3])

    # set corners for delimitation of the area of interest
    corners = [[1565, 83], [1461, 853], [53, 715], [783, 131]]
    cam_config.set_bbox_from_corners(corners)

    # resolution: this is the resolution in meters, in which you will get your orthoprojected frames,
    # once you have a complete CameraConfig including information on geographical coordinates and image coordinates,
    # and a bounding box, that defines which area you are interested in for velocity estimation. As you can see,
    # a default value of 0.05 is selected, which in many cases is suitable for velocimetry purposes.
    cam_config.resolution = 0.01
    # window_size: this is the amount of orthorectified pixels in which one may expect to find a pattern and also.
    # the size of a window in which a velocity vector will be generated. A default is here set at 10.
    # In smaller streams you may decide to reduce this number, but we highly recommend not to make it lower than 5,
    # to ensure that there are enough pixels to distinguish patterns in. If patterns seem to be really small,
    # then you may decide to reduce the resolution instead. pyorc automatically uses an overlap between windows of 50%
    # to use as much information as possible over the area of interest. With the default settings this would mean you
    # would get a velocity vector every 0.05 * 10 / 2 = 0.25 meters.
    cam_config.window_size = 25

    # save the cam_config file to same directory
    # speedup process if we want to other video with exact same setup
    cam_config.to_file(directory + "cam_config.json")

    return cam_config
