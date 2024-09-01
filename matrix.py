import pygame
import random
from typing import Final

# Definição de constantes
UP_WAY: Final = 1
RIGHT_WAY: Final = 2
DOWN_WAY: Final = 3

# Inicializa variáveis de controle
end_way = 10
matriz = [[0 for _ in range(10)] for _ in range(10)]
positions_matrix = [[0 for _ in range(10)] for _ in range(10)]

# Lista para armazenar as posições setadas como 1
active_positions = []

# Gera uma posição inicial aleatória na primeira coluna da matriz
start_matriz = random.randint(0, 9)
matriz[start_matriz][0] = 1
active_positions.append((start_matriz, 0))  # Armazena a posição inicial

# Define a posição inicial do caminho
position_x = start_matriz
position_y = 0


def next_step(end_way):
    # Determina a direção do próximo passo
    direction = random.randint(1, 3)
    if direction == UP_WAY:
        return (-1, 0)
    elif direction == RIGHT_WAY:
        return (0, 1)
    elif direction == DOWN_WAY:
        return (1, 0)


def set_way(pos_x, pos_y):
    global active_positions  # Usa a lista global para armazenar as posições

    end_way = 10
    while end_way > 0:
        step = next_step(end_way)
        x = step[0]
        y = step[1]
        pos_x = pos_x + x
        pos_y = pos_y + y

        # Verifica se o movimento é horizontal (direita) para diminuir o contador
        if x == 0 and y == 1:
            end_way -= 1

        # Ajusta os limites da posição x
        if pos_x > 9:
            pos_x = 9
        elif pos_x < 0:
            pos_x = 0

        # Ajusta os limites da posição y
        if pos_y < 0:
            pos_y = 0
        elif pos_y > 9:
            pos_y = 9

        # Define o fim do caminho se chegar à última coluna
        if pos_y == 9:
            matriz[pos_x][pos_y] = 1
            active_positions.append((pos_x, pos_y))  # Armazena a posição final
            return
        
        # Marca a posição como parte do caminho
        matriz[pos_x][pos_y] = 1
        active_positions.append((pos_x, pos_y))  # Armazena a posição atual


# Define o caminho a partir da posição inicial
set_way(position_x, position_y)