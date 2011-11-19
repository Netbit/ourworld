from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import date
from django.conf import settings


# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 60, unique = True, verbose_name = _('District name'))
    unsigned_name = models.CharField(max_length = 50, verbose_name = _('District unsigned name'))
    location    = models.CharField(max_length = 30, blank = True, verbose_name = _('Location (on map)'))
    description = models.TextField(blank = True, verbose_name = _('Description'))
    
    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
    
    def __unicode__(self):
        return self.name

class Street(models.Model):
    name    = models.CharField(max_length = 100, unique = True, verbose_name = _('Street name'))
    unsigned_name = models.CharField(max_length = 80, verbose_name = _('Street unsigned name'))
    
    class Meta:
        verbose_name = _("Street")
        verbose_name_plural = _("Streets")
    
    def __unicode__(self):
        return self.name
   
class KindPersonOfAccess(models.Model):
    access_level = models.CharField(max_length = 10, unique = True, verbose_name = _('Access level'))
    name        = models.CharField(max_length = 100, blank = True, verbose_name = _('Kind person of access name'))
    image       = models.ImageField(upload_to = 'images/person', blank = True, verbose_name = _('Image'))
    description = models.TextField(blank = True, verbose_name = _('Description'))
    
    class Meta:
        verbose_name = _("Kind Person of Access")
        verbose_name_plural = _("Kind People of Access")
        
    def get_image(self):
        if hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.STATIC_URL + "images/noimage.jpg"
    
    def __unicode__(self):
        return self.access_level + ": " + self.name
    
class KindOfConstruction(models.Model):
    name = models.CharField(max_length = 100, unique = True, verbose_name = _('Kind of construction name'))
    image = models.ImageField(upload_to = 'images/kind', blank = True, verbose_name = _('Image'))
    description = models.TextField(blank = True, verbose_name = _('Description'))
    
    class Meta:
        verbose_name = _("Kind of Construction")
        verbose_name_plural = _("Kind of Constructions")
        
    def get_image(self):
        if hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.STATIC_URL + "images/noimage.jpg"
    
    def __unicode__(self):
        return self.name
    
class Ward(models.Model):
    name = models.CharField(unique = True, max_length = 100, verbose_name = _('Ward name'))
    
    class Meta:
        verbose_name = _("Ward")
        verbose_name_plural = _("Wards")
        
    def __unicode__(self):
        return self.name

class Construction(models.Model):   
    name               = models.CharField(max_length = 100, unique = True, verbose_name = _('Construction name'))
    unsigned_name      = models.CharField(max_length = 80, verbose_name = _('Construction unsigned name'))
    number_or_alley    = models.CharField(max_length = 20, blank = True, verbose_name = _('Number or alley'))
    street             = models.ForeignKey(Street, verbose_name = _('Street'))
    ward               = models.ForeignKey(Ward, blank = True, null = True, verbose_name = _('Ward'))
    district           = models.ForeignKey(District, verbose_name = _('District'))    
    link_image         = models.ImageField(upload_to = 'images/place', blank = True, verbose_name = _('Image'))
    description_detail = models.TextField(blank = True, verbose_name = _('Description detail'))
    description_other  = models.TextField(blank = True, verbose_name = _('Description other'))
    kind_of_construction = models.ForeignKey(KindOfConstruction, verbose_name = _('Kind of Construction'))
    kind_of_person        = models.ManyToManyField(KindPersonOfAccess, verbose_name = _('Kind person of access'), blank = True)
    location           = models.CharField(max_length = 100, blank = True, verbose_name = _('Location (on map)'))
    
    class Meta:
        verbose_name = _("Construction")
        verbose_name_plural = _("Constructions")
        
    def get_image(self):
        if hasattr(self.link_image, 'url'):
            return self.link_image.url
        else:
            return ""
    
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
    content = models.TextField(verbose_name = _('Content'),  unique = True)
    comment_date = models.DateTimeField(auto_now_add = True, verbose_name = _('Comment date'))
    construction = models.ForeignKey(Construction, verbose_name = _('Construction'))
    status = models.CharField(max_length = 2, default = 'h', verbose_name = _('Status'), choices = STATUS_CHOICES)
    
    def date_format(self):
        return date(self.comment_date, 'd-m-Y H:i:s')
    date_format.admin_order_field = 'comment_date'
    date_format.short_description = _('Comment date')
    
    def get_status(self):
        if self.status == "p":
            status = "<span style='margin: auto'><img src='" + settings.STATIC_URL + "images/activate.gif' title='Published'></span>"
        else:
            status = "<span style='margin: auto'><img src='" + settings.STATIC_URL + "images/deactivate.gif' title='Hidden'></span>"
        return status
    get_status.allow_tags = True
    get_status.admin_order_field = 'status'
    get_status.short_description = _('Status')
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


    
