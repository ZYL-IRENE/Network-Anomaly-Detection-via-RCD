from flask import Flask, jsonify, render_template, request
import json
import pandas as pd

import getJson

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("./index.html")


@app.route('/tableQuery',methods=['GET','POST'])
def query():
    data = getJson.get_test_data_json()

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)
        #return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
        return jsonify(data)


@app.route('/parallelQuery',methods=['GET','POST'])
def para_query():
    data = getJson.get_test_data_json()

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/scatterPlot',methods=['GET','POST'])
def scatter_query():
    data = getJson.scatter_get_test_data_json()
    
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/radarPlot',methods=['GET','POST'])
def radar_query():
    data = getJson.radar_get_test_data_json()
    
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


@app.route('/circlePlot',methods=['GET','POST'])
def circle_query():
    data = getJson.circle_get_test_data_json()

    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        return jsonify(data)


if __name__ == '__main__':
    app.run()