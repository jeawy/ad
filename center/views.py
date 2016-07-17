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
            app = basemodels.Appinfo.objects.get(app_id = appid)
            likeapp = LikeApps.objects.create(user = request.user, app= app)
            likeapp.save()
            result['msg']    = '添加成功.'
            result['status'] = 'ok'
        except basemodels.Appinfo.DoesNotExist:
            result['msg']    = 'basemodels.Appinfo.DoesNotExist'
            result['status'] = 'error'
    else:
        result['msg']    = 'Not get parametets'
        result['status'] = 'error'
    return HttpResponse(json.dumps(result), content_type='application/json' )