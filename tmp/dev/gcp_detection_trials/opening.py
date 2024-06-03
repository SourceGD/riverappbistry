import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture("../../Rapport Final/Images/opening_explanation/art3.gif")
ret, img = cap.read()
cap.release()

# img = cv2.imread("../../Rapport Final/Images/opening_explanation/base_img.gif", 0)
if ret:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

    erosion = cv2.morphologyEx(gray, cv2.MORPH_ERODE, kernel)

    dilation = cv2.morphologyEx(erosion, cv2.MORPH_DILATE, kernel, iterations=1)

    # fig, ax = plt.subplots(1, 3)
    #
    # ax[0].imshow(gray, cmap='gray')
    # ax[1].imshow(erosion, cmap='gray')
    # ax[2].imshow(dilation, cmap='gray')
    #
    # [axi.set_axis_off() for axi in ax.ravel()]
    # plt.savefig("../../Rapport Final/Images/opening_explanation/opening_steps", bbox_inches="tight", pad_inches=0)
    # plt.show()

    plt.imshow(gray, cmap="gray")
    plt.axis("off")
    plt.savefig("../../Rapport Final/Images/opening_explanation/opening_step1", bbox_inches="tight", pad_inches=0)

    plt.imshow(erosion, cmap="gray")
    plt.axis("off")
    plt.savefig("../../Rapport Final/Images/opening_explanation/opening_step2", bbox_inches="tight", pad_inches=0)

    plt.imshow(dilation, cmap="gray")
    plt.axis("off")
    plt.savefig("../../Rapport Final/Images/opening_explanation/opening_step3", bbox_inches="tight", pad_inches=0)

