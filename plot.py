# coding: utf-8
import numpy as np
from utils import plot_learning_curve
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.ticker import AutoMinorLocator, FuncFormatter, MultipleLocator
from matplotlib import rcParams

config = {
    "font.family": "Times New Roman",  # 衬线字体
    "font.serif": ["SimSun"],  # 宋体
    "mathtext.fontset": "stix",  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    "axes.unicode_minus": False,  # 处理负号，即-号
}
rcParams.update(config)
fig = plt.figure()

ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])




maddpg_scores = np.load('data/maddpg_scores.npy')
maddpg_steps = np.load('data/maddpg_steps.npy')

# ddpg_scores = np.load('data/ddpg_scores.npy')
# ddpg_steps = np.load('data/ddpg_steps.npy')

# plot_learning_curve(x=maddpg_steps,
#                     scores=(maddpg_scores, ddpg_scores),
#                     filename='plots/maddpg_vs_ddpg.png')


window_length = 100
polyorder = 2
y_smooth = savgol_filter(maddpg_scores, window_length, polyorder)


# 设置图例
# 设置 xlabel, ylabel
# 设置字体
# 设置保存的形状




plt.plot(maddpg_steps,
         y_smooth,
         color="black",
         lw=1,
         linestyle="-",
         markerfacecolor="white",)
ax.set_xlabel("Steps",fontsize=16)
ax.set_ylabel("Reward",fontsize=16)


# 设置存储位置
plt.savefig("reward_N=10.svg")

plt.show()