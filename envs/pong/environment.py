import importlib
import pufferlib.emulation

def env_creator(name='pong', *args, **kwargs):
    if 'puffer_' not in name:
        raise pufferlib.exceptions.APIUsageError(f'Invalid environment name: {name}')

    # TODO: Robust sanity / ocean imports
    name = name.replace('puffer_', '')
    try:
        module = importlib.import_module(f'envs.{name}.{name}')
        return getattr(module, 'Pong')
    except ModuleNotFoundError:
        return 'Pong'


