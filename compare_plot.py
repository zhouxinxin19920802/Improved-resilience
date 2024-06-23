from connect_plot import Swarm_connectivity_cal
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import rcParams
import shutil
import os

import logging
logging.basicConfig(
    level=logging.INFO,  # 控制台打印的日志级别
    filename="test_log_0.txt",
    filemode="w",  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    # a是追加模式，默认如果不写的话，就是追加模式
    format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    # 日志格式
)

fig = plt.figure()

ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])

config = {
    "font.family":'Times New Roman',  # 设置字体类型
    "font.sans-serif": ['SimHei'],  # 设置字体为黑体，SimHei支持中文显示
    "font.size": 12,
#     "mathtext.fontset":'stix',
}
rcParams.update(config)

def data_average(path):
    data = []
    with open(path,"r") as f:
        lines = f.readlines()
        # print(lines)
        for line in lines:
            if line.strip()!="":
                # print(line)
                logging.info("line:{}".format(line))
                data.append(float(line.rstrip("\n")))
    cons = np.mean(data)   
    return cons

def file_save(path):
    target_directory_base = r'D:\zhouxin\科研\大论文\基于群集运动模型的无人集群韧性评估与优化\无人集群运动模型小论文\数据保存'
    target_directory = target_directory_base +"\\" + path
    
    if not os.path.exists(target_directory):
       os.makedirs(target_directory)

    # 获取当前文件夹下所有以.txt结尾的文件列表
    txt_files = [file for file in os.listdir('.') if file.endswith('.txt')]

    # 复制文件到目标目录
    for txt_file in txt_files:
        source_path = os.path.join(os.getcwd(), txt_file)
        target_path = os.path.join(target_directory, txt_file)
        shutil.copy2(source_path, target_path)

    # 移动生成的图片到指定的文件加
    figure_path = r'./figures/' + path + ".svg" 
    print(figure_path)
    shutil.copy2(figure_path, target_directory)
    print("保存成功")

# # 添加文件保存功能
# path = "N=10_P=0.3"
# file_save(path)


# 空间复杂度
space_xu = "space_complexity.txt"
space_r = "space_complexity_r.txt"

space_complexity_xu = data_average(space_xu)
space_complexity_r = data_average(space_r)

print("space_xu","space_r",space_complexity_xu,space_complexity_r )
# 时间复杂度
time_xu = "time_complexity.txt"
time_r = "time_complexity_r.txt"

time_complexity_xu = data_average(space_xu)
time_complexity_r = data_average(space_r)

print("time_xu","time_r",time_complexity_xu,time_complexity_r )

# 到达率
# 总的到达数
destination_xu = "destination_nums_xu.txt"
destination_r = "destination_nums.txt"

destination_num_xu = data_average(destination_xu)
destination_num_r = data_average(destination_r)

print("destination_num_xu","destination_num_r",destination_num_xu,destination_num_r)

# 领导者的到达数
destination_xu1 = "destination_nums_xu_leader.txt"
destination_r1 = "destination_nums1.txt"

destination_num_xu1 = data_average(destination_xu1)
destination_num_r1 = data_average(destination_r1)

print("destination_num_xu1","destination_num_r1",destination_num_xu1,destination_num_r1)




# 连通度比较
data_xu = "connect_value.txt"
data_view_xu = Swarm_connectivity_cal(data_xu)

data_r = "connect_value_r.txt"
data_view_r = Swarm_connectivity_cal(data_r)


# 连通度绘图
x_xu = np.arange(0,len(data_view_xu),1)
plt.plot(x_xu,data_view_xu,color="red",marker="o",label=u"Xu's method")

x_r = np.arange(0,len(data_view_r),1)
plt.plot(x_r,data_view_r,color="b",marker="s",label="the improved method")

path = "N=10_P=0.2"
figue_name = r'figures/' + path + '.svg' 


ax.set_xlabel("时间步",fontsize=16)
ax.set_ylabel("集群连通度",fontsize=16)

plt.ylim(0,1)
plt.legend()
plt.savefig(figue_name, format='svg')


file_save(path)


plt.show()

