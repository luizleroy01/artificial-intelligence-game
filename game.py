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


# pygame setup
import pygame

pygame.init()

# Define window game name
pygame.display.set_caption("MindWay Game")

# Define important dimensions for window and forms into the game
screen_width = 900
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

gap = 20
start_x = 50 
start_y = 50
rect_width = screen_height / 10
rect_height = screen_height / 10
rect_color = "yellow"
player_row, player_col = 0, start_matriz
score = 0

# Inicializa a matriz de posições
positions_matrix = [[(0, 0) for _ in range(10)] for _ in range(10)]

total_time = 10  # 120 segundos = 2 minutos
start_time = pygame.time.get_ticks()  # Tempo de início do temporizador



# Fonte para o placar
font = pygame.font.Font(None, 36)

def draw_timer():
    # Calcula o tempo decrescente em segundos
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = total_time - elapsed_time

    # Verifica se o tempo chegou a zero
    if remaining_time <= 0:
        remaining_time = 0
        # Aqui você pode adicionar uma lógica para quando o tempo acabar, como finalizar o jogo

    # Formata o tempo restante em minutos e segundos
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    
    # Renderiza o texto do cronômetro decrescente
    timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, "white")
    
    # Exibe o cronômetro na tela
    screen.blit(timer_text, (700, 10))


def draw_score(score):
    # Desenha o placar na tela
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (50, 10))

def draw_player():
    player_x = start_x + player_col * (rect_width + gap) + rect_width / 2
    player_y = start_y + player_row * (rect_height + gap) + rect_height / 2
    pygame.draw.circle(screen, "red", (player_x, player_y), 20)


def move_player(event, player_row, player_col):
    # Movimentos verticais
    if event.key == pygame.K_w and player_row > 0:
        player_row -= 1
    if event.key == pygame.K_s and player_row < 9:
        player_row += 1

    # Movimentos horizontais
    if event.key == pygame.K_a and player_col > 0:
        player_col -= 1
    if event.key == pygame.K_d and player_col < 9:
        player_col += 1

    return player_row, player_col


while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            player_row, player_col = move_player(event, player_row, player_col)

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Desenha o grid e define a matriz de posições
    for row in range(10):
        for col in range(10):
            x = start_x + col * (rect_width + gap)  # Calcula a posição x
            y = start_y + row * (rect_height + gap)  # Calcula a posição y
            positions_matrix[row][col] = (x, y)  # Define a posição na matriz
            pygame.draw.rect(
                screen,
                (255, 140, 0) if matriz[col][row] == 1 else rect_color,
                (x, y, rect_width, rect_height),
            )

    # Desenha o player
    draw_player()

    draw_score(score)

    draw_timer()

    # Flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # Limits FPS to 60

pygame.quit()
