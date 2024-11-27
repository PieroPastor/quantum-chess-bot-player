from .Plays import *

def main_player(board):
    clock = pygame.time.Clock()
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se seleccionó una caja de texto
                for i, (rect, _) in enumerate(input_boxes):
                    if rect.collidepoint(event.pos):
                        active_index = i
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
                        error_message = "Por favor, complete todos los campos."

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

        pygame.display.flip()
        clock.tick(60)