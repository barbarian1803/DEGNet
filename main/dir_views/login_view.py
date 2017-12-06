from django.views import View
from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.urls import reverse

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    password = forms.CharField(label="Email", max_length=255,
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class Login(View):
    context = {"title": "Login Page"}
    context["form"] = LoginForm()

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:index"))

        return render(request, "main/login_form.html", self.context)

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:index"))

        username = request.POST["username"]
        password = request.POST["password"]


        u = authenticate(username=username, password=password)

        if u is not None:
            login(request, u)
            request.session["temp_name"] = username

            return HttpResponseRedirect(reverse("main:index"))

        else:
            self.context["result"] = "error"
            self.context["message"] = "Login failed, please try again"

            return render(request, "main/login_form.html", self.context)

