# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindOfPerson, KindOfConstruction, Construction, Street, District,\
    Comment
from django.utils import translation
from django.http import HttpResponse, Http404
from mapapp.forms import CommentForm
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _

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
                   
    return render_to_response('index.html', {'kind_person'       : kind_person,
                                             'kind_construction' : kind_construction,
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

def get_information(request, id_object):
    try:
        con = Construction.objects.get(id = id_object)
        if hasattr(con.link_image, 'url'):
            url = con.link_image.url
        else:
            url = ""
        data = { "results" : {
                        "id"      : str(con.id),
                        "name"    : con.name,
                        "details" : con.description_detail.replace('\n', '<br>'),
                        "image"   : url
                    }  
               }
    except:
        data = { "results" : {} }
    return HttpResponse(json.dumps(data), mimetype = "application/json")


def kind_person_filter(request):
    id1 = request.GET.get('id1', '')
    lst = Construction.objects.filter(kind_of_person = id1)
    mData = {}    
    mArray = []
    for obj in lst:
        temp = {}
        temp['id'] = obj.id
        temp['address'] = obj.get_address()
        mArray.append(temp)        
    mData["results"] = mArray
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json")

def kind_construction_filter(request):
    id1 = request.GET['id1']
    lst = Construction.objects.filter(kind_of_construction = id1)
    mData = {}    
    mArray = []
    for obj in lst:
        temp = {}
        temp['id'] = obj.id
        temp['address'] = obj.get_address()
        mArray.append(temp)        
    mData["results"] = mArray
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json")

def district_filter(request):
    id_district  = request.GET['id_district']
    construction = Construction.objects.filter(district = id_district ) 
    mData          = {}
    tmp          = {}
    mArray       = []
    for obj in construction:
        tmp['id']      = obj.id
        tmp['address'] = obj.get_address()
        mArray.append(tmp)
    mData["results"] = mArray
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json")

@csrf_protect    
def get_details(request, id_object):
    msg = None
    try:
        con = Construction.objects.get(id = id_object)
        comments = Comment.objects.filter(construction = con).order_by('-comment_date')
    except:
        raise Http404()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(email = form.data['email'], 
                              content = form.data['content'])
            comment.construction = con
            comment.save()
            msg = _('Your comment sent.') 
            form = CommentForm()                   
    else:
        form = CommentForm()

    return render_to_response('details.html', 
                        { "form" : form, "con" : con, 'msg' : msg, 'comments' : comments},
                        context_instance = RequestContext(request))    
