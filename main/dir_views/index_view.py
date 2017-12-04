from django.http.response import *
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import json

class Index(View):

    def get(self,request):
        context = {"title":"This is the title","content":"This is content"}
        return render(request,'main/base.html',context)