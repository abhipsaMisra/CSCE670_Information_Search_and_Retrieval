import os
import json
import re
from collections import defaultdict
import math

lambda_value = 0.7
data_path = '../data/'
training_file_name = 'training_data.json'


def calculate_tokens(data_path, training_file_name):
    term_freq_collection = defaultdict(lambda: 0)
    tokens_collection_count = 0
    term_freq_class = defaultdict(lambda: 0)
    tokens_class_count = defaultdict(lambda: 0)

    fd = open(os.path.join(data_path, training_file_name), "r")
    for line in iter(fd):
        data = json.loads(line)
        text = data['text']
        label = data['label']
        for term_in_text in re.findall(r'\w+', text):
            term = term_in_text.lower()

            term_freq_collection[term] += 1
            tokens_collection_count += 1
            term_freq_class[(term, label)] += 1
            tokens_class_count[label] += 1

    return term_freq_collection, tokens_collection_count, term_freq_class, tokens_class_count

term_freq_collection, tokens_collection_count, term_freq_class, tokens_class_count = calculate_tokens(data_path, training_file_name)

testing_file_name = 'testing_data.json'

def predict_label(data_path, testing_file_name, term_freq_collection, tokens_collection_count, term_freq_class,
                  tokens_class_count):
    true_count = 0
    tp_rel = 0
    tp_irrel = 0
    fp_rel = 0
    fp_irrel = 0
    fn_rel = 0
    fn_irrel = 0
    test_data_count = 0
    fd = open(os.path.join(data_path, testing_file_name), "r")
    for line in iter(fd):
        data = json.loads(line)
        text = data['text']
        label = data['label']
        label_score_relevant = 0
        label_score_irrelevant = 0
        for term_in_text in re.findall(r'\w+', text):
            term = term_in_text.lower()
            label_score_relevant += math.log10(
                evaluate_label(term, 'Food-relevant', term_freq_collection, tokens_collection_count, term_freq_class,
                               tokens_class_count))
            label_score_irrelevant += math.log10(
                evaluate_label(term, 'Food-irrelevant', term_freq_collection, tokens_collection_count, term_freq_class,
                               tokens_class_count))
        true_count, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel, test_data_count = metrics_count(label, label_score_relevant, label_score_irrelevant, true_count, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel, test_data_count)
    evaluate_metrics(true_count, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel, test_data_count)


def evaluate_label(term, label, term_freq_collection, tokens_collection_count, term_freq_class,
                   tokens_class_count):
    term_doc_value = float(term_freq_class[(term, label)]) / float(tokens_class_count[label])
    term_collection_value = float(term_freq_collection[term]) / float(tokens_collection_count)
    term_mixture_model_value = float((1 - lambda_value) * term_collection_value + lambda_value * term_doc_value)
    if (term_mixture_model_value == 0):
        term_mixture_model_value = 1
    return term_mixture_model_value


def metrics_count(label, label_score_relevant, label_score_irrelevant, true_count, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel, test_data_count):
    label_predicted = 'Food-irrelevant'
    if label_score_relevant > label_score_irrelevant:
        label_predicted = 'Food-relevant'
    if label == label_predicted:
        true_count += 1
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
    test_data_count += 1
    return true_count, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel, test_data_count

def evaluate_metrics(true_count, tp_rel, tp_irrel, fp_rel, fp_irrel, fn_rel, fn_irrel, test_data_count):
    accuracy = float(true_count)/float(test_data_count)
    rel_precision = float(tp_rel)/float(tp_rel + fp_rel)
    rel_recall = float(tp_rel)/float(tp_rel + fn_rel)
    irrel_precision = float(tp_irrel) / float(tp_irrel + fp_irrel)
    irrel_recall = float(tp_irrel) / float(tp_irrel + fn_irrel)
    print("Accuracy : %s" %accuracy)
    print("Relevant - Precision : %s" % rel_precision)
    print("Relevant - Recall : %s" % rel_recall)
    print("Irrelevant - Precision : %s" % irrel_precision)
    print("Irrelevant - Recall : %s" % irrel_recall)


predict_label(data_path, testing_file_name, term_freq_collection, tokens_collection_count, term_freq_class,
              tokens_class_count)
