import pandas as pd
import RuleBasedClassifier
import Apriori
import Fuzzification
import RCD_normal
import time

def open_test_data(filename):
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
    file_name = "fuzzified_test.csv"
    save = pd.DataFrame(data)
    try:
        save.to_csv(file_name, header = 0, index = 0 )
    except UnicodeEncodeError:
        print("something wrong in saving")
    print("successfully saved fuzzified test data!")

def save_undefined_data(filename, data_id):
    df = pd.read_csv(filename, sep=',', header=None)#original data file
    undefined_data = df.loc[data_id]

    file_name = "undefined_test_data.csv"
    try:
        undefined_data.to_csv(file_name, header = 0, index = 0 )
    except UnicodeEncodeError:
        print("something wrong in saving")
    print("successfully saved undefined test data!")

def undefined_data_class(filename):
    df = pd.read_csv(filename, sep=',', header=None)
    select_data = df[41]
    select_data = select_data.tolist()
    return select_data


#test executive time of only RCD
def RCD_time_test():
    start_time = time.time()
    center, Ures, RCD_answer = RCD_normal.find_rare_category("data/5class_3k.csv")
    time3 = time.time() - start_time
    print("RCD: --- %s seconds ---" % (time.time() - start_time))
    #print(center)
    #print(Ures)

    data_class = undefined_data_class("data/5class_3k.csv")

    RuleBasedClassifier.check_accuracy_rare(data_class, RCD_answer)

def rule_RCD_main():
    # #---------- fuzzify test data---------
    # data = open_test_data("data/5class_3k.csv")
    #
    # #start_time = time.time()
    # fuzzified_data = Fuzzification.fuzzify_test(data)
    # #time1 = time.time() - start_time
    # #print("Fuzzyfy: --- %s seconds ---" % (time.time() - start_time))
    #
    #
    # write_fuzzified_data(fuzzified_data)

    # #----------------read fuzzified data and rule-------------
    test_data = RuleBasedClassifier.open_test_data("fuzzified_test.csv")

    rules = RuleBasedClassifier.get_rules_json('rule_11.json')



    #------------------get rule prediction result ---------------
    start_time = time.time()
    prediction_apriori = RuleBasedClassifier.find_match(test_data, rules)
    time2 = time.time() - start_time
    #print("Rule matching: --- %s seconds ---" % (time.time() - start_time))


    undefined_data_id = RuleBasedClassifier.check_accuracy_attack(test_data, prediction_apriori)

    save_undefined_data("data/5class_3k.csv", undefined_data_id)


    # #-----------------rare category detection-------------
    start_time = time.time()
    center, Ures, RCD_answer = RCD_normal.find_rare_category("undefined_test_data.csv")
    time3 = time.time() - start_time
    #print("RCD: --- %s seconds ---" % (time.time() - start_time))
    #print(center)
    #print(Ures)
    #print(RCD_answer)
    data_class = undefined_data_class("undefined_test_data.csv")
    #print(data_class)

    RuleBasedClassifier.check_accuracy_rare(data_class, RCD_answer)

    print("Total time use: --- %s seconds ---" % (time2+time3))



def rule_len_test():
    ##-------------partition rule---------------------
    # rules = RuleBasedClassifier.get_rules_json('rule_all.json')
    #
    # RuleBasedClassifier.partition_rule_len(rules)

    # #---------- fuzzify test data---------
    # data = open_test_data("data/5class_3k.csv")
    #
    # fuzzified_data = Fuzzification.fuzzify_test(data)
    #
    # write_fuzzified_data(fuzzified_data)

    # #----------------read fuzzified data and rule-------------
    test_data = RuleBasedClassifier.open_test_data("fuzzified_test.csv")

    undefined_list = []
    accuracy_list = []
    precision_list = []
    recall_list =[]
    far_list = []
    for i in range(3,15):
        print('--------------evaluating rule of len %d --------------' %(i))
        filename = filename = 'rule/partition/rule_' + str(i) + '.json'
        rules = RuleBasedClassifier.get_rules_json(filename)
        #------------------get rule prediction result ---------------

        prediction_apriori = RuleBasedClassifier.find_match(test_data, rules)
        undefined_data_id, accuracy, precision, recall, far = RuleBasedClassifier.check_accuracy_attack(test_data, prediction_apriori)

        undefined_list.append(len(undefined_data_id))
        accuracy_list.append(accuracy)
        precision_list.append(precision)
        recall_list.append(recall)
        far_list.append(far)

    print("undefened",undefined_list)
    print("accuract", accuracy_list)
    print("precision",precision_list)
    print("recall", recall_list)
    print("far", far_list)
    return

if __name__ == '__main__':
    rule_RCD_main()





