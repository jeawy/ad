from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = patterns('',
    url(r'^user/', include('administration.urls', namespace='user')),
    url(r'^$', 'ad.views.home', name='home'),
    url(r'^get_creative_info$', 'ad.views.get_creative_info', name='get_creative_info'),
    url(r'^ad_strength$', 'ad.views.ad_strength', name='ad_strength'),
    url(r'^ad_app$', 'ad.views.ad_app', name='ad_app'),
    url(r'^ad_latest$', 'ad.views.ad_latest', name='ad_latest'),
    url(r'^app_detail/(?P<appid>\d+)$', 'ad.views.app_detail', name='app_detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^center/', include('center.urls', namespace='center')),
) 
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
urlpatterns += static(settings.THUMBNAIL_URL, document_root = settings.THUMBNAIL_ROOT ) 
