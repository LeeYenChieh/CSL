import cv2
import numpy as np
# Choose your webcam: 0, 1, ...
cap = cv2.VideoCapture(0)

def nothing(x):
	pass
cv2.namedWindow('Threshold Sliders')
cv2.createTrackbar('R','Threshold Sliders',173,255,nothing)
cv2.createTrackbar('G','Threshold Sliders',0,255,nothing)
cv2.createTrackbar('B','Threshold Sliders',150,255,nothing)

while(True):
	# Get one frame from the camera
	ret, frame = cap.read()

	# Split RGB channels
	b,g,r = cv2.split(frame)

	# Perform thresholding to each channel
	r_thresh = cv2.getTrackbarPos('R','Threshold Sliders')
	g_thresh = cv2.getTrackbarPos('G','Threshold Sliders')
	b_thresh = cv2.getTrackbarPos('B','Threshold Sliders')
	_,r = cv2.threshold(r,r_thresh,255,cv2.THRESH_BINARY)
	_,g = cv2.threshold(g,g_thresh,255,cv2.THRESH_BINARY)
	_,b_inv = cv2.threshold(b,b_thresh,255,cv2.THRESH_BINARY_INV)
	

	# Get the final result using bitwise operation
	result = cv2.bitwise_and(r,b_inv,mask=None)

	# Find and draw contours
	counters, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# Iterate through each contour, check the area and find the center
	for cnt in counters:
		area = cv2.contourArea(cnt)
		(x,y), radius = cv2.minEnclosingCircle(cnt)

	# Show the frame
	zeros = np.zeros(frame.shape[:2],dtype="uint8")
	cv2.imshow('frame', frame)
	cv2.imshow("Red",cv2.merge([zeros,zeros,r]))
	cv2.imshow("Green",cv2.merge([zeros,g,zeros]))
	cv2.imshow("Blue",cv2.merge([b_inv,zeros,zeros]))
	cv2.imshow("result",result)

	# Press q to quit
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()