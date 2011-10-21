from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 60, verbose_name = _('District name'))
    unsigned_name = models.CharField(max_length = 50, verbose_name = _('District unsigned name'))
    location    = models.CharField(max_length = 30, blank = True, verbose_name = _('Location (on map)'))
    description = models.TextField(blank = True, verbose_name = _('Description'))
    
    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
    
    def __unicode__(self):
        return self.name

class Street(models.Model):
    name    = models.CharField(max_length = 100, verbose_name = _('Street name'))
    unsigned_name = models.CharField(max_length = 80, verbose_name = _('Street unsigned name'))
    
    class Meta:
        verbose_name = _("Street")
        verbose_name_plural = _("Streets")
    
    def __unicode__(self):
        return self.name
   
class KindOfPerson(models.Model):
    name        = models.CharField(max_length = 100, verbose_name = _('Kind of person name'))
    image       = models.ImageField(upload_to = 'images/person', blank = True, verbose_name = _('Image'))
    description = models.TextField(blank = True, verbose_name = _('Description'))
    
    class Meta:
        verbose_name = _("Kind of Person")
        verbose_name_plural = _("Kind of Persons")
    
    def __unicode__(self):
        return self.name
    
class KindOfConstruction(models.Model):
    name = models.CharField(max_length = 100, verbose_name = _('Kind of construction name'))
    image = models.ImageField(upload_to = 'images/kind', blank = True, verbose_name = _('Image'))
    description = models.TextField(blank = True, verbose_name = _('Description'))
    
    class Meta:
        verbose_name = _("Kind of Construction")
        verbose_name_plural = _("Kind of Constructions")
    
    def __unicode__(self):
        return self.name

class Construction(models.Model):   
    name               = models.CharField(max_length = 100, verbose_name = _('Construction name'))
    unsigned_name      = models.CharField(max_length = 80, verbose_name = _('Construction unsigned name'))
    number_or_alley    = models.CharField(max_length = 20, blank = True, verbose_name = _('Number or alley'))
    street             = models.ForeignKey(Street, verbose_name = _('Street'))
    district           = models.ForeignKey(District, verbose_name = _('District'))
    location           = models.CharField(max_length = 30, blank = True, verbose_name = _('Location (on map)'))
    link_image         = models.ImageField(upload_to = 'images/place', blank = True, verbose_name = _('Image'))
    description_detail = models.TextField(blank = True, verbose_name = _('Description detail'))
    description_other  = models.TextField(blank = True, verbose_name = _('Description other'))
    kind_of_construction = models.ForeignKey(KindOfConstruction, verbose_name = _('Kind of Construction'))
    kind_of_person     = models.ManyToManyField(KindOfPerson, verbose_name = _('Kind of Person'))
    
    class Meta:
        verbose_name = _("Construction")
        verbose_name_plural = _("Constructions")
    
    def __unicode__(self):
        return self.name
    
    def get_address(self):
        return '%s %s, Ho Chi Minh' % (self.number_or_alley, self.street)

STATUS_CHOICES = (
    ('p', _('Published')),
    ('h', _('Hidden')),
)

class Comment(models.Model):
    email = models.EmailField(verbose_name = _('Email'))
    content = models.TextField(verbose_name = _('Content'))
    comment_date = models.DateTimeField(auto_now_add = True, verbose_name = _('Comment date'))
    construction = models.ForeignKey(Construction, verbose_name = _('Construction'))
    status = models.CharField(max_length = 2, default = 'p', verbose_name = _('Status'), choices = STATUS_CHOICES)
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


    
