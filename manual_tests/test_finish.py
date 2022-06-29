import gym
import gym_cloudsimplus
import json

from utils.swf import read_swf


env = gym.make('SingleDCAppEnv-v0',
               initial_vm_count="0",
               jobs_as_json=json.dumps(read_swf()),  # added since otherwise the sim is done after the first step, and this test script would fail.
               split_large_jobs="true")
env.reset()
print("Starting a simulation")
env.step(0)

for i in range(50):
    env.step(1)
    result = env.render()
    result = json.loads(result)
    print("Added a VM: " + str(result[0][-5:]))

done = False
while not done:
    obs, reward, done, info = env.step(0)
    state = env.render()
    state = json.loads(state)
    print("Did nothing: " + str(state[0][-5:]))
    print("Result: " + str(done))

print("End of simulation")
