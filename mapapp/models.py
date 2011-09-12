from django.db import models
from django.utils.translation import ugettext


# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 60, verbose_name = ugettext('District name'))
    unsigned_name = models.CharField(max_length = 50, verbose_name = ugettext('District unsigned name'))
    location    = models.CharField(max_length = 30, blank = True, verbose_name = ugettext('Location (on map)'))
    description = models.TextField(blank = True, verbose_name = ugettext('Description'))
    
    class Meta:
        verbose_name = ugettext("District")
        verbose_name_plural = ugettext("Districts")
    
    def __unicode__(self):
        return self.name

class Street(models.Model):
    name    = models.CharField(max_length = 100, verbose_name = ugettext('Street name'))
    unsigned_name = models.CharField(max_length = 80, verbose_name = ugettext('Street unsigned name'))
    
    class Meta:
        verbose_name = ugettext("Street")
        verbose_name_plural = ugettext("Streets")
    
    def __unicode__(self):
        return self.name
   
class KindOfPerson(models.Model):
    name        = models.CharField(max_length = 100, verbose_name = ugettext('Kind of person name'))
    image       = models.ImageField(upload_to = 'images/person', blank = True, verbose_name = ugettext('Image'))
    description = models.TextField(blank = True, verbose_name = ugettext('Description'))
    
    class Meta:
        verbose_name = ugettext("Kind of Person")
        verbose_name_plural = ugettext("Kind of Persons")
    
    def __unicode__(self):
        return self.name
    
class KindOfConstruction(models.Model):
    name = models.CharField(max_length = 100, verbose_name = ugettext('Kind of construction name'))
    image = models.ImageField(upload_to = 'images/kind', blank = True, verbose_name = ugettext('Image'))
    description = models.TextField(blank = True, verbose_name = ugettext('Description'))
    
    class Meta:
        verbose_name = ugettext("Kind of Construction")
        verbose_name_plural = ugettext("Kind of Constructions")
    
    def __unicode__(self):
        return self.name

class Construction(models.Model):   
    name               = models.CharField(max_length = 100, verbose_name = ugettext('Construction name'))
    unsigned_name      = models.CharField(max_length = 80, verbose_name = ugettext('Construction unsigned name'))
    number_or_alley    = models.CharField(max_length = 20, blank = True, verbose_name = ugettext('Number or alley'))
    street             = models.ForeignKey(Street, verbose_name = ugettext('Street'))
    district           = models.ForeignKey(District, verbose_name = ugettext('District'))
    location           = models.CharField(max_length = 30, blank = True, verbose_name = ugettext('Location (on map)'))
    link_image         = models.ImageField(upload_to = 'images/place', blank = True, verbose_name = ugettext('Image'))
    description_detail = models.TextField(blank = True, verbose_name = ugettext('Description detail'))
    description_other  = models.TextField(blank = True, verbose_name = ugettext('Description other'))
    kind_of_construction = models.ForeignKey(KindOfConstruction, verbose_name = ugettext('Kind of construction'))
    kind_of_person     = models.ManyToManyField(KindOfPerson, verbose_name = ugettext('Kind of person'))
    
    class Meta:
        verbose_name = ugettext("Construction")
        verbose_name_plural = ugettext("Constructions")
    
    def __unicode__(self):
        return self.name
    
    def get_address(self):
        return '%s %s, Ho Chi Minh City' % (self.number_or_alley, self.street)


    
