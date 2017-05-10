# vim:fileencoding=utf-8
#
# yahooapi.jlp - Yahoo JLP API wrapper for python
# Copyright (c) 2007-2008, Yusuke Inuzuka(http://inforno.net/)
#
# License :
#   Artistic License 2.0
#
# Synopsis:
#   import yahooapi.jlp as jlp
#   client = jlp.MAServiceAPI("your_appid")
#   result = client.parse(sentence=u"庭には二羽ニワトリがいる。", results= jlp.MA+jlp.UNIQ, filter = jlp.VERB + jlp.NOUN)
#   print result.ma_result.word_list.word[0].surface
#   # => u"庭"
#   print result.ma_result.word_list.word[0].reading
#   # => u"にわ"


__author__  = u"Yusuke Inuzuka"
__author_email__   = u"yuin@inforno.net"
__version__ = u"0.2"
__date__    = u"2008-05-28"

import sys, os.path
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__)).decode(sys.getfilesystemencoding())))
from sets import Set
import yahooapi

class AddParam(object):
  DELIM = ","
  def __init__(self, v):
    self.v = [v]
  def __str__(self):
    return self.DELIM.join(self.v)
  def __add__(self, n):
    self.v.append(n.v[0])
    return self
  def __sub__(self, n):
    self.v.remove(n.v[0])
    return self

class ResultType(AddParam): DELIM = "," ;
class WordTypeFilter(AddParam): DELIM = "|" ;

MA = ResultType(u"ma")
UNIQ = ResultType(u"uniq")

ADJ = WordTypeFilter("1")
KEIYOU_SHI = ADJ

NADJ = WordTypeFilter("2")
KEIYOUDOU_SHI = NADJ

INTERJ = WordTypeFilter("3")
KANDOU_SHI = INTERJ

ADV = WordTypeFilter("4")
FUKU_SHI = ADV

RENTAI_SHI = WordTypeFilter("5")

CONJ = WordTypeFilter("6")
SETSUZOKU_SHI = CONJ

PREFIX = WordTypeFilter("7")
SETTOU_JI = PREFIX

SUFFIX = WordTypeFilter("8")
SETSUBI_JI = SUFFIX

NOUN = WordTypeFilter("9")
MEI_SHI = NOUN

VERB = WordTypeFilter("10")
DOU_SHI = VERB

PART = WordTypeFilter("11")
JO_SHI = PART

ANOUN = WordTypeFilter("12")
JODOU_SHI = ANOUN

OTHER = WordTypeFilter("13")

WORD_TYPE_ALL = ADJ + NADJ + INTERJ + ADV + RENTAI_SHI + CONJ + PREFIX + SUFFIX + NOUN + VERB + PART + ANOUN + OTHER

class Result(yahooapi.Result) :
  xml_root_name = "ResultSet"

class MAServiceAPI(yahooapi.YahooAPI):
  result_class    = Result
  url_format      = "http://api.jlp.yahoo.co.jp/MAService/%(version)s/%(method)s"

class JIMServiceAPI(yahooapi.YahooAPI):
  result_class    = Result
  url_format      = "http://jlp.yahooapis.jp/JIMService/%(version)s/%(method)s"
