# -*- encoding: utf-8 -*-
__author__ = 'Skyeyes'
from django.shortcuts import render_to_response
import hashlib
import re
from full.models import Short_url
from django.http import HttpResponseRedirect


def search(request):
    return render_to_response('search.html')


def short(request):
    long_url = request.GET['long_url']
    short_url = shorturl(long_url)
    if not Short_url.objects.filter(shortdata = short_url):
        Short_url.objects.create(shortdata = short_url, longdata = long_url)
    return render_to_response('result.html', {'short_url':short_url, 'long_url':long_url})


def recover(request):
    short_url = request.GET['short_url']
    key = re.findall('8000/(.*)', short_url)[0]
    urldata = Short_url.objects.filter(shortdata = key)[0]
    recover_url = urldata.longdata
    return render_to_response('result.html', {'short_url':key, 'long_url':recover_url})


def match(request, get_url):        #获取匹配到的短网址的值
    urldata = Short_url.objects.filter(shortdata = get_url)[0]
    url = urldata.longdata
    return HttpResponseRedirect(url)


# 1)将长网址md5生成32位签名串,分为4段, 每段8个字节;
# 2)对这四段循环处理, 取8个字节, 将他看成16进制串与0x3fffffff(30位1)与操作, 即超过30位的忽略处理;
# 3)这30位分成6段, 每5位的数字作为字母表的索引取得特定字符, 依次进行获得6位字符串;
# 4)总的md5串可以获得4个6位串; 取里面的任意一个就可作为这个长url的短url地址;
# 这种算法,虽然会生成4个,但是仍然存在重复几率,下面的算法一和三,就是这种的实现.


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

