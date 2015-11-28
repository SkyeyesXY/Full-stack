# Full-stack(1)-短网址

标签（空格分隔）：fullstack

---
|框架|前端语言|后台语言|
|:---:|:---:|:---:|
|Django|Html,CSS|Python|
##1.思路
###1)短网址生成
> * 用python自带的哈希库生成网址的hash值
> * 1)将长网址hash生成32位签名串,分为4段, 每段8个字节;
2)对这四段循环处理, 取8个字节, 将他看成16进制串与0x3fffffff(30位1)与操作, 即超过30位的忽略处理;
3)这30位分成6段, 每5位的数字作为字母表的索引取得特定字符, 依次进行获得6位字符串;
4)总的hash串可以获得4个6位串; 取里面的任意一个就可作为这个长url的短url地址;**本网站取得第一个**
> * 由上述步骤生成6位的短网址字符串
> * 加上本地前缀`http://127.0.0.1:8000/`即为完整的短网址

代码:
```python
import hashlib

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
```

**不足:**
> * hash的生成方法有一定的重复几率

###2)短网址储存
> * 在生成短网址的同时,在数据库中生成包含短网址,原网址的数据
####a.Django
在models.py中
```python
from django.db import models

class Short_url(models.Model):
    shortdata = models.CharField(max_length = 100)
    longdata = models.CharField(max_length = 100)
```

####b.flask
使用了SQLAlchemy数据库插件
```python
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Short_url(db.Model):
    __tablename__ = 'short-urls'
    id = db.Column(db.Integer, primary_key=True)
    shortdata = db.Column(db.String(100), unique=True)
    longdata = db.Column(db.String(100), unique=True)

    def __init__(self, shortdata, longdata):
        self.shortdata = shortdata
        self.longdata = longdata

    def __repr__(self):
        return '<Role %r>' % self.shortdata


db.drop_all()
db.create_all()
```


> * 防重机制:在生成短网址时进行判断,如果该短网址存在于数据库中则不在生成新数据

###3)自定义短网址
> * 在html文件中获取`get[自定义输入]`
> * 如果自定义输入不为空,则跳过MD5生成短网址块,将自定义的短网址和原网址存入数据库中

####a.在django中
在views.py中
```python
key = request.GET['diy_url']
if key != '':
    short_url = key
```
####b.在flask中
与django中做法基本相同


###4)恢复原网址
> * 运用python的正则表达式`re`匹配输入的网址的6位识别字符串部分
> * 根据匹配到的字符串在数据库中查找

在views.py中
```python
short_url = request.GET['short_url']
key = re.findall('8000/(.*)', short_url)[0]
urldata = Short_url.objects.filter(shortdata = key)[0]
recover_url = urldata.longdata
```

###5)重定向短网址
> * 利用Django的重定向功能,在匹配到识别字符串后在数据库中调出原网址进行重定向

####a.Django

在views.py中
```python
urldata = Short_url.objects.filter(shortdata = get_url)[0]
url = urldata.longdata
return HttpResponseRedirect(url)
```

在urls.py中
```python
    url(r'(.+)/$', match),      #匹配到识别字符串
```

####b.Flask
```python
@app.route('/<get_url>')
def match(get_url):        #获取匹配到的短网址的值
    urldata = Short_url.query.filter_by(shortdata = get_url).first()
    url = urldata.longdata
    return redirect(url)
```

##2.页面设置
###1)思路
> * 在同一页中进行全部功能
> * 利用html的if语句进行判断显示
> * 利用html的继承来进行相应后的显示

-----
作者:Skyeyes
时间:2015.11.24







