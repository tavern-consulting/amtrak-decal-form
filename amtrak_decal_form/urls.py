from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'amtrak_decal_form.views',
    # Examples:
    url(r'^$', 'index', name='index'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
