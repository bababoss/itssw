from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from os import listdir
from os.path import isfile, join
import re
from subprocess import Popen, PIPE
import math, sys
import os, json, glob, sys
import time, datetime
from django.conf import settings




def getAudioMaster(video_dir, formate='.wav'):
    paths = glob.glob(video_dir + '/*.mp4')
    total_time = 0.0
    audioPathList = []
    if isinstance(paths, list):
        for path in paths:
            try:
                file_path = path.split(".")[0]
                filename = os.path.split(path)[-1].split('.')[0]
                root = os.path.split(os.path.split(path)[0])
                audio_root_path = os.path.join(root[0], "audio")
                os.makedirs(audio_root_path)
                # python3
                # os.makedirs(audio_root_path,exist_ok=True)
                audioPath = audio_root_path + '/' + filename + '.' + formate
                print("audioPath audio_spliter",audioPath)
                if not os.path.exists(audioPath):
                    process = Popen(
                        ['ffmpeg', '-i', path, '-f', 'wav', '-ab', '1024000', '-ar', '16000', '-vn', '-ac', '1',
                         audioPath], stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                    print("Audio created")
                    audioPathList.append(audioPath)

            except Exception as e:
                print(print(sys.exc_info()))

        return audioPathList


def getAudio(video_path, formate='.wav'):
    try:

        
        
        file_name=video_path.split('/')[-1].split('.')[-2]
        print("file_anm")
        audioPath = os.path.join(settings.BASE_DIR ,'media/audio_output',file_name+formate)
        os.makedirs( os.path.join(settings.BASE_DIR ,'media/audio_output'),exist_ok=True)
        print("audioPath in spliter: ",audioPath)
        vid_path=os.path.join(settings.BASE_DIR,video_path)
        print(vid_path)
        if not os.path.exists(audioPath):
            process = Popen(
                ['ffmpeg', '-i',vid_path, '-f', 'wav', '-ab', '1024000', '-ar', '16000', '-vn', '-ac', '1',
                 audioPath], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print("Audio created")

        return os.path.join('media/audio_output',file_name+formate)
    except OSError as err:
        print(print(sys.exc_info()))
    return None


def generate_Audio_dataset(video_path, audio_folder, formate='wav'):
    try:
        for file in os.listdir(video_path):
            print(file)
            if file.endswith(".mp4"):
                filename = (str(file)).split('.')[0]
                audioPath = audio_folder + '/001/' + filename + '.' + formate
                videopath = video_path + "/" + str(file)
                if not os.path.exists(audio_folder + "/001"):
                    os.makedirs(audio_folder + "/001")
                if os.path.isfile(audioPath):
                    os.unlink(audioPath)
                process = Popen(
                    ['ffmpeg', '-i', videopath, '-f', 'wav', '-ab', '1024000', '-ar', '48000', '-vn', '-ac', '1',
                     audioPath], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                print("Audio created")
                return audioPath
    except OSError as err:
        print(print(sys.exc_info()))
    return None


if __name__ == "__main__":
    src_dir = sys.argv[1]
    getAudioMaster(src_dir)

