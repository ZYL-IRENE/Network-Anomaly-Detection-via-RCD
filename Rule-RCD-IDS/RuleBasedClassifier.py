"""
Created by Harry Pardo
Copyright (c) 2018 Reynaldo John Tristan Mahinay Jr., Franz Stewart Dizon, Stephen Kyle Farinas and Harry Pardo
"""

import time
import json
import pandas as pd

def get_rules_json(filename):
    with open(filename, 'r') as f:
        rules = json.load(f)
    return rules

def open_test_data(filename):
    df = pd.read_csv(filename, sep=',', header=None)
    return df

# Rule-base Classifier
def find_match(test_data, rules):
    answers = []
    listdata = test_data[test_data.columns[:-1]].values.tolist()
    for data in listdata:
        ans = False
        for ant, cons, conf, lift in rules:
            # n = len(ant)
            # if (n > 1):
            #     antecedents = ant.split(',')
            # else:
            #     antecedents = ant
            antecedents = ant
            ans = set(antecedents) <= set(list(data))

            if (ans == True):
                answers.append(cons[0])
                break
        if (ans == False):
            answers.append('UNDEFINED')
    return answers


def partition_rule_len(rules):
    rule_set = {'3': [], '4': [],'5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': [], '12': [], '13': [], '14': []}
    for rule in rules:
        if len(rule[0]) > 2:
            rule_set[str(len(rule[0]))].append(rule)

    rule_len =[]
    for i in range(3,15):
        rule_len.append(len(rule_set[str(i)]))
    print(rule_len)
    for i in range(3,15):
        filename = 'rule/partition/rule_' + str(i) + '.json'
        with open(filename, 'w') as f:
            json.dump(rule_set[str(i)], f, indent=4)

    print('successfully saved rules!')




def check_accuracy(test_data, rule_based_answers):
    test_data_class = test_data[test_data.columns[-1]].values.tolist()
    total = len(test_data_class)  # might need checking

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    undefined_num = 0
    testRows = 0

    undefined_data_id = []
    for x, y, i in zip(test_data_class, rule_based_answers, range(total)):
        # print(str(x) + " " + str(y))
        # print("TestRows = " + str(testRows))
        if (str(y) == 'UNDEFINED'):
            undefined_num += 1
            undefined_data_id.append(i)
        if (str(x) == 'normal.' and str(y) == 'normal.'):
            tp += 1
            # print("True Positive: " + str(tp))
        elif (str(x) != 'normal.' and str(y) == 'normal.'):
            fp += 1
            # print("False Positive: " + str(fp))
        elif (str(x) != 'normal.' and str(y) != 'normal.'):
            tn += 1
            # print("True Negative: " + str(tn))
        elif (str(x) == 'normal.' and str(y) != 'normal.'):
            fn += 1

        testRows += 1

    if (tp == 0):
        PPV = 0
    else:
        PPV = float(tp / (tp + fp))
    print("----------------Evaluating normal detection---------------------")
    print("PPV(precision):" + str(PPV * 100))
    #print("NPV:" + str(float(tn / (tn + fn) * 100)))
    print("Detection Rate(recall):" + str(float(tp / (tp + fn) * 100)))
    #print("Specificity:" + str(float(tn / (tn + fp) * 100)))
    print("accuracy:"+str(float((tp + tn) / (tp + fp + tn + fn) * 100)))
    print("False alarm rate(FAR):" + str(float(fp / ( fp + tn ) * 100)))
    if (PPV == 0):
        print("F: 0")
    else:
        print("F1:" + str(float((2 * tp) / (2 * tp + fp + fn) * 100)))
    print("TP:" + str(tp) + " FP: " + str(fp) + " TN: " + str(tn) + " FN: " + str(fn))
    print("undefined:" + str(undefined_num))

    return undefined_data_id

def check_accuracy_attack(test_data, rule_based_answers):
    test_data_class = test_data[test_data.columns[-1]].values.tolist()
    total = len(test_data_class)  # might need checking

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    undefined_num = 0
    testRows = 0

    undefined_data_id = []

    attack_type = ['DOS.', 'Probing.', 'U2R.', 'R2L.']
    for x, y, i in zip(test_data_class, rule_based_answers, range(total)):
        # print(str(x) + " " + str(y))
        # print("TestRows = " + str(testRows))
        if (str(y) == 'UNDEFINED'):
            undefined_num += 1
            undefined_data_id.append(i)
        if (str(x) in attack_type and (str(y) in attack_type or str(y) == 'UNDEFINED')):
            tp += 1
            # print("True Positive: " + str(tp))
        elif (str(x) not in attack_type and (str(y) in attack_type or str(y) == 'UNDEFINED')):
            fp += 1
            # print("False Positive: " + str(fp))
        elif (str(x) not in attack_type and str(y) not in attack_type):
            tn += 1
            # print("True Negative: " + str(tn))
        elif (str(x) in attack_type and str(y) not in attack_type):
            fn += 1

        testRows += 1

    if (tp == 0):
        PPV = 0
    else:
        PPV = float(tp / (tp + fp))
    print("----------------Evaluating Attack detection---------------------")
    print("PPV(precision):" + str(PPV * 100))
    #print("NPV:" + str(float(tn / (tn + fn) * 100)))
    print("Detection Rate(recall):" + str(float(tp / (tp + fn) * 100)))
    #print("Specificity:" + str(float(tn / (tn + fp) * 100)))
    print("accuracy:"+str(float((tp + tn) / (tp + fp + tn + fn) * 100)))
    if (fp +tn) != 0:
        print("False alarm rate(FAR):" + str(float(fp / ( fp + tn ) * 100)))
    if (PPV == 0):
        print("F: 0")
    else:
        print("F1:" + str(float((2 * tp) / (2 * tp + fp + fn) * 100)))
    print("TP:" + str(tp) + " FP: " + str(fp) + " TN: " + str(tn) + " FN: " + str(fn))
    print("undefined:" + str(undefined_num))

    accuracy = round(float((tp + tn) / (tp + fp + tn + fn) * 100),2)
    precision = round(PPV * 100,2)
    recall = round(float(tp / (tp + fn) * 100),2)
    if (fp+tn) != 0:
        far = round(float(fp / ( fp + tn ) * 100),2)
    else:
        far = 0

    return undefined_data_id, accuracy, precision, recall, far


def check_accuracy_rare(data_class, RCD_answer):
    total = len(data_class)  # might need checking

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    undefined_num = 0
    testRows = 0

    undefined_data_id = []

    rare_type = ['Probing.', 'U2R.', 'R2L.']
    for x, y, i in zip(data_class, RCD_answer, range(total)):
        # print(str(x) + " " + str(y))
        # print("TestRows = " + str(testRows))
        if (str(y) == 'UNDEFINED'):
            undefined_num += 1
            undefined_data_id.append(i)
            continue
        if (str(x) in rare_type and str(y) == 'RARE'):
            tp += 1
            # print("True Positive: " + str(tp))
        elif (str(x) not in rare_type and str(y) == 'RARE'):
            fp += 1
            # print("False Positive: " + str(fp))
        elif (str(x) not in rare_type and str(y) != 'RARE'):
            tn += 1
            # print("True Negative: " + str(tn))
        elif (str(x) in rare_type and str(y) != 'RARE'):
            fn += 1

        testRows += 1

    if (tp == 0):
        PPV = 0
    else:
        PPV = float(tp / (tp + fp))
    print("----------------Evaluating Rare detection---------------------")
    print("TP:" + str(tp) + " FP: " + str(fp) + " TN: " + str(tn) + " FN: " + str(fn))
    print("PPV(precision):" + str(PPV * 100))
    #print("NPV:" + str(float(tn / (tn + fn) * 100)))
    print("Detection Rate(recall):" + str(float(tp / (tp + fn) * 100)))
    #print("Specificity:" + str(float(tn / (tn + fp) * 100)))
    print("accuracy:"+str(float((tp + tn) / (tp + fp + tn + fn) * 100)))
    print("False alarm rate(FAR):" + str(float(fp / ( fp + tn ) * 100)))
    if (PPV == 0):
        print("F: 0")
    else:
        print("F1:" + str(float((2 * tp) / (2 * tp + fp + fn) * 100)))
    print("TP:" + str(tp) + " FP: " + str(fp) + " TN: " + str(tn) + " FN: " + str(fn))
    print("undefined:" + str(undefined_num))

    return undefined_data_id

def classfiy(test_data):
    apriori_rules = get_rules_json()
    test_data = open_test_data()

    start_time = time.time()
    prediction_apriori = find_match(test_data, apriori_rules)
    print("Apriori classify: --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    prediction_fp = find_match(test_data, fp_rules)
    print("FP classify: --- %s seconds ---" % (time.time() - start_time))

    print('---------------------------------------------------')
    print('Apriori')
    check_accuracy(test_data[-1], prediction_apriori)

    print('---------------------------------------------------')
    print('Fp Growth')
    check_accuracy(test_data['dengue_next'], prediction_fp)