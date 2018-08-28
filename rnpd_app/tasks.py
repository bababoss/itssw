
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.conf import settings

import time, os
from celery.task.control import inspect


########################## import   Model #################################
from rnpd_app import models
######################### import serializers ###########################
from rnpd_app import serializers

from celery import shared_task
from rnpd.celery import app
from django.core.exceptions import ObjectDoesNotExist
from utilities import redis_broker
from rnpd_app import common_view
from utilities import db_obj_utils,redis_broker
from celery.exceptions import SoftTimeLimitExceeded

#REDIS GLOBLE CONNECTION
REDIS=redis_broker.RedisBroker()# Start redis broker
REDIS_CONN=REDIS.get_redis_connection()#redis connection

#TASK_LIST=['rnpd_app.tasks.scene_recognition_model',]



def send_mail(email,video_id,result):
    
    subject="RNPD API Result"
    message="<h1>RNPD API Result</h1></br><h2>Result for media_id: " +str(video_id)+"<h2></br>"+str(result)
    email_obj = EmailMessage(subject, message, "visionrival.ai@gmail.com",
                         [email,])
    email_obj.content_subtype = "html"
    res = email_obj.send()


            
@app.task
def rnpd_task_image_input(ids,email):
    print("rnpd_model_image")
    media_obj =db_obj_utils.media_object(ids,email)
    result=common_view.number_plate_recognizer_image_input(media_obj)
    send_mail(email,ids,result)
    return result
    
@app.task
def rnpd_task_video_input(ids,email):
    print("rnpd_model_video")
    media_obj =db_obj_utils.media_object(ids,email)
    result=common_view.number_plate_recognizer_video_input(media_obj)
    send_mail(email,ids,result)
    return result

    





