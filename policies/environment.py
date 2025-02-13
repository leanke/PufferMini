import pufferlib.emulation
import pufferlib.postprocess

from pong.pong import Pong

MAKE_FNS = {
    'pong': Pong,

}

# Alias puffer_ to all names
MAKE_FNS = {**MAKE_FNS, **{'puffer_' + k: v for k, v in MAKE_FNS.items()}}

def env_creator(name='pong'):
    if name in MAKE_FNS:
        return MAKE_FNS[name]
    else:
        raise ValueError(f'Invalid environment name: {name}')