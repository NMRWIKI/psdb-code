from django.conf.urls.defaults import patterns, include, url
from organizations import models

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

ORG_TYPES = '|'.join(models.ORG_TYPE_URL2ID.keys())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'psdb.views.home', name='home'),
    url(
        r'^(?P<org_type>(%s))/$' % ORG_TYPES,
        'organizations.views.org_list', 
        name='org_list'
    ),
    url(r'^create', 'organizations.views.create_lab', name='create_lab'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
