import random
from collections import defaultdict

def evaluate_model(pairscore,bilinear_score,question):
    eta = 0.01
    T = 500
    t = 0
    final_weight = defaultdict(lambda: defaultdict())
    for prod_key in bilinear_score:
        for each_question in bilinear_score[prod_key]:
            question_weight = defaultdict(lambda: list())
            w = [random.random() for _ in range(3)]
            sum_weights = 0
            for i in range(0,3):
                sum_weights+=w[i]
            if (sum_weights != 0.0):
                for i in range(0,3):
                    w[i]=w[i]/sum_weights
            for each_review in bilinear_score[prod_key][each_question]:
                t = 0
                while t < T:
                    t += 1
                    sum = pairscore[prod_key][each_question][each_review]['ROGUE']+\
                        pairscore[prod_key][each_question][each_review]['BM25+']+\
                        bilinear_score[prod_key][each_question][each_review]
                    scores = [pairscore[prod_key][each_question][each_review]['ROGUE']/sum, \
                                pairscore[prod_key][each_question][each_review]['BM25+']/sum, \
                                bilinear_score[prod_key][each_question][each_review]/sum]
                    total_sum = w[0] * pairscore[prod_key][each_question][each_review]['ROGUE'] + \
                        w[1] * pairscore[prod_key][each_question][each_review]['BM25+'] + \
                        w[2] * bilinear_score[prod_key][each_question][each_review]
                    if total_sum > 0.5:
                        if question[prod_key][0]['A'] == False:
                            w[0] -= eta
                            w[1] -= eta
                            w[2] -= eta
                    else:
                        if question[prod_key][0]['A'] == True:
                            w[0] += eta
                            w[1] += eta
                            w[2] += eta
                    sum_weights = 0
                    for i in range(0,3):
                        sum_weights+=w[i]
                    if (sum_weights != 0.0):
                        for i in range(0,3):
                            w[i]=w[i]/sum_weights
                question_weight[each_question] = w
        final_weight[prod_key] = question_weight
    return final_weight