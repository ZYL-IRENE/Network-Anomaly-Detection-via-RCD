from matplotlib import pyplot as p
from lof import LOF, k_distance, distance_euclidean
import math
import os
import string
import sys

# 读入数据
source = 'normal_data256.csv'
instances = []
labels = []

with open(source, 'rb') as sourcefp:
    for line in sourcefp:
        tmp = line.decode().strip().split(',')
        coordinate = (float(tmp[1]), int(float(tmp[2])), int(float(tmp[3])), int(float(tmp[4])), float(tmp[5]),
                      float(tmp[6]), int(float(tmp[7])), float(tmp[8]), float(tmp[9]), float(tmp[10]), float(tmp[11]))
        label = (int(float(tmp[0])), int(float(tmp[12])))
        instances.append(coordinate)
        labels.append(label)
instancesBackup = instances
for instance in instances:
    print(instance)
for label in labels:
    print(label)

x, y = zip(*labels)
p.scatter(x, y, 20, color="#0000FF")
p.savefig('/home/PsyduckLiu/pics/PRP-RCD/init-log256.png')
p.show()

# KList参数设定
kLength = int(math.log(len(instances), 2))
# kLength = int(len(instances) / 2)
kList = []
tmp = 0 
# 邻接矩阵M
M = [[] for i in range(len(instances))]
pre_c1 = [list() for i in range(len(instances))]
kinf = [list() for i in range(len(instances))]
# 结果集合Ures
group = 0
Ures = [[] for i in range(len(instances))]
resLabel = [[] for i in range(len(instances))]
# 局部结果集合Ur
Ur = []
# 颜色数组
colors = ["#FF0000", "#3300FF", "#00FF00", "#CD7F32", "#FFFF00", "#FFF0F5",
          "#6A5ACD", "#008000", "#FF69B4", "#F08080", "#FAF0E6", "#808000", "#FFC0CB"]

# 初始化KList
for i in range(0, kLength, 1):
    tmp = tmp + 2
    kList.append(tmp)
print("Klist :", kList)

# 更新邻接矩阵M
def update():
    # 计算邻接矩阵M
    for instance in instances:
        instances_value_backup = list(instances)
        instances_value_backup.remove(instance)

        (k_distance_value, neighbours) = k_distance(
            len(instances_value_backup), instance, instances_value_backup)
        M[instances.index(instance)] = neighbours

# 计算Kinf
def cal_K_inf():
    for instance in instances:
        kmin = float("inf")
        for k in kList:
            value = lof.local_outlier_factor(k, instance)
            if value < kmin:
                kmin = value
                k_inf = k
        kinf[instances.index(instance)] = k_inf
        # print(instances.index(instance),'kinf',k_inf)
    print("Kinf:\n", kinf)

def pre_cal_c1():
    for instance in instances:
        k_inf = kinf[instances.index(instance)]
        # if lof.local_outlier_factor(k_inf, instance) == 0:
        #     pre_c1[instances.index(instance)] = 0
        # else:
        pre_c1[instances.index(instance)] = lof.local_outlier_factor(
            k_inf + 1, instance)/lof.local_outlier_factor(k_inf, instance)
        # print(instances.index(instance),'c1',pre_c1[instances.index(instance)])
    print("pre_c1:\n", pre_c1)

# 计算C1
def cal_C1(instance):
    return pre_c1[instances.index(instance)]

# 计算C2
def cal_C2(instance):
    sum_c1 = 0
    index = instances.index(instance)
    k_inf = kinf[instances.index(instance)]

    for i in range(0, k_inf, 1):
        if (i < len(instances)-1):
            b = M[index][i]
            sum_c1 += pre_c1[instances.index(b)]
    c2 = sum_c1/k_inf
    return c2

# 计算C3
def cal_C3(instance):
    k_inf = kinf[instances.index(instance)]
    k_avg = (2 + k_inf)/2

    (k1, neighbours) = k_distance(k_inf+1, instance, instances)
    (k2, neighbours) = k_distance(k_avg, instance, instances)

    c3 = k1/k2
    return c3

# 计算C4
def cal_C4(instance):
    index = instances.index(instance)
    k_inf_a = kinf[instances.index(instance)]
    k_inf_b = 0

    for i in range(0, k_inf_a, 1):
        if (i < len(instances)-1):
            b = M[index][i]
            k_inf_b += kinf[instances.index(b)]
    # print(k_inf_a,k_inf_b)
    mid_value = abs(k_inf_a/(k_inf_b/k_inf_a)-1)
    c4 = math.exp(mid_value)
    return c4

# 计算C
def cal_C(instance):
    c1 = cal_C1(instance)
    c2 = cal_C2(instance)
    c3 = cal_C3(instance)
    c4 = cal_C4(instance)
    c = (c1*c2*c3*c4)**0.25
    # print(instances.index(instance),'c',c)
    return c

# 扩展集合
def expand(center, init_instances):
    instances_backup = list(init_instances)
    instances_backup.remove(center)

    index = instances.index(center)
    avg_distance = 0

    for b in instances_backup:
        avg_distance += distance_euclidean(center, b)
    avg_distance = avg_distance/len(instances_backup)

    for b in instances_backup:
        index_b = instances.index(b)
        kb = M[index].index(b)

        for i in range(0, kb+1, 1):
            c = M[index_b][i]
            if c not in init_instances:
                distance = distance_euclidean(b, c)
                if distance < avg_distance:
                    init_instances.append(c)
    # print(len(init_instances))

# 扩展Klist
def refine(rc):
    min_value = float("inf")

    for k in kList:
        value = (k - len(rc))**2
        if value < min_value:
            min_value = value
            k_min = k

    #k_new = int((k_min + len(rc)) / 2)
    k_new = len(rc)
    if k_new not in kList:
        kList.append(k_new)
    kList.sort()
    # print("New klist is \n",kList)

while True:
    print("New instances is \n", instances)
    lof = LOF(instances)
    M = [[] for i in range(len(instances))]
    pre_c1 = []
    kinf = []

    for i in range(len(instances)):
        pre_c1.append(0)
        kinf.append(0)
    for k in kList:
        if k > len(instances):
            kList = kList[0:kList.index(k)]
            break
    if len(instances) == 1 and len(kList) == 0:
        kList.append(1)
    print("kList is", kList)

    update()
    cal_K_inf()
    pre_cal_c1()
    Ur.clear()

    # 找到LOF异常点
    for instance in instances:
        for k in kList:
            value = lof.local_outlier_factor(k, instance)
            if value > 1:
                Ur.append(instance)
                print("LOF points", instances.index(instance), k, value)
                break
    print("Ur is \n", Ur)

    if Ur:
        max_value = float("-inf")
        C = []

        for u in Ur:
            value = cal_C(u)
            if value > max_value:
                max_value = value
                a = u
                # print(u,max_value)
        print("center is ", a, kinf[instances.index(a)])
        C.append(a)
        index = instances.index(a)
        k_inf = kinf[instances.index(a)]
        for i in range(0, k_inf, 1):
            if (i < len(instances)-1):
                b = M[index][i]
                if b in instances:
                    C.append(b)
        for c in C:
            color = colors[0]
            p.scatter(c[0], c[1], color=color)
        p.show()

        expand(a, C)
        refine(C)
        Ures[group] = list(C)
        group += 1
        remain = set(instances) - set(C)
        instances = list(remain)
    else:
        if len(instances) != 0:
            Ures[group] = list(instances)
            group += 1
            instances = []
    if len(instances) == 0:
        break

for i in range(0, group, 1):
    for instance in Ures[i]:
        index = instancesBackup.index(instance)
        resLabel[i].append(labels[index])
    print("group", i, "is \n", Ures[i])
    print("group", i, "label is \n", resLabel[i])

for i in range(0, group, 1):
    for c in resLabel[i]:
        color = colors[i]
        p.scatter(c[0], c[1], color=color)
p.savefig('/home/PsyduckLiu/pics/PRP-RCD/final-log256+2.png')
# 画图
p.show()
