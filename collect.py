import twint

pozitive = [":)","<3","😀","😃","😄","😁","😆","😅","😂","🤣","☺️","😊","😇","🙂","🙃","😍","🤓","😎","👏","👍","🙏","❤️"]
negative = [":(",":/","</3","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","😢","😭","😤","😠","😡","🤬","😥","😓","🤒"]

print(len(pozitive))
print(len(negative))
exit(0)
c = twint.Config()
c.Lang = "tr"
c.Limit = 10
c.Store_json = True
c.Custom["tweet"] = ["id", "tweet"]
c.Output = "pozitive.json"
c.Hide_output = True


"""
for p in pozitive:
    c.Search = p
    twint.run.Search(c)
"""

c.Output = "negative.json"
for n in negative:
    c.Search = n
    twint.run.Search(c)