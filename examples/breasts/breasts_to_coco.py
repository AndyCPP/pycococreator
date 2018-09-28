#!/usr/bin/env python3

import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
from pycococreatortools import pycococreatortools

#Need to modify here#
DATA_SET_CAT = "val"
ROOT_DIR = 'C:/Project/Res/breast_coco'

IMAGE_DIR = os.path.join(ROOT_DIR, DATA_SET_CAT+"2018")
ANNOTATION_DIR = os.path.join(ROOT_DIR, "annotations_"+DATA_SET_CAT)

INFO = {
    "description": "breast Dataset",
    "url": "https://github.com/AndyCPP/pycococreator",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "AndyCPP",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'tumor',
        'supercategory': 'target',
    }
]

def filter_for_png(root, files):
    file_types = ['*.png',]
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    
    return files

def filter_for_annotations(root, files, image_filename):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension.split('_')[2] + '_*'
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]

    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

    return files

def main():

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    segmentation_id = 1
    
    image_id = 1

    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        image_files = filter_for_png(root, files)

        # go through each image
        for image_filename in image_files:
            full_path = os.path.join(root, image_filename)

            image_id = int(image_filename.split('.')[0].split('_')[3])
            image = Image.open(full_path)
            image_info = pycococreatortools.create_image_info(
                image_id, os.path.basename(full_path), image.size)
            coco_output["images"].append(image_info)

            # filter for associated png annotations
            for root, _, files in os.walk(ANNOTATION_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    
                    print(annotation_filename)
                    if 'tumor' in annotation_filename:
                        class_id = 1

                    category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                    binary_mask = np.asarray(Image.open(annotation_filename)
                        .convert('1')).astype(np.uint8)
                    
                    annotation_info = pycococreatortools.create_annotation_info(
                        segmentation_id, image_id, category_info, binary_mask,
                        image.size, tolerance=2)

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)

                    segmentation_id = segmentation_id + 1

    annotation_folder = os.path.join(ROOT_DIR, 'annotations')
    if not os.path.exists(annotation_folder):
        os.makedirs(annotation_folder)
    with open('{}/instances_{}2018.json'.format(annotation_folder, DATA_SET_CAT), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
