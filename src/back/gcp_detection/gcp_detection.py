import cv2
from os import path
import numpy as np
from scipy import ndimage
import math
from src.utils import video_to_image


def beacons_detection(video_path: str, time: int) -> tuple:
    if not isinstance(video_path, str):
        raise ValueError(f"video_path must be a string: {video_path}")

    if not path.exists(video_path):
        raise FileNotFoundError(f"Could not find {video_path}")

    gcp = sort_src(GCP_detect(video_path))
    image = video_to_image(video_path, time)

    return (image, gcp)


def GCP_detect(video_path: str) -> list:
    """
        return 4 GCP detected as most probable ones
    """
    if not isinstance(video_path, str):
        raise ValueError(f"video_path must be a string: {video_path}")

    if not path.exists(video_path):
        raise FileNotFoundError(f"Could not find {video_path}")

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    succes, frame = cap.read()

    if not succes:
        raise IOError(f"Could not read {video_path}")

    cap.release()

    # Calculate the points
    gray = cv2.cvtColor(cv2.flip(frame, 0), cv2.COLOR_RGB2GRAY)
    GCP_ref = \
    cv2.threshold(cv2.imread(path.join(path.dirname(__file__), "gcp_reference.png"), cv2.IMREAD_GRAYSCALE), 128, 255,
                  cv2.THRESH_BINARY)[1]

    img = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)[1]

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

    objects, nb_objects = ndimage.label(dilation)

    scores = {}
    for j in range(nb_objects):
        window = ndimage.find_objects(objects == j + 1)[0]
        obj = opening[window]
        scores[j + 1] = cv2.matchShapes(obj, GCP_ref, cv2.CONTOURS_MATCH_I2, 0)

    # sort the dictionary and take the 4 best scores label
    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])[:4]}

    # y value has to be first
    GCPs = np.flip([(np.mean(np.argwhere(objects == i), axis=0)).astype(int) for i in scores.keys()])
    return GCPs.tolist()


# Function to get the polar angle
# with respect to the firts point
# Note that since the y-axis is reverted, the y-coord are multiplied by -1
def get_polar_angle_wrt_first_pt(x, y, x_cent, y_cent, x_first, y_first):
    # Calculate the polar angle of the point (x, y) with respect to the centroid (x_cent, y_cent)
    angle = math.atan2(-1 * (y - y_cent), x - x_cent)
    # Calculate the polar angle of the point (x_first, y_first) with respect to the centroid (x_cent, y_cent)
    angle_first = math.atan2(-1 * (y_first - y_cent), x_first - x_cent)
    # Set the angle to be zero for the first elem
    angle = angle - angle_first
    # Adjust the angle to be positive and in the range [0, 2*pi)
    if angle < 0:
        angle += 2 * math.pi
    return angle


def sort_src(src):
    """
        Function to sort the GCP found automatically.

        The function first find the top left point to be the first one,
            then sort the remaining in clockwise order

        The finding of the first point follow these rules based on the quadrant
            around the centroid of the polygon delimited by the four points
        1. If one point in the top left quadrant it is P1
        2. If two points in the first left quadrant
            a. If they are vertically aligned, P1 is the uppermost
            b. Otherwise P1 is the most left
        3. If no point in top left quadrant then P1 is the uppermost of the
            bottom left quadrant.
    """

    src = np.array(src)

    # find the centroid
    x_cent = int(np.sum(src[:, 0]) / len(src))
    y_cent = int(np.sum(src[:, 1]) / len(src))

    # find the points in the second quadrant
    second_quad = []
    for [x, y] in src:
        if x < x_cent and y < y_cent:
            second_quad += [[x, y]]

    # find the first GCP
    first = []
    if len(second_quad) == 1:
        first = second_quad
    elif len(second_quad) == 2:
        # if they are vertically aligned, take the uppermost point (i.e. the lowest y-coord)
        if np.abs(second_quad[0][0] - second_quad[1][0]) < 0.25 * np.abs(
                0.5 * (second_quad[0][0] + second_quad[1][0]) - x_cent):
            first = [second_quad[np.argsort(np.array(second_quad)[:, 1])[0]][:]]
        # take the leftest one (i.e. the lowest x-coord)
        else:
            first = [second_quad[np.argsort(np.array(second_quad)[:, 0])[0]][:]]
    else:
        # take the uppermost point of the third quadrant (i.e. the lowest y-coord)
        third_quad = []
        for [x, y] in src:
            if x < x_cent and y > y_cent:
                third_quad += [[x, y]]
        print(third_quad)
        first = [third_quad[np.argsort(np.array(third_quad)[:, 1])[0]][:]]

    # find the polar angle of each point wrt the first GCP
    pol_angles = []
    for [x, y] in src:
        pol_angles += [get_polar_angle_wrt_first_pt(x, y, x_cent, y_cent, first[0][0], first[0][1])]

    # sort the points using the polar angles in descending order
    sorted_ind = np.flip(np.argsort(pol_angles))
    sorted_src = src[sorted_ind]
    sorted_src = np.append(sorted_src[-1:], sorted_src[:-1], axis=0)
    # switch first and third beacons to match good order for PIV
    sorted_src[[0, 2]] = sorted_src[[2, 0]]
    print("sorted src", sorted_src.tolist())
    print(type(sorted_src.tolist()))
    return sorted_src.tolist()
