from django.views import View
from django.shortcuts import render
from django import forms
from django.core.files.storage import FileSystemStorage
import chromelogger as console
import json

class DEGFileForm(forms.Form):
    dataset = forms.CharField(label="Dataset name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dataset1'}))

    gene = forms.CharField(label="Gene column name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gene    '}))

    lfc = forms.CharField(label="Log fold change column name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'log2FoldChange'}))

    CHOICES = (('\t', 'tab',), (';', ';',), (',', ',',), (' ', 'space',))
    delim = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    uploader = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'fileselector'}))

    def is_valid(self):
        return True


class DataUploader(View):
    context = {"title":"Data Uploader"}

    # TODO define a function to hande the uploaded file and check error
    def handle_uploaded_file(self, f):

        if f.content_type != "text/csv":
            return False

        fout = open('tmp/'+f.name,"wb")
        for chunk in f.chunks():
            fout.write(chunk)

        return True

    def get(self, request):
        form = DEGFileForm()
        self.context["form"] = form
        return render(request, 'main/uploader.html', self.context)

    def post(self,request):

        form = DEGFileForm(request.POST, request.FILES)

        fobj = request.FILES['uploader']

        upload_result = self.handle_uploaded_file(fobj)

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

        return render(request, 'main/uploader.html', self.context)
