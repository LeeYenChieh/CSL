import cv2
import numpy as np
import time
import math
from PIL import Image
from transformers import pipeline
import threading

INF = 6666666666

# digit classification model
pipe = pipeline("image-classification", model="farleyknight/mnist-digit-classification-2022-09-04")

# Choose your webcam: 0, 1, ...
cap = cv2.VideoCapture(2)

fps = 60
dist_thres = 100   # maximum distance to be identified as the same finger
line_thickness = 50
finger_hp = 5
frames_per_detection = 30
frame_count = 0
predicted_digit = 1
current_id = 0
tap_timestamps = []
double_tap_threshold = 5
rotate_threshold = 0.5

def nothing(x):
	pass

def predict_digit(pil_img):
	global predicted_digit
	predictions = pipe(pil_img)
	predicted_digit = max(predictions, key=lambda x: x['score'])['label']

def calculate_slope(x1, y1, x2, y2):
	if x2 - x1 == 0:
		return INF
	return (y2 - y1) / (x2 - x1)
		

cv2.namedWindow('Threshold Sliders')
cv2.createTrackbar('R','Threshold Sliders',24,255,nothing)
cv2.createTrackbar('G','Threshold Sliders',71,255,nothing)
cv2.createTrackbar('B','Threshold Sliders',74,255,nothing)

# a list of finger: a finger is a dictionary with key "id" record its id, 
# key "hp" record its hp, delete the finger when its hp reaches 0. 
# key "pos" is a list recording its positions in all the time frame
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
	_,g_inv = cv2.threshold(g,g_thresh,255,cv2.THRESH_BINARY_INV)
	_,b_inv = cv2.threshold(b,b_thresh,255,cv2.THRESH_BINARY_INV)

	# Get the final result using bitwise operation
	result = cv2.bitwise_and(r,b_inv,mask=None)
	result = cv2.bitwise_and(result,g_inv,mask=None)
	result = cv2.blur(result,(5,5))
	_,result = cv2.threshold(result,128,255,cv2.THRESH_BINARY)
	result = cv2.flip(result,1)

	# Find and draw contours
	contours, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	display = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

	# Iterate through each contour, check the area and find the center
	for contour in contours:
		area = cv2.contourArea(contour)
		if area > 3000:  # Adjust the minimum area threshold as needed
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
				fingers.append({"id": current_id, "hp": finger_hp, "pos": [center], "operation": 'None'})
				current_id += 1
				
	# Draw the lines
	operation = 'None'
	xbias = 0
	ybias = 0
	for finger in fingers:
		operation = 'None'
		finger_length = len(finger["pos"])
		if finger_length < 10:
			operation = 'tap'
			if len(tap_timestamps) >= 1 and time.time() - tap_timestamps[-1] <= double_tap_threshold:
				operation = 'double tap'
		else:
			operation = 'Long press'
		for i, pos in enumerate(finger["pos"]):
			if i == 0:
				continue
			cv2.line(display, finger["pos"][i-1], finger["pos"][i], (255, 255, 255), line_thickness)
			xbias += abs(finger["pos"][i][0] - finger["pos"][i - 1][0])
			ybias += abs(finger["pos"][i][1] - finger["pos"][i - 1][1])
			if i == len(finger["pos"]) - 1:
				if operation == 'Long press' and xbias >= 100:
					operation = 'swipe'
				elif operation == 'Long press' and ybias >= 75:
					operation = 'scroll'
				finger["operation"] = operation
				cv2.putText(display, f"id: {finger['id']}, {operation}", pos, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (242, 110, 53), 1, cv2.LINE_AA)
	extra_operation = 'None'
	if len(fingers) == 2:
		finger1 = fingers[0]
		finger2 = fingers[1]
		initial_dist = math.dist(finger1["pos"][0], finger2["pos"][0])
		final_dist = math.dist(finger1["pos"][-1], finger2["pos"][-1])
		if final_dist > initial_dist:
			extra_operation = 'zoom in'
		elif final_dist < initial_dist:
			extra_operation = 'zoom out'
		
		min_length = min(len(finger1["pos"]), len(finger2["pos"]))
		if min_length > 3:
			#print(len(finger1["pos"]), len(finger2["pos"]))
			initial_slope = calculate_slope(finger1["pos"][0][0], finger1["pos"][0][1], finger2["pos"][1][0], finger2["pos"][1][1])
			final_slope = calculate_slope(finger1["pos"][-1][0], finger1["pos"][-1][1], finger2["pos"][-2][0], finger2["pos"][-2][1])

			if (abs(initial_slope - final_slope) > rotate_threshold):
				extra_operation = 'rotate'


    # Remove finger that has not been detected in this frame
	for i, finger in enumerate(fingers):
		if finger["hp"] <= 0:
			# print(time.time())
			if finger['operation'] == 'tap':
				tap_timestamps.append(time.time())
			del fingers[i]
		finger["hp"] -= 1
	
	

	frame_count += 1
	if frame_count == frames_per_detection:
		pil_img = Image.fromarray(cv2.cvtColor(display, cv2.COLOR_BGR2RGB))
		thr = threading.Thread(target=predict_digit, args=(pil_img,))
		thr.start()
		frame_count = 0
		
	if len(fingers) != 0:
		if extra_operation != 'None':
			cv2.putText(display, f"Digit: {predicted_digit}, {extra_operation}", (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (242, 110, 53), 1, cv2.LINE_AA)
		else:
			cv2.putText(display, f"Digit: {predicted_digit}", (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (242, 110, 53), 1, cv2.LINE_AA)

	# Show the frame
	zeros = np.zeros(frame.shape[:2],dtype="uint8")
	cv2.imshow('frame', frame)
	# cv2.imshow("Red",cv2.merge([zeros,zeros,r]))
	# cv2.imshow("Green",cv2.merge([zeros,g_inv,zeros]))
	# cv2.imshow("Blue",cv2.merge([b_inv,zeros,zeros]))
	cv2.imshow("result",display)

	# Press q to quit
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	# time.sleep(1./fps)

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()