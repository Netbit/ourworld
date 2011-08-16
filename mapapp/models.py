from django.db import models

# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 100)
    location    = models.CharField(max_length = 30)
    description = models.TextField(blank = True)
    
    def __unicode__(self):
        return self.name
   
class NguoiTiepCan(models.Model):
    name      = models.CharField(max_length = 100)
    link_icon = models.ImageField(upload_to = 'images/icon')
    
    def __unicode__(self):
        return self.name
    
class KindOfConstruction(models.Model):
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return self.name

class Construction(models.Model):   
    district           = models.ForeignKey(District)
    loai_ct            = models.ForeignKey(KindOfConstruction)
    name               = models.CharField(max_length = 100)
    location           = models.CharField(max_length = 30, blank = True)
    link_image         = models.ImageField(upload_to = 'images/place')
    description_detail = models.TextField(blank = True)
    description_other  = models.TextField(blank = True)
    nguoi_tc           = models.ManyToManyField(NguoiTiepCan)
    
    def __unicode__(self):
        return self.name


    
