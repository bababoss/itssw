import requests,json,os,uuid
from django.conf import settings

def get_result(model_host,payload):
    """
    :param model_host:
    :param url_list:
    :param payload:
    :return:
    """
    #print("model url: ",model_host," payload: ",payload)
    headers = {'Content-type': 'application/json'}
    r = requests.post(model_host, data=json.dumps(payload), headers=headers)
    return r.json()

def download_file(url):

    """
    :param url: Input meadia file url
    :return: media file localpath
    """
    local_filename = url.split('/')[-1]
    uniqe_media_name = uuid.uuid4().hex
    local_filename_updated=uniqe_media_name+'.'+local_filename.split('.')[-1]
    save_file_path=os.path.join(settings.BASE_DIR,"media/uploaded_media/"+local_filename_updated)
    # NOTE the stream=True parameter
    if not os.path.exists(os.path.join(settings.BASE_DIR,"media/uploaded_media/")):
        os.makedirs(os.path.join(settings.BASE_DIR,"media/uploaded_media/"), exist_ok=True)
    r = requests.get(url, stream=True)
    with open(save_file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian

    return "media/uploaded_media/"+local_filename_updated
