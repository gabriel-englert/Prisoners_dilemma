import random as rd
import numpy as np
from numba import jit

@jit(nopython=True)
def random_players(N):
    players = np.zeros(N, dtype=np.int32)  # Criando um array NumPy
    for i in range(N):
        players[i] = np.random.randint(0, 2) 
    return players

@jit(nopython=True)
def create_lattice(L):
    N = int(L**2)
    vizinhanca = np.zeros((N, 4), dtype=np.int32) 
    for i in range(N):
        if (i%L == L-1):
            vizinhanca[i][0] = i + 1 - L #direita
        else:
            vizinhanca[i][0] = i + 1
        if (i%L == 0):
            vizinhanca[i][1] = i - 1 + L #esquerda
        else:
            vizinhanca[i][1] = i - 1
        if (i < L):
            vizinhanca[i][2] = i - L + N #acima
        else:
            vizinhanca[i][2] = i - L
        if (i >= N-L):
            vizinhanca[i][3] = i%L #abaixo
        else:
            vizinhanca[i][3] = i + L
    vizinhanca = vizinhanca.astype('int')
    return vizinhanca

@jit(nopython=True)
def play_neighbors_lattice(players, lattice, payoff_matrix): #todos os jogadores jogam com os vizinhos
    N = len(players)
    lattice_payoff = np.zeros(N, dtype=np.float64)
    for i in range(N):
        total_payoff = 0.0
        for j in lattice[i,:]:
            total_payoff += payoff_matrix[players[i],players[j]]
        lattice_payoff[i] = total_payoff
        total_payoff = 0
    return lattice_payoff


@jit(nopython=True)
def play_neighbors(player,lattice,payoff_matrix, players): #apenas um jogador joga com os vizinhos, adicionei essa para otimizar a atualização de estratégia
    total_payoff = 0.0
    for j in lattice[player,:]:
        total_payoff += payoff_matrix[players[player],players[j]]
    return total_payoff

@jit(nopython=True)
def update_strategy_mcs(players, lattice, lattice_payoff,payoff_matrix,k=0.1):
    '''
    sorteia um jogador, e analisa se troca ou não a estratégia também sorteando
    um vizinho e comparando os payoffs, é aceita a troca com uma propapilidade w.
    caso seja aceita, a lista de players com a nova estratégia
    e a lista dos payoffs é atualizada para o jogador escolhido e para todos os seus vizinhos.
    
    '''
    N = len(players)
    for i in range(N):
        chosen_player = rd.randint(0,N-1)
        r2 = np.random.randint(0, 4)
        chosen_neighbor = lattice[chosen_player,r2]
        ex = lattice_payoff[chosen_player]
        ey = lattice_payoff[chosen_neighbor]
        r = np.random.rand()
        w = 1/(1 + np.exp(-(ey-ex)/k))
        if r<w:

            players[chosen_player] = players[chosen_neighbor]
            lattice_payoff[chosen_player] = play_neighbors(chosen_player,lattice,payoff_matrix,players)
            for j in lattice[chosen_player,:]: #loop nos vizinhos do jogador sorteado
                lattice_payoff[j] = play_neighbors(j,lattice,payoff_matrix, players) #vizinhos jogam com seus vizinhos agora com a lista 'players' atualizada
    return players, lattice_payoff

