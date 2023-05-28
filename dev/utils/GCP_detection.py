import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import math

# return 4 GCP detected as most probable ones
# if verbose is True, then print out the process, and plot images at each step of the function
def GCP_detect(frame, verbose=False):

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    GCP_ref = cv2.threshold(cv2.imread("dev/utils/reference.png", cv2.IMREAD_GRAYSCALE), 128, 255, cv2.THRESH_BINARY)[1]

    img = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)[1]

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3 ,3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

    objects, nb_objects = ndimage.label(dilation)

    scores = {}
    for j in range(nb_objects):
        window = ndimage.find_objects(objects==j+1)[0]
        obj = opening[window]
        scores[j+1] = cv2.matchShapes(obj, GCP_ref, cv2.CONTOURS_MATCH_I2, 0)

    # sort the dictionary and take the 4 best scores label
    scores = {k: v for k, v in sorted(scores.items(), key = lambda item: item[1])[:4]}

    # y value has to be first
    GCPs = np.flip([(np.mean(np.argwhere(objects==i), axis=0)).astype(int) for i in scores.keys()])

    if verbose:
        print(scores)
        print(GCPs)

        plt.figure()
        f, ax = plt.subplots(2, 2)

        ax[0, 0].imshow(img, cmap='gray')
        ax[0, 1].imshow(opening, cmap='gray')
        ax[1, 0].imshow(dilation, cmap='gray')
        ax[1, 1].imshow(frame)
        ax[1, 1].plot(*zip(*GCPs), "rx", markersize=20, label="Control points")

        # using padding
        f.tight_layout()
        plt.show()

        print(GCPs)

    return GCPs.tolist()

# Function to get the polar angle between with respect to the firts point
# Note that since the y-axis is reverted, the y-coord are multiplied by -1
def get_polar_angle_wrt_first_pt(x, y, x_cent, y_cent, x_first, y_first):
    # Calculate the polar angle of the point (x, y) with respect to the centroid (x_cent, y_cent)
    angle = math.atan2(-1*(y - y_cent), x - x_cent)
    # Calculate the polar angle of the point (x_first, y_first) with respect to the centroid (x_cent, y_cent)
    angle_first = math.atan2(-1*(y_first - y_cent), x_first - x_cent)
    # set the angle to be zero for the first elem
    angle = angle - angle_first
    # Adjust the angle to be positive and in the range [0, 2*pi)
    if angle < 0:
        angle += 2 * math.pi
    return angle

def sort_src(src):
    src=np.array(src)

    # find the centroid
    x_cent = np.sum(src[:,0])/src.shape[0]
    y_cent = np.sum(src[:, 1])/src.shape[0]

    # find the points in the first quadrant
    first_quad = []
    for [x,y] in src:
        if x>x_cent and y < y_cent:
            first_quad += [[x,y]]

    # find the first GCP
    first = []
    if len(first_quad) == 1:
        first = first_quad
    elif len(first_quad) == 2:
        # take the rightest one
        first = first_quad[np.argsort(first_quad[:][0])[0],:]
    else:
        # take the uppermost of the second quadrant
        second_quad = []
        for [x, y] in src:
            if x > x_cent and y > y_cent:
                second_quad += [[x, y]]
        first = second_quad[np.argsort(second_quad[:][1])[len(second_quad)-1], :]

    # find the polar angle of each point wrt the first GCP
    pol_angles = []
    for [x,y] in src:
        pol_angles += [get_polar_angle_wrt_first_pt(x,y,x_cent,y_cent,first[0][0], first[0][1])]

    # sort the points using the polar angles in descending order
    sorted_ind = np.flip(np.argsort(pol_angles))
    sorted_src = src[sorted_ind]
    sorted_src = np.append(sorted_src[-1:], sorted_src[:-1], axis=0)

    return sorted_src.tolist()