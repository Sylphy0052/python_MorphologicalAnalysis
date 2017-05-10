import nltk
from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.text import Text

jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^　「」！？。]*[！？。]')

jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[^ぁ-んァ-ンー\u4e00-\u9FFF]+)')

ginga = PlaintextCorpusReader("./", r'sample.txt', encoding='utf-8', para_block_reader=read_line_block, sent_tokenizer=jp_sent_tokenizer, word_tokenizer=jp_chartype_tokenizer)

print(ginga.raw())

print('/'.join(ginga.words()))

# ginga_t = Text(w.encode('utf-8') for w in ginga.words())
#
# ginga_t.concordance('川')
