import Levenshtein as lev
from strsimpy.levenshtein import Levenshtein
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from strsimpy.damerau import Damerau
from strsimpy.optimal_string_alignment import OptimalStringAlignment
from strsimpy.jaro_winkler import JaroWinkler
from strsimpy.ngram import NGram
from strsimpy.qgram import QGram

qgram = QGram(2)
print(qgram.distance('ABCD', 'ABCE'))

twogram = NGram(2)
print(twogram.distance('ABCD', 'ABTUIO'))

s1 = 'Adobe CreativeSuite 5 Master Collection from cheap 4zp'
s2 = 'Adobe CreativeSuite 5 Master Collection from cheap d1x'
fourgram = NGram(4)
print(fourgram.distance(s1, s2))

jarowinkler = JaroWinkler()
print(jarowinkler.similarity('My string', 'My tsring'))
print(jarowinkler.similarity('My string', 'My ntrisg'))

optimal_string_alignment = OptimalStringAlignment()
print(optimal_string_alignment.distance('CA', 'ABC'))

damerau = Damerau()
print(damerau.distance('ABCDEF', 'ABDCEF'))
print(damerau.distance('ABCDEF', 'BACDFE'))
print(damerau.distance('ABCDEF', 'ABCDE'))
print(damerau.distance('ABCDEF', 'BCDEF'))
print(damerau.distance('ABCDEF', 'ABCGDEF'))
print(damerau.distance('ABCDEF', 'POIU'))

normalized_levenshtein = NormalizedLevenshtein()
print(normalized_levenshtein.distance('My string', 'My $string'))
print(normalized_levenshtein.distance('My string', 'My $string'))
print(normalized_levenshtein.distance('My string', 'My $string'))

print(normalized_levenshtein.similarity('My string', 'My $string'))
print(normalized_levenshtein.similarity('My string', 'My $string'))
print(normalized_levenshtein.similarity('My string', 'My $string'))

levenshtein = Levenshtein()
print(levenshtein.distance('My string', 'My $string'))
print(levenshtein.distance('My string', 'My $string'))
print(levenshtein.distance('My string', 'My $string'))
print(lev.distance('Normalized Levenshtein', 'Weighted Levenshtein'))