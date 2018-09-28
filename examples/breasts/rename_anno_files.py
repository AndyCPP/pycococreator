#!/usr/bin/env python3
import os

DATA_SET_CAT = "_train"#train/val
ROOT_DIR = 'C:/Project/Res/breast_coco/'
ANN_DIR = os.path.join(ROOT_DIR, "annotations"+DATA_SET_CAT)

def main():
    files = os.listdir(ANN_DIR)
    
    for index in range(len(files)):
        new_name = files[index].split(".")[0]+"_"+"tumor"+"_"+"0"+".png"
        new_name = os.path.join(ANN_DIR, new_name)
        cur_name = os.path.join(ANN_DIR, files[index])
        os.rename(cur_name, new_name)


if __name__ == "__main__":
    main()