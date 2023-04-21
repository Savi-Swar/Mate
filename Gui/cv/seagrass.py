import cv2 as cv
import numpy as np

# Load the image
img = cv.imread('Gui/cv/prac.png', cv.IMREAD_COLOR)

# Convert to HSV color space
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Define the boundary of green
low_g = np.array([40, 40, 40])
top_g = np.array([70, 255, 255])

# Threshold the image to obtain only the green regions
mask = cv.inRange(hsv, low_g, top_g)

# Apply morphology to clean
kernel = np.ones((5, 5), np.uint8)
mask = cv.erode(mask, kernel)
mask = cv.dilate(mask, kernel)

# Find contours of the green parts
contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Draw contours 
cv.drawContours(img, contours, -1, (0, 255, 0), 2)

# Count the number of green squares
green_squares = 0
for count in contours:
    # Compute the area and aspect ratio of the contour
    area = cv.contourArea(count)
    x, y, w, h = cv.boundingRect(count)
    aspect_ratio = float(w) / h

    # Check if the contour is approximately square and has a minimum area
    if aspect_ratio >= 0.8 and aspect_ratio <= 1.2 and area >= 200:
        green_squares += 1

# Display the results
print("Number of green squares:", green_squares)
cv.imshow('image', mask)
cv.waitKey(0)
cv.destroyAllWindows()
