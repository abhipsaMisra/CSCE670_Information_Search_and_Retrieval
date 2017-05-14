import re
import os
import time
import math
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
import operator

porter_stemmer = PorterStemmer()

class Rank_retrieval:

    def __init__(self):
        self.index= defaultdict(list)
#        self.data_path = './southpark_scripts_subset'
        self.data_path = '../data/southpark_scripts/'
        self.use_stemming = True
        self.use_casefolding = True
        self.no_of_docs = 0
        self.doc_set = set()
        self.tf_raw = {}
        self.tf={}
        self.idf={}
        self.search_tf_raw = {}
        self.tf_idf = {}
        self.tf_idf_norm = {}
        self.cosine_sim = {}
        self.search_terms_count = 0

    def create_index(self):
        for fname in os.listdir(self.data_path):
            terms = set()
            if ((fname[0] == '.') or (fname.endswith(".txt") != True)):
                continue
            self.no_of_docs += 1
            file_id = os.path.splitext(fname)[0]
            path = os.path.join(self.data_path, fname)
            f = open(path, 'r')
            freq = {}
            for line in iter(f):
                terms = self.tokenize(line,terms,freq,type="doc")
            self.tf_raw[file_id] = freq
            freq = {}
            terms_per_page = {}

            for position, term in enumerate(terms):
                if (term in terms_per_page):
                    terms_per_page[term][1].append(file_id)
                else:
                    terms_per_page[term] = file_id

            f.close()

            for term_per_page, posting_list_page in terms_per_page.iteritems():
                self.index[term_per_page].append(posting_list_page)

        return self.index

    def tokenize(self,line,word_list,freq,type):
        for term in re.findall(r'\w+', line):
            term_key = ''
            if (self.use_casefolding):
                if (self.use_stemming):
                    term_key = porter_stemmer.stem(term.lower())
                else:
                    term_key = term.lower()
            else:
                if (self.use_stemming):
                    term_key = porter_stemmer.stem(term)
                else:
                    term_key = term
            word_list.add(term_key)
            freq.setdefault(term_key, 0)
            freq[term_key] += 1
            if type == "query":
                self.search_tf_raw[term_key] = freq[term_key]
                self.search_terms_count += freq[term_key]
        return word_list

    def calculate_idf(self):
        for term in self.index:
            self.idf[term] = math.log10(float(self.no_of_docs)/len(self.index[term]))
        return self.idf

    def calculate_tf(self):
        for doc_id in self.doc_set:
            wf_raw = {}
            for term, tf_raw_value in (self.tf_raw[doc_id]).iteritems():
                wf = 1 + math.log10(tf_raw_value)
                wf_raw[term] = wf
            self.tf[doc_id] = wf_raw


    def calculate_tf_idf(self,search_terms):
        tf_idf_list = {}
        tf_idf_sqr_sum = 0
        for search_term in search_terms:
            for doc_id_list in self.index[search_term]:
                self.doc_set.add(doc_id_list)
        if len(self.doc_set) > 0:
            self.calculate_tf()
        for doc_id in self.doc_set:
            for term, tf_value in (self.tf[doc_id]).iteritems():
                tf_idf_value = tf_value * self.idf[term]
                tf_idf_list[term] = tf_idf_value
                tf_idf_sqr_sum += (tf_idf_value**2)
            tf_idf_list['tf_idf_sqr_sum'] = tf_idf_sqr_sum
            self.tf_idf[doc_id] = tf_idf_list
            tf_idf_sqr_sum = 0
            tf_idf_list = {}
        return self.tf_idf


    def calculate_tf_idf_norm(self):
        for doc_id in self.doc_set:
            tf_idf_norm = {}
            tf_idf_sqr_sum = self.tf_idf[doc_id]['tf_idf_sqr_sum']
            for term, tf_value in (self.tf_idf[doc_id]).iteritems():
                tf_idf_norm[term] = float(tf_value/float(math.sqrt(tf_idf_sqr_sum)))
            self.tf_idf_norm[doc_id] = tf_idf_norm
        return self.tf_idf_norm

    def calculate_cosine_sim(self,search_terms):
        for doc_id in self.doc_set:
            cosine_sim = 0
            for term in search_terms:
                if term in self.tf_idf_norm[doc_id]:
                    cosine_sim += float((self.tf_idf_norm[doc_id][term]*self.search_tf_raw[term])/float(math.sqrt(self.search_terms_count)))
            self.cosine_sim[doc_id] = cosine_sim
        sorted_list = list(reversed(sorted(self.cosine_sim.items(), key=operator.itemgetter(1))))
        print("Top 5 results : ")
        print sorted_list[:5]
        return self.cosine_sim

    def rank_retrieval(self):
        start_time = time.time()
        self.index = self.create_index()
        self.idf = self.calculate_idf()
        print("---Inverted Index Built : %s seconds ---" % (time.time() - start_time))
        while True:
            search_text = raw_input('Input Ranked Retrieval:')
            search_terms = set()
            if search_text == '':
                break
            search_terms = self.tokenize(search_text,search_terms,self.search_tf_raw,type="query")
            self.tf_idf = self.calculate_tf_idf(search_terms)
            self.tf_idf_norm = self.calculate_tf_idf_norm()
            self.cosine_sim = self.calculate_cosine_sim(search_terms)

if __name__=='__main__':
    q=Rank_retrieval()
    q.rank_retrieval()
