import cv2
import numpy as np
import matplotlib.pyplot as plt

def orb_detector(new_image, image_template,show_img=False,show_kp=False):
    image1 = new_image
    image2 = image_template
    

    # Create ORB detector object
    orb = cv2.ORB_create(400)
    # Obtain the keypoints and descriptors using ORB
    keypoints_1, descriptors_1 = orb.detectAndCompute(image1, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image2, None)
    if show_kp:
    	img_1 = cv2.drawKeypoints(image1,keypoints_1,image1)
    	img_2 = cv2.drawKeypoints(image2,keypoints_2,image2)
    	plt.imshow(img_1)
    	print("key_scene")
    	plt.show()
    	plt.imshow(img_2)
    	print("key_temp")
    	plt.show()

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_1,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance) 
    # Draw first 10 matches.
    img3 = cv2.drawMatches(image1,keypoints_1,image2,keypoints_2,matches[:10],None, flags=2)
    
    plt.imshow(img3)
    plt.show()

    return matches

#
#	Load images and video and crop the ROI
#

# Load the video and extract first frame
video = cv2.VideoCapture("/home/grdebray/Documents/Doc/Data/Noirath/Video_premiere_utilisation.mp4")
ret, frame = video.read()
height, width = frame.shape[:2]
frame_gr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


image_template = cv2.imread('damier.png', cv2.CV_32F)
bigger = cv2.resize(image_template, (200, 200))
gray1 = cv2.cvtColor(bigger, cv2.COLOR_BGR2GRAY)


# Define ROI Box Dimensions
top_left_x = int (2*width/3) + 140
top_left_y = int (height/3)
bottom_right_x = int (4*width/5) + 40
bottom_right_y = int (height/4)


# Crop window of observation we defined above
cropped = frame_gr[bottom_right_y:top_left_y , top_left_x:bottom_right_x]


# Get number of ORB matches
matches = orb_detector(cropped, gray1,show_img=True,show_kp=True)





