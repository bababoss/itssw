# import the necessary packages
import os
#import cv2
import argparse
#import pytesseract
from PIL import Image
import glob,sys
import matplotlib.pyplot as plt
import numpy as np
import subprocess
#path='/home/gpu-machine/combined_data/4frame48.jpg'

def get_rnpd(impath):

    p = subprocess.Popen(["./darknet", "detector", "test", "cfg/obj.data", "cfg/yolo-obj.cfg", "yolo-obj.weights ", impath], stdout=subprocess.PIPE)
    pr=p.communicate()
    input_image = Image.open(impath)
    print(input_image.size)
#     plt.imshow(input_image)
#     plt.show()

    #input_image = input_image.resize((1024, 720), Image.ANTIALIAS)
    coordinates = []

    with open('/home/cogknit/experiments/darknet_y2/result_coordinate.txt') as file:
        for items in file:
            coordinates=items.split(' ')
            break



    #print(coordinates)
    #print(" Coordinates Extracted ")
    cropped_image = input_image.crop((int(coordinates[0]), int(coordinates[2]), int(coordinates[1]), int(coordinates[3])))
    save_path="/home/cogknit/experiments/dataset/rnpd_image_dataset_crop/"+os.path.split(impath)[-1]
    #cropped_image.save(save_path)
    image = Image.open(save_path)
#     image = cv2.imread(save_path)
    plt.imshow(image)
    plt.show()
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Histogram equal for enhancing the number plate for further processing
#     y,cr,cb = cv2.split(cv2.cvtColor(image,cv2.COLOR_RGB2YCrCb))
#     # Converting the image to YCrCb model and splitting the 3 channels
#     y = cv2.equalizeHist(y)
#     # Applying histogram equalisation
#     final_image = cv2.cvtColor(cv2.merge([y,cr,cb]),cv2.COLOR_YCrCb2BGR)
#     gray=cv2.cvtColor(final_image,cv2.COLOR_BGR2GRAY)
#     text=pytesseract.image_to_string(Image.fromarray(final_image))

#     gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#     gray = cv2.medianBlur(gray, 3)

#     filename = "{}.png".format(os.getpid())
#     cv2.imwrite(filename, gray)


    #print(" GaandFaad_NumberPlate Thresholded ")

#     a = Image.open(filename)
#     #print(" Type of a  ----> ", type(a))

#     text = pytesseract.image_to_string(gray)
    #os.remove(filename)
    print(" GaandFaad_NumberPlate DETECTED ------> ")
    return ""

if __name__=="__main__":
#         path='/home/gpu-machine/rnpd/darknet_gpu/test.txt'
#         with open(path,'r') as f:
#             image_list=f.read().split('\n')
        image_list=glob.glob("/home/cogknit/experiments/dataset/rnpd_image_dataset_crop/*.jpg")
        count=0
        
        for i in range(len(image_list)):
            print(image_list[i])
            get_rnpd(image_list[i])
            count+=1
            if count==2:
                break


