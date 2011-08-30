from django.db import models

# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 60)
    name_english = models.CharField(max_length = 60)
    unsigned_name = models.CharField(max_length = 50)
    location    = models.CharField(max_length = 30, blank = True)
    description = models.TextField(blank = True)
    
    def __unicode__(self):
        return self.name

class Street(models.Model):
    name    = models.CharField(max_length = 100)
    unsigned_name = models.CharField(max_length = 80)
    
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
    name_english       = models.CharField(max_length = 100)
    unsigned_name      = models.CharField(max_length = 80)
    number_or_alley    = models.CharField(max_length = 20)
    street             = models.ForeignKey(Street)
    district           = models.ForeignKey(District)
    location           = models.CharField(max_length = 30, blank = True)
    link_image         = models.ImageField(upload_to = 'images/place')
    description_detail = models.TextField(blank = True)
    description_detail_english = models.TextField(blank = True)
    description_other  = models.TextField(blank = True)
    kind_of_construction = models.ForeignKey(KindOfConstruction)
    kind_of_person     = models.ManyToManyField(KindOfPerson)
    
    def __unicode__(self):
        return self.name
    
    def get_address(self):
        return '%s %s %s' % (self.number_or_alley, self.street, self.district)


    
