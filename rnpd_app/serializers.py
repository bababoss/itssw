"""t
@Copyright : VisionRival pvt limited
@Author :    Suresh Saini
@Date    :   6th April 2018
"""
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from rnpd_app import models

class MediaFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MediaFileUpload
        fields=('id','media_file','number_plate_text','plate_object','created')
        
