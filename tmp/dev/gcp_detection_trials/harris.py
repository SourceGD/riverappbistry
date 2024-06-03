import cv2
import numpy as np
import matplotlib.pyplot as plt
#cv2.cornerHarris() param ---
#    img - Input image. It should be grayscale and float32 type.
#    blockSize - It is the size of neighbourhood considered for corner detection
#    ksize - Aperture parameter of the Sobel derivative used.
#    k - Harris detector free parameter in the equation.
  
#
# Detect Harris keypoints for the tag
#

image = cv2.imread('damier_large.png', cv2.CV_32F)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Applying the function
dst = cv2.cornerHarris(gray_image, blockSize=3, ksize=11, k=.1)
# dilate to mark the corners
dst = cv2.dilate(dst, None)
image[dst > 0.01 * dst.max()] = [0, 255, 0]
# Plot
plt.imshow(image)
plt.show()


#
# Detect Harris keypoints for the scene
#

scene = cv2.imread('first_frame.png')
gray_scene = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
# define box to crop the scene to the interest window
width = 1920
height = 1080
top_left_x = int (2*width/3) + 40
top_left_y = int (height/3)
bottom_right_x = int (4*width/5) + 40
bottom_right_y = int (height/4)
scene = scene[bottom_right_y:top_left_y , top_left_x:bottom_right_x]
gray_scene = gray_scene[bottom_right_y:top_left_y , top_left_x:bottom_right_x]
# Applying the function
dst_sc = cv2.cornerHarris(gray_scene, blockSize=2, ksize=11, k=0.1)
# dilate to mark the corners
dst_sc = cv2.dilate(dst_sc, None)
scene[dst_sc > 0.01 * dst_sc.max()] = [0, 255, 0]
# Plot
plt.imshow(scene)
plt.show()

#
# Compute the descriptors with SIFT
#

kp1 = np.argwhere(dst > 0.01 * dst.max())
kp1 = [cv2.KeyPoint(float(x[1]), float(x[0]), 13) for x in kp1]
kp2 = np.argwhere(dst_sc > 0.01 * dst_sc.max())
kp2 = [cv2.KeyPoint(float(x[1]), float(x[0]), 13) for x in kp2]
    
sift = cv2.SIFT_create()
keypoints_1, descriptors_1 = sift.compute(gray_image, kp1)
keypoints_2, descriptors_2 = sift.compute(gray_scene, kp2)

#
# Match the keypoints
#
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
    if m.distance < 0.1 * n.distance:
        good_matches.append(m)
        matchesMask[i]=[1,0]
         
            
# Show the matches
draw_params = dict(matchColor = (0,255,0),
               singlePointColor = (255,0,0),
               matchesMask = matchesMask,
               flags = cv2.DrawMatchesFlags_DEFAULT)
img3 = cv2.drawMatchesKnn(gray_image,keypoints_1,gray_scene,keypoints_2,matches,None,**draw_params)
plt.imshow(img3)
plt.show()









