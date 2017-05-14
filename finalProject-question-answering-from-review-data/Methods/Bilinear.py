from collections import defaultdict
import random
import math

def evaluate_bilinear(cosine, tf_idf_questions, tf_idf_reviews):
    bilinear_score = defaultdict(lambda: defaultdict())
    for prod_key in cosine:
        bilinear_score_per_product = evaluate_bilinear_per_product(cosine[prod_key], tf_idf_questions[prod_key], tf_idf_reviews[prod_key])
        bilinear_score[prod_key] = bilinear_score_per_product
    return bilinear_score

def evaluate_bilinear_per_product(cosine_product, tf_idf_questions_product, tf_idf_reviews_product):
    weights_questions, weights_reviews, d, dx, dy = preprocessing_per_product(cosine_product, \
                                        tf_idf_questions_product, tf_idf_reviews_product)
    beta = gamma = 0.01
    theta_x = theta_y = 1
    L_x, L_y = RMLS_per_product(weights_questions,weights_reviews,d,beta,gamma,theta_x, theta_y)
    bilinear_per_prod = calculate_score(tf_idf_questions_product,L_x,L_y,tf_idf_reviews_product,d,dx,dy)
    return bilinear_per_prod

def calculate_score(tf_idf_questions,L_x, L_y,tf_idf_reviews,d,dx,dy):
    final_score_list = defaultdict(lambda :defaultdict())
    for each_question in tf_idf_questions:
        score_sum = 0
        prod1 = [0] * d
        for each_question_word in tf_idf_questions[each_question].keys():
            for i in range(0,d):
                prod1[i]+= tf_idf_questions[each_question][each_question_word]*L_x[each_question_word][i]
        prod2 = defaultdict(lambda :0)
        for each_review_word in L_y.keys():
            for j in range(0,d):
                prod2[each_review_word] += L_y[each_review_word][j]*prod1[j]
        score_list = defaultdict(lambda :0)
        for each_review in tf_idf_reviews:
            score = 0
            for each_review_word in tf_idf_reviews[each_review]:
                score += prod2[each_review_word]*tf_idf_reviews[each_review][each_review_word]
            score_list[each_review] = score
            score_sum += math.pow(score,2)
        for each_score in score_list:
            if score_sum != 0:
                score_list[each_score] = score_list[each_score]/math.sqrt(score_sum)
        final_score_list[each_question]=score_list
        return final_score_list



def RMLS_per_product(weights_questions, weights_reviews, d, beta, gamma, theta_x, theta_y):
    # initialize L_x
    L_x = defaultdict()
    L_y = defaultdict()
    for question_word in weights_questions:
        l_xu = [random.random() for _ in range(d)]
        L_x[question_word] = l_xu
    for review_word in weights_reviews:
        l_yv = [random.random() for _ in range(d)]
        L_y[review_word] = l_yv

    T = 10 #setting the convergence limit
    t = 0
    while t<=T:
        t += 1
        for question_word in weights_questions:
            omega_u = [0] * d
            for review_word in weights_reviews:
                col = L_y[review_word]
                for i in range(0,len(col)):
                    omega_u[i] += col[i]*weights_questions[question_word][review_word]
            l_xu = L_x[question_word]
            non_zero = False
            for i in range(0,len(l_xu)):
                if l_xu[i] != 0:
                    non_zero = True
                    break
            if non_zero == False:
                l_xu = [0] * d
            else:
                length = 0
                for z in range (0,d):
                    positive = False
                    if omega_u[z] > 0:
                        positive = True
                    z_th_element = abs(omega_u[z])
                    max_value = max(z_th_element-beta,0)
                    if positive:
                        pass
                    else:
                        max_value = -max_value
                    l_xu[z] = max_value
                    length += math.pow(max_value,2)
                length = math.sqrt(length)
                for z in range(0,d):
                    if length == 0:
                        pass
                    else:
                        l_xu[z] = l_xu[z] * (theta_x/length)

            L_x[question_word] = l_xu

        for review_word in weights_reviews:
            eta_v = [0] * d
            for question_word in weights_questions:
                col = L_x[question_word]
                for i in range(0, len(col)):
                    eta_v[i] += col[i] * weights_reviews[review_word][question_word]
            l_yv = L_y[review_word]
            non_zero = False
            for i in range(0, len(l_yv)):
                if l_yv[i] != 0:
                    non_zero = True
                    break
            if non_zero == False:
                l_yv = [0] * d
            else:
                length = 0
                for z in range(0, d):
                    positive = False
                    if eta_v[z] > 0:
                        positive = True
                    z_th_element = abs(eta_v[z])
                    max_value = max(z_th_element - gamma, 0)
                    if positive:
                        pass
                    else:
                        max_value = -max_value
                    l_yv[z] = max_value
                    length += math.pow(max_value, 2)
                length = math.sqrt(length)
                for z in range(0, d):
                    if length == 0:
                        pass
                    else:
                        l_yv[z] = l_yv[z] * (theta_y / length)

            L_y[review_word] = l_yv

    return L_x, L_y


def preprocessing_per_product(cosine_product, tf_idf_questions_product, tf_idf_reviews_product):
    question_vocab = set()
    review_vocab = set()
    # calculate dx and dy (size of vocab for all questions, all reviews respectively)
    for question_id in tf_idf_questions_product:
        question_vocab = question_vocab.union(tf_idf_questions_product[question_id].keys())
    for review_id in tf_idf_reviews_product:
        review_vocab = review_vocab.union(tf_idf_reviews_product[review_id].keys())
    dx = len(question_vocab)  # size of question vocab
    dy = len(review_vocab)  # size of review vocab
    question_vocab_list = list(question_vocab)
    review_vocab_list = list(review_vocab)
    weights_questions = defaultdict(lambda: defaultdict)
    weights_reviews = defaultdict(lambda: defaultdict)
    # Initializing everything to 0
    for u in range(0, dx):
        weights_xu = defaultdict(lambda: 0)
        for v in range(0, dy):
            weights_xu[review_vocab_list[v]] = 0
        weights_questions[question_vocab_list[u]] = weights_xu
    for v in range(0, dy):
        weights_yv = defaultdict(lambda: 0)
        for u in range(0, dx):
            weights_yv[question_vocab_list[u]] = 0
        weights_reviews[review_vocab_list[v]] = weights_yv
    # Precalculation
    nx = len(tf_idf_questions_product)  # num questions
    ny = len(tf_idf_reviews_product)  # num reviews
    for key in weights_questions:
        for question_id in cosine_product:
            for review_id in cosine_product[question_id]:
                for review_word in review_vocab_list:
                    num = float(1) / float(nx * ny)
                    try:
                        num *= tf_idf_questions_product[question_id][key]
                    except KeyError:
                        num = 0
                    num *= cosine_product[question_id][review_id]
                    try:
                        num *= tf_idf_reviews_product[review_id][review_word]
                    except KeyError:
                        num = 0
                    weights_questions[key][review_word] += num

    for key in weights_reviews:
        for question_id in cosine_product:
            for review_id in cosine_product[question_id]:
                for question_word in question_vocab_list:
                    num = float(1) / float(nx * ny)
                    try:
                        num *= tf_idf_reviews_product[review_id][key]
                    except KeyError:
                        num = 0
                    num *= cosine_product[question_id][review_id]
                    try:
                        num *= tf_idf_questions_product[question_id][question_word]
                    except KeyError:
                        num = 0
                    weights_reviews[key][question_word] += num

    d = (min(dx,dy)/3) + 1

    return weights_questions, weights_reviews, d, dx, dy


