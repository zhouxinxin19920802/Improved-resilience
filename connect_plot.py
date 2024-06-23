import logging
logging.basicConfig(
    level=logging.INFO,  # 控制台打印的日志级别
    filename="test_log_0.txt",
    filemode="w",  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    # a是追加模式，默认如果不写的话，就是追加模式
    format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    # 日志格式
)
def Swarm_connectivity_cal(path):
    connectivitys = []
    with open(path,"r") as f:
        lines = f.readlines()
        connectivity = []
        for line in lines:
            connectivity.append(line)
            if line.strip()=="":
                connectivitys.append(connectivity)
                connectivity = []
    # logging.info("length:{}".format(len(connectivitys)))
    if len(connectivitys[-1])!=len(connectivitys[0]):
        connectivitys.pop()
    
    data_presentation = [0] * (len(connectivitys[0])-1)

    for swarm_connect_index in range(len(data_presentation)):
        for item in connectivitys:
            logging.info("item:{}".format(len(item)))
            if item!="\n":
                # print(item[swarm_connect_index].rstrip("\n"))
                data_presentation[swarm_connect_index] = data_presentation[swarm_connect_index] + float(item[swarm_connect_index].rstrip("\n"))
        data_presentation[swarm_connect_index] = data_presentation[swarm_connect_index] / len(connectivitys)
    return data_presentation



if __name__=="__main__":
    data = "connect_value_r.txt"
    data_view = Swarm_connectivity_cal(data)
    import matplotlib.pyplot as plt 
    import numpy as np
    from matplotlib import rcParams
    config = {
        "font.family":'Times New Roman',  # 设置字体类型
        "font.size": 12,
    #     "mathtext.fontset":'stix',
    }
    rcParams.update(config)

    x = np.arange(0,len(data_view),1)
    plt.plot(x,data_view,color="red",marker="1",label="connect")
    plt.ylim(0,1)
    plt.savefig('figures//example_plot.svg', format='svg')
    plt.show()