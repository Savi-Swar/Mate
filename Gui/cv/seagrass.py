import cv2 as cv
import numpy as np

import cv2 as cv
import numpy as np

def count_squares(img):
    # Convert to HSV color space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Adjust the green color range boundaries
    low_g = np.array([35, 50, 50])
    top_g = np.array([75, 255, 255])

    # Threshold the image to obtain only the green regions
    mask = cv.inRange(hsv, low_g, top_g)

    # Apply morphology to clean
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel)
    mask = cv.dilate(mask, kernel)

    # Find contours of the green parts
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Count the number of green squares
    green_squares = 0
    for count in contours:
        # Compute the area and aspect ratio of the contour
        area = cv.contourArea(count)
        x, y, w, h = cv.boundingRect(count)
        aspect_ratio = float(w) / h

        # Calculate the solidity and extent of the contour
        hull = cv.convexHull(count)
        hull_area = cv.contourArea(hull)
        solidity = float(area) / hull_area
        extent = float(area) / (w * h)

        # Check if the contour is approximately square, has a minimum area, high solidity, and high extent
        if aspect_ratio >= 0.8 and aspect_ratio <= 1.2 and area >= 200 and solidity > 0.9 and extent > 0.8:
            green_squares += 1

    cv.imshow("Final", mask)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return green_squares

# Load the image
