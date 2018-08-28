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
from django.core.exceptions import ObjectDoesNotExist

###############################TRest framework #########################
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import FileUploadParser, MultiPartParser,JSONParser

########################## import   Model #################################
from rnpd_app import models,tasks
from utilities import request_utils,media_metadata,result_utils,db_obj_utils,midas_log
from utilities import video_decomposer
######################### import serializers ###########################
from rnpd_app import serializers

##################Utiliyties#############################################
import json,requests,os,sys,uuid,time,psutil
from PIL import Image

from object_detection import inference as bbx
from TextSpotting import inference as get_text

import logmatic
import logging,socket
LOGGER = logging.getLogger('rnpd')
LOGGER.setLevel(logging.INFO)
HANDLER= logging.handlers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSE = {'success': True,
        'response': "otp sent successfully"}
BEDRESPONSE = json.dumps({'success': False,
        'response': "something went worng"})
def jsonify_data(data):
    json_acceptable_string = []
    for i in data:
        d_data={}
        d_data["result"]=json.loads(i['result'].replace("'", "\""))
        d_data["model_type"]=i['model_type'].replace("'", "\"")
        #d_data["id"]=i['id']
        json_acceptable_string.append(d_data)
        
    return json_acceptable_string

def number_plate_recognizer_video_input(media_obj):
    vid_path=os.path.join(settings.BASE_DIR,str(media_obj.media_file))
    print("vid_path: ",vid_path)
    vid = video_decomposer.VideoObject(vid_path)
    fps=vid.fps
    totalframe=vid.length
    vid_duration=totalframe/fps
    final_result={}
    start_time=time.time() # for log
    frame_process_time=''
    processed_frame=0

    frame=[1,int(totalframe)-2]
    print("farame------: ",frame)
    print("totalframe---------- :",totalframe)
    print("vid_duration---------- :",vid_duration)
    detections=[]
    number_plate_path=[]
    for frm_no in range(1,int(totalframe)-2):
        plate={}
        if frm_no%20==0:

            start_time1=time.time() # for log
            fram_img = list(vid.pull_frames([frm_no]))
            print("number fraem: ",len(fram_img))
            detect_dict={}
            input_image = Image.fromarray(fram_img[0])
            file_name=str(media_obj.media_file).split('/')[-1].split('.')[0]
            temp_save_image="/home/gpu-machine/projects/rnpd/media/temp_save/"+file_name+".jpg"
            input_image.save(temp_save_image)
            text=bbx.get_rnpd(temp_save_image)
            cropped_image = input_image.crop((int(text[0]), int(text[2]), int(text[1]), int(text[3])))
            crop_save_path="/home/gpu-machine/projects/rnpd/media/result_media/"+os.path.split(temp_save_image)[-1]
            print("crop_save_path:-----",crop_save_path)
            weights_path="TextSpotting/model_rnpd/rnpd_2018-07-07-19-40-00.ckpt-48535"
            cropped_image.save(crop_save_path)
            plate["detected_path"]="media/result_media/"+os.path.split(temp_save_image)[-1]
            plate["bounding_box"]=[int(text[0]), int(text[2]), int(text[1]), int(text[3])]
            number_plate_path.append(plate)
            p_data=get_text.recognize(image_path=crop_save_path, weights_path=os.path.join(settings.BASE_DIR,weights_path))
#             os.remove(temp_save_image)
#             os.remove(save_path)
            time_sec=(frm_no*vid_duration)/totalframe
            time_code=time.strftime('%H:%M:%S', time.gmtime(time_sec))
#             detect_dict["time_code"]=time_code+':'+str(frm_no)
#             detect_dict["frame_no"]=frm_no
            detect_dict["number_plate_text"]=p_data
            detections.append(detect_dict)
            end_time1=time.time() # for log
            frame_process_time=str(end_time1-start_time1)
            processed_frame+=1
            print("frame process time: ",frame_process_time,"  frm_no: ",frm_no)
            break

    result_data={"recognition":detections}

    end_time=time.time() # for log
    process_time=str(end_time-start_time) 
    log_dict={'process_time':process_time,
              'frame_process_time':frame_process_time,
              'processed_frame':processed_frame,
              'video_id':str(media_obj.id),
              'video_duration':vid.length/vid.fps,
              'process_id':os.getpid(),
              'process_memory':psutil.Process(os.getpid()).memory_info()[0] / float(2 ** 20)
             }
    # log activity
    print("log_dict",log_dict)
    logHandler=midas_log.access_log(LOGGER,HANDLER,'logs/access-log/rnpd.log',log_data=log_dict)
    LOGGER.addHandler(logHandler)
    LOGGER.info(logHandler)
    

    media_obj.number_plate_text=result_data['recognition']
    media_obj.plate_object={"detected_plate":number_plate_path}
    media_obj.save()

    return result_data



def number_plate_recognizer_image_input(media_obj):
    im_path=os.path.join(settings.BASE_DIR,str(media_obj.media_file))
    text=bbx.get_rnpd(im_path)
    input_image = Image.open(os.path.join(settings.BASE_DIR,str(media_obj.media_file)))
    cropped_image = input_image.crop((int(text[0]), int(text[2]), int(text[1]), int(text[3])))
    save_path="/home/gpu-machine/projects/rnpd/media/result_media/"+os.path.split(im_path)[-1]
    print(save_path)
    weights_path="TextSpotting/model_rnpd/rnpd_2018-07-07-19-40-00.ckpt-48535"
    cropped_image.save(save_path)
    p_data=get_text.recognize(image_path=save_path, weights_path=os.path.join(settings.BASE_DIR,weights_path))
    number_plate=[{"bounding_box":[int(text[0]), int(text[2]), int(text[1]), int(text[3])],"detected_path":"media/result_media/"+os.path.split(im_path)[-1]}]
    result_data={"recognition":p_data}
    media_obj.number_plate_text={"number_plate_text":result_data["recognition"]}
    media_obj.plate_object={"detected_plate":number_plate}
    media_obj.save()
    return result_data

def result_data_processing(serializer_data):
    f_result=serializer_data
    f_result["media_url"]=settings.BASE_URL["api_gateway_url"]+serializer_data["media_file"]
    print("serializer_data[""]",serializer_data["plate_object"])
    if serializer_data["plate_object"]:
        coord=json.loads(serializer_data["plate_object"].replace("'", "\""))["detected_plate"]
        if coord:
            coord[0]["detected_path"]=settings.BASE_URL["api_gateway_url"]+coord[0]["detected_path"]
            f_result["plate_metadata"]=coord
        else:
            f_result["plate_metadata"]=[]
    else:
         f_result["plate_metadata"]=[]
         
    #f_result["number_plate_text"]=json.loads(serializer_data["number_plate_text"].replace("'", "\""))["number_plate_text"]
    
    del f_result['plate_object']
    del f_result['media_file']
    return f_result

class UploadMedia(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    parser_classes = (JSONParser,MultiPartParser,)

        
    def post(self, request, format=None):
        try:
            #email = request.query_params["email"]
            email = request.data["email"]
            media_file = request.data['media_file']
            print("media_file-----------: ",media_file)
        except:
            email=None
            media_file=None

        if email and media_file:
            usr=db_obj_utils.user_object(email)
            if  'http' in media_file:
                print("media_file: ",media_file)
                media_file_path=request_utils.download_file(media_file)
                media_obj = models.MediaFileUpload.objects.create(
                    usr=usr,
                    media_file=media_file_path,

                )
                #run_all_model(media_obj,email,language_type=language_type)
                RESPONSE = {"success": True,
                            "response":{"video_id":str(media_obj.id),"message":""} }
                return Response(RESPONSE,status=status.HTTP_200_OK)
            
            
            else:
                print("ffssf=====",str(media_file).split('.')[-1])
                if str(media_file).split('.')[-1] in ["jpg","jpeg","png"]:
                    media_obj=media_metadata.save_media_image(media_file,usr)['db_obj']
                    r=tasks.rnpd_task_image_input.apply_async((int(media_obj.id),email,),
                                  retry=False, queue="rnpd_q")
                    print("rnpd result ")
                    msg="Media uploded successfully ,Get mail soon"
                    RESPONSE = {"success": True,
                                "response":{"media_id":str(media_obj.id),"message":msg}}
                    return Response(RESPONSE,status=status.HTTP_200_OK)
                else:
                    media_obj=media_metadata.save_media(media_file,usr)['db_obj']
                    r=tasks.rnpd_task_video_input.apply_async((int(media_obj.id),email,),
                                  retry=False, queue="rnpd_q")
                    print("check-3: face_recognition")
                    msg="Media uploded successfully ,Get mail soon"
                    RESPONSE = {"success": True,
                                "response":{"media_id":str(media_obj.id),"message":msg}}
                    return Response(RESPONSE,status=status.HTTP_200_OK)
        RESPONSE = {"success": False,
                    "response":"Not found" }
        return Response() 

class RnprMediaUpload(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    parser_classes = (JSONParser,MultiPartParser,)

        
    def post(self, request, format=None):
        try:
            #email = request.query_params["email"]
            email = request.data["email"]
            media_file = request.data['media_file']
            print("media_file-----------: ",media_file)
        except:
            email=None
            media_file=None

        print("email RnprMediaUpload : ",email)
        if email and media_file:
            usr=db_obj_utils.user_object(email)
            if  'http' in media_file:
                print("media_file: ",media_file)
                media_file_path=request_utils.download_file(media_file)
                media_obj = models.MediaFileUpload.objects.create(
                    usr=usr,
                    media_file=media_file_path,

                )
                
                RESPONSE = {"success": True,
                            "response":{"video_id":str(media_obj.id),"message":""} }
                return Response(RESPONSE,status=status.HTTP_200_OK)
            
            
            else:
                print(usr.email)
                if str(media_file).split('.')[-1] in ["jpg","jpeg","png"]:
                    media_obj=media_metadata.save_media_image(media_file,usr)['db_obj']

                    res=number_plate_recognizer_image_input(media_obj)
                    serializer = serializers.MediaFileUploadSerializer(media_obj)
                    resl=result_data_processing(serializer.data)
                    print("result_data_processing(serializer.data)",resl)
                    RESPONSE = {'success': True,
                                'response': resl}
                    return Response(RESPONSE,status=status.HTTP_200_OK)
#                     RESPONSE = {"success": True,
#                                 "response":{"media_id":str(media_obj.id),"message":res}}
#                     return Response(RESPONSE,status=status.HTTP_200_OK)
                else:
                    media_obj=media_metadata.save_media(media_file,usr)['db_obj']
                    res=number_plate_recognizer_video_input(media_obj)

                    serializer = serializers.MediaFileUploadSerializer(media_obj)
                    resl=result_data_processing(serializer.data)
                    print("result_data_processing(serializer.data)",resl)
                    RESPONSE = {'success': True,
                                'response': resl}
                    return Response(RESPONSE,status=status.HTTP_200_OK)
                    
#                     msg="Media uploded successfully ,Get mail soon"
#                     RESPONSE = {"success": True,
#                                 "response":{"media_id":str(media_obj.id),"message":res}}
#                     return Response(RESPONSE,status=status.HTTP_200_OK)
        RESPONSE = {"success": False,
                    "response":"please send email and image file" }
        return Response() 
    

class RnpdResult(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, format=None):
#         try:
        media_id = request.query_params["media_id"]
        print("name: ", media_id, type(media_id))
        snippet =models.MediaFileUpload.objects.get(id=media_id)
        serializer = serializers.MediaFileUploadSerializer(snippet)
        RESPONSE = {'success': True,
                    'response': result_data_processing(serializer.data)}
        return Response(RESPONSE,status=status.HTTP_200_OK)
#         except:
#             RESPONSE = {'success': False,
#                         'response': "wait for processing"}
#             return Response(RESPONSE,status=status.HTTP_400_BAD_REQUEST)
        
class RnpdResultAll(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, format=None):
#         try:
        snippet =models.MediaFileUpload.objects.all().order_by("-created")[:10]
        serializer = serializers.MediaFileUploadSerializer(snippet,many=True)
        data=[result_data_processing(i) for i in serializer.data]
        RESPONSE = {'success': True,
                    'response': data}
        return Response(RESPONSE,status=status.HTTP_200_OK)
#         except:
#             RESPONSE = {'success': False,
#                         'response': "wait for processing"}
#             return Response(RESPONSE,status=status.HTTP_400_BAD_REQUEST)


