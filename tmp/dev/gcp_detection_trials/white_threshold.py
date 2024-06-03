import pyorc
import cv2
import numpy as np
import matplotlib.pyplot as plt

# load video
filepath = "../../examples/riverapp_examples/21-04-15/Limelette/Limelette_drone_coupe.mp4"
filedir = "../../examples/riverapp_examples/21-04-15/Limelette/"
video = cv2.VideoCapture(filepath)
fps = video.get(cv2.CAP_PROP_FPS)
start_frame = int(5*fps)
end_frame = start_frame + 50
video = pyorc.Video(filepath, start_frame=start_frame, end_frame=end_frame)

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma
    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)
    return cv2.LUT(src, table)


# take first frame and apply gamma correction
gam = 1.5
img = video.get_frame(0, method='rgb')
gammaImg = gammaCorrection(img, gam)

# gcp detection method to find the white with threshold
thr = 225
gray = cv2.cvtColor(gammaImg, cv2.COLOR_RGB2GRAY)
img = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)[1]
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilation1 = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

thr = 235
gray = cv2.cvtColor(gammaImg, cv2.COLOR_RGB2GRAY)
img = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)[1]
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilation2 = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

thr = 245
gray = cv2.cvtColor(gammaImg, cv2.COLOR_RGB2GRAY)
img = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)[1]
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilation3 = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel2, iterations=12)

#show the resulting white parts
f, ax = plt.subplots(2, 2)
ax[0,0].imshow(gammaImg, cmap='gray')
ax[0,0].set_title("Corrected image ($\gamma$ = %s)"%(gam))
ax[0,0].set_axis_off()
ax[0,1].imshow(dilation1, cmap='gray')
ax[0,1].set_title("Threshold = 225")
ax[0,1].set_axis_off()
ax[1,0].imshow(dilation2, cmap='gray')
ax[1,0].set_title("Threshold = 235")
ax[1,0].set_axis_off()
ax[1,1].imshow(dilation3, cmap='gray')
ax[1,1].set_title("Threshold = 245")
ax[1,1].set_axis_off()
plt.savefig(filedir+'brighting/%s.png'%(gam))
plt.show()
