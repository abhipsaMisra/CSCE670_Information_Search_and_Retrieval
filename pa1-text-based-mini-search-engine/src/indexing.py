import re
import os
import time
from collections import defaultdict

from nltk.stem.porter import PorterStemmer

def retrieve_results(use_stemming, use_casefolding,search_query,index):
    search_terms = tokenize_query(use_stemming, use_casefolding, search_query)
    search_result = {}
    for term in search_terms:
        if term in index:
            search_result[term] = index[term]
        else:
            search_result = {}
            break;

    print ("Search List: %s" %search_result)
    if search_result != {}:
        search_result = reduce(lambda x, y: x & y, map(set, search_result.values()))
    print ("use_stemming: %s AND use_casefolding: %s" %(use_stemming, use_casefolding))
    print ("Search Query: %s" % search_query)
    print ("Result: %s" %search_result)

def tokenize_query(use_stemming, use_casefolding, search_query):
    porter_stemmer = PorterStemmer()
    query_list = set()
    for term in re.findall(r'\w+', search_query):
        if (use_casefolding):
            if (use_stemming):
                query_list.add(porter_stemmer.stem(term.lower()))
            else:
                query_list.add(term.lower())
        else:
            if (use_stemming):
                query_list.add(porter_stemmer.stem(term))
            else:
                query_list.add(term)
    return query_list

def tokenize(use_stemming, use_casefolding, f):
    porter_stemmer = PorterStemmer()
    word_list = set()

    for line in iter(f):
        for term in re.findall(r'\w+', line):
            if(use_casefolding):
                if(use_stemming):
                    word_list.add(porter_stemmer.stem(term.lower()))
                else:
                    word_list.add(term.lower())
            else:
                if(use_stemming):
                    word_list.add(porter_stemmer.stem(term))
                else:
                    word_list.add(term)

    return word_list

def create_index(use_stemming, use_casefolding, data_path):
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        file_id = os.path.splitext(fname)[0]
        path = os.path.join(data_path, fname)
        f = open(path, 'r')

        terms = tokenize(use_stemming, use_casefolding, f)
        terms_per_page = {}

        for position, term in enumerate(terms):
            if(term in terms_per_page):
                terms_per_page[term][1].append(file_id)
            else:
                terms_per_page[term] = file_id

        f.close()

        for term_per_page, posting_list_page in terms_per_page.iteritems():
            index[term_per_page].append(posting_list_page)
    return index

def retrieval(use_stemming, use_casefolding, data_path):
    start_time = time.time()
    index = create_index(use_stemming, use_casefolding,data_path)
    print("--- %s seconds ---" % (time.time() - start_time))
    search_text = raw_input('Boolean Search:')
    retrieve_results(use_stemming, use_casefolding,search_text, index)

index = defaultdict(list)
data_path = './southpark_scripts'
use_stemming = True
use_casefolding = True
retrieval(use_stemming, use_casefolding,data_path)