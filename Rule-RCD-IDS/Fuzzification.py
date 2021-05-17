"""
Created by Kyle Farinas
Copyright (c) 2018 Reynaldo John Tristan Mahinay Jr., Franz Stewart Dizon, Stephen Kyle Farinas and Harry Pardo
"""

import pandas as pd
import json
from numpy import array
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

import RCD_normal

fuzzy_str = {
    "duration":['duration_level1', 'duration_level2', 'duration_level3', 'duration_level4', 'duration_level5'],
    "service": ['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u', 'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest', 'hostnames', 'http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell', 'ldap', 'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp', 'nntp', 'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje', 'shell', 'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time', 'urh_i', 'urp_i', 'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50'],
    "flag": ['OTH', 'REJ', 'RSTO', 'RSTOS0', 'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH'],
    "src_bytes": ['src_bytes_level1', 'src_bytes_level2', 'src_bytes_level3', 'src_bytes_level4', 'src_bytes_level5'],
    "dst_bytes": ['dst_bytes_level1', 'dst_bytes_level2', 'dst_bytes_level3', 'dst_bytes_level4', 'dst_bytes_level5'],
    "count": ['count_level1', 'count_level2', 'count_level3', 'count_level4', 'count_level5'],
    "serror_rate": ['serror_rate_level1', 'serror_rate_level2', 'serror_rate_level3', 'serror_rate_level4', 'serror_rate_level5'],
    "srv_rerror_rate": ['srv_rerror_rate_level1', 'srv_rerror_rate_level2', 'srv_rerror_rate_level3', 'srv_rerror_rate_level4', 'srv_rerror_rate_level5'],
    "same_srv_rate": ['same_srv_rate_level1', 'same_srv_rate_level2', 'same_srv_rate_level3', 'same_srv_rate_level4', 'same_srv_rate_level5'],
    "dst_host_count": ['dst_host_count_level1', 'dst_host_count_level2', 'dst_host_count_level3', 'dst_host_count_level4', 'dst_host_count_level5'],
    "dst_host_srv_count": ['dst_host_srv_count_level1', 'dst_host_srv_count_level2', 'dst_host_srv_count_level3', 'dst_host_srv_count_level4', 'dst_host_srv_count_level5'],
    "dst_host_same_src_port_rate": ['dst_host_same_src_port_rate_level1', 'dst_host_same_src_port_rate_level2', 'dst_host_same_src_port_rate_level3', 'dst_host_same_src_port_rate_level4', 'dst_host_same_src_port_rate_level5'],
    "dst_host_serror_rate": ['dst_host_serror_rate_level1', 'dst_host_serror_rate_level2', 'dst_host_serror_rate_level3', 'dst_host_serror_rate_level4', 'dst_host_serror_rate_level5'],
    "dst_host_srv_serror_rate": ['dst_host_srv_serror_rate_level1', 'dst_host_srv_serror_rate_level2', 'dst_host_srv_serror_rate_level3', 'dst_host_srv_serror_rate_level4', 'dst_host_srv_serror_rate_level5'],
    "class": ["normal.", "DOS.", "Probing.", "R2L.", "U2R."]
}

def fuzzify(ppsd_data):
    col_headers = list(ppsd_data)
    #col_headers_len = len(col_headers)
    #col_headers = col_headers[:col_headers_len-1]  # exclude class

    class_list = list(ppsd_data['class'])
    class_encoded = encode_class(class_list)
    class_onehot = encode_class_onehot(class_list)

    data_fuzzified = []

    clustering_result ={}

    for col in col_headers:
        if (col != "service" and col != "flag" and col !="class"):
            data_normalized = normalize(ppsd_data[col])  # certain feature

            #data_clustering = kmCluster(data_normalized, class_encoded)
            class_weight = 10
            data_clustering = kmCluster_onehot(data_normalized, class_onehot, class_weight)
            #data_clustering = RCDCluster(data_normalized)
            clustering_result[col] = data_clustering
            data_membership = membership(data_normalized, data_clustering)

            data_fuzzified.append(fuzzy(data_membership, col))
        else:
            data_fuzzified.append(list(ppsd_data[col]))

    store_clustering_result(clustering_result)

    data_fuzzified = pd.DataFrame(data_fuzzified)
    data_fuzzified = data_fuzzified.transpose()

    return data_fuzzified

def fuzzify_test(ppsd_data):
    col_headers = list(ppsd_data)

    data_fuzzified = []

    clustering_result = get_clustering_result()

    for col in col_headers:
        # print(ppsd_data[col])
        if (col != "service" and col != "flag" and col !="class"):
            data_normalized = normalize(ppsd_data[col])  # certain feature

            data_clustering = clustering_result[col]
            data_membership = membership(data_normalized, data_clustering)

            data_fuzzified.append(fuzzy(data_membership, col))
        else:
            data_fuzzified.append(list(ppsd_data[col]))

    data_fuzzified = pd.DataFrame(data_fuzzified)
    data_fuzzified = data_fuzzified.transpose()

    return data_fuzzified


def encode_class(class_list):
    class_array = array(class_list)
    label_encoder = LabelEncoder()
    class_encoded = label_encoder.fit_transform(class_array)
    # onehot_encoder = OneHotEncoder(sparse=False)
    # integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    # onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    # class_onehot = []
    # for coded in onehot_encoded:
    #     coded = list(coded)
    #     class_onehot.append(coded)
    return class_encoded

def encode_class_onehot(class_list):
    class_array = array(class_list)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(class_array)
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    class_onehot = []
    for coded in onehot_encoded:
        coded = list(coded)
        class_onehot.append(coded)

    return class_onehot

def normalize(crispVal):
    converted = []
    for x in crispVal:
        x = float(x)
        converted.append(x)

    minimum = min(converted)
    maximum = max(converted)

    normalized = []

    for x in converted:
        x = 100 * ((x - minimum) / (maximum - minimum))
        normalized.append(x)

    return normalized


def membership(normVal, clusterVal):
    cA = clusterVal[0]
    cB = clusterVal[1]
    cC = clusterVal[2]
    cD = clusterVal[3]
    cE = clusterVal[4]
    # print(clusterVal)

    mem_val = []

    # R-Function
    def A(x):
        if (x > cB):
            mem_A = 0
        elif (cA <= x <= cB):
            mem_A = (cB - x) / (cB - cA)
        elif (x < cA):
            mem_A = 1

        return mem_A

    # Triangle Function
    def B(x):

        if (x <= cA):
            mem_B = 0
        elif (cA < x <= cB):
            mem_B = (x - cA) / (cB - cA)
        elif (cB < x < cC):
            mem_B = (cC - x) / (cC - cB)
        elif (x >= cC):
            mem_B = 0

        return mem_B

    # Triangle Function
    def C(x):

        if (x <= cB):
            mem_C = 0
        elif (cB < x <= cC):
            mem_C = (x - cB) / (cC - cB)
        elif (cC < x < cD):
            mem_C = (cD - x) / (cD - cC)
        elif (x >= cD):
            mem_C = 0

        return mem_C

    # Triangle Function
    def D(x):

        if (x <= cC):
            mem_D = 0
        elif (cC < x <= cD):
            mem_D = (x - cC) / (cD - cC)
        elif (cD < x < cE):
            mem_D = (cE - x) / (cE - cD)
        elif (x >= cE):
            mem_D = 0

        return mem_D

    # L-Function
    def E(x):

        if (x < cD):
            mem_E = 0
        elif (cD <= x <= cE):
            mem_E = (x - cD) / (cE - cD)
        elif (x > cE):
            mem_E = 1

        return mem_E

    for x in normVal:
        mem_val.append([A(x), B(x), C(x), D(x), E(x)])
    # mem_vals.append(mem_val)

    return mem_val


#append tags to each feature of each data
def fuzzy(memsVal, col_header):
    fuzzy_vals = fuzzy_str.get(col_header)

    final_fuzzy = []
    for mem in memsVal:
        y = mem.index(max(mem))
        final_fuzzy.append(fuzzy_vals[y])

    return final_fuzzy


def kmCluster(toCluster, weekNo):
    kmc = []
    for x, y in zip(weekNo, toCluster):
        # smc = []
        smc = [x, y]
        kmc.append(smc)
    # print(kmc)

    mem_means = []

    kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0)
    kmeans.fit(kmc)

    kk = kmeans.cluster_centers_
    # print(kk)
    for x, y in kk:
        mem_means.append(y)

    return sorted(mem_means)

def kmCluster_onehot(toCluster, weekNo, weight):
    kmc = []
    for x, y in zip(toCluster, weekNo):
        # smc = []
        y = [i * weight for i in y]
        y.append(x)
        kmc.append(y)
    # print(kmc)

    mem_means = []

    kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0)
    kmeans.fit(kmc)

    kk = kmeans.cluster_centers_
    # print(kk)
    for center in kk:
        mem_means.append(center[-1])

    return sorted(mem_means)

def RCDCluster(toCluster):
    kmc = []

    for x in toCluster:
        smc = [x]
        smc = array(smc)
        kmc.append(smc)

    kmc = array(kmc)
    mem_means = []

    RCD = RCD_normal.RCD(kmc, kmc)
    center,Ures = RCD.handle()

    center_value = [toCluster[i] for i in center]
    mem_means = list(set(center_value)) # eliminate duplicate


    if len(mem_means)==4:
        mem_means.append(max(toCluster))
    elif len(mem_means)==3:
        mem_means.append(max(toCluster))
        mem_means.append(min(toCluster))
    elif len(mem_means)<3:
        print("too few categories!")

    print(mem_means)
    return sorted(mem_means)
# Store result to json
def store_clustering_result(result):
    print("storing clustering result to json")
    with open('clustering_result.json', 'w') as f:
        json.dump(result, f, indent = 4)
    print('successfully saved clustering result!')
    return

def get_clustering_result():
    with open('clustering_result.json', 'r') as f:
        result = json.load(f)
    return result