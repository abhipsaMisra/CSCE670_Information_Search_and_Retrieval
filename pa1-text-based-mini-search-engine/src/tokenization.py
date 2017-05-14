# Your parser function here. It will take the two option variables above as the parameters
# add cells as needed to organize your code
import re
import os
import time

from nltk.stem.porter import PorterStemmer

def tokenize(use_stemming, use_casefolding):
    data_path = '../data/southpark_scripts/'
    porter_stemmer = PorterStemmer()
    wordlist = set()
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path, fname)
        f = open(path, 'r')
        for line in iter(f):
            for term in re.findall(r'\w+', line):
                if(use_casefolding):
                    if(use_stemming):
                        wordlist.add(porter_stemmer.stem(term.lower()))
                    else:
                        wordlist.add(term.lower())
                else:
                    if(use_stemming):
                        wordlist.add(porter_stemmer.stem(term))
                    else:
                        wordlist.add(term)
        f.close()
    print "Stemming: %s | CaseFolding: %s" %(use_stemming,use_casefolding)
    print "length : %s" %len(wordlist)
    print wordlist

start_time = time.time()
tokenize(True, True)
print("--- %s seconds ---" % (time.time() - start_time))
