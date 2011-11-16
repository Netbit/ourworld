from django.contrib import admin
from mapapp.models import District, KindOfConstruction, Construction,\
    KindPersonOfAccess, Street, Comment, Ward
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import ugettext_lazy as _



class AdminDistrict(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 20
    
class AdminKindOfConstruction(admin.ModelAdmin):
    list_display = ['name','description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminComment(admin.ModelAdmin):
    list_display = ['email', 'content', 'date_format', 'construction', 'get_status']
    list_filter = ('comment_date', 'construction', 'status')
    search_fields = ('construction__name', 'construction__unsigned_name')
    list_per_page = 25
    
    actions = ['make_published', 'make_hidden']

    def make_hidden(self, request, queryset):
        queryset.update(status='h')
    make_hidden.short_description = _("Mark selected comments as hidden")
    
    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description = _("Mark selected comments as published")
    
class AdminConstruction(admin.ModelAdmin):
    list_display = ['name', 'kind_of_construction', 'street', 'district',]
    list_filter = ('kind_of_construction',  'street', 'district')
    search_fields = ('name',)
    save_on_top = True
    
class AdminKindPersonOfAccess(admin.ModelAdmin):
    list_display = ['access_level', 'name','description']
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
