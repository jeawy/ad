from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from administration import views

urlpatterns = patterns('user',
    #url(r'^$', views.index, name='index'),
    url(r'^portrait/$', views.portrait, name='portrait'), #
    url(r'^newgroup/$', views.newgroup, name='newgroup'), #
    url(r'^grouplist/$', views.grouplist, name='grouplist'), #
    url(r'^(?P<groupid>\d+)/modify_group/$', views.modify_group, name='modify_group'),
    #url(r'^modify_user/$', views.modify_user, name='modify_user'), #
    url(r'^(?P<userid>\d+)/modify_user/$', views.modify_user, name='modify_user'),
    url(r'^list_users/$', views.list_users, name='list_users'), #
    url(r'^admin_list_users/$', views.admin_list_users, name='admin_list_users'), #
    url(r'^upload_fake_portrait/$', views.upload_fake_portrait, name='upload_fake_portrait'), # 
    #url(r'^save_portrait/$', views.save_portrait, name='save_portrait'), #save portrait
    url(r'^get_email_verify_code$', views.get_email_verify_code, name='get_email_verify_code'),
    url(r'^user_register$', views.user_register, name='user_register'),
    url(r'^save_user$', views.save_user, name='save_user'), 
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout_view, name='logout'), 
    url(r'^find_password$', views.find_password, name='find_password'), 
    url(r'^reset_password$', views.reset_password, name='reset_password'), #reset password 
    url(r'^get_reset_pwd_verify_code$', views.get_reset_pwd_verify_code, name='get_reset_pwd_verify_code'),
)  
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 