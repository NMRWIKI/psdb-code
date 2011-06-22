# Create your views here.
from django.http import HttpResponse
from organizations import forms, models
from jinja2 import Environment, PackageLoader
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
ENV = Environment(loader=PackageLoader('organizations', 'templates'))

def org_main(request):
    org_type_info = list()
    for (slug, org_type_id) in models.ORG_TYPE_URL2ID:
        cnt = models.Organization.objects.filter(
                        org_type = org_type_id
                    ).count()
        if cnt == 0:
            continue
        info = {
            'url': reverse('org_list', kwargs = {'org_type': slug}),
            'org_type_name': slug.replace('-', ' '),
            'count': cnt
        }
        org_type_info.append(info)
    template = ENV.get_template('org_main.html')
    return HttpResponse(
            template.render(
                org_type_info = org_type_info,
                title = 'Organizations'
            )
        )

@csrf_exempt
def create_lab(request):
    extra = ''
    title = 'Organization Creation'
    if request.method == 'POST':
        form = forms.LabAccountForm(request.POST)
        if form.is_valid():
            form.save()
            extra = "Thanks!"
    else:
        form = forms.LabAccountForm()

    data = {'the_form': form, 'message': extra, 'title': title }
    template = ENV.get_template('create_lab.html')
    return HttpResponse(template.render(**data))

def org_list(request, org_type=None):
    org_type_id = dict(models.ORG_TYPE_URL2ID)[org_type]
    orgs = models.Organization.objects.filter(org_type = org_type_id)
    if request.user.is_authenticated():
        my_orgs = orgs.filter(appointments__user=request.user)
        all_orgs = orgs.exclude(appointments__user = request.user)
    else:
        all_orgs = orgs
    template = ENV.get_template('org_list.html')
    data = {
        'my_orgs': my_orgs,
        'all_orgs': all_orgs,
        'title': org_type.replace('-', ' ').title(),
    }
    return HttpResponse(template.render(**data))

def org_page(request, id=None, slug=None):
    requested_org = get_object_or_404(id = id)
   # try:
   #     org = models.Organization.objects.get(id = id)
   # except models.Organizations.DoesNotExist:
   #     raise Http404
    #requested_org_page = models.Organization.objects.filter(org_id = 
    data = {
        'title': requested_org.title,
    }
    template = ENV.get_template('org_page.html')
    return HttpResponse(template.render(**data))
