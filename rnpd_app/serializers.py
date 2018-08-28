"""t
# @Time    : 28/08/2018
# @Author  : Suresh Saini
# @Site    :https://github.com/bharatsush/
"""
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from rnpd_app import models

class MediaFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MediaFileUpload
        fields=('id','media_file','number_plate_text','plate_object','created')
        
