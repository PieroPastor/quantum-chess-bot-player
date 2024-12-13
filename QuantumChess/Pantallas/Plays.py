from .Constants import *

def draw_board(board):
    """Dibujar el tablero de ajedrez con etiquetas de filas y columnas."""
    # Dibujar el tablero
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(
                BOARD_OFFSET + col * SQUARE_SIZE,
                BOARD_OFFSET + row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, rect)

            # Dibujar las piezas
            piece = board[row][col]
            if piece != ".":
                screen.blit(
                    pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE)),
                    rect.topleft,
                )

    # Dibujar etiquetas de las filas (A-H) al lado derecho del tablero
    for row in range(8):
        label = font.render(chr(65 + row), True, BLACK)  # A = 65 en ASCII
        screen.blit(
            label,
            (
                BOARD_OFFSET + 8 * SQUARE_SIZE + 5,  # Justo al lado del tablero
                BOARD_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2 - label.get_height() // 2,
            ),
        )

    # Dibujar etiquetas de las columnas (1-8) debajo del tablero
    for col in range(8):
        label = font.render(str(col + 1), True, BLACK)  # 1 a 8
        screen.blit(
            label,
            (
                BOARD_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2 - label.get_width() // 2,
                BOARD_OFFSET + 8 * SQUARE_SIZE + 5,  # Justo debajo del tablero
            ),
        )

def draw_text_boxes(input_boxes, active_index):
    """Dibujar las cajas de texto."""
    y_offset = 10  # Desplazamiento vertical adicional, ajusta según sea necesario.

    for i, (rect, text) in enumerate(input_boxes):
        # Crear una nueva posición ajustada hacia abajo
        adjusted_rect = rect.move(0, y_offset)
        # Dibujar el borde de la caja de texto
        color = BLUE if i == active_index else BLACK
        pygame.draw.rect(screen, color, adjusted_rect, 2)
        # Dibujar el texto dentro de la caja
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (adjusted_rect.x + 5, adjusted_rect.y + 5))

def draw_button(button_rect, text, color=WHITE, text_col=BLACK):
    """Dibujar un botón."""
    pygame.draw.rect(screen, color, button_rect)
    text_surface = font.render(text, True, text_col)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def validate_input_boxes(input_boxes):
    for i in range(1, 5):
        if len(input_boxes[i][1]) != max_lengths[i]: return False
    for _, text in input_boxes:
        if not text.strip():  # Verifica si el campo está vacío o solo tiene espacios
            return False
    return True

# Dibujar mensaje de error
def draw_error_message(message):
    error_surface = font.render(message, True, (255, 0, 0))  # Texto en rojo
    error_rect = error_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(error_surface, error_rect)

def serialize(input_boxes, turn):
    try:
        m = (ord(input_boxes[1][1][0].upper()) - 65) * 8 + int(input_boxes[1][1][1])-1
        move = [int(input_boxes[0][1]), (int(m/8), m%8)]  # Tipo de movimiento
        if input_boxes[2][1] != "-1":
            m = (ord(input_boxes[2][1][0].upper()) - 65) * 8 + int(input_boxes[2][1][1])-1  # Casilla 2
            move.append((int(m/8), m%8))  # Casilla 2
        else: move.append(0)
        m = (ord(input_boxes[3][1][0].upper()) - 65) * 8 + int(input_boxes[3][1][1])-1
        move.append((int(m/8), m%8))  # Casilla 3
        if input_boxes[4][1] != "-1":
            m = (ord(input_boxes[4][1][0].upper()) - 65) * 8 + int(input_boxes[4][1][1]) - 1  # Casilla 4
            move.append((int(m/8), m%8))  # Casilla 4
        else: move.append(0)
        move.append(int(input_boxes[5][1]))  # Coronación
        move.append(BColors.WHITE if turn == "W" else BColors.BLACK)
        print(tuple(move))
    except Exception:
        return 0, 0, 0, 0, 0, turn
    return tuple(move)

def draw_title(title_text, color=BLACK):
    title_surface = titles.render(title_text, True, color)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))  # Centrado en la parte superior
    screen.blit(title_surface, title_rect)

def draw_back_button():
    back_button_rect = pygame.Rect(10, 10, 100, 30)  # Ubicación y tamaño del botón de retroceso
    pygame.draw.rect(screen, WHITE, back_button_rect)
    back_text = font.render("Back", True, BLACK)
    text_rect = back_text.get_rect(center=back_button_rect.center)
    screen.blit(back_text, text_rect)
    return back_button_rect

def show_alert(message):
    """Función para mostrar el mensaje de alerta en la pantalla."""
    screen.fill(WHITE)
    text = font.render(message, True, RED)
    screen.blit(text, (50, 120))
    pygame.display.update()