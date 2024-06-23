import shutil
import numpy as np
from maddpg_copy0 import MADDPG
from buffer import MultiAgentReplayBuffer
import couzin_env as env
import os

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
 
import json
# 打开文件并加载JSON数据
with open('config.json', 'r') as file:
    config_data = json.load(file)



def obs_list_to_state_vector(observation):
    state = np.array([])
    for obs in observation:
        state = np.concatenate([state, obs])
    return state


def run():
    display = False
    evaluate_ = False
    N = config_data["Num"]
    P = config_data["P"]

    env_ = env.Couzin(N,P,Is_visual= display)
    env_.attract_range = 60
    obs = env_.reset()
    n_agents = env_.n


    # logging.info("n_agents:{}".format(n_agents))

    actor_dims = []
    n_actions = []
    for agent in env_.swarm:
        actor_dims.append(4 * n_agents )
        n_actions.append(1)
    # logging.info("actor_dims:{}".format(actor_dims))
    # logging.info("n_actions:{}".format(n_actions))
    critic_dims = sum(actor_dims) + sum(n_actions)
    # logging.info("critic_dims:{}".format(critic_dims)) 
    
    maddpg_agents = MADDPG(actor_dims, critic_dims, n_agents, n_actions,
                           env_, gamma=0.95, alpha=1e-4, beta=1e-3)
    critic_dims = sum(actor_dims)
    memory = MultiAgentReplayBuffer(100000, critic_dims, actor_dims,
                                    n_actions, n_agents, batch_size=1024)

    EVAL_INTERVAL = 100
    MAX_STEPS = 300000

    total_steps = 0
    episode = 0
    eval_scores = []
    eval_steps = []

    score = evaluate(maddpg_agents, env_, episode, total_steps)
    eval_scores.append(score)
    eval_steps.append(total_steps)

    best_score = 300

    if evaluate_:
        maddpg_agents.load_checkpoint()

    while total_steps < MAX_STEPS:
        obs = env_.reset()
        terminal = [False] * n_agents
        while not any(terminal):
            # logging.info("obs:{}".format(obs))
            actions = maddpg_agents.choose_action(obs)
            if total_steps % 100 == 0:
                logging.info("actions:{}".format(actions))
            obs_, reward, done = env_.step(actions)

            list_done = list(done)
            list_obs = list(obs)
            list_reward = list(reward)
            list_actions = list(actions)
            list_obs_ = list(obs_)
        

            state = obs_list_to_state_vector(list_obs)
          
            state_ = obs_list_to_state_vector(list_obs_)

            terminal = list_done
            memory.store_transition(list_obs, state, list_actions, list_reward,
                                    list_obs_, state_, terminal)

            if total_steps % 100 == 0 and not evaluate_:
                # print("learning")
                maddpg_agents.learn(memory)
            obs = obs_
            total_steps += 1

        # 每一个大循环训练完就需要运行三次取平均值
        score = evaluate(maddpg_agents, env_, episode, total_steps)
        eval_scores.append(score)
        eval_steps.append(total_steps)
        if score > best_score:
            maddpg_agents.save_checkpoint()
            best_score = score

        # if total_steps % EVAL_INTERVAL == 0:
        #     print("learning")
        #     score = evaluate(maddpg_agents, env_, episode, total_steps)
        #     eval_scores.append(score)
        #     eval_steps.append(total_steps)
        #     if score > best_score:
        #         maddpg_agents.save_checkpoint()
        #         best_score = score
        episode += 1

    np.save('data/maddpg_scores.npy', np.array(eval_scores))
    np.save('data/maddpg_steps.npy', np.array(eval_steps))


def evaluate(agents, env, ep, step, n_eval=3):
    score_history = []
    for i in range(n_eval):
        obs = env.reset()
        score = 0
        terminal = [False] * env.n
        while not any(terminal):
            actions = agents.choose_action(obs, evaluate=True)
            logging.info("actions:{}".format(actions))
            obs_, reward, done = env.step(actions)

            
            list_reward = list(reward)
            list_done = list(done)

            terminal = list_done

            obs = obs_
            score += sum(list_reward)
        score_history.append(score)
    avg_score = np.mean(score_history)
    print(f'Evaluation episode {ep} train steps {step}'
          f' average score {avg_score:.1f}')
    return avg_score

# def evaluate0():
#     env_ = env.Couzin(5,0.4,Is_visual= False)
#     env_.attract_range = 60
#     n_agents = env_.n
#     score_history = []
#     score_data = []
#     n_eval = 1000
#     actor_dims = []
#     n_actions = []
#     for agent in env_.swarm:
#         actor_dims.append(4 * n_agents )
#         n_actions.append(1)
#     critic_dims = sum(actor_dims) + sum(n_actions)
#     maddpg_agents = MADDPG(actor_dims, critic_dims, n_agents, n_actions,
#                            env_, gamma=0.95, alpha=1e-4, beta=1e-3)
#     maddpg_agents.load_checkpoint()
#     for i in range(n_eval):
#         obs = env_.reset()
#         score = 0
#         terminal = [False] * env_.n
#         while not any(terminal):
#             actions = maddpg_agents.choose_action(obs, evaluate=True)
#             # logging.info("actions:{}".format(actions))
#             obs_, reward, done = env_.step(actions)

            
#             list_reward = list(reward)
#             list_done = list(done)

#             terminal = list_done

#             obs = obs_
#             score += sum(list_reward)
#         score_history.append(score)
#         score_data.append(i)
#         print(f'Evaluation episode {i}'
#             f' average score {score:.1f}')
#     np.save('data/maddpg_scores.npy', np.array(score_history))
#     np.save('data/maddpg_steps.npy', np.array(score_data))


if __name__ == '__main__':
    folder_path=r'tmp\maddpg\navigation'

    # 获取文件夹中的所有文件和子文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # 检查是否为文件，是则删除
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"文件 '{item}' 已删除。")
        # 如果是文件夹，递归调用删除
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"文件夹 '{item}' 及其内容已删除。")
    run()
  
