# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindOfPerson, KindOfConstruction
from django.utils import translation

def home(request):
    
    translation.activate('vi')
    kind_person = KindOfPerson.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    return render_to_response('index.html', {'kind_person' : kind_person,
                                             'kind_construction' : kind_construction}, 
                              context_instance = RequestContext(request))
