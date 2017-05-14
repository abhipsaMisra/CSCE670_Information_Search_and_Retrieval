from collections import defaultdict
import operator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

def classification(predicted_model, test_pairscore, test_bilinear_score, test_question, question, review):
    total_no = 0
    correct = 0
    incorrect = 0
    c , i = 0, 0
    relevant_reviews = defaultdict(lambda: defaultdict())
    for prod_key in test_bilinear_score:
        question_review_score = defaultdict(lambda: defaultdict())
        for each_question in test_bilinear_score[prod_key]:
            # total_no += 5
            review_score, dummy = defaultdict(), defaultdict()
            for each_review in test_bilinear_score[prod_key][each_question]:
                score = defaultdict()
                weight_list = predicted_model[prod_key][each_question]
                sum = weight_list[0] * test_pairscore[prod_key][each_question][each_review]['ROGUE'] + \
                      weight_list[1] * test_pairscore[prod_key][each_question][each_review]['BM25+'] + \
                      weight_list[2] * test_bilinear_score[prod_key][each_question][each_review]
                abs_sum = abs(sum)
                score['score'] = sum
                score['abs_score'] = abs_sum
                for x in review[prod_key]:
                    if x['ID'] == each_review:
                        score['actual_sen'] = x['actual_sen']
                        break
                review_score[each_review] = sum
                dummy[each_review] = score

            sorted_list = sorted(review_score.items(), key=lambda x: x[1], reverse=True)
            # sorted_list = list(reversed(sorted(review_score.iteritems(), key=operator.itemgetter(1))))
            i = 0
            # nltk.download()
            yes, no = 0, 0
            sid = SentimentIntensityAnalyzer()
            for x in sorted_list:
                sentence = dummy[x[0]]['actual_sen']
                #print sentence
                ss = sid.polarity_scores(sentence)
                if ss["compound"] < 0:
                    no += 1
                else:
                    yes += 1

                i += 1
                if i == 5:
                    break
            if yes >= no:
                if test_question[prod_key][0]['A'] == True:
                    c += 1
                else:
                    i += 1
            else:
                if test_question[prod_key][0]['A'] == False:
                    c += 1
                else:
                    i +=  1
    accuracy =  float(c) / float(c + i)
    print ("accuracy: %s" %accuracy)
    return c, i