from django.views import View
from django.shortcuts import render

from .dir_views.index_view import *
from .dir_views.network_view import *
from .dir_views.data_uploader import *
from .dir_views.network_uploader import *
from .dir_views.gene_conversion import *
from .dir_views.auth_util import *
from .dir_views.login_view import *
from .dir_views.create_account_view import *
from .dir_views.network_api import *