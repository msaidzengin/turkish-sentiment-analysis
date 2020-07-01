from TurkishStemmer import TurkishStemmer

with open("dataset/clean_positive_sentences.txt", encoding="utf-8") as f:
    content = f.readlines()
content = [x.strip() for x in content]

stemmer = TurkishStemmer()

f = open('dataset/stem_positive_sentences.txt', 'w', encoding='utf-8')
count = 1
for line in content:
    print(count)
    count += 1
    text = ' '.join([stemmer.stem(x) for x in line.split()])
    f.write(text + '\n')
f.close()