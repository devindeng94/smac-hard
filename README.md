### script allocation

| Map Name         | Script           | Finish | QMIX | QPLEX | VDN  | MAPPO | HAPPO |
| ---------------- | ---------------- | ------ | ---- | ----- | ---- | ----- | ----- |
| 3m               | 3m               |   S    |      |       |      |       |       |
| 8m               | 8m               |   S    |      |       |      |       |       |
| 5m_vs_6m         | 8m               |   S    |      |       |      |       |       |
| 8m_vs_9m         | 8m               |   S    |      |       |      |       |       |
| 10m_vs_11m       | 8m               |   S    |      |       |      |       |       |
| 25m              | 25m              |   S    |      |       |      |       |       |
| 27m_vs_30m       | 25m              |   S    |      |       |      |       |       |
| 2s3z             | 3s5z             |   S    |      |       |      |       |       |
| 3s5z             | 3s5z             |   S    |      |       |      |       |       |
| 3s5z_vs_3s6z     | 3s5z             |   S    |      |       |      |       |       |
| 1c3s5z           | 1c3s5z           |   R    |      |       |      |       |       |
| 3s_vs_3z         | 3s_vs_4z         |   S    |      |       |      |       |       |
| 3s_vs_4z         | 3s_vs_4z         |   S    |      |       |      |       |       |
| 3s_vs_5z         | 3s_vs_4z         |   S    |      |       |      |       |       |
| bane_vs_bane     | bane_vs_bane     |   R    |      |       |      |       |       |
| so_many_baneling | so_many_baneling |   S    |      |       |      |       |       |
| 2s_vs_1sc        | default          |   S    |      |       |      |       |       |
| 2m_vs_1z         | 2m_vs_1z         |   S    |      |       |      |       |       |
| 2c_vs_64zg       | 2c_vs_64zg       |        |      |       |      |       |       |
| MMM              | MMM2             |   S    |      |       |      |       |       |
| MMM2             | MMM2             |   S    |      |       |      |       |       |
| 6h_vs_8z         | 6h_vs_8z         |   R    |      |       |      |       |       |
| corridor         | corridor         |   R    |      |       |      |       |       |

~~~
# 5m_vs_6m
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=5m_vs_6m runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=5m_vs_6m runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# 3s5z_vs_3s6z
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=3s5z_vs_3s6z runner=parallel batch_size_run=4 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=3s5z_vs_3s6z runner=parallel batch_size_run=4 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# 6h_vs_8z
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=6h_vs_8z runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=500000 batch_size=128 td_lambda=0.3
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=6h_vs_8z runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=500000 batch_size=128 td_lambda=0.3

# 8m_vs_9m
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=8m_vs_9m runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=8m_vs_9m runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# 3s_vs_5z
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=3s_vs_5z runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=3s_vs_5z runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# corridor
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=corridor runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=corridor runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# MMM2
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=MMM2 runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=MMM2 runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# 27m_vs_30m
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=27m_vs_30m runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=27m_vs_30m runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# 2c_vs_64zg
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=2c_vs_64zg runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=2c_vs_64zg runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6

# bane_vs_bane
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qmix --env-config=sc2 with env_args.map_name=bane_vs_bane runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
CUDA_VISIBLE_DEVICES="0" python src/main.py --config=qplex --env-config=sc2 with env_args.map_name=bane_vs_bane runner=parallel batch_size_run=8 t_max=10050000 epsilon_anneal_time=100000 batch_size=128 td_lambda=0.6
~~~
