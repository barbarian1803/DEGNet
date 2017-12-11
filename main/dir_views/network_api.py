from network_analysis.lib.CSV2Cyjs import *
from django.http.response import HttpResponse
import json

def get_avail_network_json(request):
    username = request.session["temp_name"]
    networks = get_avail_network(username)
    jsondata = []
    for n in networks:
        jsondata.append({"id": n["id"], "name": n["name"]})

    return HttpResponse(json.dumps(jsondata), content_type="application/json")

def get_network_json(request):
    username = request.session["temp_name"]
    network_name = request.GET["network_name"]
    json_output = loadnetwork(username, network_name, False)
    return HttpResponse(json_output, content_type="application/json")