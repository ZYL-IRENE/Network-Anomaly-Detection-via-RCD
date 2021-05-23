import json
import pandas as pd
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors 

classes = ['normal.', 'DOS.', "PROBE.", "U2R.", "R2L."]
services = ["http", 'ecr_i', 'smtp', 'domain_u', 'auth', 'finger', 'private', 'imap4', 'telnet', 'uucp','hostnames', 'gopher', 'ftp_data', 'pm_dump', 'eco_i', 'ftp', 'other']
flags = ['SF', 'REJ', 'S0', 'SH', 'S1', 'RSTO', 'RSTR', 'S2']


def get_test_data_json(fileway):
    data_file = fileway
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

def scatter_get_tsne_data_json(fileway,selected):
    data_file = fileway
    df = pd.read_csv(data_file, sep=',', header=None)

    key = ["x", "y", "label"]
    key_index = selected
    print(key_index)
    label = []
    value = []

    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose().values
    label = data[:,data.shape[1]-1]
    data = data[:,0:data.shape[1]-1]

    if 3 in selected: 
        for i in range(0, data.shape[0]):
            data[i][selected.index(3)] = services.index(data[i][selected.index(3)])
    if 4 in selected: 
        for i in range(0, data.shape[0]):
            data[i][selected.index(4)] = flags.index(data[i][selected.index(4)])
    for i in range(0, data.shape[0]):
        label[i] = classes.index(label[i])

    data_embedded = TSNE(n_components=2).fit_transform(data)
    # data_embedded = preprocessing.MinMaxScaler().fit_transform(data_embedded)

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

def scatter_get_mds_data_json(fileway,selected):
    data_file = fileway
    df = pd.read_csv(data_file, sep=',', header=None)

    key = ["x", "y", "label"]
    key_index = selected
    print(key_index)
    label = []
    value = []

    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose().values
    label = data[:,data.shape[1]-1]
    data = data[:,0:data.shape[1]-1]

    if 3 in selected: 
        for i in range(0, data.shape[0]):
            data[i][selected.index(3)] = services.index(data[i][selected.index(3)])
    if 4 in selected: 
        for i in range(0, data.shape[0]):
            data[i][selected.index(4)] = flags.index(data[i][selected.index(4)])
    for i in range(0, data.shape[0]):
        label[i] = classes.index(label[i])

    data_embedded = MDS(n_components=2).fit_transform(data)
    # data_embedded = preprocessing.MinMaxScaler().fit_transform(data_embedded)

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

def scatter_get_lda_data_json(fileway,selected):
    data_file = fileway
    df = pd.read_csv(data_file, sep=',', header=None)

    key = ["x", "y", "label"]
    key_index = selected
    print(key_index)
    label = []
    value = []

    for k in key_index:
        value.append(list(df[k - 1]))

    data = pd.DataFrame(value)
    data = data.transpose().values
    label = data[:,data.shape[1]-1]
    data = data[:,0:data.shape[1]-1]

    if 3 in selected: 
        for i in range(0, data.shape[0]):
            data[i][selected.index(3)] = services.index(data[i][selected.index(3)])
    if 4 in selected: 
        for i in range(0, data.shape[0]):
            data[i][selected.index(4)] = flags.index(data[i][selected.index(4)])
    for i in range(0, data.shape[0]):
        label[i] = classes.index(label[i])
    label = label.astype('int')
    label = label.ravel()

    data_embedded = LDA(n_components=2).fit_transform(data,label)
    # data_embedded = preprocessing.MinMaxScaler().fit_transform(data_embedded)

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

def radar_get_test_data_json(fileway):
    data_file = fileway
    df = pd.read_csv(data_file, sep=',', header=None)

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

def circle_get_test_data_json(fileway):
    data_file = fileway
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

    neighbor_num = 31
    result = []
    neigh = NearestNeighbors(n_neighbors=neighbor_num)
    neigh.fit(data)
    kneighbors = neigh.kneighbors(data)[1].flatten()
    kneighbors = kneighbors.reshape((data.shape[0],neighbor_num))
    for i in range(0, data.shape[0]):
        result.append(int(kneighbors[i][30]))

    result = pd.DataFrame(result)
    data_json = []
    for index, row in result.iterrows():
        dict1 = {"id": index}
        dict2 = dict(zip(key, row))
        mydict = dict(dict1, **dict2)
        data_json.append(mydict)

    return data_json