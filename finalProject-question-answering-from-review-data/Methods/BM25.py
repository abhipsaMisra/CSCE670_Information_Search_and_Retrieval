import math

def getIDF(ques, review_l):
    count = 0
    for r in review_l:
        if ques in r["words"]:
            count += 1

    num = len(review_l)-count+0.5
    den = count+0.5
    idf_val = math.log(num) - math.log(den)
    return idf_val

def get_avgdl(review_l):
    length = 0
    for r in review_l:
        length += len(r["sentence"])
    avg = length/len(review_l)
    #nneed to fix this
    if avg == 0:
        avg == 1
    return avg

def okapi(review, question, pairscore):
    k1, b = (1.2+2)/2, 0.75

    for item in question:
        if item not in review:
            continue
        if item not in pairscore:
            pairscore[item] = dict()
        for q in question[item]:
            if q["ID"] not in pairscore[item]:
                pairscore[item][q["ID"]] = dict()
            # calculate avgdl
            avgdl = get_avgdl(review[item])
            norm_bm, norm_bmm = 0,0
            #find term frequency
            for r in review[item]:
                #if q["ID"] == '1950':
                    #print r["ID"]
                if r["ID"] not in pairscore[item][q["ID"]]:
                    pairscore[item][q["ID"]][r["ID"]] = dict()
                score = 0
                index = 0
                score1 = 0
                for word in q["words"]:
                    # taking review as doc get idf for each word in query
                    idf = getIDF(word, review[item])
                    if word not in r["words"]:
                        w = 0
                    else:
                        w = r["words"][word]
                    num = (k1 +1)*w
                    den = w + k1 *(1-b +b *(len(r["sentence"])/avgdl))
                    score += idf*(num/den)
                    score1+=idf
                pairscore[item][q["ID"]][r["ID"]]["BM25"] = score
                pairscore[item][q["ID"]][r["ID"]]["BM25+"] = score1
                norm_bm += score
                norm_bmm += score1
            for r in review[item]:
                if norm_bm != 0:
                    pairscore[item][q["ID"]][r["ID"]]["BM25"] /= norm_bm
                if norm_bmm !=0:
                    pairscore[item][q["ID"]][r["ID"]]["BM25+"] /= norm_bmm
                pairscore[item][q["ID"]][r["ID"]]["BM25+"] += pairscore[item][q["ID"]][r["ID"]]["BM25"]
                pairscore[item][q["ID"]][r["ID"]].pop("BM25", 0)
                #print q["ID"], r["ID"]


    return pairscore