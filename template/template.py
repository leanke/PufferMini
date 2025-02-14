'''High-perf Template

'''

import numpy as np
import gymnasium

import pufferlib
from template.cy_template import CyTemplate


class Template(pufferlib.PufferEnv):
    def __init__(self, num_envs=1, render_mode=None, width=500, height=640, max_score=21, frameskip=1, report_interval=1, buf=None):
        self.single_observation_space = gymnasium.spaces.Box(low=0, high=1, shape=(8,), dtype=np.float32,)
        self.single_action_space = gymnasium.spaces.Discrete(3)
        self.render_mode = render_mode
        self.num_agents = num_envs
        self.report_interval = report_interval
        self.human_action = None
        self.tick = 0
        super().__init__(buf)
        self.c_envs = CyTemplate(self.observations, self.actions, self.rewards, self.terminals, num_envs, width, height, max_score, frameskip)
 
    def reset(self, seed=None):
        self.tick = 0
        self.c_envs.reset()
        return self.observations, []

    def step(self, actions):
        self.actions[:] = actions
        self.c_envs.step()

        info = []
        if self.tick % self.report_interval == 0:
            log = self.c_envs.log()
            if log['episode_length'] > 0:
               info.append(log)

        self.tick += 1
        return (self.observations, self.rewards,
            self.terminals, self.truncations, info)

    def render(self):
        self.c_envs.render()

    def close(self):
        self.c_envs.close()

def test_performance(timeout=10, atn_cache=1024):
    env = Template(num_envs=1000)
    env.reset()
    tick = 0

    actions = np.random.randint(0, 2, (atn_cache, env.num_agents))

    import time
    start = time.time()
    while time.time() - start < timeout:
        atn = actions[tick % atn_cache]
        env.step(atn)
        tick += 1

    print(f'SPS: {env.num_agents * tick / (time.time() - start)}')


if __name__ == '__main__':
    test_performance()