import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

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
