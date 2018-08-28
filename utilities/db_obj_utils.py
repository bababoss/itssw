from rnpd_app import models
from django.core.exceptions import ObjectDoesNotExist

def user_object(email):
    try:
        usr=models.Usr.objects.get(email=email)
        print("user_object:  ",usr.email)
        return usr
    except ObjectDoesNotExist as e:
        usr=models.Usr.objects.create(email=email)
        print("user_object Exception:  ",usr.email)
        return usr
    
def media_object(ids,email):
    try:
        media_obj=models.MediaFileUpload.objects.get(usr=user_object(email),id=int(ids))
        print("media_object: ",media_obj.id)
        return media_obj
    except ObjectDoesNotExist as e:
        print("Exception media_object: ",str(e))
        return None
    
    
