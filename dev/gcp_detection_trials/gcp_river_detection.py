import pyorc
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from tqdm import tqdm

filepaths = []
filepaths.append("../../examples/riverapp_examples/VGC1/VGC1.mp4")
filepaths.append("../../examples/riverapp_examples/21-04-15/Noirath/video_stabilized.mp4")
filepaths.append("../../examples/riverapp_examples/21-04-15/Limelette/Limelette_drone_coupe.mp4")
filepaths.append("../../examples/riverapp_examples/21-04-15/Rosière/video_stabilized.mp4")
filedirs = []
filedirs.append("../../examples/riverapp_examples/VGC1/")
filedirs.append("../../examples/riverapp_examples/21-04-15/Noirath/")
filedirs.append("../../examples/riverapp_examples/21-04-15/Limelette/")
filedirs.append("../../examples/riverapp_examples/21-04-15/Rosière/")
for v in range(0, 4):
    filepath = filepaths[v]
    filedir = filedirs[v]

    video = cv2.VideoCapture(filepath)
    fps = video.get(cv2.CAP_PROP_FPS)
    start_frame = int(5*fps)
    end_frame = start_frame + 50
    video = pyorc.Video(filepath, start_frame=start_frame, end_frame=end_frame)

    #
    #   Detect the moving pixels and store them in 'mask'
    #

    mask = np.zeros_like(video.get_frame(0, method='grayscale'))
    previous_frame = None

    # store the moving pixels in mask
    for i in tqdm(range(0, end_frame - start_frame, round((end_frame - start_frame) / 5))):
        prepared_frame = video.get_frame(i, method='grayscale')
        prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)

        if (previous_frame is None):
            previous_frame = prepared_frame
            continue

        # absolute difference between two successive frames
        diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
        previous_frame = prepared_frame
        # dilate this difference
        kernel = np.ones((5, 5))
        diff_frame = cv2.dilate(diff_frame, kernel, 1)
        # binary frame of the moving pixels between the two frames (i.e. if the difference is greater than 20)
        thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
        # add all new moving pixels detected
        mask = np.logical_or(mask, thresh_frame)

    # plot of the moving pixels
    plt.imshow(mask, cmap='gray')
    plt.title('Mask of the moving pixels')
    plt.savefig(filedir+'Moving_pixels.png')
    plt.show()

    #
    #   Detect the biggest moving part and store it in 'mask_transform'
    #

    mask_transformed = mask.astype(np.uint8)

    # apply opening on the mask of moving pixels
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (22, 22))
    opening = cv2.morphologyEx(mask_transformed, cv2.MORPH_OPEN, kernel2)
    # apply dilation on the mask of moving pixels
    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel3, iterations=5)
    # give a label to each set of pixels  of the mask that form a touching part
    s = ndimage.generate_binary_structure(2, 2).astype(int) #Generate a structuring element that will consider features connected if they touch diagonally
    objects, nb_objects = ndimage.label(dilation,s)
    # compute the label that occurs the most (i.e. the label of the biggest moving part)
    count = np.bincount(objects.ravel())[1:] # remove the zeros from the available labels
    good_label = (-count).argsort()[0]+1
    # extract the pixels that belongs to the biggest moving part
    river_mask = np.zeros_like(mask_transformed)
    river_mask[objects == good_label] = 1
    # plot the biggest moving part
    plt.imshow(river_mask, cmap='gray')
    plt.title('Biggest moving part')
    plt.savefig(filedir+'Biggest_moving_part.png')
    plt.show()
    # load the initial frame and remove the moving parts
    gray = video.get_frame(0, method="grayscale")
    inv_river_mask = np.logical_not(river_mask)
    masked_frame = gray * inv_river_mask
    # plot the initial frame with the biggest moving part removed
    plt.imshow(masked_frame, cmap='gray')
    plt.title('Initial frame without the biggest moving part')
    plt.savefig(filedir+'Init_frame_no_moving_parts.png')
    plt.show()

    #
    #   Detection du contour et ajout d'un feature par rapport à la distance entre le gcp et le contour
    #

    # to skip this part
    continue

    contour = cv2.findContours(river_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0][0]
    print(cv2.pointPolygonTest(contour, (10, 10), True))
    print(cv2.pointPolygonTest(contour, (500, 1500), True))

    frame = video.get_frame(0)
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

    f, ax = plt.subplots(2, 2)

    ax[0, 0].imshow(img, cmap='gray')
    ax[0, 0].set_title('White filter (200-255)')

    ax[0, 1].imshow(opening, cmap='gray')
    ax[0, 1].set_title('opening')

    ax[1, 0].imshow(dilation, cmap='gray')
    ax[1, 0].set_title('dilation')

    ax[1, 1].imshow(frame)
    ax[1, 1].set_title('Initial frame')

    ax[1, 1].plot(*zip(*np.flip(GCPs)), "rx", markersize=20, label="Control points")

    # using padding
    #f.tight_layout()
    plt.show()


