from django.conf.urls import url

from .views import *

app_name = 'main'

urlpatterns = [
    url('network_view', Network.as_view(), name='network_view'),
    url('data_uploader', DataUploader.as_view(), name='data_uploader'),
    url('network_uploader', NetworkUploader.as_view(), name='network_uploader'),
    url('gene_conversion', GeneConversion.as_view(), name='gene_conversion'),
    url('anon_auth', anon_auth, name='anon_auth'),
    url('logout', logout_auth, name='logout'),
    url('login', Login.as_view(), name='login'),
    url('create_account', CreateAccount.as_view(), name='create_account'),
    url('api/get_network', get_network_json, name='get_network_api'),
    url('api/get_avail_network', get_avail_network_json, name='get_avail_network_api'),

    url('', Index.as_view(), name='index'),
]