import os
import json
import re
from collections import defaultdict
import math

data_path = '../data/'
training_file_name = 'training_data.json'

def create_index(data_path, training_file_name):

    norm_freq_rel = defaultdict(lambda: 0)
    norm_freq_irrel = defaultdict(lambda: 0)
    class_size = defaultdict(lambda: 0)
    centroid = defaultdict()

    fd = open(os.path.join(data_path, training_file_name), "r")
    index = 0
    for line in iter(fd):
        data = json.loads(line)
        text = data['text']
        label = data['label']
        freq_count = defaultdict(lambda: 0)
        sqr_sum = 0
        norm_freq = defaultdict()
        for term_in_text in re.findall(r'\w+', text):
            term = term_in_text.lower()
            freq_count[(term, label)] += 1
        for term, label in freq_count:
            sqr_sum += freq_count[(term, label)] ** 2
        norm_factor = math.sqrt(sqr_sum)
        for term, label in freq_count:
            norm_freq[term] = float(freq_count[(term, label)]) / float(norm_factor)
        if label == 'Food-relevant':
            norm_freq_rel[index] = norm_freq
        else:
            norm_freq_irrel[index] = norm_freq
        class_size[label] += 1
        index += 1
    centroid['Food-relevant'] = calculate_centroid('Food-relevant', norm_freq_rel, class_size)
    centroid['Food-irrelevant'] = calculate_centroid('Food-irrelevant', norm_freq_irrel, class_size)
    return centroid

def calculate_centroid(label, freq_matrix, class_size):
    freq_sum = defaultdict(lambda: 0)
    centroid = defaultdict()
    for index in freq_matrix:
        for term in freq_matrix[index]:
            freq_sum[term] += freq_matrix[index][term]
    for term in freq_sum:
        centroid[term] = float(freq_sum[term]) / float(class_size[label])
    return centroid

centroid = create_index(data_path, training_file_name)

testing_file_name = 'testing_data.json'


def predict_label(data_path, testing_file_name, centroid):
    accuracy = 0
    test_data_size = 0
    tp_rel = 0
    tp_irrel = 0
    fp_rel = 0
    fp_irrel = 0
    fn_rel = 0
    fn_irrel = 0
    fd = open(os.path.join(data_path, testing_file_name), "r")
    for line in iter(fd):
        test_data_size += 1
        data = json.loads(line)
        text = data['text']
        label = data['label']
        freq_count = defaultdict(lambda: 0)
        sqr_sum = 0
        norm_freq = defaultdict()
        for term_in_text in re.findall(r'\w+', text):
            term = term_in_text.lower()
            freq_count[term] += 1
        for term in freq_count:
            sqr_sum += freq_count[(term)] ** 2
        norm_factor = math.sqrt(sqr_sum)
        for term in freq_count:
            norm_freq[term] = float(freq_count[term]) / float(norm_factor)
        dist_rel = calculate_euclidean_dist(norm_freq, 'Food-relevant', centroid)
        dist_irrel = calculate_euclidean_dist(norm_freq, 'Food-irrelevant', centroid)
        label_predicted = 'Food-irrelevant'
        if dist_rel < dist_irrel:
            label_predicted = 'Food-relevant'
        accuracy, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel = metrics_count(label, label_predicted, accuracy, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel)
    accuracy_rocchio_ed = float(accuracy) / float(test_data_size)
    print ("Accuracy: %s" % accuracy_rocchio_ed)
    evaluate_metrics(tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel)


def calculate_euclidean_dist(norm_freq, label, centroid):
    dist_sqr = defaultdict()
    dist_sqr_value = 0
    for term in centroid[label]:
        if term not in norm_freq:
            norm_freq[term] = 0
        dist_sqr[term] = (centroid[label][term] - norm_freq[term]) ** 2
    for term in norm_freq:
        if term not in centroid[label]:
            dist_sqr[term] = (0 - norm_freq[term]) ** 2
    for term in dist_sqr:
        dist_sqr_value += dist_sqr[term]
    dist_value = math.sqrt(dist_sqr_value)
    return dist_value


def metrics_count(label, label_predicted, accuracy, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel):
    if label == label_predicted:
        accuracy += 1
        if label_predicted == 'Food-relevant':
            tp_rel += 1
        else:
            tp_irrel += 1
    else:
        if label_predicted == 'Food-relevant':
            fp_rel += 1
            fn_irrel += 1
        else:
            fp_irrel += 1
            fn_rel += 1
    return accuracy, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel


def evaluate_metrics(tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel):
    rel_precision = float(tp_rel) / float(tp_rel + fp_rel)
    rel_recall = float(tp_rel) / float(tp_rel + fn_rel)
    irrel_precision = float(tp_irrel) / float(tp_irrel + fp_irrel)
    irrel_recall = float(tp_irrel) / float(tp_irrel + fn_irrel)
    print("Relevant - Precision : %s" % rel_precision)
    print("Relevant - Recall : %s" % rel_recall)
    print("Irrelevant - Precision : %s" % irrel_precision)
    print("Irrelevant - Recall : %s" % irrel_recall)

predict_label(data_path, testing_file_name, centroid)