import pygame
import cv2
import numpy as np
import tensorflow as tf

# Carregar o modelo treinado (substitua pelo caminho do seu modelo)
model = tf.keras.models.load_model('caminho_do_modelo.h5')  # Carregue o modelo treinado

# Dicionário para mapear as predições para os movimentos
gestures = {
    0: "up",   # Mapeia o índice 0 para "up"
    1: "down", # Mapeia o índice 1 para "down"
    2: "left", # Mapeia o índice 2 para "left"
    3: "right" # Mapeia o índice 3 para "right"
}

# Função para capturar a imagem da webcam e fazer a predição
def get_gesture():
    ret, frame = cap.read()  # Captura o frame da webcam
    if not ret:
        return None

    # Pré-processa a imagem para o modelo
    img = cv2.resize(frame, (224, 224))  # Redimensione conforme o modelo treinado
    img = img / 255.0  # Normaliza a imagem
    img = np.expand_dims(img, axis=0)  # Expande a dimensão para o batch

    # Faz a predição
    predictions = model.predict(img)
    gesture = np.argmax(predictions)  # Seleciona o índice da classe com maior probabilidade

    return gestures.get(gesture, None)

# Inicializando o Pygame
pygame.init()
pygame.display.set_caption("MindWay Game with AI Control")

screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Parâmetros do jogo
player_row, player_col = 0, 0
rect_width = screen_height / 10
rect_height = screen_height / 10
gap = 20
start_x = 50
start_y = 50

# Inicia a captura da webcam
cap = cv2.VideoCapture(0)  # Usa a webcam padrão

running = True
while running:
    # Verifica eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Captura o gesto
    gesture = get_gesture()

    # Move o player com base na predição
    if gesture == "up" and player_row > 0:
        player_row -= 1
    elif gesture == "down" and player_row < 9:
        player_row += 1
    elif gesture == "left" and player_col > 0:
        player_col -= 1
    elif gesture == "right" and player_col < 9:
        player_col += 1

    # Limpa a tela
    screen.fill("purple")

    # Desenha o player
    player_x = start_x + player_col * (rect_width + gap) + rect_width / 2
    player_y = start_y + player_row * (rect_height + gap) + rect_height / 2
    pygame.draw.circle(screen, "red", (player_x, player_y), 20)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(30)  # Controla a taxa de atualização do jogo

# Libera recursos
cap.release()
pygame.quit()
