from django.db import models

# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 100)
    location    = models.CharField(max_length = 30)
    description = models.TextField(blank = True)
    
    def __unicode__(self):
        return self.name
   
class KindOfPerson(models.Model):
    name        = models.CharField(max_length = 100)
    image       = models.ImageField(upload_to = 'images/person')
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
class KindOfConstruction(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'images/kind')
    description = models.TextField()
    
    def __unicode__(self):
        return self.name

class Construction(models.Model):   
    name               = models.CharField(max_length = 100)
    address            = models.CharField(max_length = 50)
    district           = models.ForeignKey(District)
    location           = models.CharField(max_length = 30, blank = True)
    link_image         = models.ImageField(upload_to = 'images/place')
    description_detail = models.TextField(blank = True)
    description_other  = models.TextField(blank = True)
    kind_of_construction = models.ForeignKey(KindOfConstruction)
    kind_of_person     = models.ManyToManyField(KindOfPerson)
    
    def __unicode__(self):
        return self.name
    
    def get_address(self):
        return '%s, %s' % (self.address, self.district)


    
