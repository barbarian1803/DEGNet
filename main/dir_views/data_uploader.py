from django.views import View
from django.shortcuts import render
from django import forms
import json

class DEGFileForm(forms.Form):
    dataset = forms.CharField(label="Dataset name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dataset1'}))

    gene = forms.CharField(label="Gene column name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gene    '}))

    lfc = forms.CharField(label="Log fold change column name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'log2FoldChange'}))

    CHOICES = (('\t', 'tab',), (';', ';',), (',', ',',), (' ', 'space',))
    delim = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    uploader = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'fileselector'}))




class DataUploader(View):

    # TODO define a function to hande the uploaded file and check error
    def __handle_uploaded_file__(self, f):
        with open('tmp/name.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get(self, request):
        form = DEGFileForm()
        context = {"title": "Data uploader", "content": "This is content", "form": form}
        return render(request, 'main/uploader.html', context)

    def post(self,request):

        form = DEGFileForm(request.POST, request.FILES)
        if form.is_valid():
            self.__handle_uploaded_file__(request.FILES['uploader'])
            context = {"title": "Data uploader", "result": "success", "form": form}
        else:
            context = {"title": "Data uploader", "result": "fail", "form": form}

        return render(request, 'main/uploader.html', context)
