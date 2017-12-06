from django.views import View
from django.shortcuts import render
from django import forms
from network_analysis.lib.GeneralUtil import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class GeneConversionForm(forms.Form):
    dataset = forms.CharField(label="Dataset name", max_length=255, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'gene id, one id per line'}))
    dataset.required = False

    CHOICES = (('ensembl', 'Ensembl ID',), ('entrez', 'Entrez ID',), ('symbol', 'Gene Symbol',), ('uniprot', 'Uniprot KB ID',))
    convert_from = forms.ChoiceField(label="Convert from", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    convert_to = forms.ChoiceField(label="Convert to", initial="symbol", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    uploader = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'fileselector'}))
    uploader.required = False

    def is_valid(self):
        return True

@method_decorator(login_required, name='dispatch')
class GeneConversion(View):

    context = {"title": "Gene Conversion", "content_header": "Gene Conversion Tool", "gene_id_conv": True, "tools": True}

    def handleUpload(self, post_data, file_data):
        convert_from = post_data["convert_from"]
        convert_to = post_data["convert_to"]
        gene_db = GeneralUtil.readGeneIDDatabase("network_analysis/external_database/all_gene_id.csv", convert_from)

        fobj = file_data['uploader']
        result = {}
        for line in fobj:
            if line == "":
                continue
            line = line.strip()
            line = str(line)
            line = line.replace("'", "")
            line = line.replace("b", "")
            try:
                result[line] = gene_db[line][convert_to]
            except:
                result[line] = ""

        return result

    def handleNotUpload(self, post_data):
        convert_from = post_data["convert_from"]
        convert_to = post_data["convert_to"]
        gene_db = GeneralUtil.readGeneIDDatabase("network_analysis/external_database/all_gene_id.csv", convert_from)
        dataset = post_data["dataset"]

        result = {}

        delim = "\n"
        if "\r" in dataset:
            delim = "\r"+delim

        for line in str(dataset).split(delim):
            if line == "":
                continue
            try:
                result[line] = gene_db[line][convert_to]
            except:
                result[line] = ""

        return result

    def get(self, request):

        self.context["result"] = None

        self.context["form"] = GeneConversionForm()
        return render(request, 'main/gene_conversion.html', self.context)

    def post(self, request):

        self.context["result"] = None

        if 'uploader' not in request.FILES:
            self.context["result"] = self.handleNotUpload(request.POST)
        else:
            self.context["result"] = self.handleUpload(request.POST, request.FILES)

        self.context["form"] = GeneConversionForm(request.POST, request.FILES)
        return render(request, 'main/gene_conversion.html', self.context)