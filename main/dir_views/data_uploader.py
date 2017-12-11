from django.views import View
from django.shortcuts import render
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json

class DEGFileForm(forms.Form):
    dataset = forms.CharField(label="Dataset name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dataset1'}))

    gene = forms.CharField(label="Gene column name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gene    '}))

    lfc = forms.CharField(label="Log fold change column name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'log2FoldChange'}))

    CHOICES = (('\t', 'tab',), (';', ';',), (',', ',',), (' ', 'space',))
    delim = forms.ChoiceField(label="CSV delimiter", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    uploader = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'fileselector'}))

    def is_valid(self):
        return True

@method_decorator(login_required, name='dispatch')
class DataUploader(View):
    context = {"title": "Data Uploader ", "content_header": "Upload differential expression gene data", "upload_data": True, "analysis": True}

    def handle_uploaded_file(self, request, f, post_data):

        folder_name = "user_dir/"+request.session["temp_name"]+"/deg_file/"

        if f.content_type != "text/csv":
            return False

        file_name = folder_name+f.name
        file_metadata = folder_name+"metadata_"+f.name

        fout = open(file_name, "wb")
        for chunk in f.chunks():
            fout.write(chunk)

        data = {}
        data["file_name"] = folder_name+f.name
        data["delim"] = post_data["delim"]
        data["dataset"] = post_data["dataset"]
        data["lfc"] = post_data["lfc"]
        data["gene"] = post_data["gene"]

        fout = open(file_metadata, "w")
        fout.write(json.dumps(data))

        return True

    def get(self, request):
        self.context["result"] = None

        form = DEGFileForm()
        self.context["form"] = form
        return render(request, 'main/deg_file_uploader.html', self.context)

    def post(self, request):

        form = DEGFileForm(request.POST, request.FILES)

        fobj = request.FILES['uploader']

        upload_result = self.handle_uploaded_file(request, fobj,request.POST)

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

        return render(request, 'main/deg_file_uploader.html', self.context)
