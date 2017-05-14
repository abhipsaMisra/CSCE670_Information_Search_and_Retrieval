import random
from collections import defaultdict
import operator


def evaluate_baseline(pairscore, question, type, combination_models):
    eta = 0.1
    T = 10
    final_weight = defaultdict(lambda: defaultdict())
    for prod_key in pairscore:
        for each_question in pairscore[prod_key]:
            if combination_models:
                question_weight = defaultdict(lambda: list())
                w = [random.random() for _ in range(2)]
                sum_weights = 0
                for i in range(0, 2):
                    sum_weights += w[i]
                for i in range(0, 2):
                    w[i] = w[i] / sum_weights
            else:
                question_weight = defaultdict(lambda: 0)
                w = random.random()
            for each_review in pairscore[prod_key][each_question]:
                t = 0
                while t < T:
                    t += 1
                    if combination_models:
                        sum = pairscore[prod_key][each_question][each_review]['ROGUE'] + \
                              pairscore[prod_key][each_question][each_review]['BM25+']
                        total_sum = w[0] * pairscore[prod_key][each_question][each_review]['ROGUE'] + \
                                    w[1] * pairscore[prod_key][each_question][each_review]['BM25+']
                    else:
                        total_sum = w * pairscore[prod_key][each_question][each_review][type]
                    if total_sum > 0.5:
                        if question[prod_key][0]['A'] == False:
                            if combination_models:
                                w[0] -= eta
                                w[1] -= eta
                            else:
                                w -= eta
                    else:
                        if question[prod_key][0]['A'] == True:
                            if combination_models:
                                w[0] += eta
                                w[1] += eta
                            else:
                                w += eta
                question_weight[each_question] = w
        final_weight[prod_key] = question_weight
    return final_weight


def calculate_baseline_metrics(baseline_model_rogue, test_pairscore, test_question, type, combination_models):
    total_no = 0
    correct = 0
    incorrect = 0
    c, i = 0, 0
    relevant_reviews = defaultdict(lambda: defaultdict())
    for prod_key in test_pairscore:
        question_review_score = defaultdict(lambda: defaultdict())
        for each_question in test_pairscore[prod_key]:
            # total_no += 5
            review_score = defaultdict()
            for each_review in test_pairscore[prod_key][each_question]:
                score = defaultdict()
                if combination_models:
                    weight_list = baseline_model_rogue[prod_key][each_question]
                    sum = weight_list[0] * test_pairscore[prod_key][each_question][each_review]['ROGUE'] + \
                          weight_list[1] * test_pairscore[prod_key][each_question][each_review]['BM25+']
                else:
                    weight_list = baseline_model_rogue[prod_key][each_question]
                    sum = weight_list * test_pairscore[prod_key][each_question][each_review][type]

                abs_sum = abs(sum)
                score['score'] = sum
                score['abs_score'] = abs_sum

                review_score[each_review] = score

            sorted_list = list(reversed(sorted(review_score.iteritems(), key=operator.itemgetter(1))))
            if len(sorted_list) > 5:
                top_list = sorted_list[:5]
            else:
                top_list = sorted_list[:]
            total_no += len(top_list)
            question_review_score[each_question] = review_score
            for score_key, each_score in enumerate(top_list):
                score = each_score[1]['score']
                if score > 0.5:
                    if test_question[prod_key][0]['A'] == True:
                        correct += 1
                    else:
                        incorrect += 1
                else:
                    if test_question[prod_key][0]['A'] == False:
                        correct += 1
                    else:
                        incorrect += 1
        relevant_reviews[prod_key] = question_review_score
    accuracy = float(correct) / float(total_no)
    print ("accuracy: %s" % accuracy)
    return relevant_reviews, accuracy
