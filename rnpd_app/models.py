from django.db import models
import datetime
# Create your models here.


class Usr(models.Model):
    name=models.CharField(max_length=222,blank=True,null=True)
    email=models.EmailField(primary_key=True)
    contact=models.CharField(max_length=222,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name','email','contact','created')
        verbose_name_plural = 'User'
        ordering = ['created']

    def __str__(self):
        return 'user_email: %s ' % (self.email)

        

        
class MediaFileUpload(models.Model):
    VIDEO = 'VIDEO'
    AUDIO='AUDIO'
    IMAGE='IMAGE'
    OTHER='OTHER'

    file_typeChoices = (
        (VIDEO, 'VIDEO'),
        (AUDIO, 'AUDIO'),
        (IMAGE, 'IMAGE'),
        (OTHER, 'OTHER'),

    )
    usr = models.ForeignKey(Usr, related_name='uploaded_media_usr', on_delete=models.CASCADE,default=1)
    media_file=models.FileField(upload_to='uploaded_media',blank=True,null=True)
    plate_object=models.TextField(blank=True,null=True)
    number_plate_text=models.CharField(max_length=222,blank=True,null=True)
    file_type= models.CharField(
        max_length=25,
        choices=file_typeChoices,
        default=OTHER,
    )
    #url_list = models.TextField(blank=True,null=True)
    #result=models.TextField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = 'Uploaded media file history'
        verbose_name_plural = 'Uploaded media file history'
        ordering = ['created']

    def __str__(self):
        return 'media_file:  %s ' % (self.media_file)


        

