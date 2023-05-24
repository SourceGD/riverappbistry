import numpy as np 
import cv2 
import matplotlib.pyplot as plt 

# Load our image template, this is our reference image
image_template = cv2.imread('damier.png', cv2.CV_32F)
frame = cv2.imread('first_frame.png')


#plot the images
plt.imshow(image_template)
plt.show()
plt.imshow(frame)
plt.show()

#calculate the edges using Canny edge algorithm
edges = cv2.Canny(frame, 10, 1000) 

#plot the edges
plt.imshow(edges)
plt.show()

#calculate the edges using Canny edge algorithm
edges_tmp = cv2.Canny(image_template, 10, 1000) 

#plot the edges
plt.imshow(edges_tmp)
plt.show()
