from django.views import View
from django.shortcuts import render

import json

class Index(View):

    def get(self, request):
        context = {"content": "This is content"}
        return render(request, 'main/base.html', context)
