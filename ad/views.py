from django.shortcuts import render
import getpass
from django.contrib.auth.models import User,Group, Permission
from django.contrib import auth
import pdb
from django.utils import timezone
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import random
import string
from django.core import serializers
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import smtplib
from django.conf import settings
from django.db.models import Q
import re 
import base.models as models
from django.db.models import Max, Min
import logging
logger = logging.getLogger(settings.LOGGER)
def home( request): 
    content={}
    content['home_menu'] = True 
    if request.mobile:
        return render(request, 'm_home.html', content)
    else:
        return render(request, 'home.html', content)

def get_creative_info(request):
    
    if request.method == 'GET':
             id = request.GET['id'] 
             try:  
                 creative_ext_info = models.View_creative_ext_info.objects.get(creative__creative_id = id)
                 first    =  creative_ext_info.first_seen.strftime('%Y-%m-%d')
                 last     =  creative_ext_info.last_seen.strftime('%Y-%m-%d') 
                 serialized_obj = serializers.serialize('json', [ creative_ext_info.creative, ])
                 app_obj        = serializers.serialize('json', [ creative_ext_info.ad_app, ]) 
                 m_d_list   = models.Network.objects.filter(network_id__in = creative_ext_info.network_ids) 
                 m_d = [model_to_dict(network) for network in m_d_list] 
             except models.View_creative_ext_info.DoesNotExist:
                 logger.error('models.View_creative_ext_info.DoesNotExist, id={}'.format(id),
                 extra={'user':request.user})
             except models.View_creative_ext_info.MultipleObjectsReturned:
                 logger.error('models.View_creative_ext_info.MultipleObjectsReturned, id={}'.format(id),
                 extra={'user':request.user}) 
              
             return HttpResponse(json.dumps({'serialized_obj': serialized_obj, 
                                              'app_obj'      : app_obj, 
                                              'network_obj'  :  m_d, 
                                              'first'        : first,
                                              'network_url'  : settings.NETWORK_URL,
                                              'last'         : last}), 
                     content_type="application/json")
          

def ad_strength(request):
    creative_ls_view = models.Top_ad_creatives_today.objects.all().order_by('-share_score').\
    values_list('creative','share_score','title', 'category','ad_type','url_md5',
                 'first_seen', 'last_seen', 'icon_url60')[:100]   
   
    content ={
        'creative_ls_view'  :creative_ls_view, 
        'thumbnails'   : settings.THUMBNAIL_URL,
        'creative_url' : settings.CREATIVE_URL,
        'idea_menu'    : True,
    }  
    if request.mobile:
        return render(request, 'm_ad_latest.html', content)
    else:
        return render(request, 'ad_latest.html', content)
def ad_latest(request):
    index = 1
    appname = ''
    if request.mobile:
        page = 20
    else:
        page = 60 

    networks = models.Network.objects.all()
  

    content = {}
    kwargs  = { }
    kwargs['ready'] = 1
    category = ''
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            kwargs['ad_app__category__contains']  = category
           

    # search via network
    network_id_ls = []
    for network in networks:
        if 'network-'+ str(network.network_id) in request.GET:
            network_id_ls.append(network.network_id)
    if len( network_id_ls ) > 0:    
        pass

    if 'ad-type'  in request.GET: 
        ad_type = request.GET['ad-type']
        kwargs['ad_type']  = ad_type


    if 'index' in request.GET and 'appname' in request.GET:
        index   = request.GET['index'] 
        appname = request.GET['appname']
        
        if appname :
            kwargs['ad_app__title__contains']  = appname
            
        index = int(index)
        index += 1  

    
    creative_ls_id = models.Creative.objects.filter(**kwargs).order_by('file_md5').distinct('file_md5').values_list('creative_id',flat=True)
    if index:
        creative_ls    = models.Creative.objects.filter(creative_id__in = creative_ls_id).exclude(ad_app__title__icontains = 'unknown').order_by('-first_seen')[0: index*page]
    else:
        creative_ls    = models.Creative.objects.filter(creative_id__in = creative_ls_id).exclude(ad_app__title__icontains = 'unknown').order_by('-first_seen')[0: page]

    
    for creative in     creative_ls:
        m, s = divmod(creative.duration, 60)
        h, m = divmod(m, 60)
        creative.duration = '%d:%02d:%02d'%(h,m,s) 
        
    content ={
        'creative_ls'  :creative_ls,
        'thumbnails'   : settings.THUMBNAIL_URL,
        'creative_url' : settings.CREATIVE_URL,
        'creatives'   : settings.CREATIVE_URL,
        'index'       : index,
        'appname'     : appname,
        'latest_menu' : True,
        'category'    : category,
        'networks'    : networks,
        "media_root"  : settings.MEDIA_URL,
        'logo_url'   : settings.NETWORK_URL,
    }  
    if request.mobile:
        return render(request, 'm_index.html', content)
    else:
        return render(request, 'index.html', content)
    
def ad_app(request):
    app_ls_view = models.Top_ad_apps_today.objects.all().order_by('-ad_share_score').\
    values_list('ad_app','title','category', 'icon_url60','icon_url100',
                   'ad_share_score')[:100]   
    
    content ={
        'app_ls_view'  :app_ls_view,  
        'logo_url'     : settings.NETWORK_URL,
        'app_menu'     : True,
    }  
    return render(request, 'app.html', content)
    

def login(request):
   
    return render(request, 'admin_user/login.html', {})
    
def app_detail(request, appid):
    content = {}
    try:
        appinfo = models.Appinfo.objects.get(app_id = appid) 
         
        c_n_list    = models.Creative.objects.filter(ad_app = appinfo)#[:5]
        img_count   = c_n_list.exclude(image_url = '').count()
        video_count = c_n_list.exclude(video_url = '').count()
        c_n_list = c_n_list[:5]

        strength_history = models.App_strength_history.objects.filter(ad_app = appinfo).order_by('-ad_date')[:10]
        '''
        pdb.set_trace()
        v_c_e_i_list =  models.View_creative_ext_info.objects.filter(ad_app = appinfo)
        networks_set = set([])
        for v_c_e_i in v_c_e_i_list:
            networks_set = networks_set | set(v_c_e_i.network_ids)
        pdb.set_trace()
        networks = models.Network.objects.filter(id in networks_set)
        pdb.set_trace()
        
        content.setdefault('networks', networks)
        '''
        content.setdefault('img_count', img_count)
        content.setdefault('video_count', video_count)

        content.setdefault('strength_history', strength_history)
        content.setdefault('appinfo', appinfo)
        content.setdefault('thumbnails', settings.THUMBNAIL_URL)
        content.setdefault('creative_url', settings.CREATIVE_URL)
        content.setdefault('c_n_list', c_n_list)
    except models.Appinfo.DoesNotExist:
        logger.error('models.Appinfo.DoesNotExist, id={}'.format(appid),
                 extra={'user':request.user})
  
    return render(request, 'app_detail.html', content)

