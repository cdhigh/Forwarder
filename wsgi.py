#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" python网络请求转发器，可以轻易将其部署到任何一个支持WSGI的托管空间，兼容Python2/3。    
用法：
  http://hostedurl?k=AUTHKEY&t=timeout&u=url
  解析：
  hostedurl: 你搭建的转发服务器的URL
  url: 需要转发的url，需要先使用urllib.quote转义，特别是如果有&符号
  AUTHKEY: 为了防止滥用，需要提供一个key
  timeout: [可选]超时时间，默认为30s
 """

__Version__ = "1.3"
__Author__ = "cdhigh <https://github.com/cdhigh>"

try:
    from urllib.parse import unquote, urlparse
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib import unquote, urlparse
    import urllib2
    Request = urllib2.Request
    urlopen = urllib2.urlopen
    URLError = urllib2.URLError

from wsgiref.util import is_hop_by_hop
import os, socket, bottle

ALLOW_KEY = os.environ.get('ALLOW_KEY') or 'xzSlE'

app = bottle.Bottle()
application = app

@app.route(r'/')
def Home():
    resp = bottle.response
    qry = bottle.request.query
    url, k, timeout = qry.u, qry.k, int(qry.get('t', '30'))
    if k and k != ALLOW_KEY:
        return 'Auth Key is invalid!'
    
    if url and k:
        url = unquote(url).replace(' ', r'%20')
        parts = urlparse(url)
        referer = '%s://%s' % (parts.scheme, parts.netloc)
        try:
            req = Request(url)
            req.add_header('User-Agent', "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
            req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
            req.add_header('Accept-Language', "en,*")
            req.add_header('Referer', referer)
            ret = urlopen(req, timeout=timeout)
            content = ret.read()
            headers = [(n, v) for n, v in ret.info().items() if not is_hop_by_hop(n)]
            cookieAdded = False
            for n, v in headers:
                if n == 'Set-Cookie' and cookieAdded:
                    resp.add_header(n, v)
                else:
                    resp.set_header(n, v)
                    if n == 'Set-Cookie':
                        cookieAdded = True
            return content
        except socket.timeout:
            pass
        except Exception as e:
            print("ERR : %s : %s" % (type(e), str(e)))
            bottle.abort(400)
    else:
        return "<html><head><title>Forwarder Url</title></head><body>Forwarder(%s) : thisurl?k=AUTHKEY&t=timeout&u=url</body></html>" % __Version__

if __name__ == '__main__':
    #bottle.run(reloader=True) #for debug in computer
    bottle.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))) #for Heroku
