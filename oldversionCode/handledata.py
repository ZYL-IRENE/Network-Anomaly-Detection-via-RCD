from matplotlib import pyplot as p
import numpy as np
import pandas as pd
import csv
import sys
import shutil
from operator import itemgetter
import os

initFile = 'Data/kddcup10percent.csv'
formatFile = 'Data/selected_kddcup10percent.csv'
reduceFile = 'Data/reduced_kddcup10percent.csv'
sortFile = 'Data/sorted_kddcup10percent.csv'
standardFile = 'Data/standard_kddcup10percent.csv'
normalFile = 'Data/normal_kddcup10percent.csv'
pictureWay = 'Pics/kddcup10percent.png'

avg = np.zeros(12)
stad = np.zeros(12)
min = np.array([5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0,
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0])
max = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


def protocol(type):
    plist = ['tcp', 'udp', 'icmp']
    if type in plist:
        return plist.index(type)


def service(type):
    slist = ['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u',
             'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest', 'hostnames',
             'http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell', 'ldap',
             'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp', 'nntp',
             'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje', 'shell',
             'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time', 'urh_i', 'urp_i',
             'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50']
    if type in slist:
        return slist.index(type)


def flag(type):
    flist = ['OTH', 'REJ', 'RSTO', 'RSTOS0',
             'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH']
    if type in flist:
        return flist.index(type)


def label(type):
    llist = ['normal.', 'buffer_overflow.', 'loadmodule.', 'perl.', 'neptune.', 'smurf.',
             'guess_passwd.', 'pod.', 'teardrop.', 'portsweep.', 'ipsweep.', 'land.', 'ftp_write.',
             'back.', 'imap.', 'satan.', 'phf.', 'nmap.', 'multihop.', 'warezmaster.', 'warezclient.',
             'spy.', 'rootkit.']
    if type in llist:
        return llist.index(type)
    else:
        llist.append(type)
        return llist.index(type)


def format():
    if os.path.exists(formatFile):
        os.remove(formatFile)
    if os.path.exists(reduceFile):
        os.remove(reduceFile)
    if os.path.exists(sortFile):
        os.remove(sortFile)
    if os.path.exists(standardFile):
        os.remove(standardFile)
    if os.path.exists(normalFile):
        os.remove(normalFile)

    source = initFile
    target = formatFile
    sourcefp = open(source, 'r')
    targetfp = open(target, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(targetfp)

    # 统计行数
    length = 0
    while True:
        buffer = sourcefp.read(1024 * 8192)
        if not buffer:
            break
        length += buffer.count('\n')
    # print(length)

    count = 0
    sourcefp.seek(0, 0)
    for line in reader:
        count += 1
        print("\rProcessing progress：%.2f%%,line number is %d" %
              (float(count/length*100), count), end=' ')

        tmp = np.zeros(12)
        tmp[0] = int(line[0])
        tmp[1] = int(protocol(line[1]))
        tmp[2] = int(service(line[2]))
        tmp[3] = int(flag(line[3]))
        for i in range(4, 11, 1):
            tmp[i] = int(line[i])
        tmp[11] = int(label(line[41]))
        tmp = tmp.astype(np.int32)

        if tmp[11] != 0:
            writer.writerow(tmp)

    sourcefp.close()
    targetfp.close()


def reduce():
    source = formatFile
    target = reduceFile

    lines_seen = set()
    sourcefp = open(source, 'r', encoding='utf-8')
    targetfp = open(target, 'a+', encoding='utf-8')

    # 统计行数
    length = 0
    while True:
        buffer = sourcefp.read(1024 * 8192)
        if not buffer:
            break
        length += buffer.count('\n')

    count = 0
    sourcefp.seek(0, 0)
    for line in sourcefp:
        count += 1
        print("\rProcessing progress：%.2f%%,line number is %d" %
              (float(count/length*100), count), end=' ')
        if line not in lines_seen:
            targetfp.write(line)
            lines_seen.add(line)

    sourcefp.close()
    targetfp.close()


def sort():
    source = reduceFile
    target = sortFile
    sourcefp = open(source, 'r')
    targetfp = open(target, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(targetfp)

    table = []
    for line in reader:
        tmp = np.zeros(12)
        for i in range(0, 12, 1):
            tmp[i] = int(line[i])
        tmp = tmp.astype(np.int32)
        table.append(tmp)
    table_sorted = sorted(table, key=itemgetter(11))
    for row in table_sorted:
        writer.writerow(row)

    sourcefp.close()
    targetfp.close()


def paint():
    source = sortFile
    # Paint
    count = 0
    labels = []
    with open(source, 'rb') as paintfp:
        for line in paintfp:
            count = count+1
            tmp = line.decode().strip().split(',')
            label = (count, int(float(tmp[11])))
            labels.append(label)
    x, y = zip(*labels)
    p.scatter(x, y, 20, color="#0000FF")
    p.savefig(pictureWay)
    p.show()


def standardization():
    source = sortFile
    result = standardFile
    sourcefp = open(source, 'r')
    resultfp = open(result, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(resultfp)

    continue_list = [0, 4, 5, 7, 8, 9, 10]

    count = 0
    tmp1 = np.zeros(12)
    tmp1 = tmp1.astype(np.int64)
    for line in reader:
        count += 1
        for i in continue_list:
            tmp1[i] += int(line[i])
    for i in continue_list:
        avg[i] = round(tmp1[i] / count, 4)

    sourcefp.seek(0)
    tmp2 = np.zeros(12)
    for line in reader:
        for i in continue_list:
            tmp2[i] += np.abs(float(line[i]) - avg[i])
    for i in continue_list:
        stad[i] = round(tmp2[i] / count, 4)

    sourcefp.seek(0)
    tmp3 = np.zeros(12)
    for line in reader:
        for i in range(0, 12, 1):
            if i in continue_list:
                if float(stad[i]) == 0 or float(avg[i]) == 0:
                    tmp3[i] = 0
                else:
                    tmp3[i] = round(
                        (float(line[i])-float(avg[i]))/float(stad[i]), 4)

                if tmp3[i] < min[i]:
                    min[i] = tmp3[i]
                if tmp3[i] > max[i]:
                    max[i] = tmp3[i]
            else:
                tmp3[i] = int(line[i])
        writer.writerow(tmp3)

    sourcefp.close()
    resultfp.close()


def normalization():
    source = standardFile
    result = normalFile
    sourcefp = open(source, 'r')
    resultfp = open(result, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(resultfp)

    continue_list = [0, 4, 5, 7, 8, 9, 10]

    tmp = np.zeros(12)
    for line in reader:
        for i in range(0, 12, 1):
            if i in continue_list:
                if float(max[i])-float(min[i]) == 0:
                    tmp[i] = 0
                else:
                    tmp[i] = round((float(line[i])-float(min[i])) /
                                   (float(max[i])-float(min[i])), 4)
            else:
                tmp[i] = line[i]
        writer.writerow(tmp)

    sourcefp.close()
    resultfp.close()


if __name__ == '__main__':
    # 读入数据，删除normal类型
    format()
    print("Format is over")
    # 删除重复数据
    reduce()
    print("Reduce is over")
    # 按照异常类型进行排序
    sort()
    print("Sort is over")
    # 画图
    paint()
    print("Paint is over")
    # 数值标准化
    standardization()
    print("Standardization is over")
    # 数值归一化
    normalization()
    print("Normalization is over")
