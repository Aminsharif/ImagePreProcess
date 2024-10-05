import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    # Search for all XML files in the given directory
    for xml_file in glob.glob(os.path.join(path, "*.xml")):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            filename = root.find('filename').text

            # Extract image size
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            # Iterate through each object in the XML
            for member in root.findall('object'):
                class_name = member.find('name').text
                # Extract bounding box coordinates
                bndbox = member.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                
                # Append the extracted data to the list
                xml_list.append((filename, width, height, class_name, xmin, ymin, xmax, ymax))
        except Exception as e:
            print(f"Error processing file {xml_file}: {e}")
    
    # Define column names
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def convert_all_xml_to_csv(base_path, output_csv_path):
    all_data = pd.DataFrame(columns=['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    
    # Iterate over each subfolder in the base_path
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder_path}")
            xml_df = xml_to_csv(folder_path)
            
            if not xml_df.empty:
                # Optionally, add a column for the class type based on folder name
                # This is useful if class names in XML are inconsistent
                # xml_df['folder'] = folder  # Uncomment if needed
                
                all_data = pd.concat([all_data, xml_df], ignore_index=True)
                print(f"Added {len(xml_df)} entries from {folder}")
            else:
                print(f"No data found in {folder_path}")
    
    # Save the combined DataFrame to CSV
    all_data.to_csv(output_csv_path, index=False)
    print(f"Successfully saved all data to {output_csv_path}")

if __name__ == "__main__":
    # Define the base path to the train directory
    base_path = os.path.join(os.getcwd(), 'images', 'val')
    
    # Define the output CSV file path
    output_csv_path = os.path.join(os.getcwd(), 'images', 'val', 'val_labels.csv')
    
    # Convert all XMLs to a single CSV
    convert_all_xml_to_csv(base_path, output_csv_path)

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path, class_name):
    xml_list = []
    for xml_file in glob.glob(os.path.join(path, "*.xml")):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            filename = root.find('filename').text

            # Extract image size
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            # Iterate through each object in the XML
            for member in root.findall('object'):
                class_label = member.find('name').text
                # Extract bounding box coordinates
                bndbox = member.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                
                # Append the extracted data to the list
                # Include the class subfolder in the filename
                #for wondows then use in linux
                relative_filename = os.path.join(class_name, filename).replace("\\", "/")
                 #for linux
                #relative_filename = os.path.join(class_name, filename)
                xml_list.append((relative_filename, width, height, class_label, xmin, ymin, xmax, ymax))
        except Exception as e:
            print(f"Error processing file {xml_file}: {e}")
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def convert_all_xml_to_csv(base_path, output_csv_path):
    all_data = pd.DataFrame(columns=['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    
    # Iterate over each subfolder in the base_path
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder_path}")
            xml_df = xml_to_csv(folder_path, folder)
            
            if not xml_df.empty:
                all_data = pd.concat([all_data, xml_df], ignore_index=True)
                print(f"Added {len(xml_df)} entries from {folder}")
            else:
                print(f"No data found in {folder_path}")
    
    # Save the combined DataFrame to CSV
    all_data.to_csv(output_csv_path, index=False)
    print(f"Successfully saved all data to {output_csv_path}")

if __name__ == "__main__":
    # Define the base path to the train directory
    base_path = os.path.join(os.getcwd(), 'images', 'train')
    
    # Define the output CSV file path
    output_csv_path = os.path.join(os.getcwd(), 'images', 'train', 'train_labels.csv')
    
    # Convert all XMLs to a single CSV
    convert_all_xml_to_csv(base_path, output_csv_path)

