import os

def create_folder(dir_folder):
    # Check if the folder exists
    if not os.path.exists(dir_folder):
        # If it doesn't exist, create it
        os.makedirs(dir_folder)
    else:
        print(f"Folder '{dir_folder}' already exists.")

path_prj = "C:/Users/Xtage/OneDrive - Xtage Technologies Private Limited/UTec - Map Detection"
prj_id = "006" + "_Sample_Maps"
dir_ip = path_prj + "/" +"Input"
dir_op = path_prj + "/" +"Output"

dir_prj_ip=dir_ip + "/" + prj_id

dir_prj_op=dir_op + "/" + prj_id
create_folder(dir_prj_op)

dir_prj_op_images = dir_prj_op + "/" + "01_Images"

dir_prj_op_files = dir_prj_op + "/" + "02_Files"

dir_prj_op_mdata = dir_prj_op + "/" + "03_Metadata"


dir_prj_op_edges = dir_prj_op_images + "/" + "001_Edges"
create_folder(dir_prj_op_edges)

dir_prj_op_hough = dir_prj_op_images + "/" + "002_Hough_Lines"
create_folder(dir_prj_op_hough)



