#!/usr/bin/env python3
import os

DATA_SET_CAT = "val"#train/val
ROOT_DIR = 'C:/Project/Res/breast_coco/'
ANN_DIR = os.path.join(ROOT_DIR, DATA_SET_CAT+"2018")

def main():
    files = os.listdir(ANN_DIR)
    
    for index in range(len(files)):
        new_name = "COCO_"+DATA_SET_CAT+"2018_"+files[index]
        new_name = os.path.join(ANN_DIR, new_name)
        cur_name = os.path.join(ANN_DIR, files[index])
        os.rename(cur_name, new_name)


if __name__ == "__main__":
    main()