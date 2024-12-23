# SMAC-HARD - Enabling Mixed Opponent Strategy Script and Self-play on SMAC

This is the official repository for the paper: SMAC-HARD: Enabling Mixed Opponent Strategy Script and Self-play on SMAC. Please refer to the accompanying paper for the outline of our motivation.

[SMAC-HARD](https://github.com/devindeng94/smac-hard) is an extension environment of [SMAC](https://github.com/oxwhirl/smac) for research in the field of cooperative multi-agent reinforcement learning (MARL) based on [Blizzard](http://blizzard.com)'s [StarCraft II](https://en.wikipedia.org/wiki/StarCraft_II:_Wings_of_Liberty) RTS game. SMAC-HARD makes use of Blizzard's [StarCraft II Machine Learning API](https://github.com/Blizzard/s2client-proto) and [DeepMind](https://deepmind.com)'s [PySC2](https://github.com/deepmind/pysc2) to provide a convenient interface for autonomous agents to interact with StarCraft II, getting observations and performing actions. In the self-play implementation, we align the centralized training with decentralized execution interfaces for opponents to agents. In the opponent script editing mode, users can use pysc2 script based on raw observation to write decision-tree scripts and add them to the opponent strategy pools.

# Quick Start

## Installing SMAC-HARD

You can install SMAC-HARD by using the following command:

```shell
pip install git+https://github.com/devindeng94/smac-hard.git
```

Alternatively, you can clone the SMAC-HARD repository and then install `smac_hard` with its dependencies:

```shell
git clone https://github.com/devindeng94/smac-hard.git
pip install -e smac-hard/
```

You may also need to upgrade pip: `pip install --upgrade pip` for the install to work.

## Installing StarCraft II

SMAC-HARD is based on the full game of StarCraft II (versions >= 3.16.1). To install the game, follow the commands bellow.

### Linux

Please use the Blizzard's [repository](https://github.com/Blizzard/s2client-proto#downloads) to download the Linux version of StarCraft II. By default, the game is expected to be in `~/StarCraftII/` directory. This can be changed by setting the environment variable `SC2PATH`.

### MacOS/Windows

Please install StarCraft II from [Battle.net](https://battle.net). The free [Starter Edition](http://battle.net/sc2/en/legacy-of-the-void/) also works. PySC2 will find the latest binary should you use the default install location. Otherwise, similar to the Linux version, you would need to set the `SC2PATH` environment variable with the correct location of the game.

**It is worth noting that the Linux version of StarCraftII binary is version 4.10 and the MacOS/Windows version always follow the latest version (5.0.14 currently), which may results in incompatible performances. For example, the health value of hydralisk is 80 in 4.10 version but 90 in 5.0.14 version, which may significantly influence the difficulty of 6h\_vs\_8z scenario.**

## SMAC-HARD maps

The Maps are also based on SMAC maps but with multiplayer mode. Therefore, the original SMAC maps are not suitable in the SMAC-HARD environment. To create customised SMAC-HARD maps, you need to create two player positions in the SC2Map and let 'users' control the units instead of Computer AI (internal opponent AI). Before SMAC-HARD can be used, the maps provided in this repository need to be downloaded into the `Maps` directory of StarCraft II. Users should download and extract them to your `$SC2PATH/Maps` directory.

### List the maps

To see the list of SMAC-HARD maps, together with the number of ally and enemy units and episode limit, run:

```shell
python -m smac_hard.bin.map_list 
```


## Saving and Watching StarCraft II Replays

### Saving a replay

If you want to save replays, simply call the `save_replay()` function of SMAC-HARD's StarCraft2Env in your training/testing code. This will save a replay of all epsidoes since the launch of the StarCraft II client.

### Watching a replay

You can watch the saved replay directly within the StarCraft II client on MacOS/Windows by *clicking on the corresponding Replay file*.

You can also watch saved replays by running:

```shell
python -m pysc2.bin.play --norender --replay <path-to-replay> --map_path <path-to-SC2Map>
```

This works for any replay as long as the map can be found by the game. 

For more information, please refer to [PySC2](https://github.com/deepmind/pysc2) documentation.

# Code Examples

## Mixed Opponent Script mode
Below is a small code example which illustrates how **SMAC-HARD mixed opponent script mode** can be used. Here, individual agents execute random policies after receiving the observations and global state from the environment.  

You may apply our proposed SMAC-HARD to your codebase by simply replace 'smac' by **'smac_hard'**!


```python
from smac_hard.env import StarCraft2Env
import numpy as np

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

```
## MARL Self-Play mode

In the self-play mode, two players controlled by agents are inserted, which means observations, states and other interfaces should be acquired for agent (red) and opponent (blue) seperately. Therefore, to start the self-play mode, the 'mode=multi' parameter should be passed into the StarCraft2Env class and the 'player\_id=0' and 'player\_id=1' are taken as parameters. Consequently, the rewards, terminateds, and infos are returned as a list with two variables.

```python
from smac_hard.env import StarCraft2Env
import numpy as np

def main():
    env = StarCraft2Env(map_name="8m", mode='multi')
    env_info = env.get_env_info()

    red_n_actions = env_info[0]["n_actions"]
    red_n_agents = env_info[0]["n_agents"]

    blue_n_actions = env_info[1]["n_actions"]
    blue_n_agents = env_info[1]["n_agents"]

    n_episodes = 5

    for e in range(n_episodes):
        env.reset()
        terminated = False
        red_episode_reward = 0
        blue_episode_reward = 0


        while not terminated:
            red_obs = env.get_obs(player_id=0)
            blue_obs = env.get_obs(player_id=1)
            
            red_state = env.get_state(player_id=0)
            blue_state = env.get_state(player_id=1)


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

```


### Experimental results

| SMAC-HARD          | QMIX   | QPLEX  | LDSA   | MAPPO  | HAPPO  |
|--------------------|--------|--------|--------|--------|--------|
| 3m                 | 0.9938 | 0.0438 | **1**      | **1**      | 0.4375 |
| 8m                 | 0.9628 | 0.0875 | **0.9687** | 0.6438 | 0.8625 |
| 5m\_vs\_6m         | 0.4375 | **0.6188** | 0.4    | 0.3138 | 0.004  |
| 8m\_vs\_9m         | 0.4938 | 0      | **0.7187** | 0.3528 | 0.5006 |
| 10m\_vs\_11m       | **0.6813** | 0      | 0.625  | 0.5681 | 0.5672 |
| 25m                | **0.7813** | 0      | 0.4375 | 0.4562 | 0.2092 |
| 27m\_vs\_30m       | 0.0313 | 0      | **0.125**  | 0.0938 | 0.0063 |
| 2s3z               | 0.4125 | 0.4313 | 0.7737 | **0.8735** | 0.7547 |
| 3s5z               | 0.3625 | 0.1063 | 0.1876 | **0.7225** | 0.6691 |
| 3s5z\_vs\_3s6z     | 0      | 0      | 0.1319 | 0.1569 | **0.2573** |
| 1c3s5z             | 0.9625 | 0.7563 | 0.9375 | 0.5445 | **0.975**  |
| 3s\_vs\_3z         | 0.9913 | 0.9875 | **1**      | 0.9875 | 0.4875 |
| 3s\_vs\_4z         | 0.7938 | 0.7938 | 0.7815 | **0.9875** | 0.15   |
| 3s\_vs\_5z         | 0.3438 | 0.5    | 0.875  | **0.9407** | 0      |
| bane\_vs\_bane     | 0.975  | 0.2313 | 0.8229 | **0.9125** | 0      |
| so\_many\_baneling | **0.9625** | 0.5938 | 0.875  | 0.8813 | 0.9188 |
| 2s\_vs\_1sc        | 0.7563 | **0.8875** | 0.4375 | 0.8375 | 0      |
| 2m\_vs\_1z         | 0      | 0      | 0      | 0      | 0      |
| 2c\_vs\_64zg       | 0.7891 | 0.5    | 0.9062 | **0.9741** | 0.7686 |
| MMM                | **0.9875** | 0.95   | 0.875  | 0.3267 | 0.8813 |
| MMM2               | 0.275  | 0.0006 | **0.5312** | 0.1925 | 0.0425 |
| 6h\_vs\_8z         | 0.0188 | 0      | **0.0625** | 0.0607 | 0      |
| corridor           | **0.3063** | 0.1688 | 0      | 0.1804 | 0      |

The codebase for generating the QMIX, QPLEX results above is [pymarl2](https://github.com/hijkzzz/pymarl2). We also follow the hyper-parameters described in [pymarl3](https://github.com/tjuHaoXiaotian/pymarl3).
~~~
# 3s5z_vs_3s6z
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=3s5z_vs_3s6z runner=parallel batch_size_run=4 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=3s5z_vs_3s6z runner=parallel batch_size_run=4 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# 6h_vs_8z
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=6h_vs_8z runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=500000 batch_size=128 td_lambda=0.3
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=6h_vs_8z runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=500000 batch_size=128 td_lambda=0.3

# other scenarios
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=other_scenarios runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=other_scenarios runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
~~~

# Citing  SMAC-HARD 

If you use SMAC in your research, please cite the [SMAC-HARD paper](xxxxxx).

In BibTeX format:

```tex
comming soon ^_^
```