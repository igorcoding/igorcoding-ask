from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from igorcoding_ask import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^', include('ask.urls')),
    (r'^admin/', include(admin.site.urls)),
    # url(r'^igorcoding_ask/', include('igorcoding_ask.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
