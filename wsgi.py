#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" python网络请求转发器，没有任何外部依赖，可以轻易将其部署到任何一个支持WSGI的托管空间，兼容Python2/3。    
用法：
  http://hostedurl?k=AUTHKEY&t=TIMEOUT&u=URL
  解析：
  hostedurl: 转发服务器的URL
  URL: 需要转发的url，需要先使用urllib.quote转义，特别是如果有&符号
  AUTHKEY: 为了防止滥用，需要提供一个key
  TIMEOUT: [可选]超时时间，默认为30s
"""
import os, socket
from wsgiref.util import is_hop_by_hop
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

ALLOW_KEY = os.environ.get('ALLOW_KEY') or 'xzSlE'
DEFAULT_TIMEOUT = 30
__Version__ = "1.4"

def msg(txt):
    return "<html><head><title>Url Forwarder</title></head><body><h3>Url Forwarder v{}</h3>{}</body></html>".format(__Version__, txt).encode('utf-8')

def application(environ, start_response):
    #from wsgiref.util import setup_testing_defaults
    #setup_testing_defaults(environ)
    
    # Parse query parameters
    query_string = environ.get('QUERY_STRING', '')
    query_params = dict(qc.split("=", 1) for qc in query_string.split("&") if "=" in qc)
    
    url = query_params.get('u')
    key = query_params.get('k')
    try:
        timeout = int(query_params.get('t', DEFAULT_TIMEOUT))
    except:
        timeout = DEFAULT_TIMEOUT
    
    if key and key != ALLOW_KEY:
        start_response('403 FORBIDDEN', [('Content-Type', 'text/html')])
        return [msg('Auth Key is invalid!')]
    
    if not url or not key:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [msg('<strong>Usage: </strong>thisurl?k=AUTHKEY&t=TIMEOUT&u=URL')]

    url = unquote(url).replace(' ', r'%20')
    parts = urlparse(url)
    referer = f'{parts.scheme}://{parts.netloc}'
    
    try:
        req = Request(url)
        req.add_header('User-Agent', "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        req.add_header('Accept-Language', "en,*")
        req.add_header('Referer', referer)
        ret = urlopen(req, timeout=timeout)
        content = ret.read()
        headers = [(n, v) for n, v in ret.info().items() if not is_hop_by_hop(n)]
        start_response('200 OK', headers)
        return [content]
    except socket.timeout:
        start_response('504 GATEWAY TIMEOUT', [('Content-Type', 'text/html')])
        return [msg('Timeout error')]
    except Exception as e:
        err_msg = str(e).replace("<", "&lt;").replace(">", "&gt;")
        print("ERROR : {} : {}".format(type(e), str(e)))
        start_response('400 BAD REQUEST', [('Content-Type', 'text/html')])
        return [msg('Error occurred: <br/>{}'.format(err_msg))]
    
app = application

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = int(os.environ.get('PORT', 5000))
    with make_server('0.0.0.0', port, application) as httpd:
        print("Serving on port {}...".format(port))
        httpd.serve_forever()
