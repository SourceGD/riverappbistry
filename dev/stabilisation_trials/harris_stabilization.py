import cv2
import numpy as np
import matplotlib.pyplot as plt
  
# Reading the image and converting the image to B/W
image = cv2.imread('damier_large.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = np.float32(gray_image)
  
# Applying the function
dst = cv2.cornerHarris(gray_image, blockSize=3, ksize=11, k=.1)
  
print(dst[np.where(dst!=0.0)])
  
# dilate to mark the corners
dst = cv2.dilate(dst, None)
image[dst > 0.01 * dst.max()] = [0, 255, 0]
  
plt.imshow(image)
plt.show()

scene = cv2.imread('first_frame.png')
gray_scene = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
gray_scene = np.float32(gray_scene)

width = 1920
height = 1080
top_left_x = int (2*width/3) + 40
top_left_y = int (height/3)
bottom_right_x = int (4*width/5) + 40
bottom_right_y = int (height/4)
scene = scene[bottom_right_y:top_left_y , top_left_x:bottom_right_x]
gray_scene = gray_scene[bottom_right_y:top_left_y , top_left_x:bottom_right_x]


dst_sc = cv2.cornerHarris(gray_scene, blockSize=2, ksize=11, k=0.1)
  
# dilate to mark the corners
dst_sc = cv2.dilate(dst_sc, None)
scene[dst_sc > 0.01 * dst_sc.max()] = [0, 255, 0]

plt.imshow(scene)
plt.show()

#cv2.cornerHarris() param ---
#    img - Input image. It should be grayscale and float32 type.
#    blockSize - It is the size of neighbourhood considered for corner detection
#    ksize - Aperture parameter of the Sobel derivative used.
#    k - Harris detector free parameter in the equation.

