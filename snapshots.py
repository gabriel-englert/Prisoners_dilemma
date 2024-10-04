import numpy as np
from modules import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#definindo parâmetros do jogo
r = 0.020

R = 1
P = 0
T = 1+r
S = -r

payoff_matrix = np.array([[R,S],[T,P]])
#parâmetros da rede quadrada
L = 150
N = L**2
players = random_players(N)

p_c = players.count(0)/N
p_d = players.count(1)/N
print(p_c,p_d)

p_c_list = [p_c]
p_d_list = [p_d]
        
lattice = create_lattice(L)

lattice_payoff = play_neighbors_lattice(players, lattice, payoff_matrix)
#snapshots for animation
snapshots = [np.reshape(np.array(players),[L,L])]

#monte carlo steps
for i in range(1,1000):
    players, lattice_payoff = update_strategy_mcs(players,lattice,lattice_payoff,payoff_matrix)

    p_c = players.count(0)/N
    p_d = players.count(1)/N
    p_c_list.append(p_c)
    p_d_list.append(p_d)
    snapshots.append(np.reshape(np.array(players),[L,L]))
    if i%100 == 0:
        plt.imshow(snapshots[i], cmap='bwr', vmin=0, vmax=1)
        if i==0:
            plt.colorbar()
        plt.pause(0.00001)
        

#animation
plt.show()


