from django.views import View
from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User

class CreateAccountForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    firstname = forms.CharField(label="First name", required=False, max_length=255,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))

    lastname = forms.CharField(label="Last name", required=False, max_length=255,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    email = forms.CharField(label="Email", max_length=255,
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    password = forms.CharField(label="Email", max_length=255,
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    password2 = forms.CharField(label="Email", max_length=255,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))



class CreateAccount(View):

    context = {"title": "Create Account"}
    context["form"] = CreateAccountForm()

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:index"))

        return render(request, "main/create_account_form.html", self.context)

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("main:index"))

        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        try:
            u = User.objects.get(username=username)

            self.context["result"] = "error"
            self.context["message"] = "Create account failed, email is already registered!"

        except User.DoesNotExist:

            if not password == password2:
                self.context["result"] = "error"
                self.context["message"] = "Create account failed, password doesn't match!"
            else:
                newuser = User()
                newuser.username = username
                newuser.first_name = firstname
                newuser.last_name = lastname
                newuser.set_password(password)
                newuser.email = email
                newuser.save()
                self.context["result"] = "success"
                self.context["message"] = "User successfully created, please login"

        return render(request, "main/create_account_form.html", self.context)