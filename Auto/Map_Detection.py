# import config
import time

# A_01: Import python classes & functions
from datetime import datetime
from matplotlib import pyplot as plt
from PIL import Image

# A_02: Import python libraries 
import os
import streamlit as st

# A_03: Import configuration variables
# import config

def create_folder(dir_folder):
    # Check if the folder exists
    if not os.path.exists(dir_folder):
        # If it doesn't exist, create it
        os.makedirs(dir_folder)
    else:
        print(f"Folder '{dir_folder}' already exists.")

path_folder="/Upload"
print("################")
create_folder(path_folder)

print("wd")
print(os.getcwd())
print("################")


# Function to save the uploaded image
def save_uploaded_image(uploaded_image, folder_path):
    image = Image.open(uploaded_image)
    image.save(os.path.join(folder_path, uploaded_image.name))

# Function to display multiple images vertically
def display_images_in_directory(directory):
    image_files = os.listdir(directory)
    for image_file in image_files:
        print("displaying: ")
        print(os.path.join(directory, image_file))
        st.image(os.path.join(directory, image_file), use_column_width=True, caption=image_file)

st.title("Map Detection")


# Upload an image and save it to the "uploads" folder
uploaded_image = st.file_uploader("Upload an image for OCR", type=["jpg", "png", "jpeg"])
if uploaded_image is not None:
    save_uploaded_image(uploaded_image, path_folder)

    # # Introduce a 10-second delay (if needed)
    time.sleep(10)

    display_images_in_directory(path_folder)

