from coffin.conf.urls.defaults import patterns, include, url
from organizations import models

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

ORG_TYPES = '|'.join(dict(models.ORG_TYPE_URL2ID).keys())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'organizations.views.org_main', name='org_main'),
    url(
        r'^(?P<org_type>(%s))/$' % ORG_TYPES,
        'organizations.views.org_list', 
        name='org_list'
    ),
    url(
        r'^(?P<id>\d+)/(?P<slug>[a-z0-9\-]+)/$',
        'organizations.views.org_page',
        name='org_page'
    ),
    url(
       # r'^create_lab/\?org_type=(?P<org_type>[a-z0-9\-]+)/$', 
        r'^create_lab/',
        'organizations.views.create_lab', 
        name='create_lab'
    ),
    url(
        r'^create_appointment', 
        'organizations.views.create_appointment',
        name='create_appointment'
    ),
    url(
        r'^save_org_description',
        'organizations.views.save_org_description',
        name='save_org_description'
    ),
    url(
        r'^get_org_description',
        'organizations.views.get_org_description',
        name='get_org_description'
    ),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
