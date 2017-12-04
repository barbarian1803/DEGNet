from django.views import View
from django.shortcuts import render

import json

class Network(View):

    def get(self, request):
        context = {"title": "This is the title", "content": "This is content"}
        return render(request, 'main/base.html', context)
