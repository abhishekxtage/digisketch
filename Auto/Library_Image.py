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
        
        cv2.imwrite(dir_op + "/" + "Extracted.png", image_raw)

    return lines, image_raw

def get_horizontal_lines(lines, threshold, verbose=False):
    horizontal_lines = []
    # Iterate through each line
    for line in lines:
        x1, y1, x2, y2 = line[0]  # Extract line coordinates

        # Check if the line is approximately horizontal
        if abs(y2 - y1) < threshold:
            horizontal_lines.append(line)

    if verbose:
        print("horizontal_lines")
        print(horizontal_lines)
    horizontal_lines = [np.array([[min(x[0][0], x[0][2]), x[0][1], max(x[0][0], x[0][2]), x[0][3]]]) for x in horizontal_lines]
    
    return horizontal_lines

def get_vertical_lines(lines, threshold, verbose=False):
    vertical_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]  # Extract line coordinates
        # Check if the line is approximately vertical
        if abs(x2 - x1) < threshold:
            vertical_lines.append(line)

    if verbose:
        print("vertical_lines")
        print(vertical_lines)


    vertical_lines = [np.array([[x[0][0], min(x[0][1], x[0][3]), x[0][2], max(x[0][1], x[0][3])]]) for x in vertical_lines]    

    return vertical_lines

def calculate_intersection(rect1, rect2):
    # Extract coordinates from the format [x1, y1, x2, y2]
    x1_1, y1_1, x2_1, y2_1 = rect1
    x1_2, y1_2, x2_2, y2_2 = rect2

    # Calculate intersection rectangle coordinates
    x_intersect = max(x1_1, x1_2)
    y_intersect = max(y1_1, y1_2)
    w_intersect = min(x2_1, x2_2) - x_intersect
    h_intersect = min(y2_1, y2_2) - y_intersect

    # Check if there is an intersection
    if w_intersect > 0 and h_intersect > 0:
        return [x_intersect, y_intersect, x_intersect + w_intersect, y_intersect + h_intersect]
    else:
        return None
    
def plot_lines(image=None, lines=None, type="1d", lines_h=None, lines_v=None, fill_rectangle=True, draw_corners=True, rectangle_width=5):
    if image is None:
        return "image not found"
    blank_image = create_blank_image(image)

    if type == "1d":
        for index, line in enumerate(lines):
            # print(line)
            cv2.line(blank_image, (line[0], line[1]), (line[2], line[3]), (0, 0, 0), 1, cv2.LINE_AA)
    if type == "2d":
        if fill_rectangle:
            rectangles = []
        for index, line in enumerate(lines_h):    
            # print(line)
            cv2.line(blank_image, (line[0], line[1]), (line[2], line[3]), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(blank_image, (line[0], line[1]-rectangle_width), (line[2], line[3]-rectangle_width), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(blank_image, (line[0], line[1]), (line[0], line[1]-rectangle_width), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(blank_image, (line[2], line[3]), (line[2], line[3]-rectangle_width), (0, 0, 0), 2, cv2.LINE_AA)
            if fill_rectangle:
                # Draw and fill the rectangle on the image
                rectangles.append([line[0], line[1]-rectangle_width, line[2], line[3]])
                cv2.rectangle(blank_image, (line[0], line[1]-rectangle_width), (line[2], line[3]), (169, 169, 169), thickness=cv2.FILLED)

        for index, line in enumerate(lines_v):    
            # print(line)
            cv2.line(blank_image, (line[0], line[1]), (line[2], line[3]), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(blank_image, (line[0]-rectangle_width, line[1]), (line[2]-rectangle_width, line[3]), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(blank_image, (line[0], line[1]), (line[0]-rectangle_width, line[1]), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(blank_image, (line[2], line[3]), (line[2]-rectangle_width, line[3]), (0, 0, 0), 2, cv2.LINE_AA)
            if fill_rectangle:
                rectangles.append([line[0]-rectangle_width, line[1], line[2], line[3]])
                # Draw and fill the rectangle on the image
                cv2.rectangle(blank_image, (line[0]-rectangle_width, line[1]), (line[2], line[3]), (169, 169, 169), thickness=cv2.FILLED)

        if draw_corners:
            # identifying intersecing rectangles:
            intersecting_rectangles = []

            for i in range(len(rectangles)):
                for j in range(i + 1, len(rectangles)):
                    intersection = calculate_intersection(rectangles[i], rectangles[j])
                    if intersection:
                        intersecting_rectangles.append(intersection)
                        x1, y1, x2, y2 = intersection
                        cv2.rectangle(blank_image, (x1, y1), (x2, y2), (0, 0, 0), thickness=cv2.FILLED)


    return blank_image    

def group_horizontal_lines(lines=None, threshold=10, verbose=False):
    horizontal_lines = sorted(lines, key=lambda line: line[1])  # Sort lines based on x coordinates
    grouped_lines_horizontal = []

    if horizontal_lines:
        current_group = [horizontal_lines[0]]
        if verbose:
            print("step 01: cg", current_group)

        for i in range(1, len(horizontal_lines)):
            # Check the difference between y coordinates
            if abs(horizontal_lines[i][1] - horizontal_lines[i-1][1]) < threshold:
                current_group.append(horizontal_lines[i])
                if verbose:
                    print("step 02: ag", horizontal_lines[i])
            else:
                grouped_lines_horizontal.append(current_group)
                current_group = [horizontal_lines[i]]

        grouped_lines_horizontal.append(current_group)
        
    grouped_lines_horizontal_max = []
    for index, grp in enumerate(grouped_lines_horizontal):
        grouped_lines_horizontal_max.append([np.array([min([x[0] for x in grp]), grp[0][1], max([x[2] for x in grp]), grp[0][3]], dtype=np.int32)][0])

    horizontal_lines_first_adjusted = [np.array([x[0], x[1], x[2], x[1]], dtype=np.int32) for x in grouped_lines_horizontal_max]
    
    return grouped_lines_horizontal, grouped_lines_horizontal_max, horizontal_lines_first_adjusted

def group_vertical_lines(lines=None, threshold=10, verbose=False):
    vertical_lines = sorted(lines, key=lambda line: line[0])  # Sort lines based on y coordinates
    grouped_lines_vertical = []

    if vertical_lines:
        current_group = [vertical_lines[0]]

        for i in range(1, len(vertical_lines)):
            # Check the difference between y coordinates
            if (abs(vertical_lines[i][0] - vertical_lines[i-1][0])) < threshold:
                current_group.append(vertical_lines[i])
                # print("detected")
            else:
                grouped_lines_vertical.append(current_group)
                current_group = [vertical_lines[i]]

        grouped_lines_vertical.append(current_group)

    grouped_lines_vertical_max = []
    for index, grp in enumerate(grouped_lines_vertical):
        grouped_lines_vertical_max.append([np.array([grp[0][0], min(x[1] for x in grp), grp[0][2], max([x[3] for x in grp])], dtype=np.int32)][0])

    vertical_lines_first_adjusted = [np.array([x[0], x[1], x[0], x[3]], dtype=np.int32) for x in grouped_lines_vertical_max]

    return grouped_lines_vertical, grouped_lines_vertical_max, vertical_lines_first_adjusted

def correct_image(lines=None, image=None, dir_ip=None, dir_op=None, verbose=False):

    print("step 01: extracting horizontal lines")
    horizontal_lines = get_horizontal_lines(lines.copy(), threshold=10, verbose=False)
    horizontal_lines = [x[0] for x in horizontal_lines]
    image_horizontal_lines = plot_lines(image = image.copy(), lines = horizontal_lines)
    if verbose:
        plt.imshow(image_horizontal_lines)
    
    print("step 02: extracting vertical lines")
    vertical_lines = get_vertical_lines(lines.copy(), threshold=10)
    vertical_lines = [x[0] for x in vertical_lines]
    image_vertical_lines = plot_lines(image = image.copy(), lines = vertical_lines)
    if verbose:
        plt.imshow(image_vertical_lines)

    print("step 03: grouping horizontal lines")
    grouped_lines_horizontal, grouped_lines_horizontal_max, horizontal_lines_first_adjusted = \
    group_horizontal_lines(lines=horizontal_lines, threshold=10)
    image_horizontal_lines_grouped = plot_lines(image=image.copy(), lines=horizontal_lines_first_adjusted, type="1d")
    # plt.imshow(image_horizontal_lines_grouped)

    print("step 04: grouping vertical lines")
    grouped_lines_vertical, grouped_lines_vertical_max, vertical_lines_first_adjusted = \
        group_vertical_lines(lines=vertical_lines, threshold=20)
    image_vertical_lines_grouped = plot_lines(image=image.copy(), lines=vertical_lines_first_adjusted, type="1d")
    # plt.imshow(image_vertical_lines_grouped)

    print("step 05: consolidating lines")
    consolidated_lines = horizontal_lines_first_adjusted.copy()
    consolidated_lines.extend(vertical_lines_first_adjusted)
    # image_lines_grouped = plot_lines(image = image.copy(), lines = consolidated_lines)
    image_lines_grouped = plot_lines(image = image.copy(), lines = None, lines_h=horizontal_lines_first_adjusted, lines_v=vertical_lines_first_adjusted, type="2d", fill_rectangle=True, draw_corners=True)

    if verbose:
        plt.imshow(image_lines_grouped)

    print("step 06: saving image")
    cv2.imwrite(dir_op + "/" + "Corrected.png", image_lines_grouped)

    return image_lines_grouped
