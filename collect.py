import twint

pozitive = [":)","<3","😀","😃","😄","😁","😆","😅","😂","🤣","☺️","😊","😇","🙂","🙃","😍","🤓","😎","👏","👍","🙏","❤️"]
negative = [":(","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","😢","😭","😤","😠","😡","😥","😓","🤒"]

c = twint.Config()
c.Lang = "tr"
c.Limit = 10000
c.Store_csv = True
c.Custom["tweet"] = ["tweet"]
c.Hide_output = True

count = 1
for p in pozitive:
    print(p)
    c.Output = "p" + str(count) +".txt"
    c.Search = p
    twint.run.Search(c)
    count += 1

count = 1
for n in negative:
    print(n)
    c.Output = "n" + str(count) +".txt"
    c.Search = n
    twint.run.Search(c)
    count += 1