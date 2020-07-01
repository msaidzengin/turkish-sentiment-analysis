import string
import re

with open("dataset/negative_sentences.txt", encoding="utf-8") as f:
    content = f.readlines()
content = [x.strip() for x in content] 

whitelist = set('abcçdefgğhıijklmnoöprsştuüvwxyz ')

f = open('dataset/clean_negative_sentences.txt', 'w', encoding='utf-8')
for text in content:
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    text = ''.join(filter(whitelist.__contains__, text))
    text = ' '.join(filter(lambda x:x[:10]!='pictwitter' and x[:4]!='http', text.split()))
    if text != '':
        f.write(text + '\n')
f.close()
