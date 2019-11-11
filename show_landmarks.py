import xml.etree.ElementTree as ET
import cv2

def get_box_points(box):
        top =int(box.get('top'))
        left = int(box.get('left'))
        right = int(box.get('width')) + left 
        bottom = int(box.get('height')) + top
        return (left, top), (right, bottom)

def get_point(point):
        x =int(point.get('x'))
        y = int(point.get('y'))
        return x, y
images_tag="images"

tree = ET.parse('New_Database.xml')
root = tree.getroot()
images_root=None

for child in root:
    if(child.tag==images_tag):
        images_root=child

if(images_root is not None):
    for child in images_root:
        file_path = child.attrib['file']
        image_node = child
        img = cv2.imread(file_path)
        print(file_path)
        for box in image_node.iter('box'):
                pt1, pt2 = get_box_points(box)
                img = cv2.rectangle(img, pt1, pt2, (255,0,0), 2)
                for point in box.iter('part'):
                        x, y = get_point(point)
                        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imwrite("tagged{}".format(file_path.split('/')[-1]),img)
        cv2.namedWindow('sample', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('sample', 640,360)
        cv2.imshow("sample", img)
        cv2.waitKey(500) 