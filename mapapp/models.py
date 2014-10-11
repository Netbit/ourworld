from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import date
from django.conf import settings


# Create your models here.
class District(models.Model):
    name        = models.CharField(max_length = 60, unique = True, verbose_name = _('District name'))
    unsigned_name = models.CharField(max_length = 50, verbose_name = _('District unsigned name'))
    #location    = models.CharField(max_length = 30, blank = True, verbose_name = _('Location (on map)'))
    
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
        ordering = ['-name',]
    
    def __unicode__(self):
        return self.name


class KindPersonOfAccess(models.Model):
    access_level = models.CharField(max_length = 10, unique = True, verbose_name = _('Access level'))
    name        = models.CharField(max_length = 100, blank = True, verbose_name = _('Kind person of access name'))
    image       = models.ImageField(upload_to = 'images/person', blank = True, verbose_name = _('Image'))
    
    class Meta:
        verbose_name = _("Kind Person of Access")
        verbose_name_plural = _("Kind People of Access")
        
    def get_image(self):
        if hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.STATIC_URL + "images/noimage.jpg"
    
    def show_image(self):
        if hasattr(self.image, 'url'):
            img = "<span style='margin: auto'><img height='20' src='" + self.image.url + "' title='" + self.name + "'></span>"
        else:
            img = "<span style='margin: auto'><img height='20' src='" + settings.STATIC_URL + "images/noimage.jpg' title='" + self.name + "'></span>"
        return img
    show_image.allow_tags = True
    show_image.short_description = _('Image')
    
    def __unicode__(self):
        return self.access_level + ": " + self.name
    
class KindOfConstruction(models.Model):
    name = models.CharField(max_length = 100, unique = True, verbose_name = _('Kind of construction name'))
    image = models.ImageField(upload_to = 'images/kind', blank = True, verbose_name = _('Image'))
    
    class Meta:
        verbose_name = _("Kind of Construction")
        verbose_name_plural = _("Kind of Constructions")
        
        
    def get_image(self):
        if hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.STATIC_URL + "images/noimage.jpg"
    
    def show_image(self):
        if hasattr(self.image, 'url'):
            img = "<span style='margin: auto'><img height='20' src='" + self.image.url + "' title='" + self.name + "'></span>"
        else:
            img = "<span style='margin: auto'><img height='20' src='" + settings.STATIC_URL + "images/noimage.jpg' title='" + self.name + "'></span>"
        return img
    show_image.allow_tags = True
    show_image.short_description = ''
    
    def __unicode__(self):
        return self.name
       
class AccessibleIcon(models.Model):
    kind_of_contruction = models.ForeignKey(KindOfConstruction, verbose_name = _('Kind of Construction'))
    access_level = models.ForeignKey(KindPersonOfAccess, verbose_name = _('Access level'))
    icon        = models.ImageField(upload_to = 'images/icon_map', blank = True, verbose_name = _('Icon'))
    
    class Meta:
        verbose_name = _("Accessible Icon")
        verbose_name_plural = _("Accessible Icons")
        unique_together = ['access_level', 'kind_of_contruction']
    
    def __str__(self):
        return "Accessible Icon"
        
    
class Ward(models.Model):
    name = models.CharField(unique = True, max_length = 100, verbose_name = _('Ward name'))
    
    class Meta:
        verbose_name = _("Ward")
        verbose_name_plural = _("Wards")
        
    def __unicode__(self):
        return self.name

class Construction(models.Model):   
    name               = models.CharField(max_length = 100, verbose_name = _('Construction name'))
    unsigned_name      = models.CharField(max_length = 80, verbose_name = _('Construction unsigned name'))
    number_or_alley    = models.CharField(max_length = 20, blank = True, verbose_name = _('Number or alley'))
    street             = models.ForeignKey(Street, verbose_name = _('Street'))
    ward               = models.ForeignKey(Ward, blank = True, null = True, verbose_name = _('Ward'))
    district           = models.ForeignKey(District, verbose_name = _('District'))    
    link_image         = models.ImageField(upload_to = 'images/place', blank = True, verbose_name = _('Image'))
    description_detail = models.TextField(blank = True, verbose_name = _('Description detail'))
    description_other  = models.TextField(blank = True, verbose_name = _('Description other'))
    kind_of_construction = models.ForeignKey(KindOfConstruction, verbose_name = _('Kind of Construction'))
    kind_of_person     = models.ForeignKey(KindPersonOfAccess, verbose_name = _('Kind person of access'), blank = True)
    location           = models.CharField(max_length = 100, blank = True, verbose_name = _('Location (on map)'))
    #active             = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Construction")
        verbose_name_plural = _("Constructions")
        unique_together = ('name', 'street')
        
    def get_image(self):
        '''Get image of construciton'''
        if hasattr(self.link_image, 'url'):
            return self.link_image.url
        else:
            return ""
        
    def get_icon(self):
        try:
            obj = AccessibleIcon.objects.get(kind_of_contruction = self.kind_of_construction, access_level = self.kind_of_person)
            if hasattr(obj.icon, 'url'):
                return obj.icon.url
        except:
            pass
        return ""
    
    def __unicode__(self):
        return self.name
    
    def get_address(self):
        if self.ward:
            return u'%s %s, %s, %s, Ho Chi Minh' % (self.number_or_alley, self.street, self.ward.name, self.district.name)
        else:
            return '%s %s, %s, Ho Chi Minh' % (self.number_or_alley, self.street, self.district.name)
        
    def get_location(self):
        if self.location != '':
            return list(eval(self.location))
        else:
            return []

STATUS_CHOICES = (
    ('p', _('Published')),
    ('h', _('Hidden')),
)

class Comment(models.Model):
    email = models.EmailField(verbose_name = _('Email'))
    content = models.TextField(verbose_name = _('Content'))
    comment_date = models.DateTimeField(auto_now_add = True, verbose_name = _('Date'))
    construction = models.ForeignKey(Construction, verbose_name = _('Construction'))
    status = models.CharField(max_length = 2, default = 'p', verbose_name = _('Status'), choices = STATUS_CHOICES)
    
    def date_format(self):
        return date(self.comment_date, 'd-m-Y H:i:s')
    date_format.admin_order_field = 'comment_date'
    date_format.short_description = _('Date')
    
    def get_status(self):
        if self.status == "p":
            status = "<span style='margin: auto'><img src='" + settings.STATIC_URL + "images/activate.gif' title='Published'></span>"
        else:
            status = "<span style='margin: auto'><img src='" + settings.STATIC_URL + "images/deactivate.gif' title='Hidden'></span>"
        return status
    get_status.allow_tags = True
    get_status.admin_order_field = 'status'
    get_status.short_description = ''
    
    def get_content(self):
        return self.content
    get_content.allow_tags = True
    get_content.admin_order_field = 'content'
    get_content.short_description = _('Content')
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
    
