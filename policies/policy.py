from torch import nn
import torch
import torch.nn.functional as F

from functools import partial
import pufferlib.models

from pufferlib.models import Default as Policy
from pufferlib.models import Convolutional as Conv
Recurrent = pufferlib.models.LSTMWrapper
import numpy as np