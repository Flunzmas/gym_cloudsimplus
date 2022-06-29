import gym
import gym_cloudsimplus
import json
import sys

from utils.swf import read_swf

if len(sys.argv) > 1:
    initial_vm_count = sys.argv[1]
else:
    initial_vm_count = '10'

env = gym.make('SingleDCAppEnv-v0',
               initial_vm_count=initial_vm_count,
               jobs_as_json=json.dumps(read_swf()),
               simulation_speedup="1000",
               split_large_jobs="true",
               )

env.reset()

it = 0
reward_sum = 0
while True:
    obs, reward, done, info = env.step(0)
    print(f'{it}, {[str(i) for i in obs]}, {reward}')
    reward_sum += reward

    it += 1
    if done:
        print(f"Episode finished! Reward sum: {reward_sum}")
        break
