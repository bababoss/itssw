"""

# @Time    : 28/08/2018
# @Author  : Suresh Saini
# @Site    :https://github.com/bharatsush/
"""
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import HttpResponse,render
from django.utils import timezone
from django.conf import settings
from passlib.hash import django_pbkdf2_sha256 as handler
from django.core.mail import EmailMessage

################################TRest framework #########################
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import FileUploadParser, MultiPartParser,JSONParser

########################## import   Model #################################
from rnpd_app import models,tasks
######################### import serializers ###########################
from rnpd_app import serializers

##################Utiliyties#############################################
from PIL import Image
from io import BytesIO
import base64,time
import json,requests,os,sys,time,psutil
import logmatic
import logging,socket
from utilities import audio_spliter as spliter
from utilities import audio_spliter ,request_utils, video_decomposer,media_metadata,midas_log,result_utils,db_obj_utils

from django.core.exceptions import ObjectDoesNotExist

def video_callback(self, request,model_function, format=None):
    """
    :param request: request body will be MultiPartParser media file
    :param format:  media formate
    :return:  Return status of successfully processed and json response
    """
    try:
        #email = request.query_params["email"]
        email = request.data["email"]
        media_file = request.data['media_file']
    except:
        email=None
        media_file=None
    language_type="english"
    try:
        language_type = request.data['language_type']
    except:
        pass
    print("email: ",email)
    if email and media_file:
        usr=db_obj_utils.user_object(email)
        print(usr.email)
        media_obj=media_metadata.save_media(media_file,usr)['db_obj']
        media_obj.language=language_type
        media_obj.save()
        print("media_objmedia_objmedia_objmedia_obj: ",media_obj.media_file,"fsdfs ",int(media_obj.id))
        run_all_model(media_obj,email,language_type=language_type)
        RESPONSE = {"success": True,
                    "response":{"video_id":str(media_obj.id),"message":"Video uploaded successfully. You will get mail soon"} }
        return Response(RESPONSE,status=status.HTTP_200_OK)
    RESPONSE = {"success": False,
                "response":"Not found" }
    return Response()