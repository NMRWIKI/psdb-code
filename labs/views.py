# Create your views here.
from django.http import HttpResponse
from labs import forms
from jinja2 import Environment, PackageLoader
from django.views.decorators.csrf import csrf_exempt
ENV = Environment(loader=PackageLoader('labs', 'templates'))

@csrf_exempt
def create_lab(request):
    extra = ''
    if request.method == 'POST':
        form = forms.LabAccountForm(request.POST)
        if form.is_valid():
            form.save()
            extra = "Thanks!"
    else:
        form = forms.LabAccountForm()

    data = {'the_form': form, 'message': extra }
    template = ENV.get_template('create_lab.html')
    return HttpResponse(template.render(**data))

@csrf_exempt
def all(request):
    if request.method == 'GET':
        
