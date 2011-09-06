from modeltranslation.translator import translator, TranslationOptions
from mapapp.models import District, KindOfPerson, KindOfConstruction,\
    Construction


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    
class KindOfPersonTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    
class KindOfConstructionTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    
class ConstructionTranslationOptions(TranslationOptions):
    fields = ('name', 'description_detail')    


translator.register(District, DistrictTranslationOptions)
translator.register(KindOfPerson, KindOfPersonTranslationOptions)
translator.register(KindOfConstruction, KindOfConstructionTranslationOptions)
translator.register(Construction, ConstructionTranslationOptions)
