import pyorc
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import riverapp.dev.utils.GCP_detection as gcp

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


for idx in range(0, 4):
    filepath = filepaths[idx]
    filedir = filedirs[idx]

    video = cv2.VideoCapture(filepath)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_second = 1
    frame = round(frame_second * fps)
    # we just need one frame in order to place our markers
    video = pyorc.Video(filepath, start_frame=frame, end_frame=frame + 1)
    frame = video.get_frame(0, method="rgb")

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    GCP_ref_gray = cv2.imread("../utils/reference.png", cv2.IMREAD_GRAYSCALE)
    GCP_ref = cv2.threshold(GCP_ref_gray, 128, 255, cv2.THRESH_BINARY)[1]

    # todo : résultats sur vgc1 avec la balise en X?
    #GCP_ref_gray_bis = cv2.imread("../utils/reference_bis.png", cv2.IMREAD_GRAYSCALE)
    #GCP_ref_bis = cv2.threshold(GCP_ref_gray, 128, 255, cv2.THRESH_BINARY)[1]

    img = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)[1]

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3 ,3))
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

    objects, nb_objects = ndimage.label(dilation)

    # fit the shape of the reference tag and gives a distance score
    scores = {}
    for j in range(nb_objects):
        window = ndimage.find_objects(objects==j+1)[0]
        gray_win = gray[window]
        binary_win = opening[window]
        scores[j+1] = cv2.matchShapes(binary_win, GCP_ref, cv2.CONTOURS_MATCH_I2, 0)

    # sort the dictionary and take the 4 best (i.e. lowest) score label
    scores = {k: v for k, v in sorted(scores.items(), key = lambda item: item[1])[:6]}

    # take the GCP as the objects corresponding to the highest scores
    GCPs = np.flip([(np.mean(np.argwhere(objects==i), axis=0)).astype(int) for i in scores.keys()])

    src = GCPs.tolist()
    src_sorted = gcp.sort_src(GCPs.tolist()[-4:])

    # flag to print id of GCPs detected in original RGB frame
    flag_print_GCP_id_sorted = False
    if flag_print_GCP_id_sorted:
        plt.figure()
        plt.imshow(frame)
        label = 1
        for [x_src,y_src] in src_sorted:
            plt.text(x_src,y_src,'P%s'%label,fontsize='x-large',color='red')
            label+=1
        plt.plot(*zip(*GCPs), "rx", markersize=10, label="Control points")
        #plt.savefig(filedir + 'GCP_detection_triangle.png')
        plt.show()

    # flag to print the id of GCP based on their matching score
    flag_print_GCP_id_scored = True
    if flag_print_GCP_id_scored:
        f, ax = plt.subplots(1, 3,figsize=(12, 4))
        ax[0].imshow(opening,cmap='gray', vmin=0, vmax=255)
        ax[0].set_axis_off()
        ax[0].set_title('Post-processed image')
        ax[1].imshow(frame)
        label_tag = 1
        for [x_src, y_src] in src:
            ax[1].text(x_src, y_src, 'T%s' % (-label_tag+len(scores)+1), fontsize='x-large', color='darkblue')
            label_tag += 1
        ax[1].plot(*zip(*GCPs), "rx", markersize=5, label="Control points ")
        ax[1].set_axis_off()
        ax[1].set_title('Tags ranked by shape similarity')
        ax[2].imshow(frame)
        label = 1
        for [x_src, y_src] in src_sorted:
            ax[2].text(x_src, y_src, 'P%s' % label, fontsize='x-large', color='chartreuse')
            label += 1
        ax[2].plot(*zip(*src_sorted), "rx", markersize=5, label="Control points")
        ax[2].set_axis_off()
        ax[2].set_title('Tags ranked by the sorting routine')
        #plt.savefig("../../Rapport Final/pres_teams/example_" + str(idx))
        #plt.savefig(filedir+'GCP_result.png')
        plt.show()

    print("video " + str(idx))
    print(scores)

    # zoom sur la balise la plus ressemblante à la balise de référence
    #bestscoreKey = [k for k, v in scores.items() if v==min(scores.values())][0]
    #plt.imshow(frame[ndimage.find_objects(objects==bestscoreKey)[0]])
    #plt.show()

    # plot the pixel used for the shape matching on the opened image
    #lab = (objects==bestscoreKey)
    #for i in range(dilation.shape[0]):
    #    for j in range(dilation.shape[1]):
    #        if not lab[i,j]:
    #            opening[i,j]= 0

    #plt.imshow(opening, cmap='gray')
    #plt.axis('off')
    #plt.savefig(filedir+'lim_best_tag.png')
    #plt.show()


