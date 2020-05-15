import twint

pozitive = [":)","<3","😀","😃","😄","😁","😆","😅","😂","🤣","☺️","😊","😇","🙂","🙃","😍","🤓","😎","👏","👍","🙏","❤️"]
negative = [":(",":/","</3","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","😢","😭","😤","😠","😡","🤬","😥","😓","🤒"]

c = twint.Config()
c.Lang = "tr"
c.Limit = 10
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
    print(p)
    c.Output = "n" + str(count) +".txt"
    c.Search = n
    twint.run.Search(c)
    count += 1