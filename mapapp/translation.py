from modeltranslation.translator import translator, TranslationOptions
from mapapp.models import District, KindPersonOfAccess, KindOfConstruction,\
    Construction, Ward


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)
    
class KindPersonOfAccessTranslationOptions(TranslationOptions):
    fields = ('name',)
    
class KindOfConstructionTranslationOptions(TranslationOptions):
    fields = ('name',)
    
class ConstructionTranslationOptions(TranslationOptions):
    fields = ('name', 'description_detail', 'description_other')    

class WardTranslationOptions(TranslationOptions):
    fields = ('name',)
    
translator.register(District, DistrictTranslationOptions)
translator.register(KindPersonOfAccess, KindPersonOfAccessTranslationOptions)
translator.register(KindOfConstruction, KindOfConstructionTranslationOptions)
translator.register(Construction, ConstructionTranslationOptions)
translator.register(Ward, WardTranslationOptions)