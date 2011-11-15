#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv
import codecs
import cStringIO
from mapapp.models import Ward

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