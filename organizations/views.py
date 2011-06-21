# Create your views here.
from django.http import HttpResponse
from organizations import forms, models
from jinja2 import Environment, PackageLoader
from django.views.decorators.csrf import csrf_exempt
ENV = Environment(loader=PackageLoader('organizations', 'templates'))

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

def org_list(request, org_type=None):
    org_type_id = models.ORG_TYPE_URL2ID[org_type]
    orgs = models.Organization.objects.filter(org_type = org_type_id)
    if request.user.is_authenticated():
        my_orgs = orgs.filter(appointments__user=request.user)
        all_orgs = orgs.exclude(appointments__user = request.user)
    else:
        all_orgs = orgs
    template = ENV.get_template('all_labs.html')
    data = {
        'my_orgs': my_orgs,
        'all_orgs': all_orgs,
    }
    return HttpResponse(template.render(**data))
