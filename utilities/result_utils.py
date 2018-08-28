"""
@Copyright : Cogknit Semantics pvt limited
@Author :    Suresh Saini
@Email  :    suresh@cogknit.com
@Date    :   12th April 2018
"""
from django.shortcuts import render

from django.shortcuts import HttpResponse,render
from django.utils import timezone
from django.conf import settings


################################TRest framework #########################
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from rest_framework.parsers import FileUploadParser, MultiPartParser,JSONParser

########################## import   Model #################################
from rnpd_app import models
######################### import serializers ###########################
from rnpd_app import serializers

##################Utiliyties#############################################
import jwt,json,requests,os,sys,cv2,uuid
from PIL import Image
from io import BytesIO
import base64,time
from utilities import audio_spliter as spliter
from utilities import midas_log
import json,requests,os,sys,time,psutil

def model_instance_result(media_obj,model_type):
    result=None

    model_res=models.MidasResult.objects.filter(mediafile=media_obj,
                        model_type=model_type,
                       ).order_by('-created')[:1]
    if model_res:
        serializer=serializers.MidasResultSerializer(model_res,many=True)
        json_acceptable_string = serializer.data[0]['result'].replace("'", "\"")
        result = json.loads(json_acceptable_string)
        print("result utils: ",result)
    return  result

def processed_model_result(request,model_type):
    try:
        video_id = request.query_params["video_id"]
        media_obj=models.MediaFileUpload.objects.get(id=int(video_id))
        result=result_utils.model_instance_result(media_obj,model_type)
        return result
    except:
        return None