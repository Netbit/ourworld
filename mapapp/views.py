# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindOfPerson, KindOfConstruction, Construction, Street, District
from django.utils import translation, simplejson
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from compiler.pycodegen import TRY_FINALLY
import json

    
def home(request):
    lang = request.GET.get("lang", '')
    
    if request.session.has_key('django_language') == False:
        request.session['django_language'] = 'vi'
        
    if lang == '':
        lang = request.session['django_language']
        
    if request.session['django_language'] != lang:        
        request.session['django_language'] = lang
        
    translation.activate(lang)        
    kind_person       = KindOfPerson.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    districts         = District.objects.all()
    default_district  = District.objects.get(unsigned_name = "Quan 1")
    construction      = Construction.objects.filter(district = default_district.id)
    location          = ''
    for con in construction:
        location += con.get_address()
        location += ';'
               
    return render_to_response('index.html', {'kind_person'       : kind_person,
                                             'kind_construction' : kind_construction,
                                             'location'          : location, 
                                             'districts'         : districts,
                                             }, 
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
    try:
        con = Construction.objects.get(id = id)
        data = { "results" : {
                        "details" : con.description_detail,
                        "image": con.link_image.url
                    }  
               }
    except:
        data = { "results" : {}
               }
    return HttpResponse(json.dumps(data), mimetype = "application/json")


def kind_person_filter(request):
    id1 = request.GET.get('id1', '')
    id2 = request.GET.get('id2', '')
    
    if id1 != '' and id2 != '':
        lst = Construction.objects.filter(kind_of_person = id1, kind_of_construction = id2)
    else:
        lst = Construction.objects.filter(kind_of_person = id1)
    
    map = {}    
    mArray = []
    for obj in lst:
        temp = {}
        temp['id'] = obj.id
        temp['address'] = obj.get_address()
        mArray.append(temp)
        
    map["results"] = mArray
    
    return HttpResponse(json.dumps(map), mimetype = "application/json")

def kind_construction_filter(request):
    id1 = request.GET['id1']
    id2 = request.GET['id2']
    
    if id1 != '' and id2 != '':
        lst = Construction.objects.filter(kind_of_construction = id1, kind_of_person = id2)
    else:
        lst = Construction.objects.filter(kind_of_construction = id1)
    
    map = {}    
    mArray = []
    for obj in lst:
        temp = {}
        temp['id'] = obj.id
        temp['address'] = obj.get_address()
        mArray.append(temp)
        
    map["results"] = mArray
    
    return HttpResponse(json.dumps(map), mimetype = "application/json")

