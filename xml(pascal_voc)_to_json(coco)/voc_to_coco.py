#pip install xmltodict pillow

import os
import json
import xmltodict
from PIL import Image
from collections import defaultdict

def get_categories(xml_files):
    """
    Create a list of unique categories from the Pascal VOC XML files.
    """
    categories = set()
    for xml_file in xml_files:
        with open(xml_file, 'r') as f:
            doc = xmltodict.parse(f.read())
            objects = doc['annotation'].get('object', [])
            if isinstance(objects, dict):
                objects = [objects]
            for obj in objects:
                categories.add(obj['name'])
    return sorted(categories)

def convert_voc_to_coco(voc_folder, output_json):
    """
    Convert Pascal VOC dataset in XML format to COCO JSON format.
    Args:
        voc_folder: The folder containing VOC XML files and images.
        output_json: The path to save the COCO JSON file.
    """
    # Folder paths
    xml_folder = os.path.join(voc_folder, "Annotations")
    img_folder = os.path.join(voc_folder, "images")
    
    # Collect all XML annotation files
    xml_files = [os.path.join(xml_folder, f) for f in os.listdir(xml_folder) if f.endswith(".xml")]
    
    # COCO structure
    coco = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    # Get all categories (unique class names)
    categories = get_categories(xml_files)
    category_map = {cat: i + 1 for i, cat in enumerate(categories)}  # Category names mapped to IDs
    
    # Add categories to COCO format
    for cat, cat_id in category_map.items():
        coco['categories'].append({
            "id": cat_id,
            "name": cat,
            "supercategory": "none"
        })

    annotation_id = 1
    for idx, xml_file in enumerate(xml_files):
        with open(xml_file, 'r') as f:
            doc = xmltodict.parse(f.read())
        
        image_info = {}
        annotation_info = []

        # Image details
        filename = doc['annotation']['filename']
        img_path = os.path.join(img_folder, filename)
        
        # Get image width, height, and id
        img = Image.open(img_path)
        width, height = img.size
        
        image_info = {
            "id": idx + 1,
            "file_name": filename,
            "width": width,
            "height": height
        }
        coco["images"].append(image_info)

        # Object annotations
        objects = doc['annotation'].get('object', [])
        if isinstance(objects, dict):
            objects = [objects]  # Handle cases with a single object

        for obj in objects:
            category_name = obj['name']
            category_id = category_map[category_name]

            bndbox = obj['bndbox']
            xmin = int(bndbox['xmin'])
            ymin = int(bndbox['ymin'])
            xmax = int(bndbox['xmax'])
            ymax = int(bndbox['ymax'])
            
            width_box = xmax - xmin
            height_box = ymax - ymin

            # Create annotation dictionary
            annotation = {
                "id": annotation_id,
                "image_id": idx + 1,
                "category_id": category_id,
                "bbox": [xmin, ymin, width_box, height_box],
                "area": width_box * height_box,
                "iscrowd": 0,
                "segmentation": []
            }
            coco["annotations"].append(annotation)
            annotation_id += 1

    # Save COCO JSON
    with open(output_json, 'w') as json_file:
        json.dump(coco, json_file, indent=4)

    print(f"COCO dataset saved at: {output_json}")
#folder strcture will be: pascal_voc_data->train->Annotations(Xmlfile)|images(jpg or png file)|output
#folder strcture will be: pascal_voc_data->val->Annotations(Xmlfile)|images(jpg or png file)|output
# Example usage:
voc_folder = os.path.join(os.getcwd(), 'pascal_voc_data', 'val')  # Update with your path
output_json = os.path.join(os.getcwd(), 'pascal_voc_data', 'val','output', 'coco_annotations.json')  # Update with your path

convert_voc_to_coco(voc_folder, output_json)
