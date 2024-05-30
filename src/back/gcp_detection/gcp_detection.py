import cv2
from os import path
import numpy as np
from scipy import ndimage
import math
from src.utils import video_to_image


def beacons_detection(video_path: str, time: int) -> tuple:
    """
    Detects beacons in a video frame at a specified time

    This function takes a video path and a time step (in seconds) as input and aims to
    perform beacon detection. It performs the following steps:

    1. **Input Validation:**

       - Checks if the provided `video_path` is a string. Raises a `ValueError` if not.

       - Checks if the video file exists at the specified path. Raises a
         `FileNotFoundError` if not found.
    2. **Beacon Detection :**

       - The function uses an unspecified function `GCP_detect` on the video path. The output is
         stored in `gcp`. The details of `GCP_detect` are not provided in this function.

       - Sorts the output from `GCP_detect` using the `sort_src` function.
    3. **Extracting Image Frame:**

       - Extracts an image frame from the video at the specified `time` (in seconds).

       - The function uses the `video_to_image` function (assumed to be defined elsewhere)
         to perform this task.

    Parameters
    ----------

    - str video_path :
        The path to the video file.

    - int time :
        The time step (in seconds) at which the image frame is to be extracted.

    Returns
    -------

    tuple :
        A tuple containing the extracted image frame and the sorted beacon data.


    Raises
    ------
    - `ValueError`: If the provided `video_path` is not a string.
    - `FileNotFoundError`: If the video file at the specified path is not found.

    """
    if not isinstance(video_path, str):
        raise ValueError(f"video_path must be a string: {video_path}")

    if not path.exists(video_path):
        raise FileNotFoundError(f"Could not find {video_path}")

    gcp = sort_src(GCP_detect(video_path))
    image = video_to_image(video_path, time)

    return (image, gcp)


def GCP_detect(video_path: str) -> list:
    """
    Detects GCPs (Ground Control Points) in the first frame of a video

    This function takes a video path as input and aims to detect GCPs (assumed to be
    predefined reference points) in the first frame of the video. It performs
    the following steps:

    1. **Input Validation:**

       - Checks if the provided `video_path` is a string. Raises a `ValueError` if not.

       - Checks if the video file exists at the specified path. Raises a
         `FileNotFoundError` if not found.
    2. **Open Video and Read First Frame:**

       - Opens the video using OpenCV's `cv2.VideoCapture`.

       - Sets the frame position to the first frame (frame number 0) using
         `cap.set(cv2.CAP_PROP_POS_FRAMES, 0)`.

       - Reads the first frame using `cap.read()` and stores success and frame data
         in separate variables.

       - Raises an `IOError` if reading the frame fails.
    3. **Convert Frame to Grayscale and Flip:**

       - Converts the read frame from BGR (OpenCV's default color format) to
         grayscale using `cv2.cvtColor`.

       - Flips the frame vertically using `cv2.flip`.
    4. **Load Reference GCP Image:**

       - Loads a reference image containing the known GCP patterns using
         `cv2.imread`. The reference image path is constructed by joining the
         directory of the current script with "gcp_reference.png".

    5. **Thresholding:**

       - Applies thresholding to both the frame and the reference image to convert
         them to binary images. Uses OpenCV's `cv2.threshold` function. Specific
         threshold values (128 for reference image, 235 for frame) are used to
         separate foreground (GCPs) from background.

    6. **Morphological Operations:**

       - Performs morphological operations on the thresholded frame image to improve
         GCP detection:

         - Opening: Removes small objects and noise using `cv2.morphologyEx` with
           kernel `kernel1`.

         - Dilation: Expands the remaining objects (potential GCPs) using
           `cv2.morphologyEx` with kernel `kernel2` and multiple iterations (12).
    7. **Object Detection and Scoring:**

       - Uses `ndimage.label` to identify connected objects (potential GCPs) in the
         processed frame image.

       - Iterates through each labeled object:

         - Extracts a window containing the object using `ndimage.find_objects`.

         - Calculates a score using `cv2.matchShapes` to compare the object's shape
           with the reference GCP image. The score indicates how well the shapes match.

    8. **Selecting Top GCP Candidates:**

       - Sorts the dictionary of object labels and their corresponding scores.
       - Takes the top 4 entries (objects with the highest matching scores) from the
         sorted dictionary.
       - Flips the y and x coordinates of the detected GCPs (likely due to the
         earlier image flipping).
       - Converts the NumPy array of GCP coordinates to a list.

    9. **Return GCPs:**
       - Returns a list containing the top 4 detected GCPs as (y, x) coordinates.

    Parameters
    ----------

    - str `video_path` :
        The path to the video file.

    Returns
    -------
    list :
        A list containing the top 4 detected GCPs as (y, x) coordinates.

    Raises
    ------

    - `ValueError`: If the provided `video_path` is not a string.

    - `FileNotFoundError`: If the video file at the specified path is not found.

    - `IOError`: If there's an error reading the video frame.

    Notes
    -----

    - This function assumes the presence of a reference GCP image named
      "gcp_reference.png" in the same directory as the script.

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


def get_polar_angle_wrt_first_pt(x, y, x_cent, y_cent, x_first, y_first):
    """
    Calculates the polar angle of a point relative to a first point and centroid

    This function takes the coordinates of a point, the centroid of a set of points,
    and the coordinates of a designated "first point" as input. It calculates the
    polar angle of the given point with respect to the centroid, considering the
    "first point" as a reference for angle orientation.

    Parameters
    ----------

    - float `x`:
        X-coordinate of the point of interest.
    - float `y`:
        Y-coordinate of the point of interest.
    - float `x_cent` :
        X-coordinate of the centroid.
    - float `y_cent` :
        Y-coordinate of the centroid.
    - float `x_first` :
        X-coordinate of the designated "first point".
    - float `y_first` :
        Y-coordinate of the designated "first point".

    Returns
    -------

    float
        The polar angle (in radians) of the point (x, y) relative to the centroid and with
        orientation based on the "first point".

    Notes
    -----

    - The Y-axis is assumed to be flipped (origin at top), so Y values are
      negated during calculations.

    - The function ensures the returned angle is positive and within the range [0, 2*pi].

    """
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
    Sorts a list of GCPs (Ground Control Points) based on their polar angles

    This function takes a list of GCP coordinates (represented as a 2D NumPy
    array where each row contains [x, y] coordinates) as input. It sorts the GCPs
    in a clockwise order, treating the "top-left" GCP as the reference point.

    The logic for finding the top-left GCP prioritizes points in the following
    quadrants:

    1. **Top-left quadrant (X < centroid_X, Y < centroid_Y):** If there's exactly
       one point here, it's chosen as the top-left GCP.
    2. **Top-left quadrant (X < centroid_X, Y < centroid_Y):** If there are two
       points, the one that's:

         - Uppermost (lowest Y value) if they are close vertically.

         - Leftmost (lowest X value) otherwise.

    3. **Bottom-left quadrant (X < centroid_X, Y > centroid_Y):** If no points
       are found in the top-left quadrant, the uppermost point (lowest Y value)
       here becomes the top-left GCP.

    After identifying the top-left GCP, the function:

    - Calculates the polar angle of each remaining GCP relative to the top-left
      GCP and the centroid.
    - Sorts the GCPs in descending order based on their polar angles (clockwise
      order).

    Parameters
    ----------

    - `src` (`list`): A list of GCP coordinates, likely represented as
      [[x1, y1], [x2, y2], ...] where each sub-list represents a GCP's (X, Y)
      coordinates.

    Returns
    -------

    - `list`: A new list containing the sorted GCP coordinates. The sorting
      ensures a clockwise order starting from the designated "top-left" GCP.

    Notes
    -----

    - The function assumes the `get_polar_angle_wrt_first_pt` function is defined
      elsewhere to calculate polar angles.
    - Note that in order for the PIV to work correctly, the top-left beacon is the P4,
      top-right is P1, bottom-right is P2 and bottom-left is P3.

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
