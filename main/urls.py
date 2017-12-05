from django.conf.urls import url

from .views import *

app_name = 'main'

urlpatterns = [
    url('network_view', Network.as_view(), name='network_view'),
    url('data_uploader', DataUploader.as_view(), name='data_uploader'),
    url('gene_conversion', GeneConversion.as_view(), name='gene_conversion'),
    url('login', GeneConversion.as_view(), name='login'),
    url('login', Index.as_view(), name='login'),
    url('create_account', Index.as_view(), name='create_account'),
    url('', Index.as_view(), name='index'),
]