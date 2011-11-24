#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv
import codecs
import cStringIO
from mapapp.models import Construction
import json
import urllib2
from django.utils.http import urlquote
import threading
from threading import Thread
from timeit import Timer
import time
from django.db import transaction
import logging
import datetime


logger = logging.getLogger(__name__)

def unsigned_vi(vi_str):
    if isinstance(vi_str, unicode): 
        vi_str = "".join([c.encode('utf-8') for c in vi_str])
        
    text_to_find = "áàảãạâấầẩẫậăắằẳẵặđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶĐÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ"
    text_to_find = [ch.encode('utf8') for ch in unicode(text_to_find, 'utf8')]
    text_to_replace = 'a'*17 + 'd' + 'e'*11 + 'i'*5 + 'o'*17 + 'u'*11 + 'y'*5 + \
                      'A'*17 + 'D' + 'E'*11 + 'I'*5 + 'O'*17 + 'U'*11 + 'Y'*5
    r = re.compile("|".join(text_to_find))
    replaces_dict = dict(zip(text_to_find, text_to_replace))
    return r.sub(lambda m: replaces_dict[m.group(0)], vi_str)
    
def get_address(address):
    lst = address.split(',')
    result = []
    result.append(lst[0][:lst[0].find(' ')])
    result.append(lst[0][lst[0].find(' ') + 1 :])
    if lst[1].find(u'Phường'.encode('utf-8')) <> -1:
        result.append(lst[1].strip())
    else:
        result.append('')
        try:
            if lst[1].find(u'Quận'.encode('utf-8')) <> -1:
                result.append(lst[1].strip())
        except:
            raise Exception("Missed District") 
            
    if len(lst) > 2:
        try:
            if lst[2].find(u'Quận'.encode('utf-8')) <> -1:
                result.append(lst[2].strip())
        except:
            raise Exception("Missed District")
    
    return result

@transaction.autocommit    
def get_location():
    logger.info("\t\t ****************** Starting get location at " + str(datetime.datetime.now()) + " ******************")
    con_lst = Construction.objects.filter(location = '')
    for con in con_lst:
        address = con.get_address()
        req = json.load(urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=' + 
                        urlquote(address)))
        if req['status'] == u'OK':
            lat = req['results'][0]['geometry']['location']['lat']
            lng = req['results'][0]['geometry']['location']['lng']
            con.location = '(%s, %s)' % (str(lat), str(lng))
            con.save()
            logger.info(address + ': (%s, %s)' % (str(lat), str(lng)))
            
    logger.info("\t\t ****************** End get location at " + str(datetime.datetime.now()) + " ******************")        
    time.sleep(3600)       

class LocationGetter(threading.Thread):
    def __init__(self):
        Thread.__init__(self,)
    
    def run(self):
        t = Timer("get_location()", "from mapapp.utils import get_location")
        t.repeat(1)    
    
    
    pass
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self
    
    def next(self):
        return self.reader.next().encode("utf-8")

class CsvUnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
    
class CsvUnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)