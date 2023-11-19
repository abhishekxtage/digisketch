import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def create_blank_image(image=None):
    if image is None:
        return "image not found"

    # Get the height and width of the image
    height, width, _ = image.shape

    # Create a blank image of the same size
    blank_image = np.ones((height, width, 3), np.uint8) * 255

    return blank_image

def read_image(dir_ip=None, image_name=None):
    image = cv2.imread(dir_ip + "/" + image_name)
    return image

def detect_edges(image=None, dir_ip=None, dir_op=None):
    if image is None:
        return "image not found"
    edges = cv2.Canny(image, 50, 150, apertureSize = 3)
    cv2.imwrite(dir_op + "/" + "Edges.png", edges)
    return edges

def detect_lines(image_edges = None, image_raw = None, dir_ip=None, dir_op=None, line_color=(0, 165, 255), is_on_blank=False):
    if image_edges is None:
        return "image not found"
    minLineLength=100
    # best:minLineLength=100, threshold=100, maxLineGap=80
    lines = cv2.HoughLinesP(image=image_edges,
                            rho=1,
                            theta=np.pi/180, 
                            threshold=100, 
                            lines=np.array([]), 
                            minLineLength=minLineLength,
                            maxLineGap=80)
    a,b,c = lines.shape

    if is_on_blank==False:
        for i in range(a):
            cv2.line(image_raw, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), line_color, 1, cv2.LINE_AA)
        cv2.imwrite(dir_op + "/" + "Lines.png", image_raw)
    elif is_on_blank==True:
        image_raw = create_blank_image(image=image_raw)    
        for i in range(a):
            cv2.line(image_raw, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), line_color, 1, cv2.LINE_AA)
        
        cv2.imwrite(dir_op + "/" + "Lines2.png", image_raw)

    return image_raw

