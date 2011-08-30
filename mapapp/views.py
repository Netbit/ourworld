# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindOfPerson, KindOfConstruction, Construction
from django.utils import translation
from django.http import HttpResponse
from django.db.models import Q

    
def home(request):
    lang = request.GET.get("lang", 'vi')
    translation.activate(lang)
    kind_person = KindOfPerson.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    return render_to_response('index.html', {'kind_person' : kind_person,
                                             'kind_construction' : kind_construction}, 
                              context_instance = RequestContext(request))
    
    
    
def lookup(request):
    if request.GET.has_key(u'q'):
        value = request.GET[u'q']
        lst = KindOfConstruction.objects.filter(name__contains = value)
        if len(lst) < 2:
            lst.extend(KindOfConstruction.objects.filter(unsgined_name__contains = value))
        
        data = ""
        for i in lst:
            data += i.name + "\n"
        return HttpResponse(data)
    else:
        return HttpResponse("")
