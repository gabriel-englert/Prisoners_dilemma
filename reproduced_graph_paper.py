import numpy as np
from modules import *
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import time
start_time = time.time()

@jit(nopython=True)
def f(r_list,tf,players,lattice,p_c_list,p_d_list):
    for ir,r in enumerate(r_list):
        R = 1
        P = 0
        T = 1+r
        S = -r
        payoff_matrix = np.array([[R,S],[T,P]])
        lattice_payoff = play_neighbors_lattice(players, lattice, payoff_matrix)
        for i in range(0,tf+1):
            players, lattice_payoff = update_strategy_mcs(players,lattice,lattice_payoff,payoff_matrix)
            if i == tf:
                p_c = np.sum(players==0)/N
                p_d = np.sum(players==1)/N
                p_c_list[ir] = p_c
                p_d_list[ir] = p_d
    return

#definindo parâmetros do jogo
r_list = np.arange(0, 0.032, 0.001)

L = 100
N = L**2

players = np.array(random_players(N))
lattice = create_lattice(L)

p_c_list = np.zeros(len(r_list), dtype=np.float64)
p_d_list = np.zeros(len(r_list), dtype=np.float64)
tf = 20000

f(r_list,tf,players,lattice,p_c_list,p_d_list)

print((time.time() - start_time))

plt.scatter(r_list, p_c_list, label='cooperators')
plt.scatter(r_list, p_d_list, label = 'defectors')
plt.xlabel('r')
plt.ylabel('frequency')
plt.legend()
plt.title('Densidades em função do parâmetro r')
plt.savefig('density_game_theory_paper.png',dpi=1200)
plt.show()

        


