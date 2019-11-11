from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
from glob import glob 
from xml.dom import minidom
import xml.etree.cElementTree as ET
from tkinter import messagebox
import tkinter as tk
import os
from  my_dictionary import my_dictionary

selected_landmark_point = 5
landmark_points = []

red_color = (0,0,255)
green_color = (0,255,0)
selected_color = red_color
dataset = ET.Element("dataset")               
images = ET.SubElement(dataset, "images")
refPt = None
image = None
faces_folder_path ="./img" # Select your image folder path
images_list = []
image_number = len(glob(os.path.join(faces_folder_path,"*.jpg")))
database_path = "dataset"
backupdatabase_path ="backup_dataset"
database_image_path ="image_dataset"
#
def add_landmark_points(_landmark_points,filename,face_box_rect):
	global image
	image = ET.SubElement(images,"image", attrib={"file":filename})               
	height = str(face_box_rect.bottom()-face_box_rect.top())
	width = str(face_box_rect.right() - face_box_rect.left())
	top = str(face_box_rect.top())
	left = str(face_box_rect.left())
	box = ET.SubElement(image, "box", attrib={"height":height,"left":left,"top":top,"width":width})
	for i,landmarkpoint in enumerate(_landmark_points):
		name = "{name:02d}".format(name=i)
		x = "{}".format(landmarkpoint[0])     
		y = "{}".format(landmarkpoint[1])        
		ET.SubElement(box, "part", attrib={"name":name,"x":x,"y":y})


# When image open and if you mouse clicked you can find 
# (x,y) coordinate your clicked point, or RGB values or etc.

def click_and_reset_point(event, x, y, flags, param):
	# grab references to the global variables
	global refPt

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		if refPt is None:
			refPt = [x, y]

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		flags = flags + 1
		cv2.circle(frame, (refPt[0],refPt[1]), 2, red_color)
		
		cv2.imshow("frame", frame)

def re_read_frame_and_add_landmarks(_image_file, _landmark_points):
	frame = cv2.imread(_image_file, cv2.IMREAD_COLOR)
	for landmark_index, landmark in enumerate(_landmark_points):
		if(landmark_index<16):
			cv2.circle(frame,(landmark[0],landmark[1]),2,red_color)
		else:
			cv2.circle(frame,(landmark[0],landmark[1]),2,green_color)
	return frame

# Create dictionary for showing landmark end of the script (Check added point)
check_points = my_dictionary()
landmark_dict = my_dictionary()
def checkpoint (_check_points,_landmark_dict,_landmark_points):
	for j,value in enumerate(landmark_points):
		_landmark_dict.add(j+1,value)
		# print(landmark_dict.items())
		# print(check_points.items())
		if(_landmark_dict.items() == _check_points.items()):
			for k in range(0,selected_landmark_point) :
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(frame,"{}".format(k+1),(_landmark_points[k][0]-10,_landmark_points[k][1]-13),font,1,(255,50,180),2)
	
	cv2.imshow("frame2",frame)

# save to xml file
def save2file(_dataset,_path):
	xmlstr = minidom.parseString(ET.tostring(_dataset)).toprettyxml(indent="   ")
	OUTPUT_DIR = "./data"
	if not os.path.exists(OUTPUT_DIR):
        	os.mkdir(OUTPUT_DIR)
	assert os.path.exists(OUTPUT_DIR)

	with open(OUTPUT_DIR+"/"+_path+".xml", "a") as f:
		f.write(xmlstr)

# to determine face on the image       
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()

# loop over the frames from the video stream
for index,image_file in enumerate(glob(os.path.join(faces_folder_path,"*.jpg"))):
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = cv2.imread(image_file, cv2.IMREAD_COLOR)
	#frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	images_list.append(image_file)
	print(images_list)
	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	LABELLED_DIR = "./labelled/"
	if not os.path.exists(LABELLED_DIR):
        	os.mkdir(LABELLED_DIR)
	assert os.path.exists(LABELLED_DIR)
	cv2.namedWindow('frame')
	labelled = image_file[6:]
	print(labelled)
	cv2.imwrite(LABELLED_DIR+str(labelled),frame)
	# cv2.resizeWindow('frame',600,600)	

	cv2.setMouseCallback("frame",click_and_reset_point)
	
	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		# print(rect)
		top = rect.top()
		left = rect.left()
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		
		landmark_points = []
		i=1
		while(i<selected_landmark_point+1):
			frame = re_read_frame_and_add_landmarks(image_file, landmark_points)
			cv2.putText(frame,"nokta : {}".format(i),(left,top+20), cv2.FONT_HERSHEY_COMPLEX,1, (selected_color))
			cv2.putText(frame,"image: {}\{}".format(index+1,image_number),(left,top+50), cv2.FONT_HERSHEY_COMPLEX,1, selected_color)
			if(i>=17):
				selected_color = green_color
			# show the frame
			while True:
				cv2.imshow("frame", frame)
				key = cv2.waitKey(1) & 0xFF  
				# if the `q` key was pressed, break from the loop
				if key == ord("q"):
					break
				if key == 32:
					if refPt is not None:
						landmark_points.append(refPt)
						check_points.add(i,refPt)
						refPt=None
						# print(landmark_points)
						# print(check_points.items()
						break
					else:
						root = tk.Tk()
						root.withdraw()
						messagebox.showinfo("Hata", "Nokta eklemeden boşluğa bastın\n Önce nokta eklemeklisin.")
				if key == ord("z") or key == ord("Z"):
					try:
						landmark_points.pop()
						i-=2
					except IndexError:
						root = tk.Tk()
						root.withdraw()
						messagebox.showerror("Hata", "Nokta eklemedin \n Farklı nokta eklemek için X'e basın.")
					break
				if key == ord("h") or key == ord("H"):
					root = tk.Tk()
					root.withdraw()
					messagebox.showinfo("Kullanım Bilgisi", "Nokta eklemedin \n Farklı nokta eklemek için X'e basın.")
				if key == ord("x") or key == ord("X"):  # Backspace ascii hex value
					frame = re_read_frame_and_add_landmarks(image_file, landmark_points)
					refPt = None
			i+=1

		checkpoint(check_points,landmark_dict,landmark_points)
     
	while True:
		 
		key = cv2.waitKey(1) & 0xFF
		if key == 13:
			cv2.destroyWindow("frame2")
			add_landmark_points(landmark_points, image_file,rect)
			save2file(image,database_image_path)                
			for z in range(0,1):
				BACKUP_IMAGE_DIR ="./check_done_img/"
				s=image_file[6:]

				if not os.path.exists(BACKUP_IMAGE_DIR):
        				os.mkdir(BACKUP_IMAGE_DIR)
				assert os.path.exists(BACKUP_IMAGE_DIR)	
				cv2.imwrite(BACKUP_IMAGE_DIR+str(s),frame)
				os.remove(images_list[z])
				images_list.pop()
				break
			
			break
		if key == 8:
			save2file(dataset,database_path)                
			save2file(dataset,backupdatabase_path)	
			cv2.destroyAllWindows()


# do a bit of cleanup 
cv2.destroyAllWindows()
  
