# Create your models here.
from django.db import models  

class Appinfo(models.Model):
    app_id         = models.AutoField(primary_key=True)
    store_id       = models.CharField(max_length=1024, default='')
    bundle_id      = models.CharField(max_length=1024, default='')
    title          = models.CharField(max_length=1024, default='')
    platform_type  = models.SmallIntegerField()
    
    
    description  = models.CharField(max_length=4096, default='')
    current_version      = models.CharField(max_length=128, default='')
    category     = models.CharField(max_length=256, default='')
    icon_url60   = models.CharField(max_length=1024, default='')
    icon_url100  = models.CharField(max_length=1024, default='')
    icon_url512  = models.CharField(max_length=1024, default='')
    seller  = models.CharField(max_length=2048, null=True)

    class Meta:
          db_table = 'appinfo'
          managed  = False
          
    def __str__(self):              # __unicode__ on Python 2
        return str(self.app_id)
class Network(models.Model):
    network_id  = models.AutoField(primary_key=True)
    name        = models.CharField(max_length = 32, null=True)
    #description = models.CharField(max_length = 256, null=True)
    logo_url    = models.CharField(max_length = 256, null=True)
    website     = models.CharField(max_length = 256, null=True)
    sdk_version = models.CharField(max_length = 256, null=True)
    class Meta:
          db_table = 'network'
          managed  = False
          
class Creative(models.Model):
    creative_id   = models.AutoField(primary_key=True)
    ad_app        = models.ForeignKey(Appinfo)
    ad_type       = models.SmallIntegerField()
    platform_type = models.SmallIntegerField()
    file_md5      = models.CharField(max_length=1024)
    
    url_md5       = models.CharField(max_length=1024)
    campaign_id   = models.CharField(max_length=1024)
    video_url     = models.CharField(max_length=2048)
    image_url     = models.CharField(max_length=2048)
    tracking_url  = models.CharField(max_length=2048)
    
    
    height        = models.SmallIntegerField()
    width         = models.SmallIntegerField()
    file_ext      = models.CharField(max_length=128)
    first_seen    = models.DateTimeField()
    last_seen     = models.DateTimeField()
    
    ready        = models.SmallIntegerField(null = True)
    filesize     = models.IntegerField(null = True)
    duration     = models.IntegerField(null = True)
     
    
    class Meta:
          db_table = 'creative'
          managed  = False
          
    def __str__(self):              # __unicode__ on Python 2
        return str(self.creative_id)
    
 


class View_creative_ext_info(models.Model):
    first_seen   =  models.DateField(primary_key=True)
    last_seen    =  models.DateField()
    creative     =  models.ForeignKey(Creative)
    ad_app       = models.ForeignKey(Appinfo) 
    network_ids  =  models.CommaSeparatedIntegerField(max_length = 4096)
    class Meta:
        db_table = 'view_creative_ext_info'
        managed  = False
        
class Top_ad_creatives_today( models.Model ):
    creative    =  models.ForeignKey(Creative)
    share_score =  models.DecimalField(max_digits = 10, decimal_places=2 )
    title       = models.CharField(max_length=128)
    category    = models.CharField(max_length=128)
    ad_type     = models.SmallIntegerField(null = True)
    url_md5     = models.CharField(max_length=1024)
    file_ext    = models.CharField(max_length=32)
    first_seen    = models.DateTimeField()
    last_seen     = models.DateTimeField()
    icon_url60   = models.CharField(max_length=1024, default='') 
    class Meta:
        db_table = 'top_ad_creatives_today'
        managed  = False
    
    
class View_top_ad_app( models.Model ):
    ad_app         = models.ForeignKey(Appinfo) 
    title          = models.CharField(max_length=128)
    category       = models.CharField(max_length=128)
    logo_url       = models.CharField(max_length=128)
    icon_url60     = models.CharField(max_length=1024)
    icon_url100    = models.CharField(max_length=128)
    network        = models.ForeignKey(Network)
    ad_share_score = models.DecimalField(max_digits = 10, decimal_places=2 )
    class Meta:
        db_table = 'view_top_ad_app'
        managed  = False
        
class Top_ad_apps_today(models.Model):
    ad_app         = models.ForeignKey(Appinfo) 
    title          = models.CharField(max_length=128)
    category       = models.CharField(max_length=128) 
    icon_url60     = models.CharField(max_length=1024)
    icon_url100    = models.CharField(max_length=128) 
    ad_share_score = models.DecimalField(max_digits = 10, decimal_places=2 )
    class Meta:
        db_table = 'top_ad_apps_today'
        managed  = False
        
class App_strength_history(models.Model):
    ad_app         = models.ForeignKey(Appinfo) 
    ad_date        = models.DateTimeField(primary_key=True)
    ad_share_score = models.DecimalField(max_digits = 10, decimal_places=4 )
    class Meta:
        db_table  = 'app_strength_history'
        managed   = False
    