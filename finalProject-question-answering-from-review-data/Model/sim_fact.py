from collections import defaultdict
import math

class similarity_fact:
    
    def __init__(self, review, question):
        self.review_data = review
        self.question_data = question

    def evaluate_cosine_similarity(self):
        tf_scores_questions = self.evaluate_tf_questions(self.question_data)
        tf_scores_reviews = self.evaluate_tf_reviews(self.question_data, self.review_data)
        idf_scores = self.evaluate_idf(self.question_data, self.review_data)
        tf_idf_questions = self.evaluate_tf_idf_qstns(tf_scores_questions, idf_scores)
        tf_idf_reviews = self.evaluate_tf_idf_reviews(tf_scores_questions, tf_scores_reviews, idf_scores)
        cosine = self.evaluate_cosine(tf_idf_questions, tf_idf_reviews)
        return cosine,tf_idf_questions,tf_idf_reviews
    
    def evaluate_cosine(self, tf_idf_questions, tf_idf_reviews):
        cosine_score = defaultdict()
        for prod_key in tf_idf_questions:
            if prod_key in tf_idf_reviews:
                cosine_score[prod_key] = defaultdict(lambda: defaultdict())
                for question_id,each_question in tf_idf_questions[prod_key].iteritems():
                    question_length = 0
                    temp_tf_idf_multiplied = defaultdict(lambda: 0)
                    for key1, question_tf_idf in each_question.iteritems():
                        question_length += math.pow(question_tf_idf,2)
                    question_length = math.sqrt(question_length)
                    for review_id,each_review in tf_idf_reviews[prod_key].iteritems():
                        review_length = 0
                        score = 0
                        for key2,question_tf_idf in each_question.iteritems():
                            if key2 not in each_review:
                                review_tf_idf = 0
                            else:
                                review_tf_idf = each_review[key2]
                            score += question_tf_idf*review_tf_idf
                        for key3, review_tf_idf in each_review.iteritems():
                            review_length += math.pow(review_tf_idf,2)
                        review_length = math.sqrt(review_length)
                        if review_length == 0 or question_length == 0:
                            temp_tf_idf_multiplied[review_id] = 0
                        else:
                            temp_tf_idf_multiplied[review_id] = score/(review_length*question_length)
                    cosine_score[prod_key][question_id] = temp_tf_idf_multiplied
        return cosine_score
    
    
    def evaluate_tf_idf_reviews(self, tf_scores_questions, tf_scores_reviews, idf_scores):
        tf_idf_score = defaultdict()
        for prod_key in tf_scores_questions:
            if prod_key in tf_scores_reviews:
                tf_idf_score[prod_key] = defaultdict()
                review_id = -1
                for r_id,each_review in tf_scores_reviews[prod_key].iteritems():
                    review_id += 1
                    scores = defaultdict(lambda: 0)
                    for key, value in each_review.iteritems():
                        if prod_key in idf_scores:
                            idf_value = idf_scores[prod_key][key]
                        else:
                            idf_value = 0
                            idf_scores[prod_key][key] = idf_value
                        tf_idf = value * idf_value
                        scores[key] = tf_idf
                    # tf_idf_score[prod_key].append(scores)
                    tf_idf_score[prod_key][r_id] = scores
        return tf_idf_score
    
    
    def evaluate_tf_idf_qstns(self, tf_scores_questions, idf_scores):
        tf_idf_score = defaultdict()
        for prod_key in tf_scores_questions:
            if prod_key not in tf_idf_score:
                tf_idf_score[prod_key] = defaultdict()
            question_id = -1
            for q_id,each_question in tf_scores_questions[prod_key].iteritems():
                question_id += 1
                scores = defaultdict(lambda: 0)
                for key, value in each_question.iteritems():
                    if prod_key in idf_scores and key in idf_scores[prod_key]:
                        idf_value = idf_scores[prod_key][key]
                    else:
                        idf_value = 0
                        # idf_scores[prod_key][key] = idf_value
                    tf_idf = value * idf_value
                    scores[key] = tf_idf
                tf_idf_score[prod_key][q_id] = scores
                # tf_idf_score[prod_key].append(scores)
        return tf_idf_score
    
    
    def evaluate_tf_reviews(self,question_data, review_data):
        tf_scores = defaultdict()
        for prod_key, question in question_data.iteritems():
            if prod_key in review_data:
                if prod_key not in tf_scores:
                    tf_scores[prod_key] = defaultdict()
                for review in review_data[prod_key]:
                    term_count = defaultdict(lambda: 0)
                    words = review['words']
                    r_id = review['ID']
                    for key, count in words.iteritems():
                        term_count[key] = 1 + math.log(float(count))
                    tf_scores[prod_key][r_id] = term_count
                    # tf_scores[prod_key] = term_count
        return tf_scores
    
    
    def evaluate_tf_questions(self,question_data):
        tf_scores = defaultdict()
        for prod_key, question in question_data.iteritems():
            if prod_key not in tf_scores:
                tf_scores[prod_key] = defaultdict()
            for each_question in question:
                term_count = defaultdict(lambda: 0)
                words = each_question['words']
                q_id = each_question['ID']
                for key, count in words.iteritems():
                    term_count[key] = 1 + math.log(float(count))
                tf_scores[prod_key][q_id] = term_count
        return tf_scores
    
    
    def evaluate_idf(self,question_data, review_data):
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