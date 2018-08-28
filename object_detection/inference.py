# import the necessary packages
# @Time    : 28/08/2018
# @Author  : Suresh Saini
# @Site    :https://github.com/bharatsush/

import os
import cv2
import argparse
#import pytesseract
from PIL import Image
import glob,sys
import matplotlib.pyplot as plt
import numpy as np
import subprocess
#path='/home/gpu-machine/combined_data/4frame48.jpg'

def get_rnpd(impath):
    cwd = os.getcwd()
    os.chdir("/home/gpu-machine/projects/rnpd/object_detection")
    p = subprocess.Popen(["./darknet", "detector", "test", "cfg/obj.data", "cfg/yolo-obj.cfg", "yolo-obj.weights ", impath], stdout=subprocess.PIPE)
    pr=p.communicate()
    coordinates = []
    
    with open('/home/gpu-machine/projects/rnpd/object_detection/result_coordinate.txt') as file:
        for items in file:
            coordinates=items.split(' ')
            print(coordinates)
            break
    os.chdir(cwd)
    return coordinates

if __name__=="__main__":

        image_list=glob.glob("/home/gpu-machine/projects/dataset/rnpd_image_part1/*.jpg")
        count=0
        for i in range(len(image_list)):
            print(image_list[i])
            get_rnpd(image_list[i])
            count+=1
            if count==2:
                break
            print(count,end=' ')

