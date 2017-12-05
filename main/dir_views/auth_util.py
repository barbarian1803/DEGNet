from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.crypto import get_random_string

def anon_auth(request):
    user = authenticate(username="anon123", password="anon123")
    request.session["temp_name"] = get_random_string(length=10)
    login(request, user)

    return HttpResponseRedirect(reverse("main:index"))

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:index"))