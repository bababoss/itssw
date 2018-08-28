"""
@Copyright : Cogknit Semantics pvt limited
@Author :    Suresh Saini
@Email  :    suresh@cogknit.com
@Date    :   12th June 2018
"""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from webvtt import WebVTT, Caption
import json,requests,os,sys,uuid,time
from utilities import audio_spliter ,request_utils, video_decomposer,media_metadata,result_utils,db_obj_utils
from rnpd_app import scene,object_detector,face,speech,tasks

########################## import   Model #################################
from rnpd_app import models,tasks
######################### import serializers ###########################
from rnpd_app import serializers

def jsonify_data(data):
    json_acceptable_string = []
    for i in data:
        d_data={}
        d_data["result"]=json.loads(i['result'].replace("'", "\""))
        d_data["model_type"]=i['model_type'].replace("'", "\"")
        #d_data["id"]=i['id']
        json_acceptable_string.append(d_data)
        
    return json_acceptable_string

def json_to_vtt(data,SAVE_PATH):
    webvtt = WebVTT()
    for i in range(len(data)):
        s_sec = str(data[i]["start_time"])
        e_sec = str(data[i]["end_time"])
        st = time.strftime('%H:%M:%S', time.gmtime(float(s_sec)))
        start_time = st + '.' + s_sec.split('.')[-1] + '000'
        et = time.strftime('%H:%M:%S', time.gmtime(float(e_sec)))
        end_time = et + '.' + e_sec.split('.')[-1] + '000'

        text=data[i]["text"]
        caption = Caption(
            start_time,
            end_time,
            text
        )
        webvtt.captions.append(caption)

    if (os.path.exists(SAVE_PATH)):
        pass
    else:
        webvtt.save(SAVE_PATH)
    print(SAVE_PATH)
    return webvtt

def tagit(media_obj):
    try:
        process_dict={}
        model_result=models.MidasResult.objects.get(mediafile=media_obj,model_type="object_detection")
        frames=[]
        if model_result:
            serializer_data=serializers.DemoSerializer(model_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            totalItemsDetected=0
            totalDetetctionFrames=0
            for k in p_data.values():
                for j in k["detections"]:
                    frame_dict={}
                    frame_dict["frame_no"]=j["frame_no"]
                    frame_dict["time_code"]=j["time_code"]
                    objects=[]
                    totalDetetctionFrames+=1
                    for y in j["objects"]:
                        object_dict={}
                        object_dict["y_position"]=float(y["y_position"])
                        object_dict["x_position"]=float(y["x_position"])
                        object_dict["width"]=float(y["width"])
                        object_dict["class"]=y["class"]
                        object_dict["height"]=float(y["height"])
                        object_dict["confidence"]=float(y["score"])
                        objects.append(object_dict)
                        totalItemsDetected+=1
                    frame_dict["objects"]=objects 
                    frames.append(frame_dict)
            process_dict["frames"]=frames
            process_dict["totalItemsDetected"]=totalItemsDetected
            process_dict["totalDetetctionFrames"]=totalDetetctionFrames
            return process_dict
        else:
            return process_dict
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return process_dict
    
def clapboard(media_obj):
    try:
        process_dict={}
        model_result=models.MidasResult.objects.get(mediafile=media_obj,model_type="scene_recognition")
        scenes=[]
        if model_result:
            serializer_data=serializers.DemoSerializer(model_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            process_dict["totalScenesDetected"]=len(p_data)
            
            for k in p_data.values():
                sc_data={}
                tags=[]
                sc_data["end_time"]=k["end_time"]
                sc_data["start_time"]=float(k["start_time"])
                sc_data["start_frame"]=float(k["start_frame"])
                sc_data["end_frame"]=k["end_frame"]
                for j in k["detections"]:
                    tags_dict={}
                    tags_dict["frame_no"]=j["frame_no"]
                    tags_dict["time_code"]=j["time_code"]
                    tags_dict["scene_type"]=j["tags"]["scene_type"]
                    tags_dict["confidence"]=j["tags"]["confidence"]
                    tags.append(tags_dict)
                sc_data["tags"]=tags
                scenes.append(sc_data)
            process_dict["scenes"]=scenes
            return process_dict
        else:
            return process_dict
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return process_dict
def  visage(media_obj):
    try:
        process_dict={}
        gender_result=models.MidasResult.objects.get(mediafile=media_obj,model_type="demographics_gender")
        age_result=models.MidasResult.objects.get(mediafile=media_obj,model_type="demographics_age")
        if gender_result:
            gender_serializer_data=serializers.DemoSerializer(gender_result)
            age_serializer_data=serializers.DemoSerializer(age_result)
            gender_metadata=gender_serializer_data.data
            age_metadata=age_serializer_data.data
            gender_data=json.loads(gender_metadata["result"].replace("'", "\"")).values()
            age_data=json.loads(age_metadata["result"].replace("'", "\"")).values()
            temp=list(gender_data)
            
            for i in range(len(gender_data)):
                #print(list(temp)[i]["detections"])
                for j in range(len(temp[i]["detections"])):
                    for k in range(len(list(gender_data)[i]["detections"][j]["face"])):
                        try:
                            temp[i]["detections"][j]["face"][k]["age"]=list(age_data)[i]["detections"][j]["face"][k]["age"]
                        except:
                            print("Exception:hjgdhagsdhadghadhahj ")
            frames=[]
            totalFacesDetected=0
            totalDetectionFrames=0
            for x in temp:
                for y in x["detections"]:    
                    frame_dict={}
                    if y["face"]: 
                        totalFacesDetected+=1
                        frame_dict["time_code"]=y["time_code"]
                        frame_dict["frame_no"]=y["frame_no"]
                        frame_dict["face"]=y["face"]
                        for z in range(len(y["face"])):
                            frame_dict["face"][z]["confidence"]=float(y["face"][z]["confidence"])
                        frames.append(frame_dict)
                    totalDetectionFrames+=1
                

            process_dict["totalFacesDetected"]=totalFacesDetected
            process_dict["totalDetectionFrames"]=totalDetectionFrames
            process_dict["frames"]=frames
            return process_dict
        else:
            return process_dict
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return process_dict
def audition(media_obj):
    try:
        process_dict={}
        model_result=models.MidasResult.objects.get(mediafile=media_obj,model_type="face_recognition")
        if model_result:
            serializer_data=serializers.DemoSerializer(model_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            process_dict["frames"]=p_data.values()
            {'frame_no': 20, 'time_code': '00:00:00:20', 'face_name': [{'height': 0.10078125, 'width': 0.17916666666666667, 'x_position': 0.5305555555555556, 'y_position': 0.04140625, 'real_name': 'Michael_Scofield', 'reel_name': 'NA'}]}
            frames=[]
            totalPeopleDetected=0
            totalDetectionFrames=0
            for x in p_data.values():
                for y in x["detections"]:
                    frame_dict={}
                    people=[]
                    print("yyyyyyyyyy: ",y,type(y))
                                       

                    if isinstance(y["face_name"],dict):
                        if y["face_name"] != "NA" and y["face_name"]["real_name"]  != "NA":
                            coordinates={}
                            character={}
                            personality={}
                            face_dict={}
                            frame_dict["time_code"]=y["time_code"]
                            frame_dict["frame_no"]=y["frame_no"]
                            character["name"]=y["face_name"]["real_name"]
                            face_dict["character"]=character
                            face_dict["personality"]=personality
                            face_dict["coordinates"]=coordinates
                            people.append(face_dict)
                            frame_dict["people"]=people
                            frames.append(frame_dict)
                            totalPeopleDetected+=1
                        
                    if isinstance(y["face_name"],list):
                        face_list=[]
                        

                        for z in y["face_name"]:
                            if z["real_name"]  != "NA":
                                frame_dict["time_code"]=y["time_code"]
                                frame_dict["frame_no"]=y["frame_no"]
                                coordinates={}
                                character={}
                                personality={}
                                face_dict={}
                                coordinates["x_position"]=z["x_position"]
                                coordinates["y_position"]=z["y_position"]
                                coordinates["height"]=z["height"]
                                coordinates["width"]=z["width"]
                                character["name"]=z["real_name"]
                                face_dict["character"]=character
                                face_dict["personality"]=personality
                                face_dict["coordinates"]=coordinates
                                people.append(face_dict)
                                frame_dict["people"]=people
                                totalPeopleDetected+=1
                            if frame_dict:
                                frames.append(frame_dict)
                                
                            
                    totalDetectionFrames+=1
            process_dict["frames"]=frames
            process_dict["totalDetectionFrames"]=totalDetectionFrames
            process_dict["totalPeopleDetected"]=totalDetectionFrames
            return process_dict
        else:
            return process_dict
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return process_dict
def silence(media_obj):
    try:
        process_dict={}
        label_result=models.MidasResult.objects.get(mediafile=media_obj,model_type="non_speech_labeling")
        speaker_result=models.MidasResult.objects.get(mediafile=media_obj,model_type__icontains="speaker_identification")
        asr_result=models.MidasResult.objects.get(mediafile=media_obj,model_type__icontains="asr")
        s_data=[]
        asr_data=[]
        if label_result:
            serializer_data=serializers.DemoSerializer(label_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            process_dict["nonSpeech"]=p_data["segments"]

        if asr_result:
            serializer_data=serializers.DemoSerializer(asr_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            asr_data=p_data["segments"]
            
        if speaker_result:
            serializer_data=serializers.DemoSerializer(speaker_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            s_data=p_data["segments"]
        temp=s_data
        for k in range(len(s_data)):
            temp[k]["text"]=asr_data[k]["text"]
            temp[k]["start_time"]=float(temp[k]["start_time"])
            temp[k]["end_time"]=float(temp[k]["end_time"])
        process_dict["speech"]=s_data
        return process_dict
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return process_dict

def caption(media_obj):
    try:
        process_dict={}
        model_result=models.MidasResult.objects.get(mediafile=media_obj,model_type__icontains="asr")
        if model_result:
            serializer_data=serializers.DemoSerializer(model_result)
            metadata=serializer_data.data
            p_data=json.loads(metadata["result"].replace("'", "\""))
            process_dict["captions"]=p_data["segments"]
            json_to_vtt(p_data["segments"],
                    os.path.join(settings.BASE_DIR,
                                 "media/vtt/"+str(media_obj.audio_file).split(".")[0].split("/")[-1]+".vtt"))
            process_dict["vttUrl"]=settings.BASE_URL["api_gateway_url"]+"media/vtt/"+str(media_obj.audio_file).split(".")[0].split("/")[-1]+".vtt"
            return process_dict
        else:
            return process_dict
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return process_dict


    
def get_meta_data(media_obj):
    final_result={}
    media={"video_id":media_obj.id,
        "video_url":settings.BASE_URL['api_gateway_url']+str(media_obj.media_file),
        "audio_url":settings.BASE_URL['api_gateway_url']+str(media_obj.audio_file),
        "duration":float(media_obj.duration),
        "language":str(media_obj.language)}
    
    models={
        "clapboard":clapboard(media_obj),
        "tagit":tagit(media_obj),
        "visage":visage(media_obj),
        "audition":audition(media_obj),
        "silence":silence(media_obj),
        "caption":caption(media_obj)
        
    }
    final_result={"media":media,
                "models":models}
    #print("final_result",final_result)
    return final_result
    
           
           
    
      
    
    
    
                
            
            
