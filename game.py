import pygame
import random
from typing import Final
from fpdf import FPDF

#Recohnecimento de voz
import speech_recognition as sr
def call_game():
    # Cria um reconhecedor
    recognizer = sr.Recognizer()

    # Usa o microfone como fonte de áudio
    with sr.Microphone() as source:
        print("Fale algo...")
        audio = recognizer.listen(source)

    # Reconhece a fala usando o Google Web Speech API
    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {text}")
        return text
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError:
        print("Erro ao solicitar os resultados do serviço de reconhecimento de fala")

    


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
active_positions.append({'x':start_matriz,'y': 0,'status':False})  # Armazena a posição inicial

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
    global final_position 

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
            active_positions.append({'x':pos_x, 'y':pos_y,'status':True})  # Armazena a posição final
            return
        
        # Marca a posição como parte do caminho
        matriz[pos_x][pos_y] = 1
        active_positions.append({'x':pos_x, 'y':pos_y,'status':True})


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
large_font = pygame.font.Font(None, 72)  # Fonte maior para o letreiro


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
    return minutes,seconds


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

def draw_goal_message():
    # Renderiza o texto de objetivo alcançado
    goal_text = large_font.render("OBJETIVO ALCANÇADO!", True, (10,92,10))
    text_rect = goal_text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(goal_text, text_rect)

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Explicação do Loop sobre Active Positions", ln=True, align="C")

    explanation = """
O loop a seguir é responsável por iterar sobre todas as `active_positions`, que são as
posições ativadas na matriz ao longo do jogo. Cada posição é verificada se tem seu
status como `True`, indicando que ainda é válida para interação.

Código Explicado:
for position in active_positions:
    if position['status']:
        if position['x'] == player_col and position['y'] == player_row:
            score += 10
            position['status'] = False

Explicação:
1. O loop percorre cada posição da lista `active_positions`.
2. Se o status da posição for `True`, indica que ainda não foi "consumida" pelo jogador.
3. Se as coordenadas `x` e `y` da posição coincidirem com a posição atual do jogador
   (representadas por `player_col` e `player_row`), a posição é considerada como atingida.
4. O score do jogador é incrementado e o status da posição é alterado para `False`,
   indicando que o jogador já passou por essa posição.

Esse loop é essencial para o mecanismo de pontuação e progresso do jogo, permitindo que
o jogador colete pontos ao passar por posições ativas na matriz.
    """
    
    pdf.multi_cell(0, 10, explanation)
    pdf.output("explicacao_loop_active_positions.pdf")
    print("PDF gerado com sucesso: explicacao_loop_active_positions.pdf")

chamou  = True


    

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            player_row, player_col = move_player(event, player_row, player_col)
       

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    time_m,time_s = draw_timer()

    # Desenha o grid e define a matriz de posições
    for row in range(10):
        for col in range(10):
            x = start_x + col * (rect_width + gap)  # Calcula a posição x
            y = start_y + row * (rect_height + gap)  # Calcula a posição y
            positions_matrix[row][col] = (x, y)  # Define a posição na matriz
            pygame.draw.rect(
                screen,
                (255, 140, 0) if matriz[col][row] == 1 and time_s != 0 else rect_color,
                (x, y, rect_width, rect_height),
            )

    # Desenha o player
    if player_row < 6: 
        draw_player()

    draw_score(score)

    if player_row >= 6:
        draw_goal_message()

    for position in active_positions:
        if position['status']:
            if position['x'] == player_col and position['y'] == player_row:
                score = score + 10
                position['status'] = False
       

    # Flip() the display to put your work on screen
    pygame.display.flip()

    if chamou :
        commands = call_game()
        print(commands)
        list_commands = commands.split(' ')

        for c in list_commands:
            if c == 'baixo':
                player_row += 1
            elif c == 'esquerda':
                player_col -= 1
            elif c == 'direita':
                player_col += 1
            
            chamou = False
    
    

    dt = clock.tick(60) / 1000  # Limits FPS to 60
generate_pdf()
pygame.quit()
