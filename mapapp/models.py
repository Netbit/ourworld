from django.db import models

# Create your models here.
class District(models.Model):
    name        = models.CharField(50)
    #location   = 
    description = models.TextField()
   
class NguoiTiepCan(models.Model):
    link_icon = models.ImageField()
    
class KindOfConstruction(models.Model):
    name = models.CharField(100)

class Construction(models.Model):   
    district           = models.ForeignKey(District)
    loai_ct            = models.ForeignKey(KindOfConstruction)
    location           = models.CharField()
    link_image         = models.ImageField()
    description_detail = models.TextField()
    description_other  = models.TextField()
    nguoi_tc           = models.ManyToManyField(NguoiTiepCan)


    
