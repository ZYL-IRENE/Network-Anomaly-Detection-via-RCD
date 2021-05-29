from flask import Flask, jsonify,render_template,request,redirect,url_for
import json
from numpy.core.arrayprint import printoptions
from numpy.lib.function_base import select
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import getJson
import RCD_normal
import os
from sklearn import preprocessing
import csv
import pandas as pd

app = Flask(__name__)
pwd = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(pwd,'save_file')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Fileway = "save_file/TEST.csv"
RCDFileway = "save_file/rcd_data.csv"
labelList = ['normal', 'DOS', 'PROBE', 'R2L', 'U2R']
selected = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39, 42]
center = []
Ures = []
label = []
group_num = 0

@app.route('/')
def index():
    return render_template("./index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global Fileway,label

    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Fileway = filename
        RCD(Fileway,selected)
        print("file uploaded successfully")
        return redirect("/")
        # return 'file uploaded successfully'
    return "file uploaded Fail"


@app.route('/upload_features', methods=['GET', 'POST'])
def upload_features():
    global selected,label
    key = ["duration", "service", "flag", "src_bytes", "dst_bytes", "count", "serror_rate", "srv_rerror_rate",
           "same_srv_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_src_port_rate",
           "dst_host_serror_rate", "dst_host_srv_serror_rate"]
    key_index = [1, 3, 4, 5, 6, 23, 25, 28, 29, 32, 33, 36, 38, 39]
    
    selected = request.form.getlist('selected_features')
    for i in range(0,len(selected)):
        selected[i] = key_index[key.index(selected[i])]
    RCD(Fileway,selected)
    selected.append(42)

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


@app.route('/centerArray',methods=['GET','POST'])
def center_array():
    data = center.tolist()

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/labelArray',methods=['GET','POST'])
def updatelabel():
    global group_num,label,center,Ures,labelList
    if request.method == 'POST':
        for index in Ures[group_num]:
            label[index] = request.form.get('label')
        group_num += 1

        if group_num == len(center):
            group_num = 0

            data = []  
            linenum = 0
            with open(Fileway, "r") as the_file:
                reader = csv.reader(the_file, delimiter=",")
                for row in reader:
                    new_row = []
                    for row_item in row:
                        new_row.append(row_item)
                    new_row.append(label[linenum])
                    linenum+=1
                    data.append(new_row)
            with open(Fileway, "w+",newline='') as the_file:
                writer = csv.writer(the_file, delimiter=",")
                for new_row in data:
                    writer.writerow(new_row)
            
            data = []  
            linenum = 0
            with open(RCDFileway, "r") as the_file:
                reader = csv.reader(the_file, delimiter=",")
                for row in reader:
                    new_row = []
                    for row_item in row:
                        new_row.append(row_item)
                    new_row[-1] = labelList.index(label[linenum])
                    linenum+=1
                    data.append(new_row)
            with open(RCDFileway, "w+",newline='') as the_file:
                writer = csv.writer(the_file, delimiter=",")
                for new_row in data:
                    writer.writerow(new_row)
        return redirect("/")
    if request.method == 'GET':
        return "get"


def RCD(Fileway,selected):
    global center,Ures,label
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

    label = ['normal' for i in range(len(init_data))]
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


if __name__ == '__main__':
    RCD(Fileway,selected)
    app.run()
