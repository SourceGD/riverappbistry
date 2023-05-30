import pyorc
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from tqdm import tqdm

filepaths = []
filepaths.append("../examples/VGC1/VGC1.mp4")
filepaths.append("../examples/data/Noirath/Vidéo première utilisation.mp4")
filepaths.append("../examples/data/Limelette/Limelette_drone.mp4")
filepaths.append("../examples/data/Rosière/video_stabilized.mp4")
for v in range(0, 4):
    filepath = filepaths[v]


    video = cv2.VideoCapture(filepath)
    fps = video.get(cv2.CAP_PROP_FPS)
    start_frame = int(5*fps)
    end_frame = start_frame + 50
    video = pyorc.Video(filepath, start_frame=start_frame, end_frame=end_frame)

    mask = np.zeros_like(video.get_frame(0, method='grayscale'))
    previous_frame = None

    for i in tqdm(range(0, end_frame - start_frame, round((end_frame - start_frame) / 5))):
        prepared_frame = video.get_frame(i, method='grayscale')
        prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)

        if (previous_frame is None):
            previous_frame = prepared_frame
            continue

        diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
        previous_frame = prepared_frame

        kernel = np.ones((5, 5))
        diff_frame = cv2.dilate(diff_frame, kernel, 1)

        thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

        mask = np.logical_or(mask, thresh_frame)

    plt.imshow(mask, cmap='gray')
    plt.show()
    # %%
    mask_transformed = mask.astype(np.uint8)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (22, 22))
    opening = cv2.morphologyEx(mask_transformed, cv2.MORPH_OPEN, kernel2)

    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel3, iterations=5)

    objects, nb_objects = ndimage.label(dilation)

    count = np.bincount(objects.ravel())
    good_label = (-count).argsort()[1]  # take indices of 4 bigger numbered labeled

    river_mask = np.zeros_like(mask_transformed)
    river_mask[objects == good_label] = 1
    plt.imshow(river_mask, cmap='gray')
    plt.show()
    # %%
    contour = cv2.findContours(river_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0][0]

    print(cv2.pointPolygonTest(contour, (10, 10), True))
    print(cv2.pointPolygonTest(contour, (500, 1500), True))
    # %%
    frame = video.get_frame(0)
    gray = video.get_frame(0, method="grayscale")
    inv_river_mask = np.logical_not(river_mask)
    masked_frame = gray * inv_river_mask
    plt.imshow(masked_frame, cmap='gray')
    plt.show()
    # %%
    _, img = cv2.threshold(masked_frame, 200, 255, cv2.THRESH_BINARY)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel2)

    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel3, iterations=12)

    objects, nb_objects = ndimage.label(dilation)

    scores = {}
    scores_dist = {}

    for j in range(nb_objects):
        central_pt = tuple(np.round(np.mean(np.argwhere(objects == j + 1), axis=0)))
        dist_score = np.abs(cv2.pointPolygonTest(contour, np.flip(central_pt), True))
        scores_dist[j + 1] = dist_score
        scores[central_pt] = dist_score

    dist = list(scores.values())

    if np.std(dist) > (min(img.shape) / 10):
        label_filtered = [k for k, v in scores_dist.items() if v < np.quantile(list(scores_dist.values()), 0.3)]
    else:
        label_filtered = list(scores_dist.keys())

    scores = {}
    _, GCP_ref = cv2.threshold(cv2.imread("../../examples/data/GCPs detection/reference.png", cv2.IMREAD_GRAYSCALE), 128, 255,
                               cv2.THRESH_BINARY)
    for j in label_filtered:
        window = ndimage.find_objects(objects == j)[0]
        obj = opening[window]
        scores[j] = cv2.matchShapes(obj, GCP_ref, cv2.CONTOURS_MATCH_I2, 0)

    # sort the dictionary and take the 4 best scores label
    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])[:4]}

    GCPs = [np.round(np.mean(np.argwhere(objects == i), axis=0)) for i in scores.keys()]

    plt.figure()
    f, ax = plt.subplots(2, 2)

    ax[0, 0].imshow(img, cmap='gray')
    ax[0, 1].imshow(opening, cmap='gray')
    ax[1, 0].imshow(dilation, cmap='gray')
    ax[1, 1].imshow(frame)
    ax[1, 1].plot(*zip(*np.flip(GCPs)), "rx", markersize=20, label="Control points")

    # using padding
    f.tight_layout()
    plt.show()


