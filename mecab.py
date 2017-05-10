import MeCab

mecab = MeCab.Tagger('-Ochasen')

for line in open('sample.txt', 'r'):
    result = mecab.parse(line)
    print(result)
