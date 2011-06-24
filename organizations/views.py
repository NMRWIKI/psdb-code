# Create your views here.
from datetime import datetime
from django.db.models import Q
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from jinja2 import Environment, PackageLoader
from organizations import forms, models
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
    return http.HttpResponse(
            template.render(
                org_type_info = org_type_info,
                title = 'Organizations',
                title_link = reverse('create_lab'),
                title_link_text = '(add)'
            )
        )

@csrf_exempt
def create_lab(request):
   # org_type = request.GET.get('org_type')
    extra = ''
    title = 'Organization Creation'
    if request.method == 'POST':
        form = forms.LabAccountForm(request.POST)
        if form.is_valid():
            form.save()
            extra = "Thanks!"
    else:
        form = forms.LabAccountForm()

    data = {'the_form': form, 'message': extra, 'title': title}
    template = ENV.get_template('create_lab.html')
    return http.HttpResponse(template.render(**data))

@csrf_exempt
def create_appointment(request):
    user = request.user
    org_id = request.GET.get('org', '')
    organization = models.Organization.objects.get(id = org_id)
    title = 'Appointment Creation for %s' % organization.name
    if request.method == 'POST':
        appointment = models.Appointment(user=user, organization=organization)
        form = forms.AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(organization.get_absolute_url())
    else:
        form = forms.AppointmentForm()

    data = {
            'the_form': form, 
            'title': title, 
            }
    template = ENV.get_template('create_appointment.html')
    return http.HttpResponse(template.render(**data))

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
        'title_link': reverse('create_lab'),
        'title_link_text': '(add)'
    }
    return http.HttpResponse(template.render(**data))

def org_page(request, id=None, slug=None):
    add_link = reverse('create_appointment')
    org = get_object_or_404(models.Organization, id = id)
    now = datetime.now()
    org_members = models.Appointment.objects.filter(organization = org)
    current_members = org_members.filter(
        Q(to_date = None)|
        Q(to_date__gt = now)
    )
    former_members = org_members.exclude(
        Q(to_date = None)
        | Q(to_date__gt = now)
    )
    data = {
        'title': org.name,
        'organization': org,
        'current_appointments': current_members,
        'former_appointments': former_members,
        'add_link': add_link,
    }
    template = ENV.get_template('org_page.html')
    return http.HttpResponse(template.render(**data))
