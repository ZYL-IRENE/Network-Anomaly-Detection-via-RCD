import json
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

def get_test_data_json():
    data_file = "test2.csv"
    df = pd.read_csv(data_file, sep=',', header=None)
    # listdata = df[df.columns[:-1]].values.tolist()
    key = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate",
           "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate",
           "dst_host_serror_rate",
           "dst_host_srv_serror_rate", "class"]
    key_index = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39, 42]
    value = []
    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose()

    data_json = []
    for index, row in data.iterrows():
        dict1 = {"id": index}
        dict2 = dict(zip(key, list(row)))
        mydict = dict(dict1, **dict2)
        data_json.append(mydict)

    #data_json = json.dumps(data_json, indent=4)
    return data_json


def scatter_get_test_data_json():
    classes = ['normal.', 'DOS.', "PROBE.", "U2R.", "R2L."]
    services = ["http", 'ecr_i', 'smtp', 'domain_u', 'auth', 'finger', 'private', 'imap4', 'telnet', 'uucp',
                'hostnames', 'gopher', 'ftp_data', 'pm_dump', 'eco_i', 'ftp', 'other']
    flags = ['SF', 'REJ', 'S0', 'SH', 'S1', 'RSTO', 'RSTR', 'S2']

    data_file = "test2.csv"
    df = pd.read_csv(data_file, sep=',', header=None)
    # listdata = df[df.columns[:-1]].values.tolist()
    key = ["x", "y", "label"]
    key_index = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39]
    label = []
    value = []
    label.append(list(df[41]))
    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose().values
    label = pd.DataFrame(label)
    label = label.transpose().values

    for i in range(0, data.shape[0]):
        data[i][1] = services.index(data[i][1])
        data[i][2] = flags.index(data[i][2])
        label[i] = classes.index(label[i])

    data_embedded = TSNE(n_components=2).fit_transform(data)
    data_embedded = preprocessing.MinMaxScaler().fit_transform(data_embedded)

    data = pd.DataFrame(data_embedded)
    label = pd.DataFrame(label)
    data['label'] = label

    data_json = []
    for index, row in data.iterrows():
        dict1 = {"id": index}
        dict2 = dict(zip(key, row))
        mydict = dict(dict1, **dict2)
        data_json.append(mydict)

    return data_json

def radar_get_test_data_json():
    classes = ['normal.','DOS.',"PROBE.","U2R.","R2L."]
    services = ["http", 'ecr_i','smtp','domain_u','auth','finger','private','imap4','telnet','uucp','hostnames','gopher','ftp_data','pm_dump','eco_i','ftp','other']
    flags = ['SF','REJ','S0','SH','S1','RSTO','RSTR','S2']

    data_file = "test2.csv"
    df = pd.read_csv(data_file, sep=',', header=None)
    # listdata = df[df.columns[:-1]].values.tolist()
    key = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate",
           "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate",
           "dst_host_serror_rate",
           "dst_host_srv_serror_rate"]
    key_index = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39]
    value = []
    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose().values

    for i in range(0,data.shape[0]):
        data[i][1] = services.index(data[i][1])
        data[i][2] = flags.index(data[i][2])

    data = pd.DataFrame(data)

    data_json = []              
    for index, row in data.iterrows():
        dict1 = {"id": index}
        dict2 = dict(zip(key, row))
        mydict = dict(dict1, **dict2)
        data_json.append(mydict)

    return data_json


def circle_get_test_data_json():
    classes = ['normal.', 'DOS.', "PROBE.", "U2R.", "R2L."]
    services = ["http", 'ecr_i', 'smtp', 'domain_u', 'auth', 'finger', 'private', 'imap4', 'telnet', 'uucp',
                'hostnames', 'gopher', 'ftp_data', 'pm_dump', 'eco_i', 'ftp', 'other']
    flags = ['SF', 'REJ', 'S0', 'SH', 'S1', 'RSTO', 'RSTR', 'S2']

    data_file = "test2.csv"
    df = pd.read_csv(data_file, sep=',', header=None)
    # listdata = df[df.columns[:-1]].values.tolist()
    key = ["kneighbors"]
    key_index = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39]
    value = []
    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose().values

    for i in range(0, data.shape[0]):
        data[i][1] = services.index(data[i][1])
        data[i][2] = flags.index(data[i][2])

    result = []
    neigh = NearestNeighbors(n_neighbors=31)
    neigh.fit(data)
    for i in range(0, data.shape[0]):
        kneighbors = neigh.kneighbors([data[i]])[1].flatten()
        result.append(int(kneighbors[30]))

    result = pd.DataFrame(result)

    data_json = []
    for index, row in result.iterrows():
        dict1 = {"id": index}
        dict2 = dict(zip(key, row))
        mydict = dict(dict1, **dict2)
        data_json.append(mydict)

    return data_json