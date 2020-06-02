# %matplotlib inline
import numpy as np
import random


import time

import matplotlib.pyplot as plt
from IPython import display
import pylab as pl


class Agent():
    def __init__(self,env):
        print("Action size: ", env.action_size)
        self.action_size = env.action_size

    def get_action(self,state):
        # pole_angle = state[2]
        # action = 0 if pole_angle<0 else 1
        action = random.choice(range(self.action_size))
        return action
