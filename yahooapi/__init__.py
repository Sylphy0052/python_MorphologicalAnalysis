# vim:fileencoding=utf-8
#
# yahooapi - Yahoo WEB API wrapper for python
# Copyright (c) 2007-2008, Yusuke Inuzuka(http://inforno.net/)
#
# License :
#   Artistic License 2.0
#
__author__  = u"Yusuke Inuzuka"
__author_email__   = u"yuin@inforno.net"
__version__ = u"0.2"
__date__    = u"2008-05-28"

import sys
import os
import urllib2
from sets import Set
import xml.dom.minidom as minidom
import re
from urllib import urlencode
from types import *

def urlparam(dict) :
  return urlencode([(k, unicode(v).encode("utf-8")) for k,v in dict.items()])

#constants
BAD_REQUEST = 400
FORBIDDEN   = 403
SERVICE_UNAVAILABLE = 503

class Storage(dict):
    def __getattr__(self, key): 
        if self.has_key(key): 
            return self[key]
        raise AttributeError, repr(key)
    def __setattr__(self, key, value): 
        self[key] = value
    def __repr__(self):     
        return '<Storage ' + dict.__repr__(self) + '>'

class Error(StandardError):
  def __init__(*args):
    StandardError.__init__(*args)

class ApiError(Error):
  def __init__(self, code, message):
    Error.__init__(self, u"Yahoo API error:\n code: %s\n message: %s\n" % (code, message))

class ApiRequest(object) :
  def __init__(self, frontend):
    self.frontend = frontend

  def call(self, method, api_version = "V1", *dummy, **params) :
    fe = self.frontend
    url = fe.url_format % {"version":api_version, "method":method}
    params["appid"] = fe.appid
    http_method = (method in fe.http_method_get) and "GET" or "POST"
    params = urlparam(params)
    data = ""
    try:
      response_code = 200
      if http_method == "POST":
        data = urllib2.urlopen(url, params).read()
      else:
        data = urllib2.urlopen(url+u"?"+params).read()
    except urllib2.HTTPError, e:
      response_code = e.code
      if e.code >= BAD_REQUEST : raise ApiError(e.code, data)
    return self.frontend.result_class(data, response_code)

class Result(object) :
  xml_root_name = "ResultSet"
  def __init__(self, raw_xml, response_code) :
    self.response_code = response_code
    self.is_error = response_code >= BAD_REQUEST 
    if response_code <= BAD_REQUEST:
      self._xml_root_name = self.is_error and "Error" or self.xml_root_name
      self.doc = minidom.parseString(raw_xml)
      self.parse_data()
      if self.is_error: raise ApiError(response_code, self.message)

  def parse_data(self) :
    all_data = dict()
    def func(elm, data) :
      is_arr = False
      name = elm.nodeName
      node = data.get(name)
      if node :
        is_arr = True
        if not isinstance(node, [].__class__):
          data[name] = [data[name]]
      children_size = len(elm.childNodes)
      if children_size == 0 :
        value = ""
      elif children_size == 1 and elm.childNodes[0].nodeType == minidom.Node.TEXT_NODE :
        value = elm.childNodes[0].data
        if value.isdigit(): value = int(value)
      else :
        value = dict()
        for child in elm.childNodes :
          func(child, value)
        value = Storage(value)
      if is_arr :
        data[name].append(value)
      else :
        data[name] = value
    func(self.doc, all_data)
    self.data = Storage(all_data["#document"][self._xml_root_name])

  def __getattr__(self, key): 
    if self.data.has_key(key): 
      return self.data[key]
    raise AttributeError, repr(key)

  def __repr__(self):     
      return '<yahooapi.Result ' + dict.__repr__(self.data) + '>'


class YahooAPI(object):
  http_method_get = Set([])
  result_class    = None
  url_format      = ""

  def __init__(self, appid):
    self.appid = appid
    self._api = ApiRequest(self)
    parent = self
    class ApiWrapper(object) :
      class _element(object) :
        def __init__(self, key) :
          self.key = key
        def __getattr__(self, key) :
          return self.__class__(".".join([self.key, key]))
        def __call__(self, *args, **keywords) :
          return parent._api.call(self.key, **keywords)

      def __init__(self): pass
      def __getattr__(self, key):
        return self._element(key)
    self.api = ApiWrapper()

  def __getattr__(self, key): 
    return getattr(self.api, key)
