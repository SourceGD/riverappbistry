import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
#os.environ["QT_QPA_PLATFORM"] = "xorg"
#os.environ["QT_DEBUG_PLUGINS"] = "1"


def sift_detector(new_image, image_template,show_img=False,show_kp=False):
    image1 = new_image
    image2 = image_template
    

    # Create SIFT detector object
    sift = cv2.SIFT_create()
    # Obtain the keypoints and descriptors using SIFT
    keypoints_1, descriptors_1 = sift.detectAndCompute(image1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(image2, None)
    if show_kp:
    	img_1 = cv2.drawKeypoints(image1,keypoints_1,image1)
    	img_2 = cv2.drawKeypoints(image2,keypoints_2,image2)
    	plt.imshow(img_1)
    	plt.show()
    	plt.imshow(img_2)
    	plt.show()

    # Create the Flann Matcher object
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 3)
    search_params = dict(checks = 100)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)
    
    # Store good matches using Lowe's ratio test
    good_matches = []
    matchesMask = [[0,0] for i in range(len(matches))]
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.96 * n.distance:
            good_matches.append(m)
            matchesMask[i]=[1,0]
            
            
    # Show the matches
    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv2.DrawMatchesFlags_DEFAULT)
    img3 = cv2.drawMatchesKnn(image1,keypoints_1,image2,keypoints_2,matches,None,**draw_params)
    plt.imshow(img3)
    plt.show()

    return len(good_matches), matches

#
#	Load images and video and crop the ROI
#

# Load the video and extract first frame
frame = cv2.imread('first_frame.png', cv2.CV_32F)
height, width = frame.shape[:2]
frame_gr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Load our image template, this is our reference image
image_template = cv2.imread('damier.png', cv2.CV_32F)
bigger = cv2.resize(image_template, (100, 100))
gray1 = cv2.cvtColor(bigger, cv2.COLOR_BGR2GRAY)


# Define ROI Box Dimensions
top_left_x = int (2*width/3) + 140
top_left_y = int (height/3)
bottom_right_x = int (4*width/5) + 40
bottom_right_y = int (height/4)


# Crop window of observation we defined above
cropped = frame_gr[bottom_right_y:top_left_y , top_left_x:bottom_right_x]


# Get number of SIFT matches
num_matches, matches = sift_detector(cropped, gray1,show_img=True,show_kp=True)


#
# Wayland errors may be fixed using this to switch to xorg:
#	https://helpdesk.psionline.com/hc/en-gb/articles/13470827149332-How-to-perform-the-switch-from-the-Wayland-display-server-to-Xorg-X11-on-Linux-Ubuntu-22-04-LTS

