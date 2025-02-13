from .environment import *

try:
    import torch
except ImportError:
    pass
else:
    from .policy import Policy
    try:
        from .policy import Recurrent
    except:
        Recurrent = None