import cv2
import os
from glob import glob
import dlib
import argparse

detector = dlib.get_frontal_face_detector()

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=False,
	help="path of images", default="")
args = vars(ap.parse_args())

path = "*.jpg"
if args['folder']!="":
	path = '{}\\*.jpg'.format(args['folder'])

OUTPUT_DIR= "./deleted_img/"
for index,image_file in enumerate(glob(path)):
    frame = cv2.imread(image_file,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)   
    new_image_file = image_file.replace('\\','/')
    rects = detector(gray, 0)
    for rect in rects:
        height = str(rect.bottom()-rect.top())
        width = str(rect.right() - rect.left())
        IntHeight =int(height)
        IntWidth = int (width)
        if IntHeight<=180 and IntWidth<=130:
            try:
                print(image_file)
                if not os.path.exists(OUTPUT_DIR):
                    os.mkdir(OUTPUT_DIR)
                assert os.path.exists(OUTPUT_DIR)
                s=new_image_file[6:]
                cv2.imwrite(OUTPUT_DIR+str(s),frame)
                os.remove(new_image_file)
            except:
                pass
            break

