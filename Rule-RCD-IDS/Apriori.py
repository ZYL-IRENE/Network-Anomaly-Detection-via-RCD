"""
Copyright (c) 2016 Ariel Barmat
Edited by Yanling Zhang.
"""

from itertools import chain, combinations
import json

# Open the data in .csv file format
def open_data(filename):
    f = open(filename, 'rU')
    for l in f:
        l = l.strip().rstrip(',')
        row = frozenset(l.split(','))
        yield row


def itemset_from_data(data):
    itemset = set()
    transaction_list = list()
    for row in data:
        transaction_list.append(frozenset(row))
        for item in row:
            if item:
                itemset.add(frozenset([item]))
    return itemset, transaction_list


# get support for each item
def itemset_support(transaction_list, itemset, min_support=0):
    len_transaction_list = len(transaction_list)
    l = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row))) / len_transaction_list)
        for item in itemset
    ]

    return dict([(item, support) for item, support in l if support > min_support])


# get itemset with support > min_support
def frequent_itemset(transaction_list, c_itemset, min_support):
    f_itemset = dict()

    k = 1
    while True:
        if k > 1:
            c_itemset = joinset(l_itemset, k)
        l_itemset = itemset_support(transaction_list, c_itemset, min_support)
        print(k)
        if not l_itemset or k > 15:
            print("break")
            break
        f_itemset.update(l_itemset)
        k += 1

    return f_itemset


def joinset(itemset, k):
    return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == k])


def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])


# Generate Association Rules
def get_rules(f_itemset, min_confidence, min_lift):
    rules = list()
    intru_cons = ["normal.", "DOS.", "Probing.", "R2L.", "U2R."]

    for item, support in f_itemset.items():
        if len(item) ==15:
            for antecedent in subsets(item):
                consequent = item.difference(antecedent)
                if consequent and consequent <= set(intru_cons):
                    antecedent = frozenset(antecedent)
                    XY = antecedent.union(consequent)
                    confidence = float(f_itemset[XY]) / f_itemset[antecedent]
                    lift = confidence / (f_itemset[antecedent] * f_itemset[consequent])
                    if confidence >= min_confidence:
                        if lift >= min_lift:
                            #if consequent == "normal."or consequent == "DOS."or consequent == "Probing."or consequent == "R2L."or consequent == "U2R.":
                            if consequent <= set(intru_cons) :
                                if len(antecedent)+len(consequent)==15:
                                    antecedent = list(antecedent)
                                    consequent = list(consequent)
                                    rules.append((antecedent, consequent, confidence, lift))

    rules = sorted(rules, key=lambda iterator: iterator[2], reverse = True)
    return rules


# APRIORI ALGORITHM
def generate_itemsets_rules(data, min_support, min_confidence, min_lift):
    csv = open_data(data)

    # Get first itemset and transactions
    itemset, transaction_list = itemset_from_data(csv)

    # Get the frequent itemset
    f_itemset = frequent_itemset(transaction_list, itemset, min_support)

    # Association rules
    rules = get_rules(f_itemset, min_confidence, min_lift)
    return rules


# Print the frequent itemset and association rules
def print_result(rules):
    print('--Rules--')
    for antecedent, consequent, confidence, lift in sorted(rules, key=lambda iterator: iterator[0]):
        print('RULES: {} => {} : {} : {}'.format(tuple(antecedent), tuple(consequent), round(confidence, 5),
                                                 round(lift, 3)))

def print_result_txt(rules):
    print("--Print Rule Txt--")
    file_write_obj = open("rule.txt", 'w')
    for antecedent, consequent, confidence, lift in rules:
        file_write_obj.writelines('RULES: {} => {} : {} : {}'.format(tuple(antecedent), tuple(consequent), round(confidence, 5),
                                                 round(lift, 3)))
        file_write_obj.write('\n')
    file_write_obj.close()

# Store result to database
def store_result(rules, frequent_itemset):
    rulesnew = []

    ant = []
    cons = []
    conf = []
    lift = []
    for antecedent, consequent, confidence, lift in sorted(rules, key=lambda iterator: iterator[0]):
        ant.append(tuple(antecedent))
        cons.append(tuple(consequent))
        conf.append(round(confidence, 4))
        lift.append(round(lift, 3))
    return ant, cons, conf, lift


# Store result to json
def store_rule_json(rules):
    print("store rule to json")
    with open('rule.json', 'w') as f:
        json.dump(rules, f, indent=4)
    print('successfully saved rules!')
    return


def mine(csv, default_support=0.01, default_confidence=0.8, default_lift=1):

    data = open_data(csv)

    rules, itemset = generate_itemsets_rules(data, default_support, default_confidence, default_lift)

    return store_result(rules, itemset)
