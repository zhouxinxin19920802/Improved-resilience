# import json

# # 打开文件并加载JSON数据
# with open('config.json', 'r') as file:
#     config_data = json.load(file)
    
# if __name__ == '__main__':
#     print("hha")
#     print(config_data["Num"])
#     print(config_data["P"])

import shutil


target_directory = r'D:\zhouxin\科研\大论文\基于群集运动模型的无人集群韧性评估与优化\无人集群运动模型小论文\数据保存'
path = "N=10_P=0.3"
target_directory = target_directory +"\\" + path
figure_path = r'./figures/' + path + ".svg" 
print(figure_path)
shutil.copy2(figure_path, target_directory)
