import cv2
import numpy as np

class BeaconDetector:
    def __init__(self):
        pass

    def detect_beacons(self, frame):
        # Convert frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for beacon color (customize these values)
        lower_beacon_color = np.array([100, 150, 0])
        upper_beacon_color = np.array([140, 255, 255])

        # Create a mask for the beacon color
        mask = cv2.inRange(hsv_frame, lower_beacon_color, upper_beacon_color)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        beacons = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # minimum area to consider
                x, y, w, h = cv2.boundingRect(contour)
                beacons.append((x, y, w, h))  # Save bounding box of beacon

        return beacons


# Example of usage:
# detector = BeaconDetector()
# detected_beacons = detector.detect_beacons(frame)

