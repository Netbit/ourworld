from django.contrib import admin
from mapapp.models import District, KindOfConstruction, Construction,\
    KindOfPerson, Street
from modeltranslation.admin import TranslationAdmin


class AdminDistrict(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminKindOfConstruction(admin.ModelAdmin):
    list_display = ['name','description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminConstruction(admin.ModelAdmin):
    list_display = ['name', 'kind_of_construction', 'street', 'district',]
    list_filter = ('name', 'kind_of_construction',  'street', 'district')
    search_fields = ('name',)
    
class AdminKindOfPerson(admin.ModelAdmin):
    list_display = ['name','description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminStreet(admin.ModelAdmin):
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
admin.site.register(KindOfPerson, AdminKindOfPerson)
admin.site.register(Street, AdminStreet)


