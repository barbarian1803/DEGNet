from django.views import View
from django.shortcuts import render

class Index(View):
    context = {"title": "DEGNet Home Page"}

    def get(self, request):
        if request.user.is_authenticated:
            self.context["is_auth"] = True
        else:
            self.context["is_auth"] = False
        return render(request, 'main/index.html', self.context)
