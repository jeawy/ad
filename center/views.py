# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from base import models as basemodels
from .models import LikeApps
 
import pdb
@login_required
@csrf_exempt
def add_like_app(request):
    'add appinfo to personal center'
    result = {}
    if request.method == 'POST' and 'appid' in request.POST:
        appid = request.POST['appid']
        try:  
            likeapp,created = LikeApps.objects.get_or_create(user = request.user, appid= appid)
            likeapp.save()
            result['msg']    = '添加成功.'
            result['status'] = 'ok' 
        except LikeApps.MultipleObjectsReturned:
            result['msg']    = '添加成功.'
            result['status'] = 'ok'
    else:
        result['msg']    = 'Not get parametets'
        result['status'] = 'error'
    return HttpResponse(json.dumps(result), content_type='application/json' )

@login_required
def mycenter(request):
    'personal center'
    content = {} 
    likeapps = LikeApps.objects.filter(user = request.user)
    appids = []
    for likeapp in likeapps:
        appids.append(likeapp.appid)
    if len(appids) > 0 :
        apps = basemodels.Appinfo.objects.filter(app_id__in = appids)
        content['apps']  = apps

    content['likeapps']  = likeapps
         
    if request.mobile:
        return render(request, 'center\m_usercenter.html', content)
    else:
        return render(request, 'center\usercenter.html', content)