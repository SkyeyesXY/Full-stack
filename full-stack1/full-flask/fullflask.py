# -*- encoding: utf-8 -*-
__author__ = 'Skyeyes'
import os
from flask import Flask, render_template, request, abort, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import hashlib
import re


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


@app.route('/', methods=['GET'])
def toshow():
    args = request.args
    longurl = args.get('long_url')
    shorturl = args.get('short_url')
    diyurl = args.get('diy_url')

    if not shorturl and longurl:
        if bool(diyurl):
            shorturl = diyurl
        else:
            shorturl = short(longurl)
        if not Short_url.query.filter_by(shortdata = shorturl).first():
            if Short_url.query.filter_by(longdata = longurl).first():
                old = Short_url.query.filter_by(longdata = longurl).first()
                db.session.delete(old)
                db.session.commit()
            db.session.add(Short_url(shorturl, longurl))
            db.session.commit()
        return render_template('show1.html', short_url=shorturl)

    elif not longurl and shorturl:
        key = re.findall(':5000/(.*)', shorturl)[0]
        urldata = Short_url.query.filter_by(shortdata = key).first()
        recover_url = urldata.longdata
        return render_template('show2.html', long_url=recover_url)

    else:
        return render_template('search.html')


@app.route('/<get_url>')
def match(get_url):        #获取匹配到的短网址的值
    urldata = Short_url.query.filter_by(shortdata = get_url).first()
    url = urldata.longdata
    return redirect(url)


def short(url):
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


if __name__ == '__main__':
    app.run(debug=True)
