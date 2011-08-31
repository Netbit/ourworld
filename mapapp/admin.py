from django.contrib import admin
from mapapp.models import District, KindOfConstruction, Construction,\
    KindOfPerson, Street


class AdminDistrict(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminKindOfConstruction(admin.ModelAdmin):
    list_display = ['name','description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminConstruction(admin.ModelAdmin):
    list_display = ['name', 'kind_of_construction', 'district',]
    list_filter = ('name', 'kind_of_construction', 'district')
    search_fields = ('name','kind_of_construction', 'district')
    
class AdminNguoiTiepCan(admin.ModelAdmin):
    list_display = ['name','description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminStreet(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ('name',)
    search_fields = ('name',)    


admin.site.register(District, AdminDistrict)
admin.site.register(KindOfConstruction, AdminKindOfConstruction)
admin.site.register(Construction, AdminConstruction)
admin.site.register(KindOfPerson, AdminNguoiTiepCan)
admin.site.register(Street, AdminStreet)