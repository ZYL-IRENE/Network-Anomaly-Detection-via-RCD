import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize

x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
precision = [98.27, 98.26, 98.26, 98.26, 98.1, 97.56, 97.55, 93.75, 86.49, 80.38, 69.44, 52.33]
recall = [97.58, 97.34, 97.42, 96.95, 96.79, 96.87, 96.64, 97.34, 97.11, 98.98, 99.14, 100.0]
accuracy = [97.83, 97.71, 97.75, 97.5, 97.34, 97.09, 96.97, 95.21, 90.55, 86.82, 76.72, 52.33]
base = 12*[96.32]
far = [1.89, 1.89, 1.89, 1.89, 2.06, 2.66, 2.66, 7.12, 16.65, 26.52, 47.9, 100.0]
far1 = [100-i for i in far]
unlabeled = [0, 0, 0, 0, 0, 4, 17, 118, 273, 416, 668, 1337]
unlabeled_p = [i*100/2444 for i in unlabeled]
rule_num = [2251, 7733, 17651, 28458, 33611, 29591, 19467, 9449, 3282, 770, 109, 7]

fuzhu = [100, 98.26, 98.26, 98.26, 98.1, 97.56, 97.55, 93.75, 86.49, 80.38, 69.44, 50]

#plt.title('扩散速度')  # 折线图标题
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
plt.xlabel('Rule Length')  # x轴标题
#plt.ylabel('False Alarm Rate (%)')  # y轴标题
# plt.plot(x, precision, marker='', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
# plt.plot(x, recall, marker='', markersize=3)
# plt.plot(x, accuracy, marker='', markersize=3)
# plt.plot(x, base, marker='', markersize=3, color = 'grey', linestyle=':')


plt.axvspan(9, 10, facecolor='grey', alpha=0.1, **dict())#垂直x轴区域
#plt.plot(x, far, marker='', markersize=3)
#plt.plot(x, unlabeled_p, marker='', markersize=3)
plt.plot(x, rule_num, marker='', markersize=3)

'''
for a, b in zip(x, precision):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
for a, b in zip(x, recall):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(x, accuracy):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(x, far):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
'''
#plt.text(14, 96.32, 96.32, ha='center', va='bottom', fontsize=9, color='dimgrey')
#plt.legend([ 'False Alarm Rate (%)'],loc='lower left',bbox_to_anchor=(0, 0.1))
#plt.legend([ 'Unlabeled Percentage (%)'],loc='lower left',bbox_to_anchor=(0, 0.1))
plt.legend([ 'Number of Rules'],loc='lower left',bbox_to_anchor=(0, 0))
#plt.legend(['Precision (%)', 'Detection Rate (%)', 'Accuracy (%)'])  # 设置折线名称

plt.savefig('rule_num.png')
plt.show()  # 显示折线图
