import gym
import gym_cloudsimplus
import json

from utils.swf import read_swf


env = gym.make('SingleDCAppEnv-v0',
               initial_vm_count="0",
               jobs_as_json=json.dumps(read_swf()),  # added since otherwise the sim is done after the first step, and this test script would fail.
               split_large_jobs="true")
env.reset()

result = env.render()
result = json.loads(result)
print("Start: " + str(result[0][-5:]))

test_actions = [0, 1, 0, 2, 0, 0, 0]
for i, test_action in enumerate(test_actions):
    env.step(test_action)
    result = env.render()
    result = json.loads(result)
    print(f"Step {i+1} (Action {test_action}): " + str(result[0][-5:]))

print("finishing test and closing env...")
env.close()
