import cv2

# Read the image
frame = cv2.imread("test.png")

# Split RGB channels


# Perform thresholding to each channel


# Get the final result using bitwise operation


# Find and draw contours


# Iterate through each contour, check the area and find the center


# Show the frame
cv2.imshow('frame', frame)

# Press any key to quit
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()