from .Plays import *
from Utils import *

# Función para aplicar escalamiento de temperatura
def apply_temperature_scaling(logits, temperature):
    exp_scaled = np.exp(logits / temperature)
    probabilities = exp_scaled / np.sum(exp_scaled, axis=1, keepdims=True)
    return probabilities

def predict_move(model, board, turn, T):
    x = [turn] + board
    predictions = model.predict(x)
    adjusted_predictions = {
        'o_mov': apply_temperature_scaling(predictions['o_mov'], T),
        'o_beg1': apply_temperature_scaling(predictions['o_beg1'], T),
        'o_beg2': apply_temperature_scaling(predictions['o_beg2'], T),
        'o_end1': apply_temperature_scaling(predictions['o_end1'], T),
        'o_end2': apply_temperature_scaling(predictions['o_end2'], T),
        'o_pown': apply_temperature_scaling(predictions['o_pown'], T),
    }
    raise NotImplementedError

def predict_move_thread(model, board, turn, T, move, moves, done_flag, stopper):
    while stopper[0] == False and move[0] not in moves:
        pass
        #move[0] = predict_move(model, board, turn, T)
    done_flag[0] = True

def main_ai(board, color):
    clock = pygame.time.Clock()
    # Temperatura para el ajuste
    T = 2.0  #Se variará dependiendo de los resultados obtenidos
    #model = tf.keras.models.load_model('Weights/weights.h5')
    model = None
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
    player = "W" if color == 1 else "B"
    moves = board.GetMoves(turn)
    thread = None
    move_ai = [None]  # Contenedor para la predicción
    done_flag = [False]
    stopper = [False]
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
                stopper[0] = True
                thread.join()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    stopper[0] = True
                    thread.join()
                    return

            #Analiza jugadas del player
            if turn == player:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Verificar si se seleccionó una caja de texto
                    for i, (rect, _) in enumerate(input_boxes):
                        if rect.collidepoint(event.pos):
                            active_index = i
                            input_boxes[active_index] = (rect, "")  # Limpiar caja de texto
                            break
                        else:
                            active_index = -1

                        # Verificar si se presionó el botón
                        if button_rect.collidepoint(event.pos):
                            if validate_input_boxes(input_boxes):
                                neo_move = serialize(input_boxes, turn)
                                if neo_move in moves:
                                    board.GenericMove(neo_move)
                                    turn = "B" if turn == "W" else "W"
                                    moves = board.GetMoves(turn)
                                    error_message = ""  # Borrar mensaje de error
                                else: error_message = "Movimiento inválido."
                            else:
                                error_message = "Por favor, complete todos los campos correctamente."

                            #Llenado de datos si es el turno
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Detectar Enter
                        # Simula el clic del botón de enviar
                        if validate_input_boxes(input_boxes):
                            neo_move = serialize(input_boxes, turn)
                            if neo_move in moves:
                                board.GenericMove(neo_move)
                                turn = "B" if turn == "W" else "W"
                                moves = board.GetMoves(turn)
                                error_message = ""  # Borrar mensaje de error
                            else:
                                error_message = "Movimiento inválido."
                        else:
                            error_message = "Por favor, complete todos los campos."
                    elif active_index != -1:
                        # Manejo de entrada en las cajas de texto
                        _, text = input_boxes[active_index]
                        if event.key == pygame.K_BACKSPACE:
                            input_boxes[active_index] = (input_boxes[active_index][0], text[:-1])
                        elif len(text) < max_lengths[active_index]:  # Límite de caracteres
                            input_boxes[active_index] = (input_boxes[active_index][0], text + event.unicode)

        #Lanza el hilo si no hay hilo activo y no es el turno del jugador
        if not turn == player and thread == None:
            thread = threading.Thread(target=predict_move_thread, args=(model, board.tablero, turn, T, move_ai, moves, done_flag, stopper))
            thread.start()

        #Si ya encontró una jugada posible, la realiza
        if done_flag[0]:
            thread.join()
            move_ai = move_ai[0]
            board.GenericMove(move_ai)
            turn = "B" if turn == "W" else "W"
            moves = board.GetMoves(turn)
            done_flag[0] = False
            thread = None

        pygame.display.flip()
        clock.tick(60)