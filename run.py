import numpy as np
from maddpg import MADDPG
from buffer import MultiAgentReplayBuffer
from pettingzoo.mpe import simple_adversary_v3
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


def run():
    parallel_env = simple_adversary_v3.parallel_env(
            continuous_actions=True)
    _, _ = parallel_env.reset()
    n_agents = parallel_env.max_num_agents
    logging.info("n_agents:{}".format(n_agents))

    actor_dims = []
    n_actions = []
    for agent in parallel_env.agents:
        actor_dims.append(parallel_env.observation_space(agent).shape[0])
        n_actions.append(parallel_env.action_space(agent).shape[0])
    logging.info("actor_dims:{}".format(actor_dims))
    logging.info("n_actions:{}".format(n_actions))
    critic_dims = sum(actor_dims) + sum(n_actions)
    logging.info("critic_dims:{}".format(critic_dims)) 

    maddpg_agents = MADDPG(actor_dims, critic_dims, n_agents, n_actions,
                           env1=parallel_env, gamma=0.95, alpha=1e-4, beta=1e-3)
    critic_dims = sum(actor_dims)
    memory = MultiAgentReplayBuffer(1_000_000, critic_dims, actor_dims,
                                    n_actions, n_agents, batch_size=1024)

    EVAL_INTERVAL = 1000
    MAX_STEPS = 1000000

    total_steps = 0
    episode = 0
    eval_scores = []
    eval_steps = []

    score = evaluate(maddpg_agents, parallel_env, episode, total_steps)
    eval_scores.append(score)
    eval_steps.append(total_steps)

    while total_steps < MAX_STEPS:
        obs, _ = parallel_env.reset()
        terminal = [False] * n_agents
        while not any(terminal):
            actions = maddpg_agents.choose_action(obs)

            obs_, reward, done, trunc, info = parallel_env.step(actions)
            logging.info("obs_:{}".format(obs_))
            logging.info("reard_:{}".format(reward))
            list_done = list(done.values())
            list_obs = list(obs.values())
            list_reward = list(reward.values())
            list_actions = list(actions.values())
            list_obs_ = list(obs_.values())
            list_trunc = list(trunc.values())

            state = obs_list_to_state_vector(list_obs)
            logging.info("state:{}".format(state))
            state_ = obs_list_to_state_vector(list_obs_)

            terminal = [d or t for d, t in zip(list_done, list_trunc)]
            memory.store_transition(list_obs, state, list_actions, list_reward,
                                    list_obs_, state_, terminal)

            if total_steps % 100 == 0:
                maddpg_agents.learn(memory)
            obs = obs_
            total_steps += 1

        if total_steps % EVAL_INTERVAL == 0:
            score = evaluate(maddpg_agents, parallel_env, episode, total_steps)
            eval_scores.append(score)
            eval_steps.append(total_steps)

        episode += 1

    np.save('data/maddpg_scores.npy', np.array(eval_scores))
    np.save('data/maddpg_steps.npy', np.array(eval_steps))


def evaluate(agents, env, ep, step, n_eval=3):
    score_history = []
    for i in range(n_eval):
        obs, _ = env.reset()
        score = 0
        terminal = [False] * env.max_num_agents
        while not any(terminal):
            actions = agents.choose_action(obs, evaluate=True)
            obs_, reward, done, trunc, info = env.step(actions)

            list_trunc = list(trunc.values())
            list_reward = list(reward.values())
            list_done = list(done.values())

            terminal = [d or t for d, t in zip(list_done, list_trunc)]

            obs = obs_
            score += sum(list_reward)
        score_history.append(score)
    avg_score = np.mean(score_history)
    print(f'Evaluation episode {ep} train steps {step}'
          f' average score {avg_score:.1f}')
    return avg_score


if __name__ == '__main__':
    run()
