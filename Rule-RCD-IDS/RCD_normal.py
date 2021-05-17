import numpy as np
import pandas as pd
import csv
import sys
import shutil
import os
import math
import matplotlib.pyplot as plt
from operator import itemgetter
from sklearn import preprocessing
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import json

np.set_printoptions(threshold = 1e6)
class ReadData():
    def __init__(self,dataFileWay):
        self.dataFileWay = dataFileWay

    def protocol(self,type):
        plist = ['tcp', 'udp', 'icmp']
        if type in plist:
            return plist.index(type)

    def service(self,type):
        slist = ['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u',
                'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest', 'hostnames',
                'http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell', 'ldap',
                'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp', 'nntp',
                'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje', 'shell',
                'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time', 'urh_i', 'urp_i',
                'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50']
        if type in slist:
            return slist.index(type)

    def flag(self,type):
        flist = ['OTH', 'REJ', 'RSTO', 'RSTOS0',
                'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH']
        if type in flist:
            return flist.index(type)

    def label(self,type):
        llist = ['normal.', 'DOS.', 'Probing.', 'R2L.', 'U2R.']
        if type in llist:
            return llist.index(type)
        else:
            llist.append(type)
            return llist.index(type)

    def readData(self):
        source = self.dataFileWay
        sourcefp = open(source, 'r')
        reader = csv.reader(sourcefp)

        # 统计行数
        length = 0
        while True:
            buffer = sourcefp.read(1024 * 8192)
            if not buffer:
                break
            length += buffer.count('\n')
        
        count = 0
        sourcefp.seek(0, 0)
        init_data = np.zeros((length,42))
        for line in reader:
            #print("\rReadData Processing progress：%.2f%%,line number is %d" %(float((count+1)/length*100), count), end=' ')
            tmp = np.zeros(42)
            tmp[0] = line[0]
            tmp[1] = self.protocol(line[1])
            tmp[2] = self.service(line[2])
            tmp[3] = self.flag(line[3])
            for i in range(4, 41, 1):
                tmp[i] = line[i]
            tmp[41] = self.label(line[41])
            tmp = tmp.astype(np.float)
            init_data[count] = tmp
            count += 1

        sourcefp.close()
        return init_data

class RCD():
    def __init__(self,dataSet_onehot,dataSet_normal):
        self.dataSet = dataSet_onehot
        self.dataSet_backup = dataSet_normal
        self.picsFileWay = 'Pics/result_5krare_noexpand.png'
        self.group = 0
        self.U = np.zeros(len(self.dataSet)).astype(np.int)
        #self.Ures = [[] for i in range(len(self.dataSet))]
        self.Ures = []
        self.Ur = []
        self.center = []

        for i in range(0,len(self.dataSet)):
            self.U[i] = i

    def init_Klist(self):
        # kLength = int(math.log(self.dataSet.shape[0],2)-1)
        # kList = np.zeros(kLength)
        # element = 1
        # for i in range(0, kLength, 1):
        #     element = element*2
        #     kList[i] = element

        kLength = int(self.dataSet.shape[0]/5)
        kList = np.zeros(kLength)
        element = 0
        for i in range(0, kLength, 1):
            element = element+5
            kList[i] = element


        self.kList = kList.astype(np.int)
        self.lof_score = np.zeros((self.kList.shape[0],self.dataSet.shape[0]))
        print("Klist is:",self.kList)
    
    def update_Klist(self):
        group_size = len(self.Ures[self.group-1])
        min_val = float("inf")
        for k in self.kList:
            if (k-group_size)**2 < min_val:
                min_val = (k-group_size)**2
                min_k = k
        
        while abs(min_k-group_size) > 5:
            min_k = (min_k + group_size)/2
            min_k = int(min_k)
            self.kList = self.kList.tolist()
            self.kList.append(min_k)
            self.kList = np.array(self.kList)
        self.kList.sort()

        for i in range(0,len(self.kList)):
            if self.kList[i] > self.dataSet.shape[0]:
                self.kList = self.kList[:i]
                break

        self.lof_score = np.zeros((self.kList.shape[0],self.dataSet.shape[0]))

    def get_outlierPoints_and_Kinf(self):
        outlier_points_label = np.zeros(self.dataSet.shape[0])
        Kinf = np.zeros(self.dataSet.shape[0])
        lof_min = np.zeros(self.dataSet.shape[0])
        for i in range(0,len(lof_min)):
            lof_min[i] = float("inf")

        count = 0
        for k in self.kList:
            #print("\rGet_outlierPoints_and_Kinf Processing progress：%.2f%%,K number is %d" %(float((count+1)/len(self.kList)*100), k), end=' ')
            clf = LocalOutlierFactor(n_neighbors=k)
            clf.fit_predict(self.dataSet)
            lof_score = -clf.negative_outlier_factor_
            self.lof_score[count] = lof_score

            for i in range(0,len(lof_score)):
                if lof_score[i] > 1:
                    outlier_points_label[i] = 1
                if lof_score[i] <= lof_min[i]:
                    # 这里用不用等号？
                    lof_min[i] = lof_score[i]
                    Kinf[i] = k
            count += 1

        for i in range(0,len(outlier_points_label)):
            if outlier_points_label[i] == 1:
                self.Ur.append(self.U[i])

        self.Kinf = Kinf.astype(np.int)

    def cal_all_C1(self):
        C1_val = np.zeros(self.dataSet.shape[0])
        for i in range(0,self.dataSet.shape[0]):
            #print("\rcal_all_C1 Processing progress：%.2f%%" %(float((i+1)/self.dataSet.shape[0]*100)), end=' ')
            C1_val[i] = self.cal_C1(i)
        self.C1_val = C1_val

    def cal_C1(self,index):
        Kinf_of_index = self.Kinf[index]
        pos = np.argwhere(self.kList == Kinf_of_index)
        pos = int(pos[0][0])

        if pos < len(self.kList)-1:
            Kinf_addone = pos+1
        elif pos >= 1:
            Kinf_addone = pos-1
        else:
            Kinf_addone = pos

        C1 = self.lof_score[Kinf_addone][index]/self.lof_score[pos][index]
        return C1

    def cal_C2(self,index):
        Kinf_of_index = self.Kinf[index]
        neigh = NearestNeighbors(n_neighbors=int(Kinf_of_index))
        neigh.fit(self.dataSet)
        kneighbors = neigh.kneighbors([self.dataSet[index]])[1].flatten()
        
        C1_sum = 0
        for i in kneighbors:
            C1_sum += self.C1_val[i]
        C2 = C1_sum / Kinf_of_index
        return C2
    
    def cal_C3(self,index):
        Kinf_of_index = self.Kinf[index]
        Kavg = (Kinf_of_index+2)/2

        neigh1 = NearestNeighbors(n_neighbors=int(Kinf_of_index))
        neigh1.fit(self.dataSet)
        kdistances1 = neigh1.kneighbors([self.dataSet[index]])[0].flatten()
        distance1 = kdistances1[len(kdistances1)-1]

        neigh2 = NearestNeighbors(n_neighbors=int(Kavg))
        neigh2.fit(self.dataSet)
        kdistances2 = neigh2.kneighbors([self.dataSet[index]])[0].flatten()
        distance2 = kdistances2[len(kdistances2)-1]
        
        if distance2 == 0:
            C3 = 1
        else:
            C3 = distance1/distance2
        return C3
    
    def cal_C4(self,index):
        Kinf_of_index = self.Kinf[index]

        neigh = NearestNeighbors(n_neighbors=int(Kinf_of_index))
        neigh.fit(self.dataSet)
        kneighbors = neigh.kneighbors([self.dataSet[index]])[1].flatten()

        Kinf_of_neighbors = 0
        for i in kneighbors:
            Kinf_of_neighbors += self.Kinf[i]
        
        mid_val = abs(Kinf_of_index / (Kinf_of_neighbors / Kinf_of_index)-1)
        C4 = math.exp(-mid_val)
        return C4
    
    def cal_C(self,index):
        C1 = self.C1_val[index]
        C2 = self.cal_C2(index)
        C3 = self.cal_C3(index)
        C4 = self.cal_C4(index)
        C = (C1*C2*C3*C4)**0.25
        return C

    def find_class(self):
        C = []
        C_pos = []
        C_max = -1
        count = 0
        for u in self.Ur:
            #print("\rfind_class Processing progress：%.2f%%" %(float((count+1)/len(self.Ur)*100)), end=' ')
            pos = np.argwhere(self.U == u)
            pos = int(pos)
            C_tmp = self.cal_C(pos)
            if C_tmp > C_max:
                C_max = C_tmp
                a = pos
            count += 1

        self.center.append(self.U[a])
        C.append(self.U[a])
        C_pos.append(a)
        Kinf_of_index = self.Kinf[a]
        neigh = NearestNeighbors(n_neighbors=int(Kinf_of_index))
        neigh.fit(self.dataSet)
        kdistances = neigh.kneighbors([self.dataSet[a]])[0].flatten()
        kneighbors = neigh.kneighbors([self.dataSet[a]])[1].flatten()
        for neighbor in kneighbors:
            if self.U[neighbor] not in C:
                C.append(self.U[neighbor])
                C_pos.append(neighbor)

        # expand
        # distance_avg = np.mean(kdistances)
        # C_expand = []
        # for b in C_pos:
        #     if b != a:
        #         neigh = NearestNeighbors(n_neighbors=self.dataSet.shape[0])
        #         neigh.fit(self.dataSet)
        #         kdistances = neigh.kneighbors([self.dataSet[b]])[0].flatten()
        #         kneighbors = neigh.kneighbors([self.dataSet[b]])[1].flatten()
        #         for i in range(0,len(kdistances)):
        #             if kdistances[i] < distance_avg and kneighbors[i] not in C_pos and kneighbors[i] not in C_expand:
        #                 C_expand.append(kneighbors[i])
        #                 C.append(self.U[kneighbors[i]])
        #                 C_pos.append(kneighbors[i])
        
        #self.Ures[self.group] = list(C)
        self.Ures.append(list(C))
        self.group += 1
        C = np.array(C)
        self.U = np.setdiff1d(self.U,C)
        C_pos = np.array(C_pos)
        self.dataSet = np.delete(self.dataSet,C_pos,axis=0)

    def handle(self):
        self.init_Klist()

        while True:
            print("Length of Dataset is:",self.dataSet.shape[0])
            self.Ur = []
            self.get_outlierPoints_and_Kinf()
            #print("Ur is:",len(self.Ur))
            self.cal_all_C1()
            if len(self.Ur) != 0:
                self.find_class()
                self.update_Klist()
                #print('\n')
                #print("New Klist is:",self.kList)
            else:
                if len(self.U) != 0 :
                    self.center.append(self.U[int(len(self.U)/2)])
                    #self.Ures[self.group] = self.U.tolist()
                    self.Ures.append(self.U.tolist())
                    self.group += 1
                break
            if len(self.kList) == 0:
                if len(self.U) != 0:
                    self.center.append(self.U[int(len(self.U) / 2)])
                    #self.Ures[self.group] = self.U.tolist()
                    self.Ures.append(self.U.tolist())
                    self.group += 1
                break

        self.center = np.array(self.center).astype(np.int)
        
        # colors = ["#FF0000", "#3300FF", "#00FF00", "#CD7F32", "#FFFF00", "#FFF0F5", "#E0FFFF",
        #   "#6A5ACD", "#008000", "#FF69B4", "#F08080", "#FAF0E6", "#808000", "#FFC0CB",
        #   "#F0F8FF", "#00FFFF", "#7FFF00", "#E9967A", "#B22222", "#008000", "#FFF0F5",
        #   "#FFB6C1", "#B0C4DE", "#3CB371", "#FFA500", "#FFEFD5", "#D2B48C", "#9ACD32"]
        # print("\nUres is: \n")
        # for i in range(0,self.group):
        #     print("Group ",i,",Center is point",self.center[i])
        #     print("Group points are ",self.Ures[i])
        #     print("Point number of group is",len(self.Ures[i]))
        #     for j in range(0,len(self.Ures[i])):
        #         row = int(self.Ures[i][j])
        #         plt.scatter(self.dataSet_backup[row,0], self.dataSet_backup[row,1], color=colors[i])
        # plt.savefig(self.picsFileWay)
        # plt.show()

        return self.center,self.Ures


def find_rare_category(filename):
    myReadData = ReadData(filename)

    init_data = myReadData.readData()
    key_index = [0, 2, 3, 4, 5, 22, 24, 27, 28, 31, 32, 35, 37, 38]  # start at 0
    select_column = key_index
    select_data = init_data[:, select_column]

    #数据归一化
    select_data_scaled = preprocessing.StandardScaler().fit_transform(select_data)
    select_data_scaled = preprocessing.MinMaxScaler().fit_transform(select_data_scaled)

    myRCD = RCD(select_data_scaled,select_data_scaled)
    center,Ures = myRCD.handle()
    for i in range(0,len(center)):
        print("Group ",i,",Center is point",center[i])
        #print("value is:",select_data[center[i]])
        print("Group points are ",Ures[i])

    #-----------store result in json file----------
    result = {}
    result['center'] = list(map(str, center.tolist()))
    result['Ures'] = [list(map(str, u)) for u in Ures]

    print("store RCD result to json")
    with open('RCD_result.json', 'w') as f:
        json.dump(result, f, indent=4)
    print('successfully saved RCD result!')

    #------------RCD based answer--------
    answer = RCD_answer(center.tolist(), Ures, select_data_scaled.shape[0])
    #print(answer)

    return center, Ures, answer

def RCD_answer(center, Ures, data_len):
    answer = data_len*['']

    for u in Ures:
        if len(u) < 0.1* data_len:
            for i in u:
                answer[i] = 'RARE'
        else:
            for i in u:
                answer[i] = 'normal.'

    return answer



if __name__=="__main__":
    # dataFileWay = 'Data/5class_5krare.csv'
    # picsFileWay = 'Pics/5class_5krare.png'
    dataFileWay = '5class_300.csv'
    ReadData = ReadData(dataFileWay)

    # 获得的原始数据 9654*32
    init_data = ReadData.readData()
    # 选择特定列的数据 9654*n
    select_column = [22]
    select_data = init_data[:,select_column]


    # onehot编码
    # enc = OneHotEncoder()
    # select_data_onehot = enc.fit_transform(select_data).toarray()
    # print('\n')
    # print("Shape of select_data is:",select_data.shape)
    # print("Shape of select_data_onehot is:",select_data_onehot.shape)
    # print('\n')

    # 数据归一化
    # select_data_scaled = preprocessing.StandardScaler().fit_transform(select_data)
    # select_data_scaled = preprocessing.MinMaxScaler().fit_transform(select_data_scaled)

    # 画图（原始数据）
    # colors = ['red','yellow','blue','black','purple']
    # colors = np.array(colors)
    # for i in range(0,select_data.shape[0]):
    #         plt.scatter(select_data[i,0], select_data[i,1], color=colors[int(init_data[i,41])])
    # plt.savefig(picsFileWay)
    # plt.show()

    RCD = RCD(select_data,select_data)
    center,Ures = RCD.handle()
    for i in range(0,len(center)):
        print("Group ",i,",Center is point",center[i])
        print("value is:",select_data[center[i]])
        print("Group points are ",Ures[i])

    #find_rare_category("undefined_test_data.csv")



