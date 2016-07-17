from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from center import views
urlpatterns = patterns('',
    url(r'^add_like_app/$', views.add_like_app, name='add_like_app'), 
) 
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
urlpatterns += static(settings.THUMBNAIL_URL, document_root = settings.THUMBNAIL_ROOT )
