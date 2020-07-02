with open("dataset/positive_cut_words.txt", encoding="utf-8") as f:
    positive = f.readlines()
positive = [x.strip() for x in positive]

with open("dataset/negative_cut_words.txt", encoding="utf-8") as f:
    negative = f.readlines()
negative = [x.strip() for x in negative]

allwords = {}
for i in positive:
    word = i.split()[0]
    count = int(i.split()[1])
    allwords[word] = [count, 0]

for i in negative:
    word = i.split()[0]
    count = int(i.split()[1])
    if word in allwords:
        old = allwords[word]
        old[1] = count
        allwords[word] = old
    else:
        allwords[word] = [0, count]

allwords = dict(sorted(allwords.items(), key=lambda x:x))

f = open('dataset/all_words.txt', 'w', encoding='utf-8')
count = 1
for x,y in allwords.items():
    print(count)
    count += 1
    f.write(x + ' ' + str(y[0]) + ' ' + str(y[1]) + '\n')
f.close()