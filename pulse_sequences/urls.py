from coffin.conf.urls.defaults import patterns, include, url
from psdbgit import models

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'organizations.views.org_main', name='org_main'),
    url(
        r'^(?P<id>\d+)/(?P<slug>[a-z0-9\-]+)/$',
        'psdbgit.views.org_page',
        name='org_page'
    ),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
