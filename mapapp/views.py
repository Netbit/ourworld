# Create your views here.
import json

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mapapp.models import KindPersonOfAccess, KindOfConstruction, Construction, Street, District,\
    Comment, Ward
from django.utils import translation
from django.http import HttpResponse, Http404
from mapapp.forms import CommentForm, InputFile
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from mapapp.utils import unsigned_vi, get_address, LocationGetter
import xlrd

#t = LocationGetter()
#t.start()
    
def home(request):
    lang = request.GET.get("lang", '')
    
    if request.session.has_key('django_language') == False:
        request.session['django_language'] = 'vi'
        
    if lang == '':
        lang = request.session['django_language']
        
    if request.session['django_language'] != lang:        
        request.session['django_language'] = lang
        
    translation.activate(lang)        
    #kind_person       = KindOfPerson.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    districts         = District.objects.all()
                   
    return render_to_response('index.html', {#'kind_person'       : kind_person,
                                             'kind_construction' : kind_construction,
                                             'districts'         : districts,
                                             }, 
                              context_instance = RequestContext(request))
    
    
    
def lookup(request):
    if request.GET.has_key(u'q'):
        value = request.GET[u'q']
        lst = Street.objects.filter(Q(name__contains = value) | Q(unsgined_name__contains = value))
        
        data = "\n".join([i.name for i in lst])
        return HttpResponse(data)
    else:
        return HttpResponse("\n")

def get_detail_of_construction(id_object):
    try:
        con = Construction.objects.get(id = id_object)
        return { "results" : {
                        "id"      : str(con.id),
                        "name"    : con.name,
                        "details" : con.description_detail.replace('\n', '<br>'),
                        "image"   : con.get_image()
                    }  
               }
    except:
        raise Exception('Object not found')
    
def get_information(request, id_object):
    data = { "results" : {} }
    try:        
        data = get_detail_of_construction(id_object)
    except:
        if request.GET.has_key(u'address'):
            address = request.GET['address'].split(',')[0].strip()
            number_or_alley = address[: address.find(' ')] 
            street_name = address[address.find(' ') + 1 :].strip()
            
            result = Construction.objects.filter(Q(number_or_alley__exact = number_or_alley),
                                                 Q(street__name = street_name) | Q(street__unsigned_name = street_name))
            
            if len(result) > 0:
                data = get_detail_of_construction(result[0].id)
            
    return HttpResponse(json.dumps(data, indent=2), mimetype = "application/json")


def kind_person_filter(request):
    id1 = request.GET.get('id1', '')
    lst = Construction.objects.filter(kind_of_person = id1)
    mData = {}           
    mData["results"] = [{'id' : obj.id, 'address' : obj.get_address()} for obj in lst]
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json")

def kind_construction_filter(request):
    id1 = request.GET['id1']
    lst = Construction.objects.filter(kind_of_construction = id1)
    mData = {}           
    mData["results"] = mData["results"] = [{'id' : obj.id, 'address' : obj.get_address()} for obj in lst]
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json")

def district_filter(request):
    id_district  = request.GET['id_district']
    construction = Construction.objects.filter(district = id_district ) 
    mData          = {}
    mData["results"] = [{'id' : obj.id, 'address' : obj.get_address()} for obj in construction]
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json")

@csrf_protect    
def get_details(request, id_object):
    msg = None
    try:
        con = Construction.objects.get(id = id_object)
        comments = Comment.objects.filter(construction = con, status='p').order_by('-comment_date')
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
    
def get_kind_person_contruction(request):
    kind_person       = KindPersonOfAccess.objects.all()
    kind_construction = KindOfConstruction.objects.all()
    mData             = {}
    mData["kind_person"]        = [{'id' : obj.id, 'name' : obj.name, 'image' : obj.get_image()} 
                                   for obj in kind_person]
    mData["kind_construction"]  = [{'id' : obj.id, 'name' : obj.name, 'image' : obj.get_image()} 
                                   for obj in kind_construction]
    
    return HttpResponse(json.dumps(mData), mimetype = "application/json") 

@login_required
@csrf_protect 
def upload_file(request):
    request.session['django_language'] = 'vi'
    translation.activate('vi')
    messages = []
    flag = 0
    if request.method == "POST":
        data_form = InputFile(request.POST, request.FILES)
        if request.FILES['data'].content_type != 'application/vnd.ms-excel':
            messages.append("Invalid file input!!")
            flag = 3
        elif request.user.is_superuser:            
            if data_form.is_valid():
                fo = open('temp.xls', 'wb')
                for line in request.FILES['data'].chunks():
                    fo.write(line)
                fo.close()
                reader = xlrd.open_workbook('temp.xls', encoding_override = 'utf-8').sheets()[0]                
                for line in range(1, reader.nrows):
                    row = reader.row(line)                             
                    try: 
                        try:
                            obj = Construction.objects.get(Q(name_vi = row[0].value) | Q(name_en = row[1].value))
                        except:
                            obj = Construction() 
                         
                        obj.name_vi = row[0].value
                        obj.unsigned_name = unsigned_vi(row[0].value)
                        obj.name_en = row[1].value
                        address = get_address(row[2].value.encode('utf-8'))
                        obj.number_or_alley = address[0]
                        obj.street = Street.objects.get_or_create(name = address[1])[0]
                        if address[2] != '':
                            ward = Ward.objects.get_or_create(name = address[2])[0]
                            obj.ward = ward                            
                        obj.district = District.objects.get_or_create(name = address[3])[0]
                        obj.description_detail = row[3].value
                        obj.description_detail_vi = row[3].value
                        obj.description_detail_en = row[4].value
                        obj.description_other = row[5].value
                        obj.description_other_vi = row[5].value
                        obj.description_other_en = row[6].value
                        obj.kind_of_construction = KindOfConstruction.objects.get_or_create(name = row[7].value)[0]
                        obj.save()
                        obj.kind_of_person.add(KindPersonOfAccess.objects.get_or_create(access_level = str(row[8].value))[0])
                        obj.save()
                        if flag == 0:
                            flag = 2                        
                    except:
                        messages.append(str(line))
                        flag = 1
                        continue
        else:
            messages.append("You must login by superuser permission to upload file")
            flag = 3
    else:
        data_form = InputFile()
        
    return render_to_response('admin/mapapp/construction/upload.html', {'form': data_form, "msgs" : ", ".join(messages), 'flag' : flag}, 
                              context_instance = RequestContext(request))         
            
                
