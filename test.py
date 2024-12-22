from smac_hard.env import StarCraft2Env
import numpy as np

'''
def main():
    env = StarCraft2Env(map_name="8m")
    env_info = env.get_env_info()

    n_actions = env_info["n_actions"]
    n_agents = env_info["n_agents"]

    n_episodes = 5

    for e in range(n_episodes):
        env.reset()
        terminated = False
        episode_reward = 0

        while not terminated:
            obs = env.get_obs()
            state = env.get_state()
            # env.render()  # Uncomment for rendering

            actions = []
            for agent_id in range(n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                actions.append(action)

            reward, terminated, _ = env.step(actions)
            episode_reward += reward

        print("Total reward in episode {} = {}".format(e, episode_reward))

    env.close()
'''

def main():
    env = StarCraft2Env(map_name="8m", mode='multi')
    env_info = env.get_env_info()

    red_n_actions = env_info[0]["n_actions"]
    red_n_agents = env_info[0]["n_agents"]

    blue_n_actions = env_info[1]["n_actions"]
    blue_n_agents = env_info[1]["n_agents"]

    n_episodes = 2

    for e in range(n_episodes):
        env.reset()
        terminated = False
        red_episode_reward = 0
        blue_episode_reward = 0


        while not terminated:
            red_obs = env.get_obs(0)
            blue_obs = env.get_obs(1)
            
            red_state = env.get_state(0)
            blue_state = env.get_state(1)


            red_actions = []
            for agent_id in range(red_n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id, player_id=0)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                red_actions.append(action)

            blue_actions = []
            for agent_id in range(blue_n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id, player_id=1)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                blue_actions.append(action)

            rewards, terminateds, _ = env.step([red_actions, blue_actions])
            red_episode_reward += rewards[0]
            blue_episode_reward += rewards[1]
            terminated = terminateds[0]


        print("Total reward in episode {} = {} and {}".format(e, red_episode_reward, blue_episode_reward))

    env.close()

if __name__ == '__main__':

    main()