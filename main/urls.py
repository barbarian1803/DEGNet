from django.conf.urls import url

from .views import *

app_name = 'main'

urlpatterns = [
    url('network_view', Network.as_view(), name='network_view'),
    url('data_uploader', DataUploader.as_view(), name='data_uploader'),
    url('', Index.as_view(), name='index'),
]