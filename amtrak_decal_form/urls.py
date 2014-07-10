from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'amtrak_decal_form.views',
    # Examples:
    url(r'^$', 'index', name='index'),
)
