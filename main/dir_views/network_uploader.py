from django.views import View
from django.shortcuts import render
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from network_analysis.lib.CSV2Cyjs import csv2cyjs
import os
from network_analysis.lib.CSV2Cyjs import *


class NetworkFileForm(forms.Form):
    name = forms.CharField(label="Network name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'network name'}))
    desc = forms.CharField(label="Network description", max_length=255,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'network description'}))
    YESNO = (('yes', 'Yes',), ('no', 'No',))
    yesno = forms.ChoiceField(label="Use header", choices=YESNO, widget=forms.Select(attrs={'class': 'form-control'}))

    CHOICES = (('\t', 'tab',), (';', ';',), (',', ',',), (' ', 'space',))
    delim = forms.ChoiceField(label="CSV delimiter", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    uploader = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'fileselector'}))

    def is_valid(self):
        return True


@method_decorator(login_required, name='dispatch')
class NetworkUploader(View):
    context = {
        "title": "Network Uploader ",
        "content_header": "Upload custom network data",
        "upload_network": True, "analysis": True
    }

    def write_pos_file(self, folder_name, file_name, request):
        from django.utils.crypto import get_random_string
        from subprocess import call
        import os

        cyjs_json = csv2cyjs(file_name, "")
        output = file_name.replace(".csv", "_pos.csv")

        # generate js script to generate network pos file
        script_tpl = open(settings.SCRIPT_ROOT+"/cytoscapeheadless.js", "r").read()
        script_tpl = script_tpl.replace("{{json_data}}", cyjs_json)
        script_tpl = script_tpl.replace("{{output_file}}", output)

        script_file_name = settings.SCRIPT_ROOT+"/"+get_random_string(length=10)+".js"
        script_file = open(script_file_name, "w")
        script_file.write(script_tpl)
        script_file.close()

        call(["node", script_file_name])
        os.remove(script_file_name)

        return output.replace(folder_name, "")

    def handle_uploaded_file(self, request, f, post_data):
        post_data = post_data.copy()
        folder_name = settings.BASE_DIR + "/user_dir/"+request.session["temp_name"]+"/network/"

        if f.content_type != "text/csv":
            return False

        file_name = folder_name+f.name

        fout = open(file_name, "wb")
        for chunk in f.chunks():
            fout.write(chunk)
        fout.close()

        pos_file = self.write_pos_file(folder_name, file_name, request)

        # write network metadata here
        user_networks = []
        usr_metadata = settings.BASE_DIR + "/user_dir/" + request.session["temp_name"] + "/network/metadata.json"
        metadata_user = None

        if os.path.isfile(usr_metadata):
            metadata_user = open(usr_metadata, "r")
            user_networks = json.loads(metadata_user.read())["networks"]
            metadata_user.close()

        new_data = [{
            "id": post_data["name"].lower().replace(" ", "_"),
            "name": post_data["name"],
            "main_file": f.name,
            "pos_file": pos_file,
            "desc": post_data["desc"],
            "type": "user"
        }]

        metadata_user = open(usr_metadata, "w")
        user_networks = user_networks + new_data
        metadata_user.write(json.dumps({"networks": user_networks}))
        metadata_user.close()

        return True

    def get(self, request):
        form = NetworkFileForm()
        self.context["form"] = form
        self.context["result"] = None
        return render(request, 'main/network_uploader.html', self.context)

    def post(self, request):

        form = NetworkFileForm(request.POST, request.FILES)
        self.context["form"] = form
        fobj = request.FILES['uploader']

        upload_result = self.handle_uploaded_file(request, fobj, request.POST)

        if form.is_valid():
            if upload_result:
                self.context["message"] = ""
                self.context["result"] = "success"
            else:
                self.context["message"] = "File is not csv."
                self.context["result"] = "fail"
        else:
            self.context["message"] = "Form is not valid."
            self.context["result"] = "fail"

        return render(request, 'main/network_uploader.html', self.context)