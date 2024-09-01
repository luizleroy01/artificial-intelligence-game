import cv2
import numpy as np
import tensorflow as tf

# Carregar o modelo treinado (assumindo que já está treinado)
model = tf.keras.models.load_model('meu_modelo.h5')

# Inicializar a captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    # Capturar um frame
    ret, frame = cap.read()

    # Pré-processar a imagem (ajustar tamanho, converter para grayscale, etc.)
    processed_image = preprocess_image(frame)

    # Fazer a previsão
    prediction = model.predict(processed_image.reshape(1, 224, 224, 3))
    class_index = np.argmax(prediction)

    # Mapear a classe para uma ação
    if class_index == 0:
        # Mover para cima
        # ... (enviar comando para o jogo)
        continue
    elif class_index == 1:
        # Mover para baixo
        # ...
    # ... e assim por diante
        continue

    # Mostrar o frame
    cv2.imshow('frame', frame)

    # Sair ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura de vídeo e fechar todas as janelas
cap.release()
cv2.destroyAllWindows()