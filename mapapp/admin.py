from django.contrib import admin
from mapapp.models import District, KindOfConstruction, Construction,\
    KindPersonOfAccess, Street, Comment, Ward, AccessibleIcon
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import ugettext_lazy as _


class AdminDistrict(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ('name',)
    search_fields = ('name',)

class AccessibleIconInline(admin.TabularInline):
    model = AccessibleIcon
    extra = 1
            
class AdminKindOfConstruction(admin.ModelAdmin):
    list_display = ['name', 'show_image']
    list_filter = ('name',)
    search_fields = ('name',)    
    inlines = [
        AccessibleIconInline,
    ]
    
    class Media:
        js = ('js/jquery.min.js', 'js/icon.js')

    
class AdminComment(admin.ModelAdmin):
    list_display = ['email', 'get_content', 'date_format', 'construction', 'get_status']
    list_filter = ('comment_date', 'status')
    search_fields = ('email', 'construction__name', 'construction__unsigned_name')
    list_per_page = 50
    
    actions = ['make_published', 'make_hidden']

    def make_hidden(self, request, queryset):
        queryset.update(status='h')
    make_hidden.short_description = _("Mark selected comments as hidden")
    
    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description = _("Mark selected comments as published")
    
class AdminConstruction(admin.ModelAdmin):
    list_display = ['name', 'kind_of_construction', 'street', 'district',]
    list_filter = ('district', 'kind_of_construction',  'street', )
    search_fields = ('name_vi', 'unsigned_name', 'street__name', 'street__unsigned_name', 
                     'ward__name', 'district__name', 'district__unsigned_name', 
                     'kind_of_construction__name_vi')
    save_on_top = True
    list_per_page = 200
    
class AdminKindPersonOfAccess(admin.ModelAdmin):
    list_display = ['access_level', 'name', 'show_image']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminStreet(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ('name',)
    search_fields = ('name',)    
    
class AdminWard(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ('name',)
    search_fields = ('name',)  


class MyTranslatedNewsAdmin(AdminConstruction, TranslationAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(MyTranslatedNewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

admin.site.register(District, AdminDistrict)
admin.site.register(KindOfConstruction, AdminKindOfConstruction)
admin.site.register(Construction, AdminConstruction)
admin.site.register(KindPersonOfAccess, AdminKindPersonOfAccess)
admin.site.register(Street, AdminStreet)
admin.site.register(Comment, AdminComment)
admin.site.register(Ward, AdminWard)
