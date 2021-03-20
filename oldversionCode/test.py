import sys,time
length=100
for i in range(1,101): 
    print("\r下载进度：%.2f%%" %(float(i/length*length)),end=' ') 
    time.sleep(0.01)

# 统计行数
    length=0
    while True:
        buffer = sourcefp.read(1024 * 8192)
        if not buffer:
            break
        length += buffer.count('\n')
    # print(length)
sourcefp.seek(0, 0)
count = count+1
    print("\rProcessing progress：%.2f%%" %(float(count/length*length)),end=' ') 
    time.sleep(0.01)