import os

def create_stremlit_folder(base_directory = None):
    # Define the base directory where you want to create folders
    if base_directory is None:
        return ("directory not provided")

    # Loop through numbers from 0 to 999
    for i in range(1000):
        # Format the number as a three-digit string (e.g., '001', '012', '123', etc.)
        folder_name = '{:03d}'.format(i)

        # Check if the folder already exists
        folder_path = os.path.join(base_directory, folder_name)
        if not os.path.exists(folder_path):
            # If the folder does not exist, create it
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created.")
            return folder_name
        # else:
        #     print(f"Folder '{folder_name}' already exists.")
        

def create_folder(dir_folder, ):
    # Check if the folder exists
    if not os.path.exists(dir_folder):
        # If it doesn't exist, create it
        os.makedirs(dir_folder)
    else:
        print(f"Folder '{dir_folder}' already exists.")

