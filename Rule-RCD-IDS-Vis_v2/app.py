from flask import Flask, jsonify,render_template,request,redirect
import json
from numpy.lib.function_base import select
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import getJson
import RCD_normal
import os
from sklearn import preprocessing
import csv

app = Flask(__name__)
pwd = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(pwd,'save_file')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Fileway = "save_file/test2.csv"
RCDFileway = "save_file/rcd_data.csv"
selected = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39, 42]

def RCD(Fileway,selected):
    ReadData = RCD_normal.ReadData(Fileway)
    init_data = ReadData.readData()
    select_column = [x-1 for x in selected]
    select_column.pop()
    select_data = init_data[:,select_column]
    select_data_scaled = preprocessing.StandardScaler().fit_transform(select_data)
    select_data_scaled = preprocessing.MinMaxScaler().fit_transform(select_data_scaled)

    RCD = RCD_normal.RCD(select_data_scaled,select_data_scaled)
    center,Ures = RCD.handle()
    for i in range(0,len(center)):
        print("Group ",i,",Center is point",center[i])
        print("Group points are ",Ures[i])

    f = open(RCDFileway,'w',encoding='utf-8',newline="")
    csv_writer = csv.writer(f)
    tmpdata = []
    for index in range(0,len(init_data)):
        for i in range(0,len(Ures)):
            for j in range(0,len(Ures[i])):
                if Ures[i][j]==index:
                    tmpdata = select_data[Ures[i][j]].tolist()
                    tmpdata.append(i)
                    csv_writer.writerow(tmpdata)
    f.close()

@app.route('/')
def index():
    return render_template("./index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global Fileway

    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Fileway = filename
        print("file uploaded successfully")
        return redirect("/")
        # return 'file uploaded successfully'
    return "file uploaded Fail"


@app.route('/upload_features', methods=['GET', 'POST'])
def upload_features():
    global selected
    key = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate",
           "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate",
           "dst_host_serror_rate", "dst_host_srv_serror_rate", "class"]
    key_index = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39, 42]
    
    selected = request.form.getlist('selected_features')
    for i in range(0,len(selected)):
        selected[i] = key_index[key.index(selected[i])]
    RCD(Fileway, selected)

    return render_template("./index.html")


@app.route('/tableQuery',methods=['GET','POST'])
def query():
    data = getJson.get_test_data_json(Fileway)

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)
        return jsonify(data)


@app.route('/parallelQuery',methods=['GET','POST'])
def para_query():
    data = getJson.get_test_data_json(Fileway)

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/scatterTSNEPlot',methods=['GET','POST'])
def scatter_tsne_query():
    data = getJson.scatter_get_tsne_data_json(RCDFileway,selected)
    
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/scatterMDSPlot',methods=['GET','POST'])
def scatter_mds_query():
    data = getJson.scatter_get_mds_data_json(RCDFileway,selected)
    
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/scatterLDAPlot',methods=['GET','POST'])
def scatter_lda_query():
    data = getJson.scatter_get_lda_data_json(RCDFileway,selected)
    
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/radarPlot',methods=['GET','POST'])
def radar_query():
    data = getJson.radar_get_test_data_json(Fileway)
    
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/circlePlot',methods=['GET','POST'])
def circle_query():
    data = getJson.circle_get_test_data_json(Fileway)

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)

@app.route('/heatMap',methods=['GET','POST'])
def rule_query():
    data = getJson.rule_get()

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)

@app.route('/featureCorr',methods=['GET','POST'])
def get_feature_corr():
    data, temp = getJson.feature_corr(Fileway)

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)

@app.route('/featureVar',methods=['GET','POST'])
def get_feature_var():
    temp, data = getJson.feature_corr(Fileway)

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()
