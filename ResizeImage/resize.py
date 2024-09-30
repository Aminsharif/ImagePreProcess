import cv2
import os

# Define the input and output base folders
input_base_folder = 'input'   # e.g., 'input'
output_base_folder = 'output' # e.g., 'output'

# Create the output base folder if it doesn't exist
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

# Specify the new size (width, height)
new_size = (640, 640)

# Function to resize images in each subfolder
def resize_images_in_folder(input_folder, output_folder):
    # Create output subfolder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input subfolder
    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)

        # If the file is an image
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            # Read the image
            img = cv2.imread(img_path)

            if img is not None:
                # Resize the image
                resized_img = cv2.resize(img, new_size)

                # Save the resized image to the corresponding output folder
                output_img_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_img_path, resized_img)
                print(f'Resized and saved: {output_img_path}')
            else:
                print(f'Error reading image: {img_path}')

# Traverse the input folder structure
for root, subdirs, files in os.walk(input_base_folder):
    # Determine the relative path of the subfolder
    relative_path = os.path.relpath(root, input_base_folder)

    # Build corresponding output folder path
    output_folder = os.path.join(output_base_folder, relative_path)

    # Resize images in the current subfolder
    resize_images_in_folder(root, output_folder)
