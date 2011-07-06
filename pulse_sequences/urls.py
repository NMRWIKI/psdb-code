from coffin.conf.urls.defaults import patterns, include, url
from psdbgit import models

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pulse_sequences.views.org_main', name='ps_main'),
    url(
        r'^(?P<slug>[a-z0-9\-]+)/$',
        'pulse_sequences.views.database_page',
        name='database_page'
    ),
    url(
        r'^(?P<slug>[a-z0-9\-]+)-(?P<device_type>[a-z])(?P<id>\d+)/$',
        'pulse_sequences.views.repo_page',
        name='repo_page'
    ),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
