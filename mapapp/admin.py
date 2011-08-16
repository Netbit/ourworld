from django.contrib import admin
from mapapp.models import District, KindOfConstruction, Construction,\
    NguoiTiepCan


class AdminDistrict(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminKindOfConstruction(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ('name',)
    search_fields = ('name',)
    
class AdminConstruction(admin.ModelAdmin):
    list_display = ['name', 'loai_ct', 'district',]
    list_filter = ('name', 'loai_ct', 'district')
    search_fields = ('name','loai_ct', 'district')
    
class AdminNguoiTiepCan(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ('name',)
    search_fields = ('name',)
    

admin.site.register(District, AdminDistrict)
admin.site.register(KindOfConstruction, AdminKindOfConstruction)
admin.site.register(Construction, AdminConstruction)
admin.site.register(NguoiTiepCan, AdminNguoiTiepCan)