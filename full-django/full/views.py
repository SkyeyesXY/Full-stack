# -*- encoding: utf-8 -*-
__author__ = 'Skyeyes'
from django.shortcuts import render_to_response
import hashlib
import re
from full.models import Short_url
from django.http import HttpResponseRedirect

for each in Short_url.objects.all():
    each.delete()

def search(request):
    print(Short_url.objects.all())
    try:
        try:
            if request.GET['long_url']:
                long_url = request.GET['long_url']
                key = request.GET['diy_url']
                if key != '':
                    short_url = key
                else:
                    short_url = shorturl(long_url)
                if not Short_url.objects.filter(shortdata = short_url):
                    Short_url.objects.create(shortdata = short_url, longdata = long_url)
                return render_to_response('show1.html', {'short_url':short_url})
        except:
            if request.GET['short_url']:
                short_url = request.GET['short_url']
                key = re.findall('8000/(.*)', short_url)[0]
                urldata = Short_url.objects.filter(shortdata = key)[0]
                recover_url = urldata.longdata
                return render_to_response('show2.html', {'long_url':recover_url})

    except:
        return render_to_response('search.html')


def match(request, get_url):        #获取匹配到的短网址的值
    urldata = Short_url.objects.filter(shortdata = get_url)[0]
    url = urldata.longdata
    return HttpResponseRedirect(url)


def shorturl(url):
    base32 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
       'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
       'y', 'z',
       '0', '1', '2', '3', '4', '5'
    ]
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    hexStr = m.hexdigest()
    hexStrLen = len(hexStr)
    subHexLen = int(hexStrLen / 8)
    output = []
    for i in range(0,subHexLen):
        subHex = '0x'+hexStr[i*8:(i+1)*8]
        res = 0x3FFFFFFF & int(subHex,16)
        out = ''
        for j in range(6):
            val = 0x0000001F & res
            out += (base32[val])
            res = res >> 5
        output.append(out)
    output = output[0]
    return output

