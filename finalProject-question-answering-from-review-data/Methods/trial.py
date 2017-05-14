from collections import defaultdict
import math


def evaluate_cosine_similarity(data_id, question_data, review_data):
    tf_scores_questions = evaluate_tf_questions(question_data)
    tf_scores_reviews = evaluate_tf_reviews(question_data, review_data)
    idf_scores = evaluate_idf(question_data, review_data)
    tf_idf_questions = evaluate_tf_idf_qstns(tf_scores_questions, idf_scores)
    tf_idf_reviews = evaluate_tf_idf_reviews(tf_scores_questions, tf_scores_reviews, idf_scores)
    cosine = evaluate_cosine(tf_idf_questions, tf_idf_reviews)
    return cosine

def evaluate_cosine(tf_idf_questions, tf_idf_reviews):
    cosine_score = defaultdict()
    for prod_key in tf_idf_questions:
        if prod_key in tf_idf_reviews:
            cosine_score[prod_key] = defaultdict(lambda: defaultdict())
            for index_question,each_question in tf_idf_questions[prod_key]:
                temp_tf_idf_multiplied = defaultdict(lambda: 0)
                for index_review, each_review in tf_idf_reviews[prod_key]:
                    score = 0
                    for key,question_tf_idf in each_question.iteritems():
                        if key not in each_review:
                            review_tf_idf = 0
                        else:
                            review_tf_idf = each_review[key]
                        score += question_tf_idf*review_tf_idf
                    temp_tf_idf_multiplied['r'+str(index_review)] = score
                cosine_score[prod_key]['q'+str(index_question)] = temp_tf_idf_multiplied




def evaluate_tf_idf_reviews(tf_scores_questions, tf_scores_reviews, idf_scores):
    tf_idf_score = defaultdict()
    for prod_key in tf_scores_questions:
        if prod_key in tf_scores_reviews:
            tf_idf_score[prod_key] = list()
            for each_review in tf_scores_reviews[prod_key]:
                scores = defaultdict(lambda: 0)
                for key, value in each_review.iteritems():
                    if prod_key in idf_scores:
                        idf_value = idf_scores[prod_key][key]
                    else:
                        idf_value = 0
                        idf_scores[prod_key][key] = idf_value
                    tf_idf = value * idf_value
                    scores[key] = tf_idf
                tf_idf_score[prod_key].append(scores)
    return tf_idf_score


def evaluate_tf_idf_qstns(tf_scores_questions, idf_scores):
    tf_idf_score = defaultdict()
    for prod_key in tf_scores_questions:
        if prod_key not in tf_idf_score:
            tf_idf_score[prod_key] = list()
        for each_question in tf_scores_questions[prod_key]:
            scores = defaultdict(lambda: 0)
            for key, value in each_question.iteritems():
                if prod_key in idf_scores:
                    idf_value = idf_scores[prod_key][key]
                else:
                    idf_value = 0
                    idf_scores[prod_key][key] = idf_value
                tf_idf = value * idf_value
                scores[key] = tf_idf
            tf_idf_score[prod_key].append(scores)
    return tf_idf_score


def evaluate_tf_reviews(question_data, review_data):
    tf_scores = defaultdict()
    for prod_key, question in question_data.iteritems():
        if prod_key in review_data:
            if prod_key not in tf_scores:
                tf_scores[prod_key] = list()
            for review in review_data[prod_key]:
                term_count = defaultdict(lambda: 0)
                words = review['words']
                for key, count in words.iteritems():
                    term_count[key] = 1 + math.log(float(count))
                tf_scores[prod_key].append(term_count)
                # tf_scores[prod_key] = term_count
    return tf_scores


def evaluate_tf_questions(question_data):
    tf_scores = defaultdict()
    for prod_key, question in question_data.iteritems():
        if prod_key not in tf_scores:
            tf_scores[prod_key] = list()
        for each_question in question:
            term_count = defaultdict(lambda: 0)
            words = each_question['words']
            for key, count in words.iteritems():
                term_count[key] = 1 + math.log(float(count))
            tf_scores[prod_key].append(term_count)
    return tf_scores


def evaluate_idf(question_data, review_data):
    collection_freq = defaultdict()
    for prod_key, question in question_data.iteritems():
        term_count = defaultdict(lambda: 0)
        review_count = 0
        if prod_key in review_data:
            for review in review_data[prod_key]:
                review_count += 1
                words = review['words']
                for key, count in words.iteritems():
                    term_count[key] += 1
            term_count['review_count'] = review_count
            collection_freq[prod_key] = term_count

    idf_scores = defaultdict()
    for prod in collection_freq:
        idf = defaultdict(lambda: 0)
        term_count = collection_freq[prod]
        for key, count in term_count.iteritems():
            idf_value = math.log(float(term_count['review_count']) / float(count))
            idf[key] = idf_value
        idf_scores[prod] = idf
    return idf_scores
