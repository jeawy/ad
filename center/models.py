# -*- coding:utf-8 -*-
from django.db import models
from administration.models import User
from base.models import Appinfo

class LikeApps(models.Model):
    user = models.ForeignKey(User) 
    appid  = models.IntegerField(null = True)
    date = models.DateTimeField(auto_now_add = True)
 

