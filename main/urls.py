from django.conf.urls import url

from .views import *

app_name = 'polls'

urlpatterns = [
    url('', Index.as_view(), name='index'),
]