from django.views import View
from django.shortcuts import render
import pandas as pd
import numpy as np

import json

class Network(View):

    def get(self, request):
        context = {"title": "View network", "network_view": True, "content_header": "View network"}
        return render(request, 'main/network_view.html', context)
