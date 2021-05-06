import json
import pandas as pd


def get_test_data_json():
    data_file = "TEST.csv"
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
