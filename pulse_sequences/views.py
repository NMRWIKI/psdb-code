# Create your views here.
from coffin.shortcuts import render_to_response
from django import http
from django.core.urlresolvers import reverse
from jinja2 import Environment, PackageLoader
from pulse_sequences import models
ENV = Environment(loader=PackageLoader('organizations', 'templates'))

def ps_main(request):
    return http.HttpResponse('jajaja')

def ps_list(request, ps_type=None):
# may keep the filtration, perhaps amongst the different tool types.  (A,B,J)
# keeping the my/all filtration
# would this be a list of ps or repo?
    ps_type_id = dict(models.ORG_TYPE_URL2ID)[ps_type]
    pslist = models.Organization.objects.filter(org_type = org_type_id)
    if request.user.is_authenticated():
        my_ps = pslist.filter(appointments__user = request.user)
        all_ps = pslist.exclude(appointments__user = request.user)
    else:
        my_ps = None
        all_ps = orgs
    template = ENV.get_template('ps_list.html')
    data = {
        'request': request,
        'my_orgs': my_ps,
        'all_orgs': all_ps,
        'title': ps_type.replace('-', ' ').title(),
   #     'title_link': reverse('create_lab') + '?org_type=' + ps_type,
   #     'title_link_text': '(add)'
    }
    return render_to_response('ps_list.html', data)

def ps_page(request):

def ps_creation(request):

def ps_edit(request):
