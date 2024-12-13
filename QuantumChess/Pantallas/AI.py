from .Plays import *
from Utils import *

def tuplas_con_max_coincidencias(arreglo, nueva_tupla):
    max_coincidencias = 0
    mejores_tuplas = []

    for tupla in arreglo:
        coincidencias = 0
        for i in range(min(len(tupla), len(nueva_tupla))):  # Comparar solo posiciones válidas
            if tupla[i] == nueva_tupla[i]:  # Comparación estricta posición por posición
                coincidencias += 1

        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            mejores_tuplas = [tupla]
        elif coincidencias == max_coincidencias:
            mejores_tuplas.append(tupla)

    return mejores_tuplas, max_coincidencias


# Función para aplicar escalamiento de temperatura
def softmax_temperature(logits, temperature):
    logits_scaled = logits / temperature  # Aplicamos temperatura
    exp_logits = np.exp(logits_scaled - np.max(logits_scaled))  # Evitar overflow
    probabilities = exp_logits / np.sum(exp_logits)
    return probabilities

def apply_temperature(logits, temperature):
    logits = logits[0]
    if temperature < 0.1: return np.argmax(logits) #Si no hay temperatura elige el máximo
    else: #Se selecciona con base a probabilidades si hay temperatura
        probabilites = softmax_temperature(logits, temperature)
        return np.random.choice(len(logits), p=probabilites)

def predict_move(model, board, turn, T):
    x = [1 if turn == 'W' else 0] + board
    x = np.array(x)
    x = np.expand_dims(x, axis=0) # Cambia la forma a (1, 65)
    predictions = model.predict(x, verbose=0)
    adjusted_predictions = {
        'o_mov': apply_temperature(predictions[0], T),
        'o_beg1': apply_temperature(predictions[1], T),
        'o_beg2': apply_temperature(predictions[2], T),
        'o_end1': apply_temperature(predictions[3], T),
        'o_end2': apply_temperature(predictions[4], T),
        'o_pown': apply_temperature(predictions[5], T),
    }
    b1 = adjusted_predictions['o_beg1']
    b2 = adjusted_predictions['o_beg2']-1 #-1 porque empiezan por -1
    e1 = adjusted_predictions['o_end1']
    e2 = adjusted_predictions['o_end2']-1 #-1 porque empiezan por -1
    out = (adjusted_predictions['o_mov']+1, (int(b1/8), b1%8), (int(b2/8), b2%8), (int(e1/8), e1%8), (int(e2/8), e2%8), adjusted_predictions['o_pown'])
    neo_out = [out[0], out[1]]
    if out[0] == 3: neo_out.append(out[2])
    else: neo_out.append(0)
    neo_out.append(out[3])
    if out[0] == 2: neo_out.append(out[4])
    else: neo_out.append(0)
    neo_out.append(out[5])
    neo_out.append(BColors.WHITE if turn == 'W' else BColors.BLACK)
    return tuple(neo_out) #El movimiento predicho

def predict_move_thread(model, board, turn, move, moves, done_flag, stopper):
    neo_board = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == ".": neo_board.append(0)
            elif board[i][j][0:5] == BColors.WHITE: neo_board.append(1*ord(board[i][j][5]))
            elif board[i][j][0:5] == BColors.BLACK: neo_board.append(-1*ord(board[i][j][5]))
    T = 0.1 #Temperatura inicial que se irá aumentando conforme falle
    max_iguales = 0
    max_sol = None
    mejores_similares = None
    while stopper[0] == False and move[0] not in moves and T <= 1:
        move[0] = predict_move(model, neo_board, turn, T)
        T += 0.1
        similares, iguales = tuplas_con_max_coincidencias(moves, move[0])
        if iguales > max_iguales:
            max_iguales = iguales
            max_sol = move[0]
            mejores_similares = similares
            T = 0.1
    if T > 1 and max_sol is None and mejores_similares != []: move[0] = random.choice(moves)  #Selecciona un movimiento aleatorio si no encontró uno
    elif T > 1:
        move[0] = random.choice(mejores_similares)  #Lo completa con ciertas partes aleatorias, pero gran parte del movimiento está predicho
    done_flag[0] = True

def main_ai(board, color):
    clock = pygame.time.Clock()
    model = tf.keras.models.load_model('Weights/weights.h5')
    #model = None
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
        if len(moves) == 0:
            show_alert("Jaque mate")
            print("Jaque mate")
            time.sleep(2)
            return
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
                if thread is not None: thread.join()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    stopper[0] = True
                    if thread is not None: thread.join()
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
                                    for i in range(len(input_boxes)):
                                        input_boxes[i] = (input_boxes[i][0], "")
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
                                for i in range(len(input_boxes)):
                                    input_boxes[i] = (input_boxes[i][0], "")
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
        if not turn == player and thread is None:
            thread = threading.Thread(target=predict_move_thread, args=(model, board.tablero, turn, move_ai, moves, done_flag, stopper))
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
            move_ai = [None]

        pygame.display.flip()
        clock.tick(60)