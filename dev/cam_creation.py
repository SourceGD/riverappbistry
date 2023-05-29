import matplotlib.pyplot as plt
import pyorc
import math
import cv2
from dev.utils.GCP_detection import GCP_detect, sort_src
import numpy as np

"""
module where we create all the camera setup/configuration necessary 
to compute the PIV process
"""

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

def cam_create(video, directory, dim, water_level):
    init_frame = video.get_frame(0, method = "rgb")

    # todo : here the user should be asked if he wants to point the tags by himself or detect them automatically with GCP_detect()
    # if the automatic detection is chosen then a window displaying the four tags on the init_frame should be shown and the user need to validate
    # if the validation is denied, the user need to point out by himself the four tags

    # todo add interface showing init_frame to get the four tags points (i.e. scr) after they are sorted and show them with their index in the list since this index will refer to the label of the tag

    auto_detect = False
    # src points, in the image referential
    if auto_detect:
        # try to detect all four GCP with function (depends on the GCP visibility of the frame)
        src = GCP_detect(init_frame,False)
    else:
        # manual input
        src = [[1523, 117], [1455, 748], [203, 650], [768, 155]]

    src = sort_src(src)

    if False:
        plt.figure()
        plt.imshow(init_frame)
        label = 1
        for [x_src,y_src] in src:
            plt.text(x_src,y_src,'P%s'%label,fontsize='x-large',color='red')
            label+=1
        plt.show()

    dst = convert_dist_to_dest_points(dim)

    # build the gcps dictionary
    gcps = {"src": src, "dst": dst}

    # water level in the local referential
    gcps["z_0"] = water_level

    # set the height and width
    height, width = init_frame.shape[0:2]

    # now we use everything to make a camera configuration note that the lens_position does not seem to be used for
    # the process but has to be indicated to avoid error/warnings
    cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps, lens_position=[7, -2, 3])

    # set corners for delimitation of the area of interest
    cam_config.set_bbox_from_corners(src)

    # todo : add user input to get resolution and window_size parameters

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
    cam_config.to_file(directory + "cam_config.json")

    return cam_config
