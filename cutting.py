from collections import Counter

with open("dataset/clean_negative_sentences.txt", encoding="utf-8") as f:
    content = f.readlines()
content = [x.strip() for x in content]

wordlist = []
for line in content:
    wordlist += line.split()

for i in range(len(wordlist)):
    wordlist[i] = wordlist[i][:5]

words = dict(Counter(wordlist))
words = dict(sorted(words.items(), key=lambda x:x))

f = open('dataset/negative_cut_words.txt', 'w', encoding='utf-8')
count = 1
for x,y in words.items():
    print(count)
    count += 1
    f.write(x + ' ' + str(y) + '\n')
f.close()