from django.conf.urls import include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

import captcha
from edure import views

admin.autodiscover()

admin.site.site_header = 'Edure Administration'

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
]


urlpatterns += [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^get_captcha/$', views.get_captcha, name='get_captcha'),
    url(r'^admin/', admin.site.urls),

    url(r'^storage/', views.storage, name='storage'),
    url(r'^word_processing/(?P<key>[a-zA-Z0-9]+)$', views.word_processing, name='word_processing'),
    url(r'^word_processing/', views.word_processing, name='word_processing'),
    url(r'^onlyoffice/', views.onlyoffice, name='onlyoffice'),


    url(r'^file_manager/library/(?P<key>[0-9]+)$', views.file_manager_library, name='file_manager_library'),
    url(r'^file_manager/library/', views.file_manager_library, name='file_manager_library'),

    url(r'^file_manager/drive/(?P<key>[0-9]+)$', views.file_manager_drive, name='file_manager_drive'),
    url(r'^file_manager/drive/', views.file_manager_drive, name='file_manager_drive'),

    url(r'^file_manager/dropbox/(?P<key>[0-9]+)$', views.file_manager_dropbox, name='file_manager_dropbox'),
    url(r'^file_manager/dropbox/', views.file_manager_dropbox, name='file_manager_dropbox'),

    url(r'^file_manager/', views.file_manager, name='file_manager'),

    url(r'^info_tech/', views.info_tech, name='info_tech'),
    url(r'^physics/', views.physics, name='physics'),
    url(r'^computer/', views.computer, name='computer'),
    url(r'^friend_lists/', views.friend_lists, name='friend_lists'),
    url(r'^sports/', views.sports, name='sports'),
    url(r'^events/', views.events, name='events'),
    url(r'^on_this_day/', views.on_this_day, name='on_this_day'),

    url(r'^activation/(?P<key>[a-zA-Z0-9]{32})$', views.activation, name='activation'),
    url(r'^(?P<slug>.*)$', views.home, name='visitor'),
]

handler404 = 'views.handle_page_not_found_404'

