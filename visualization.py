import numpy as np
from modules import *
import matplotlib.pyplot as plt


L = 50
N = L**2

players = np.array(random_players(N))
players = np.reshape(players,[L,L])


plt.imshow(players)
plt.show()