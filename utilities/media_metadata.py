from rnpd_app import models
from django.conf import settings
import uuid,os,glob
import cv2
from subprocess import Popen, PIPE
from utilities import audio_spliter ,request_utils, video_decomposer

# save video and return video system path
def  run_save(media_upload_obj,media_input):
    uniqe_media_name = uuid.uuid4().hex
    original_media_name, media_type = media_input.name.split('.')[-2], media_input.name.split('.')[-1]
    video_path = os.path.join(settings.BASE_DIR, "media/uploaded_media/" + media_input.name)
    if media_type == 'h2649':
        final_path=os.path.join(settings.BASE_DIR, "media/uploaded_media/" + uniqe_media_name + '.' + 'mp4')
        process = Popen(
            ['ffmpeg', '-framerate','24','-i', video_path, '-c','copy',final_path], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        media_upload_obj.media_file = "media/uploaded_media/" + uniqe_media_name + '.' + 'mp4'
        media_upload_obj.save()
        os.remove(video_path)
    else:
        rename_path = os.path.join(settings.BASE_DIR, "media/uploaded_media/" + uniqe_media_name + '.' + media_type)
        os.rename(video_path, rename_path)
        media_upload_obj.media_file = "media/uploaded_media/" + uniqe_media_name + '.' + media_type
        media_upload_obj.save()
    print("media_upload_obj: save method, ",media_upload_obj.media_file)
    media_url=settings.BASE_URL['api_gateway_url']+"media/uploaded_media/" + uniqe_media_name + '.' + media_type
    return {"media_file":media_upload_obj.media_file,"db_obj":media_upload_obj,"media_url":media_url}

# save video and return video system path
def  run_save_image(media_upload_obj,media_input):
    uniqe_media_name = uuid.uuid4().hex
    original_media_name, media_type = media_input.name.split('.')[-2], media_input.name.split('.')[-1]
    video_path = os.path.join(settings.BASE_DIR, "media/uploaded_media/" + media_input.name)
    rename_path = os.path.join(settings.BASE_DIR, "media/uploaded_media/" + uniqe_media_name + '.' + media_type)
    os.rename(video_path, rename_path)
    media_upload_obj.media_file = "media/uploaded_media/" + uniqe_media_name + '.' + media_type
    media_upload_obj.save()
    print("media_upload_obj: save method, ",media_upload_obj.media_file)
    media_url=settings.BASE_URL['api_gateway_url']+"media/uploaded_media/" + uniqe_media_name + '.' + media_type
    return {"media_file":media_upload_obj.media_file,"db_obj":media_upload_obj,"media_url":media_url}

def save_media(media_input,usr=None):
    """

    :param media_input: media_file incoming from request body
    :return:  dict of media_file path and .MediaFileUpload model database object
    """
    with open(settings.BASE_DIR+'/media/uploaded_media/' + media_input.name, 'wb+') as destination:
        for chunk in media_input.chunks():
            destination.write(chunk)

    if usr:    
        media_upload_obj = models.MediaFileUpload.objects.create(
            usr=usr,
            media_file=media_input,
            file_type='VIDIO'
        )
        return run_save(media_upload_obj,media_input)
    else:
        usr=models.Usr.objects.get(email='suresh@cogknit.com')
        media_upload_obj = models.MediaFileUpload.objects.create(
            usr=usr,
            media_file=media_input,
            file_type='VIDIO'
        )
        return run_save(media_upload_obj,media_input)


    
def save_media_image(media_input,usr=None):
    """

    :param media_input: media_file incoming from request body
    :return:  dict of media_file path and .MediaFileUpload model database object
    """
    with open(settings.BASE_DIR+'/media/uploaded_media/' + media_input.name, 'wb+') as destination:
        for chunk in media_input.chunks():
            destination.write(chunk)

    if usr:    
        media_upload_obj = models.MediaFileUpload.objects.create(
            usr=usr,
            media_file=media_input,
            file_type='AUDIO'
        )
        return run_save_image(media_upload_obj,media_input)
    else:
        usr=models.Usr.objects.get(email='suresh@cogknit.com')
        media_upload_obj = models.MediaFileUpload.objects.create(
            usr=usr,
            media_file=media_input,
            file_type='AUDIO'
        )
        return run_save_image(media_upload_obj,media_input)
def get_frame_extractor(video_path,media_db_obj=None):
    """

    :param video_path:  video file path
    :param media_db_obj: MediaFileUpload model database object
    :return:
    """
    # Create frame from imput video
    dirname, filename = os.path.split(video_path)
    file_name=filename.split('.')[-2]
    decomposer_obj = video_decomposer.VideoObject(video_path)
    frame_lists = decomposer_obj.get_frames()
    frame_path = os.path.join(settings.BASE_DIR, 'media/uploaded_media_frames', file_name)
    count = 1
    os.makedirs(frame_path, exist_ok=True)
    frame_url_list=[]
    for i in frame_lists:
        image_path = "/{}_%d.jpg".format(file_name) % count
        cv2.imwrite(frame_path + image_path, i)
        frame_url = frame_path +image_path
        if media_db_obj:
            models.UploadedMediaFrames.objects.create(mediafile=media_db_obj, url=frame_url)
        frame_url_list.append(settings.BASE_URL['api_gateway_url']+'media/uploaded_media_frames/'+file_name+image_path)
        count += 1
        if count == 50:
            break
    print("frame_url_list")
    return frame_url_list
