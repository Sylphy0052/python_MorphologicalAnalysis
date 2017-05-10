import nltk
from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.text import Text
from chasen import *

jeita = ChasenCorpusReader('./', '*.chasen', encoding='utf-8')
