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
        print("Não foi possível entender o que você disse.")
    except sr.RequestError as e:
        print(f"Erro ao acessar o serviço de reconhecimento de voz: {e}")
    


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
all_positions = [[True for _ in range(10)] for _ in range(10)]

# Gera uma posição inicial aleatória na primeira coluna da matriz
start_matriz = random.randint(0, 9)
matriz[start_matriz][0] = 1
active_positions.append({'x':start_matriz,'y': 0,'status':False})  # Armazena a posição inicial
# Define a posição inicial do caminho
position_x = start_matriz
position_y = 0
all_positions[position_x][position_y] = False


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
    global all_positions

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
        all_positions[pos_x][pos_y] = False
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
large_font = pygame.font.Font(None, 60)  # Fonte maior para o letreiro


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

def draw_exception_message():
    # Renderiza o texto de objetivo alcançado
    text = f"Exceção Lançada!\nvocê saiu do caminho correto"
    goal_text = large_font.render(f"Exceção Lançada! você perdeu", True, (255,0,0))
    text_rect = goal_text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(goal_text, text_rect)


chamou  = True
show_modal = False
modal_active = False
input_text = ''
end_game = False

def draw_button(screen):
    global show_modal
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(200, 10, 40, 30))  # Desenha o botão azul
    font = pygame.font.SysFont(None, 24)
    text = font.render("Info", True, (255, 255, 255))  # Texto do botão
    screen.blit(text, (pygame.Rect(200, 10, 30, 30).x + 5, pygame.Rect(200, 10, 30, 30).y + 10))

def draw_button_function(screen):
    global modal_active
    pygame.draw.rect(screen, (0, 132, 0), pygame.Rect(300, 10, 150, 30))  # Desenha o botão verde
    font = pygame.font.SysFont(None, 24)
    text = font.render("Create Function", True, (255, 255, 255))  # Texto do botão
    screen.blit(text, (pygame.Rect(300, 10, 150, 30).x + 5, pygame.Rect(300, 10, 150, 30).y + 10))


# Função para desenhar o modal
def draw_modal(screen):
    pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 300))  # Desenha o modal cinza
    font = pygame.font.SysFont(None, 24)
    texto_modal = [
    "Informações do jogo:",
    "1 - O score é sua pontuação no jogo quando acerta ao caminho da trilha",
    "destacada.",
    "2 - Ao errar o caminho da trilha configura-se uma exceção que pode ser",
    "verificável",
    " ou não verificável.",
    "3 - Se você tiver score suficiente acima de 0,a exceção será verificável.",
    "Se não tiver score suficiente, a execeção não será verificavel e dará", 
    "fim ao jogo",
    ]
    start_x = 120
    start_y = 120
    line_height = 30  # Altura entre as linhas de texto

    # Desenha cada texto no modal
    for i, line in enumerate(texto_modal):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (start_x, start_y + i * line_height))

def draw_modal_function(screen):
    global input_text
    pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 300))  # Desenha o modal cinza
    font = pygame.font.SysFont(None, 24)
    texto_modal = [
    "Digite sua função:",
    input_text
    ]
    start_x = 120
    start_y = 120
    line_height = 30  # Altura entre as linhas de texto

    # Desenha cada texto no modal
    for i, line in enumerate(texto_modal):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (start_x, start_y + i * line_height))


while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            if event.key == pygame.K_k:
                direction = call_game()
                if direction == 'esquerda':
                    player_col-=1
                elif direction == 'baixo':
                    player_row+=1
                elif direction == 'direita':
                    player_col+=1
                elif direction == 'cima':
                    player_row-=1
            
            if modal_active:  # Captura apenas quando o modal está ativo
                    if event.key == pygame.K_RETURN:
                        print(f"Texto digitado: {input_text}")  # Faz algo com o texto digitado

                        key_words = input_text.split(' ')
                        if key_words[0] == 'function' and key_words[1] == 'move':
                            direction = int(key_words[3])
                            if key_words[2] == 'esquerda':
                                player_col-=direction
                            elif key_words[2]  == 'baixo':
                                player_row+=direction
                            elif key_words[2]  == 'direita':
                                player_col+=direction
                            elif key_words[2]  == 'cima':
                                player_row-=direction
                        input_text = ""  # Limpa o texto após o uso
                        modal_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]  # Remove o último caractere
                    else:
                        input_text += event.unicode 
            player_row, player_col = move_player(event, player_row, player_col)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(200, 10, 60, 30)
            button_rect_function = pygame.Rect(300, 10, 150, 30)

            if button_rect.collidepoint(mouse_pos):
                show_modal = not show_modal

            if button_rect_function.collidepoint(mouse_pos):
                modal_active = not modal_active
       

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
    if player_row < 6 and not end_game: 
        draw_player()

    draw_score(score)

    if player_row >= 6 and not end_game:
        draw_goal_message()

    for position in active_positions:
        if position['status']:
            if position['x'] == player_col and position['y'] == player_row:
                score = score + 10
                position['status'] = False

    
    if all_positions[player_col][player_row]:
        score = score - 10
        all_positions[player_col][player_row] = False
        if score < 0:
            print("Você perdeu , não tem mais score para tratar suas exceções")

    if score < 0:
        end_game = True

    if end_game:
        draw_exception_message()

    draw_button(screen)
    if show_modal:
        draw_modal(screen)

    draw_button_function(screen)
    if modal_active:
        draw_modal_function(screen)


    # Flip() the display to put your work on screen
    pygame.display.flip()
    

    dt = clock.tick(60) / 1000  # Limits FPS to 60

pygame.quit()
