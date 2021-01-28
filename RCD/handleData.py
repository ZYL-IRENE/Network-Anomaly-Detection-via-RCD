from matplotlib import pyplot as p
import numpy as np
import pandas as pd
import csv

avg = np.zeros(13)
stad = np.zeros(13)
min = np.array([5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0,
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0])
max = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


def handleData():
    source = 'test_data500.csv'
    result = 'selected_data500.csv'
    sourcefp = open(source, 'r')
    resultfp = open(result, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(resultfp)

    count = 0
    for line in reader:
        count += 1

        tmp = np.zeros(13)
        tmp[0] = int(count)
        tmp[1] = int(line[0])
        tmp[2] = int(protocol(line[1]))
        tmp[3] = int(service(line[2]))
        tmp[4] = int(flag(line[3]))
        for i in range(5, 12, 1):
            tmp[i] = int(line[i-1])
        tmp[12] = int(label(line[41]))
        tmp = tmp.astype(np.int32)

        writer.writerow(tmp)
        # print(count,'status:',tmp[1],tmp[2],tmp[3],tmp[12])

    sourcefp.close()
    resultfp.close()


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


def Remove():
    source = 'selected_data500.csv'
    result = 'removed_data500.csv'
    sourcefp = open(source, 'r')
    resultfp = open(result, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(resultfp)

    tmp_instances = []
    instances = []
    tmp_labels = []
    labels = []
    pos = []

    for line in reader:
        coordinate = (float(line[1]), int(float(line[2])), int(float(line[3])), int(float(line[4])), float(line[5]),
                      float(line[6]), int(float(line[7])), float(line[8]), float(line[9]), float(line[10]), float(line[11]))
        label = (int(float(line[0])), int(float(line[12])))
        tmp_instances.append(coordinate)
        tmp_labels.append(label)

    for i in range(0, len(tmp_instances), 1):
        if tmp_instances.count(tmp_instances[i]) > 1 and tmp_instances.index(tmp_instances[i]) not in pos:
            pos.append(tmp_instances.index(tmp_instances[i]))
            for j in range(0, len(tmp_instances), 1):
                if tmp_instances[i] == tmp_instances[j] and j != tmp_instances.index(tmp_instances[j]):
                    for k in range(0, len(tmp_labels), 1):
                        if tmp_labels[k][0] == j + 1:
                            tmp_labels.remove(tmp_labels[k])
                            break

    for i in tmp_instances:
        if i not in instances:
            instances.append(i)
    for i in range(0, len(tmp_labels), 1):
        labels.append((i+1, tmp_labels[i][1]))

    for i in range(0, len(instances), 1):
        tmp = np.zeros(13)
        tmp[0] = labels[i][0]
        for j in range(0, 11, 1):
            tmp[j+1] = instances[i][j]
        tmp[12] = labels[i][1]
        tmp = tmp.astype(np.int32)
        writer.writerow(tmp)

    sourcefp.close()
    resultfp.close()

    x, y = zip(*labels)
    p.scatter(x, y, 20, color="#0000FF")
    p.show()


def standardization():
    source = 'removed_data500.csv'
    result = 'standard_data500.csv'
    sourcefp = open(source, 'r')
    resultfp = open(result, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(resultfp)

    contlist = [1, 5, 6, 8, 9, 10, 11]
    count = 0

    tmp1 = np.zeros(13)
    tmp1 = tmp1.astype(np.int64)
    for line in reader:
        count += 1
        for i in contlist:
            tmp1[i] += int(line[i])
    for i in contlist:
        avg[i] = round(tmp1[i] / count, 4)

    sourcefp.seek(0)
    tmp2 = np.zeros(13)
    for line in reader:
        for i in contlist:
            tmp2[i] += np.abs(float(line[i]) - avg[i])
    for i in contlist:
        stad[i] = round(tmp2[i] / count, 4)

    sourcefp.seek(0)
    tmp3 = np.zeros(13)
    for line in reader:
        for i in range(0, 13, 1):
            if i in contlist:
                if float(stad[i]) == 0 or float(avg[i]) == 0:
                    tmp3[i] = 0
                else:
                    tmp3[i] = round(
                        (float(line[i])-float(avg[i]))/float(stad[i]), 4)

                if tmp3[i] < min[i]:
                    min[i] = tmp3[i]
                if tmp3[i] > max[i]:
                    max[i] = tmp3[i]
                print(tmp3[i], min[i], max[i])
            else:
                tmp3[i] = int(line[i])

        writer.writerow(tmp3)

    sourcefp.close()
    resultfp.close()


def normalization():
    source = 'standard_data500.csv'
    result = 'normal_data500.csv'
    sourcefp = open(source, 'r')
    resultfp = open(result, 'w', newline='')
    reader = csv.reader(sourcefp)
    writer = csv.writer(resultfp)

    contlist = [1, 5, 6, 8, 9, 10, 11]
    tmp = np.zeros(13)
    for line in reader:
        for i in range(0, 13, 1):
            if i in contlist:
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
    handleData()
    print("first handle is over")
    Remove()
    print("Remove is over")
    standardization()
    print("standardization is over")
    normalization()
    print("normalization is over")
