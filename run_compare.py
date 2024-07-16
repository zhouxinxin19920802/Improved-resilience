import numpy as np
from maddpg_copy0 import MADDPG
from buffer import MultiAgentReplayBuffer
import couzin_env as env
import logging
logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename='test_log.txt',
                    filemode='w',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

def obs_list_to_state_vector(observation):
    state = np.array([])
    for obs in observation:
        state = np.concatenate([state, obs])
    return state


# 删除相关文件
import os

def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"File '{file_path}' does not exist.")

file_path_space = "space_complexity_r.txt"
file_path_time = "time_complexity_r.txt"
file_path_connect = "connect_value_r.txt"
file_path_destination = "destination_nums.txt"
file_path_destination1 = "destination_nums1.txt"

try:
    delete_file_if_exists(file_path_space)
    delete_file_if_exists(file_path_time)
    delete_file_if_exists(file_path_connect)
    delete_file_if_exists(file_path_destination)
    delete_file_if_exists(file_path_destination1) 
except OSError as e:
    print(f"删除文件时发生错误: {e}")

import json
with open('config.json', 'r') as file:
    config_data = json.load(file)
N = config_data["Num"]
P = config_data["P"]

display = False
env_ = env.Couzin(N,P,Is_visual= display)
env_.attract_range = 30
# 进行评价，运行2000次结束
env_.evaluate = True

obs = env_.reset()
n_agents = env_.n



# 这部分代码可能要去掉，后面要进行验证
# ///////////////////////////////////////////////
actor_dims = []
n_actions = []
for agent in env_.swarm:
    actor_dims.append(4 * n_agents )
    n_actions.append(1)
critic_dims = sum(actor_dims) + sum(n_actions)
maddpg_agents = MADDPG(actor_dims, critic_dims, n_agents, n_actions,
                        env_, gamma=0.95, alpha=1e-4, beta=1e-3)
critic_dims = sum(actor_dims)
# ///////////////////////////////////////////////



maddpg_agents.load_checkpoint()


# 构造一个类似main的函数


for ngame in range(50):
    env_.reset()
    for i in range(2000):
        actions = maddpg_agents.choose_action(obs)
        obs1_,  reward_temp, done = env_.step(actions=actions)
        obs = obs1_
        # print(ngame,i)
    with open("connect_value_r.txt","a+") as space:
            space.write("\n") 
