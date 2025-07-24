#!/bin/sh
env="StarCraft2"
map="3m"
algo="rmappo"
exp="check"
seed=3

echo "seed is ${seed}:"
CUDA_VISIBLE_DEVICES=1 python ../train/train_smac.py --env_name ${env} --algorithm_name ${algo} --experiment_name ${exp} \
--map_name ${map} --seed ${seed} --n_training_threads 1 --n_rollout_threads 8 --num_mini_batch 1 --episode_length 400 \
--num_env_steps 10050000 --ppo_epoch 15 --use_value_active_masks --use_eval --eval_episodes 32
