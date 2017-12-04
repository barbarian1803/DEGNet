from django.views import View
from django.shortcuts import render

import json

class DataUploader(View):

    def get(self, request):
        context = {"title": "Data uploader", "content": "This is content"}
        return render(request, 'main/uploader.html', context)