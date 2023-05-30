import pyorc
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import dev.utils.GCP_detection as gcp

filepaths = []
filepaths.append("../examples/data/VGC1/VGC1.mp4")
filepaths.append("../examples/data/Noirath/Vidéo première utilisation.mp4")
filepaths.append("../examples/data/Limelette/Limelette_drone.mp4")
filepaths.append("../examples/data/Rosière/video.mp4")

verbose=True

for idx in range(0, 4):
    filepath = filepaths[idx]

    video = cv2.VideoCapture(filepath)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_second = 1
    frame = round(frame_second * fps)
    # we just need one frame in order to place our markers
    video = pyorc.Video(filepath, start_frame=frame, end_frame=frame + 1)
    frame = video.get_frame(0, method="rgb")

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    GCP_ref_gray = cv2.imread("./utils/reference.png", cv2.IMREAD_GRAYSCALE)
    GCP_ref = cv2.threshold(GCP_ref_gray, 128, 255, cv2.THRESH_BINARY)[1]

    img = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)[1]

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3 ,3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

    objects, nb_objects = ndimage.label(dilation)

    scores = {}
    for j in range(nb_objects):
        window = ndimage.find_objects(objects==j+1)[0]
        gray_win = gray[window]
        binary_win = opening[window]
        scores[j+1] = cv2.matchShapes(binary_win, GCP_ref, cv2.CONTOURS_MATCH_I2, 0)

    # sort the dictionary and take the 4 best scores label
    scores = {k: v for k, v in sorted(scores.items(), key = lambda item: item[1])[:4]}

    # y value has to be first
    GCPs = np.flip([(np.mean(np.argwhere(objects==i), axis=0)).astype(int) for i in scores.keys()])

    src = gcp.sort_src(GCPs.tolist())

    # flag to print id of GCPs detected in original RGB frame
    # flag_print_GCP_id = True
    # if flag_print_GCP_id:
    #     plt.figure()
    #     plt.imshow(frame)
    #     label = 1
    #     for [x_src,y_src] in src:
    #         plt.text(x_src,y_src,'P%s'%label,fontsize='x-large',color='red')
    #         label+=1
    #     plt.plot(*zip(*GCPs), "rx", markersize=5, label="Control points")
    #     plt.show()

    f, ax = plt.subplots(1, 2)
    ax[0].imshow(frame)
    ax[1].imshow(frame)
    label = 1
    for [x_src, y_src] in src:
        ax[1].text(x_src, y_src, 'P%s' % label, fontsize='x-large', color='red')
        label += 1
    ax[1].plot(*zip(*GCPs), "rx", markersize=5, label="Control points")
    plt.savefig("../../Rapport Final/pres_teams/example_" + str(idx))
    plt.show()

    print("video " + str(idx))
    print(scores)
    bestscoreKey = [k for k, v in scores.items() if v==min(scores.values())][0]
    plt.imshow(frame[ndimage.find_objects(objects==bestscoreKey)[0]])
    plt.show()
    #
    # if verbose:
    #     print(scores)
    #     print(GCPs)
    #
    #     plt.figure()
    #     f, ax = plt.subplots(2, 2)
    #
    #     ax[0, 0].imshow(gray, cmap='gray')
    #     ax[0, 1].imshow(img, cmap='gray')
    #     ax[1, 0].imshow(dilation, cmap='gray')
    #     ax[1, 1].imshow(frame)
    #     ax[1, 1].plot(*zip(*GCPs), "rx", markersize=20, label="Control points")
    #
    #     # using padding
    #     f.tight_layout()
    #     plt.show()
    #
    #     print(GCPs)
