# import config
import time

# A_01: Import python classes & functions
from datetime import datetime
from matplotlib import pyplot as plt
from PIL import Image
import cv2

# A_02: Import python libraries 
import os
import streamlit as st

# A_03: Import user defined libraries
from Library_Directory import create_stremlit_folder, create_folder
from Library_Image import read_image, detect_edges, detect_lines, create_blank_image, get_horizontal_lines, get_vertical_lines, plot_lines
from Library_Image import get_horizontal_lines, get_vertical_lines, correct_image
from Library_Streamlit import save_uploaded_image, display_images_in_directory

# A_03: Import configuration variables
# import config

path_upload="./Auto/Uploads"
image = Image.open('./Auto/Source/header_ultratech.png')

st.image(image, caption='')
st.title("Map Detection")

# Upload an image and save it to the "uploads" folder
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:

    folder_path = None
    if folder_path is None:
        folder_path = path_upload + "/" + create_stremlit_folder(base_directory=path_upload)

    save_uploaded_image(uploaded_image, folder_path)

    # # Introduce a 10-second delay (if needed)
    time.sleep(2)

    # Displaying Image
    st.subheader('Uploaded Image', divider='orange')
    display_images_in_directory(folder_path, image_name="Raw.png")

    # Processing image
    # Step 01: Reading Image
    image_raw = read_image(dir_ip=folder_path,image_name="Raw.png")
    # Apply Gaussian blur
    # ksize = (5, 5)  # Adjust the kernel size according to your needs
    # sigmaX = 0      # Adjust the standard deviation if needed
    # image_raw = cv2.GaussianBlur(image_raw, ksize, sigmaX)
    # display_images_in_directory(folder_path, image_name="Raw.png")

    # Step 02: Detecting Edges
    st.subheader('Detected Edges', divider='orange')
    image_edges = detect_edges(image=image_raw, dir_op=folder_path)
    display_images_in_directory(folder_path, image_name="Edges.png")

    # Step 03: Detecting Lines
    st.subheader('Detected Map', divider='orange')
    lines, image_map = detect_lines(image_edges=image_edges, image_raw=image_raw, dir_op=folder_path, line_color=(0, 165, 255), is_on_blank=False)
    display_images_in_directory(folder_path, image_name="Lines.png")

    # Step 04: Detecting Lines
    st.subheader('Extracted Map', divider='orange')
    lines_extrcated, image_extracted = detect_lines(image_edges=image_edges, image_raw=image_raw, dir_op=folder_path, line_color=(0, 165, 255), is_on_blank=True)
    display_images_in_directory(folder_path, image_name="Extracted.png")

    # Step 05: Corrcet Lines
    st.subheader('Corrected Map', divider='orange')
    image_corrected = correct_image(lines=lines_extrcated, image=image_extracted, dir_ip=folder_path, dir_op=folder_path, verbose=False)
    display_images_in_directory(folder_path, image_name="Corrected.png")



