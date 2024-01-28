# A_01: Import python classes & functions
from matplotlib import pyplot as plt
from PIL import Image
import os
import streamlit as st

# Function to save the uploaded image
def save_uploaded_image(uploaded_image, folder_path):
    image = Image.open(uploaded_image)
    image.save(os.path.join(folder_path, "Raw.png"))

# Function to display multiple images vertically
def display_images_in_directory(directory, image_name=None):
    if image_name is None:
        image_files = os.listdir(directory)
    else:
        image_files = [image_name]

    for image_file in image_files:
        print("displaying: ")
        print(os.path.join(directory, image_file))
        st.image(os.path.join(directory, image_file), use_column_width=True, caption=image_file)
