from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from operator import itemgetter, attrgetter
import math

def create_dict(question, review):
    make_ques(question)
    #print question['B0046HA9XQ']
    make_review(review, question)
    #print review['B0046HA9XQ']


def make_ques(question):
    en_stop = get_stop_words('en')
    p_stemmer = PorterStemmer()
    with open('questions_AppliancesO.txt') as fp:
        for line in fp:
            words = line.split()
            #not taking open ended question for now
            if len(words) == 0 or words[1] == "A":
                continue
            #product id
            if words[0] not in question:
                question[words[0]] = list()

            if words[1] == "Q":
                freq = list()
                line = ""
               # freq["words"] = dict()
               # freq["sentence"] = list()
               # freq["ID"] = words[3]
                for i in range(5, 5+int(words[4])):
                    line += " " + words[i]
                    if words[i] == ".":
                        continue
                    freq.append(words[i])
                # remove stop words from tokens
                freq = [i for i in freq if not i in en_stop]
                # stem tokens
                freq = [p_stemmer.stem(i) for i in freq]
                freq.append(line)

                question[words[0]].append(freq)

def make_review(review, question):
    en_stop = get_stop_words('en')
    p_stemmer = PorterStemmer()

    with open('reviews_Appliances2.txt') as fp:
        for line in fp:
            words = line.split()
            if len(words) == 0 or words[1] not in question:
                continue
            if words[1] not in review:
                review[words[1]] = list()
            freq = list()
            line = ""
            for i in range(5, 5+int(words[4])):
                line += " "+words[i]
                if words[i] == ".":
                    continue
                freq.append(words[i])
            # remove stop words from tokens
            freq = [i for i in freq if not i in en_stop]
            # stem tokens
            freq = [p_stemmer.stem(i) for i in freq]
            freq.append(line)

            review[words[1]].append(freq)



def find(question, review):
    for item in question:
        val = list()
        r_review = list()
        if item not in review:
            continue
        for x in review[item]:
            r_review.append(x[-1])
            val.append(x[:len(x)-1])
        qr = corpora.Dictionary(val)
        qr.save('auto_review.dict')
        corpus = [qr.doc2bow(text) for text in val]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        lda_model = models.LsiModel(corpus_tfidf, id2word=qr, num_topics=5)
        corpus_lsi = lda_model[corpus_tfidf]
        for i in range(0, len(corpus_lsi)):
            print i+1, r_review[i], corpus_lsi[i]#sorted(, key=itemgetter(1), reverse=True)

        c_list = dict()
        result = sorted(corpus_lsi[-1], key=lambda x: math.fabs(x[1]), reverse=True)
        print result
        for i in range(0, len(corpus_lsi) - 1):
            for x in corpus_lsi[i]:
                if x[0] == result[0][0]:
                    c_list[i] = x[1]
                    break

       # for key in c_list:
        #    print r_review[key]
        c_list = {x: math.fabs(c_list[x]) for (x, _) in c_list.iteritems()}
        print c_list
        sorted_x = sorted(c_list.items(), key=itemgetter(1), reverse=True)
        i = 0
        for key in sorted_x:
            if i > 0.05*(len(corpus_lsi)-1):
                break
            print r_review[key[0]], "\n"
            i += 1


question, review = dict(), dict()
create_dict(question, review)
find(question, review)