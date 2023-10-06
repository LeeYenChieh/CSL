import cv2
import numpy as np
import time
import math

# Choose your webcam: 0, 1, ...
cap = cv2.VideoCapture(0)

fps = 60
dist_thres = 50   # maximum distance to be identified as the same finger
line_thickness = 50
finger_hp = 5

def nothing(x):
	pass

cv2.namedWindow('Threshold Sliders')
cv2.createTrackbar('R','Threshold Sliders',173,255,nothing)
cv2.createTrackbar('G','Threshold Sliders',0,255,nothing)
cv2.createTrackbar('B','Threshold Sliders',150,255,nothing)

# a list of finger: a finger is a dictionary with key "hp" record its hp, delete the finger when hp reach 0. 
# and key "pos" which is a list recording its positions in all time frame
# a finger is removed from the list if it is not detected for {hp} frames.
fingers = []

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
	contours, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	display = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

	# Iterate through each contour, check the area and find the center
	for contour in contours:
		area = cv2.contourArea(contour)
		if area > 2000:  # Adjust the minimum area threshold as needed
			(x, y), radius = cv2.minEnclosingCircle(contour)
			center = (int(x), int(y))
			cv2.circle(display, center, int(radius), (0, 255, 0), 2)  # Draw a green hollow circle
			cv2.circle(display, center, 5, (0, 0, 255), -1)  # Draw a red center point
			
            # draw the line base on the distance
			is_new = True
			for finger in fingers:
				dist = math.dist(center, finger["pos"][-1])
				if dist < dist_thres:
					finger["pos"].append(center)
					finger["hp"] = finger_hp
					is_new = False
					break
            
			if is_new:
				fingers.append({"hp": finger_hp, "pos": [center]})
				
	# Draw the lines
	for finger in fingers:
		for i, pos in enumerate(finger["pos"]):
			if i == 0:
				continue
			cv2.line(display, finger["pos"][i-1], finger["pos"][i], (255, 255, 255), line_thickness)
				
    # Remove finger that has not been detected in this frame
	for i, finger in enumerate(fingers):
		if finger["hp"] <= 0:
			del fingers[i]
		finger["hp"] -= 1

	# Show the frame
	# zeros = np.zeros(frame.shape[:2],dtype="uint8")
	# cv2.imshow('frame', frame)
	# cv2.imshow("Red",cv2.merge([zeros,zeros,r]))
	# cv2.imshow("Green",cv2.merge([zeros,g,zeros]))
	# cv2.imshow("Blue",cv2.merge([b_inv,zeros,zeros]))
	cv2.imshow("result",display)

	# Press q to quit
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	# time.sleep(1./60)

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()