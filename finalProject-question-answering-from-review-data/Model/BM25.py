import math


class bm25:
    def __init__(self, review, question, pairscore):
        self.review = review
        self.question = question
        self.pairscore = pairscore
        
    def getIDF(self, ques, review_l):
        count = 0
        for r in review_l:
            if ques in r["words"]:
                count += 1
    
        num = len(review_l)-count+0.5
        den = count+0.5
        idf_val = math.log(num) - math.log(den)
        return idf_val

    def get_avgdl(self, review_l):
        length = 0
        for r in review_l:
            length += len(r["sentence"])
        avg = length/len(review_l)
        #nneed to fix this
        if avg == 0:
            avg == 1
        return avg

    def okapi(self):
        k1, b = (1.2+2)/2, 0.75
    
        for item in self.question:
            if item not in self.review:
                continue
            if item not in self.pairscore:
                self.pairscore[item] = dict()
            for q in self.question[item]:
                if q["ID"] not in self.pairscore[item]:
                    self.pairscore[item][q["ID"]] = dict()
                # calculate avgdl
                avgdl = self.get_avgdl(self.review[item])
                norm_bm, norm_bmm = 0,0
                #find term frequency
                for r in self.review[item]:
                    if r["ID"] not in self.pairscore[item][q["ID"]]:
                        self.pairscore[item][q["ID"]][r["ID"]] = dict()
                    score = 0
                    index = 0
                    score1 = 0
                    for word in q["words"]:
                        # taking review as doc get idf for each word in query
                        idf = self.getIDF(word, self.review[item])
                        if word not in r["words"]:
                            w = 0
                        else:
                            w = r["words"][word]
                        num = (k1 +1)*w
                        den = w + k1 *(1-b +b *(len(r["sentence"])/avgdl))
                        score += idf*(num/den)
                        score1+=idf
                    self.pairscore[item][q["ID"]][r["ID"]]["BM25"] = score
                    self.pairscore[item][q["ID"]][r["ID"]]["BM25+"] = score1
                    norm_bm += score
                    norm_bmm += score1
                for r in self.review[item]:
                    if norm_bm != 0:
                        self.pairscore[item][q["ID"]][r["ID"]]["BM25"] /= norm_bm
                    if norm_bmm !=0:
                        self.pairscore[item][q["ID"]][r["ID"]]["BM25+"] /= norm_bmm
                    self.pairscore[item][q["ID"]][r["ID"]]["BM25+"] += self.pairscore[item][q["ID"]][r["ID"]]["BM25"]
                    self.pairscore[item][q["ID"]][r["ID"]].pop("BM25", 0)
                    #print q["ID"], r["ID"]
        return self.pairscore