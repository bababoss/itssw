"""t
@Copyright : Cogknit Semantics pvt limited
@Author :    Suresh Saini
@Date    :   6th April 2018
"""
from django.conf.urls import url
from rnpd_app import common_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[

    
       # Meta data
       #url(r'^api/v1/modeldetail', common_view.ModelMediaResultDetail.as_view(), name='ModelDetails'),
       
       url(r'^api/v1/rnpd', common_view.RnprMediaUpload.as_view(), name='RnprMediaUpload'),
       url(r'^api/v1/media/upload', common_view.UploadMedia.as_view(), name='UploadMedia'),
       url(r'^api/v1/result', common_view.RnpdResult.as_view(), name='RnpdResult'),
       url(r'^api/v1/allresult', common_view.RnpdResultAll.as_view(), name='RnpdResultAll'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)