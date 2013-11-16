import urllib
import re
from collections import Counter

def words(text): return re.findall('[a-z]+', text.lower())

url = "http://norvig.com/big.txt"
text = urllib.urlopen(url).read()
words = words(text)
freqs = Counter(words)
with open("sowpods.txt") as f:
    dictionary = f.read().lower().split()
outputfile = open("freqs.csv", "w")
for word in freqs:
    if word in dictionary:
        outputfile.write("%s,%s\n" %(word, freqs[word]))
outputfile.close()
