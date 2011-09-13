# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindOfPerson, KindOfConstruction, Construction, Street
from django.utils import translation
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings

    
def home(request):
    lang = request.GET.get("lang", '')
    
    if request.session.has_key('django_language') == False:
        request.session['django_language'] = 'vi'
        
    if lang == '':
        lang = request.session['django_language']
        
    if request.session['django_language'] != lang:        
        request.session['django_language'] = lang
        
    translation.activate(lang)        
    kind_person = KindOfPerson.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    return render_to_response('index.html', {'kind_person' : kind_person,
                                             'kind_construction' : kind_construction}, 
                              context_instance = RequestContext(request))
    
    
    
def lookup(request):
    if request.GET.has_key(u'q'):
        value = request.GET[u'q']
        lst = Street.objects.filter(name__contains = value)
        if len(lst) < 2:
            lst.extend(Street.objects.filter(unsgined_name__contains = value))
        
        data = ""
        for i in lst:
            data += i.name + "\n"
        return HttpResponse(data)
    else:
        return HttpResponse("")

def get_information(request, id):
    return HttpResponse("This is a respond text.")
