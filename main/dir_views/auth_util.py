from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.conf import settings
import os

def anon_auth(request):
    user = authenticate(username="anon123", password="anon123")
    random_str = get_random_string(length=10)
    request.session["temp_name"] = random_str
    login(request, user)

    if not os.path.exists("user_dir/" + random_str):
        basepath = settings.BASE_DIR + "/user_dir/" + random_str
        os.makedirs(basepath)
        os.makedirs(basepath + "/network")
        os.makedirs(basepath + "/deg_file")
        os.makedirs(basepath + "/result")

    return HttpResponseRedirect(reverse("main:index"))

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:index"))