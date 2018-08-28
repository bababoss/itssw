from django.contrib import admin

from rnpd_app import models

admin.site.site_header = "   RNPD Administration ";
admin.site.site_title = "VisionRival RNPD Api ";



@admin.register(models.MediaFileUpload)
class UploadMediaAdmin(admin.ModelAdmin):
    list_display = ['usr', 'plate_object','number_plate_text','created']
    list_filter = ('usr',)
    fields = [('usr','media_file','plate_object','number_plate_text',)]


admin.site.register(models.Usr)

# Register your models here.
