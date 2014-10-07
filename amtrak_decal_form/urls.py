from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    'amtrak_decal_form.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^success/$', 'success', name='success'),
    url(
        r'^validate_user_info/$',
        'validate_user_info',
        name='validate_user_info',
    ),
)
