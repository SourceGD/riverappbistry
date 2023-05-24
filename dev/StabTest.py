import pyorc
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

filepaths = []
filepaths.append("../examples/VGC1/VGC1.mp4")
filepaths.append("../examples/data/Noirath/Vidéo première utilisation.mp4")
filepaths.append("../examples/data/Limelette/Limelette_drone.mp4")
filepath = filepaths[0]


video = cv2.VideoCapture(filepath)
fps = video.get(cv2.CAP_PROP_FPS)
frame_second = 5
frame = round(frame_second * fps)
# we just need one frame in order to place our markers
video = pyorc.Video(filepath, start_frame=frame, end_frame=frame + 1)
frame = video.get_frame(0, method="rgb")

gray = video.get_frame(0, method='grayscale')

img = (gray > 245).astype(np.uint8)
kernel = np.ones((9, 9),np.uint8)
n = 11
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel2)

kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3 ,3))
dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel3, iterations=12)

objects, nb_objects = ndimage.label(dilation)

rep = []
count = np.bincount(objects.ravel())
good_label = (-count).argsort()[1:5] # take indices of 4 bigger numbered labeled
for i in good_label:
    rep.append(np.round(np.mean(np.argwhere(objects==i), axis=0)))


print("nombre de repères trouvés = " +str(nb_objects))

plt.imshow(opening, cmap='gray')
plt.show()

plt.imshow(dilation, cmap='gray')
plt.show()

plt.imshow(frame)
plt.plot(*zip(*np.flip(rep)), "rx", markersize=20, label="Control points")
plt.show()

