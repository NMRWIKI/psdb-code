# Create your views here.
from datetime import datetime
from django.db.models import Q
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from jinja2 import Environment, PackageLoader
from organizations import forms, models
from wikimarkup import parse
from coffin.shortcuts import render_to_response
ENV = Environment(loader=PackageLoader('organizations', 'templates'))

def org_main(request):
    org_type_info = list()
    title_link = reverse('create_lab')
    title_link_text = '(add)'
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
        data = {
            'request': request,
            'org_type_info': org_type_info,
            'title': 'Organizations',
            'title_link': title_link,
            'title_link_text': title_link_text
            }
    return render_to_response('org_main.html', data)

@login_required
@csrf_exempt
def create_lab(request):
    org_type = request.GET.get('org_type', '')
    type_map = dict(models.ORG_TYPE_URL2ID)
    org_type_id = type_map.get(str(org_type), None)
    title = 'Organization Creation'
    if request.method == 'POST':
        form = forms.OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            organization = form.instance
            return http.HttpResponseRedirect(organization.get_absolute_url())
    else:
        form = forms.OrganizationForm(initial = {'org_type': org_type_id})

    data = {'request': request, 
            'the_form': form, 
            'title': title
            }
    return render_to_response('create_lab.html', data) 

@login_required
@csrf_exempt
def create_appointment(request):
    user = request.user
    org_id = request.GET.get('org', '')
    organization = models.Organization.objects.get(id = org_id)
    title = 'Have you worked at %s?' % organization.name
    if request.method == 'POST':
        appointment = models.Appointment(user=user, organization=organization)
        form = forms.AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(organization.get_absolute_url())
    else:
        form = forms.AppointmentForm()

    data = {
            'request': request,
            'the_form': form, 
            'title': title, 
            }
    return render_to_response('create_appointment.html', data) 

def org_list(request, org_type=None):
    org_type_id = dict(models.ORG_TYPE_URL2ID)[org_type]
    orgs = models.Organization.objects.filter(org_type = org_type_id)
    if request.user.is_authenticated():
        my_orgs = orgs.filter(appointments__user=request.user)
        all_orgs = orgs.exclude(appointments__user = request.user)
    else:
        my_orgs = None
        all_orgs = orgs
    template = ENV.get_template('org_list.html')
    data = {
        'request': request,
        'my_orgs': my_orgs,
        'all_orgs': all_orgs,
        'title': org_type.replace('-', ' ').title(),
        'title_link': reverse('create_lab') + '?org_type=' + org_type,
        'title_link_text': '(add)'
    }
    return render_to_response('org_list.html', data)

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
        Q(to_date = None)|
        Q(to_date__gt = now)
    )
    data = {
        'request': request,
        'title': org.name,
        'organization': org,
        'org_members': org_members,
        'current_appointments': current_members,
        'former_appointments': former_members,
        'add_link': add_link,
    }
    return render_to_response('org_page.html', data)

@csrf_exempt
def save_org_description(request):
    if request.user.is_anonymous():
        raise Http404
    text = request.POST['text']
    org_id = request.POST['id']
    field = request.POST['field']
    org = models.Organization.objects.get(id = org_id)
    setattr(org, field, text)
    org.save()
    #save the descr
    data = simplejson.dumps({'text': parse(text), 'id': org_id })
    return http.HttpResponse(data, mimetype="application/json")

def get_org_description(request):
    if request.user.is_anonymous():
        raise Http404
    org_id = request.GET['id']
    field = request.GET['field']
    org = models.Organization.objects.get(id = org_id)
    data = simplejson.dumps({'text': getattr(org, field)})
    return http.HttpResponse(data, mimetype="application/json")
