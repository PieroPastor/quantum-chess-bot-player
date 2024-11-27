from .Plays import *
from Utils import *

# Función para aplicar escalamiento de temperatura
def apply_temperature_scaling(logits, temperature):
    exp_scaled = np.exp(logits / temperature)
    probabilities = exp_scaled / np.sum(exp_scaled, axis=1, keepdims=True)
    return probabilities

def main_ai(board, color):
    clock = pygame.time.Clock()
    # Temperatura para el ajuste
    T = 2.0  #Se variará dependiendo de los resultados obtenidos
    model = tf.keras.models.load_model('Weights/weights.h5')
    input_boxes = [
        (pygame.Rect(50, 550, 100, 30), ""),  # Tipo de movimiento
        (pygame.Rect(160, 550, 50, 30), ""),  # Casilla 1
        (pygame.Rect(220, 550, 50, 30), ""),  # Casilla 2
        (pygame.Rect(280, 550, 50, 30), ""),  # Casilla 3
        (pygame.Rect(340, 550, 50, 30), ""),  # Casilla 4
        (pygame.Rect(400, 550, 130, 30), ""),  # Coronación
    ]
    active_index = -1
    button_rect = pygame.Rect(235, 600, 100, 30)  # Botón de enviar
    error_message = ""
    turn = "W"
    moves = board.GetMoves(turn)
    while True:
        screen.fill(GRAY)  # Fondo gris claro

        # Dibujar el tablero
        draw_board(board.tablero)

        # Dibujar el botón de retroceso
        back_button_rect = draw_back_button()

        # Dibujar las cajas de texto
        draw_text_boxes(input_boxes, active_index)

        # Dibujar el botón de enviar
        draw_button(button_rect, "Enviar")

        # Mostrar mensaje de error si existe
        if error_message:
            draw_error_message(error_message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button_rect.collidepoint(event.pos):
                return