"""
1. fuzzify data
2. compute rule
"""

import csv
import pyodbc
import time

import pandas as pd
import Apriori
import Fuzzification
import tqdm



def open_train_data(filename):
    df = pd.read_csv(filename, sep=',', header=None)
    # 14 features
    key = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate", "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "class"]
    key_index = [0, 2, 3, 4, 5, 22, 24, 27, 28, 31, 32, 35, 37, 38, 41] #start at 0
    value = []
    for k in key_index:
        value.append(list(df[k]))
    data = dict(zip(key, value))
    #print(data)
    return data


def write_fuzzified_data(data):
    file_name = "fuzzified.csv"
    save = pd.DataFrame(data)
    try:
        save.to_csv(file_name, header = 0, index = 0 )
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")
    print("successfully saved fuzzified.csv!")



if __name__ == '__main__':

    #------------fuzzify train data-----------
    data = open_train_data("5class_10k.csv")

    fuzzified_data = Fuzzification.fuzzify(data)
    #print(fuzzified_data)

    write_fuzzified_data(fuzzified_data)

    # ----------------compute rule--------------
    rules = Apriori.generate_itemsets_rules("fuzzified.csv",0.01, 0.95, 1)
    print("finish compute rule")

    Apriori.store_rule_json(rules)

    # Apriori.print_result(rules)
    #Apriori.print_result_txt(rules)
