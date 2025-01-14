#!/bin/sh
env="StarCraft2"
map="3s_vs_5z"
algo="mappo"
exp="check"


for seed in 5;
do
    echo "seed is ${seed}:"
    CUDA_VISIBLE_DEVICES=1 python ../train/train_smac.py --env_name ${env} --algorithm_name ${algo} --experiment_name ${exp} \
    --map_name ${map} --seed ${seed} --n_training_threads 1 --n_rollout_threads 8 --num_mini_batch 1 --episode_length 400 \
    --num_env_steps 10050000 --ppo_epoch 15 --clip_param 0.05 --use_value_active_masks --use_eval --eval_episodes 32 --stacked_frames 4 --use_stacked_frames
done