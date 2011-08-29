# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindOfPerson, KindOfConstruction, Construction
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


def change_languge(request, lang_cd):
    translation.activate(lang_cd)
    return HttpResponseRedirect(translation.get_language())

    
def home(request):
    a = translation.get_language()
    kind_person = KindOfPerson.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    return render_to_response('index.html', {'kind_person' : kind_person,
                                             'kind_construction' : kind_construction}, 
                              context_instance = RequestContext(request))
    
    
    
def lookup(request):
    if request.GET.has_key(u'q'):
        value = request.GET[u'q']
        lst = KindOfConstruction.objects.filter(name__contains = value)
        data = ""
        for i in lst:
            data += i.name + "\n"
        return HttpResponse(data)
    else:
        return HttpResponse("")
