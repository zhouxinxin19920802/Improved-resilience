# Multi-Agent-Reinforcement-Learning
算法细节
----------------------------------------------
1. follower共享一个actor网络，leader共享一个actor网络,follower和leader共享一 个critic网络。

2. 每个智能体的target actor网络和target critic不共享各自用各自的，所以最后保存的网络数量为 n * target_actor + n * target_critic + 1 * general_actor + 1 * general_critic, 例如，当N=5时候，会有5个target_actor， 5个target_actor,1个general_actor, 1个general_actor_leader, 1个general_critic.


----------------------------------------------

操作过程
-----------------------------------------------
1. run_my  启动训练

2. plot.py 学习过程中的奖励收敛过程

3. run_compare 加载学习到的策略进行评估

4. couzin_env_xu 评估xu方法

4. connect_plot 单独计算连通度

5. compare_plot 提出的方法和Xu进行比较

---------------------------------------------- 