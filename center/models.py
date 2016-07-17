from django.db import models
from administration.models import User
from base.models import Appinfo

class LikeApps(models.Model):
    user = models.ForeignKey(User)
    app  = models.ForeignKey(Appinfo)
    date = models.DateTimeField(auto_now_add = True)
 

