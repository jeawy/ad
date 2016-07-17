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
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import smtplib
from django.conf import settings
from django.db.models import Q
import re 
import base.models as models


def home( request):
    #appinfos = models.Appinfo.objects.all()[:1]
    index = 1
    appname = ''
    page = 20 
    if 'index' in request.GET and 'appname' in request.GET:
        index   = request.GET['index'] 
        appname = request.GET['appname'] 
        
        kwargs ={ }
        
        if appname :
            kwargs['ad_app__title__contains']  = appname
            #kwargs['ready']  = 1
            
            
        index = int(index)
        index += 1 
        if kwargs:
             
            creative_ls_id = models.Creative.objects.filter(**kwargs).exclude(image_url= '').order_by('file_md5').distinct('file_md5').values_list('creative_id',flat=True)
            creative_ls_id = creative_ls_id.exclude(file_ext = 'm4v')
        else:
            creative_ls_id = models.Creative.objects.exclude(file_ext = 'm4v').order_by('file_md5').distinct( 'file_md5').values_list('creative_id',flat=True)
            
        creative_ls = models.Creative.objects.filter(creative_id__in = creative_ls_id).order_by('-first_seen')[0: index*page]
        '''
        result = {} 
        
        result['index']            = index 
        creatives          = [model_to_dict(creative) for creative in creative_ls] 
        for creative in creatives: 
            try:
                app = models.Appinfo.objects.get(app_id = creative['ad_app'])
                creative['app_title']         = app.title
                creative['app_platform_type'] = app.platform_type
                creative['app_description']   = app.description
                creative['app_version']       = app.version
                creative['app_category']      = app.category
                
                
            except models.Appinfo.DoesNotExist:
                creatives.remove(creative)
            except models.Appinfo.MultipleObjectsReturned:
                creatives.remove(creative)
            
        result['creative_ls']      = creatives
        return HttpResponse(json.dumps(result,   cls=DjangoJSONEncoder), content_type='application/json')
        '''
        
    elif 'appname' in request.GET: 
        appname = request.GET['appname']
        
         
    else:
        creative_ls_id = models.Creative.objects.exclude(file_ext = 'm4v').order_by('file_md5').distinct('file_md5').values_list('creative_id',flat=True)
        creative_ls = models.Creative.objects.filter(creative_id__in = creative_ls_id).order_by('-first_seen')[0: page]
         
    content ={
        'creative_ls'  :creative_ls,
        'thumbnails'   : settings.THUMBNAIL_URL,
        'creative_url' : settings.CREATIVE_URL,
        'creatives'   : settings.CREATIVE_URL,
        'index'       : index,
        'appname'     : appname
    }  
    return render(request, 'index.html', content)
