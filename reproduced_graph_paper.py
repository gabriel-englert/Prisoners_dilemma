import numpy as np
from modules import *
import matplotlib.pyplot as plt
plt.style.use('ggplot')
r = 0
#definindo parâmetros do jogo
r_list = [r for r in np.arange(0,0.032,0.002)]

L = 50
N = L**2

players = random_players(N)
lattice = create_lattice(L)

p_c_list = []
p_d_list = []

for r in r_list:
    R = 1
    P = 0
    T = 1+r
    S = -r
    payoff_matrix = np.array([[R,S],[T,P]])
    lattice_payoff = play_neighbors_lattice(players, lattice, payoff_matrix)
    for i in range(0,301):
        players, lattice_payoff = update_strategy_mcs(players,lattice,lattice_payoff,payoff_matrix)
        if i == 300:
            p_c = players.count(0)/N
            p_d = players.count(1)/N
            p_c_list.append(p_c)
            p_d_list.append(p_d)


plt.scatter(r_list, p_c_list, label='cooperators')
plt.scatter(r_list, p_d_list, label = 'defectors')
plt.xlabel('r')
plt.ylabel('frequency')
plt.legend()
plt.title('Densidades em função do parâmetro r')
plt.savefig('density_game_theory_paper.png',dpi=1200)
plt.show()

        

