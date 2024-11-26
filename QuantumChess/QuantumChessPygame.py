import pygame
import sys
from Tablero import Tablero
from Piezas import BColors

# Configuración inicial
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 580, 700
SQUARE_SIZE = 60
BOARD_OFFSET = 50
FONT_SIZE = 24

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Inicializar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Chess")
max_lengths = [1, 2, 2, 2, 2, 1]

# Fuente para texto
font = pygame.font.Font(None, FONT_SIZE)

# Tablero por defecto
default_board = Tablero()

# Cargar piezas
PIECES = {
    f"{BColors.BLACK}R{BColors.RESET}": pygame.image.load("Images/br.png"),
    f"{BColors.BLACK}K{BColors.RESET}": pygame.image.load("Images/bk.png"),
    f"{BColors.BLACK}B{BColors.RESET}": pygame.image.load("Images/bb.png"),
    f"{BColors.BLACK}Q{BColors.RESET}": pygame.image.load("Images/bq.png"),
    f"{BColors.BLACK}E{BColors.RESET}": pygame.image.load("Images/be.png"),
    f"{BColors.BLACK}P{BColors.RESET}": pygame.image.load("Images/bp.png"),
    f"{BColors.WHITE}R{BColors.RESET}": pygame.image.load("Images/wr.png"),
    f"{BColors.WHITE}K{BColors.RESET}": pygame.image.load("Images/wk.png"),
    f"{BColors.WHITE}B{BColors.RESET}": pygame.image.load("Images/wb.png"),
    f"{BColors.WHITE}Q{BColors.RESET}": pygame.image.load("Images/wq.png"),
    f"{BColors.WHITE}E{BColors.RESET}": pygame.image.load("Images/we.png"),
    f"{BColors.WHITE}P{BColors.RESET}": pygame.image.load("Images/wp.png"),
}


def draw_board(board):
    """Dibujar el tablero de ajedrez."""
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

            piece = board[row][col]
            if piece != ".":
                screen.blit(
                    pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE)),
                    rect.topleft,
                )


def draw_text_boxes(input_boxes, active_index):
    """Dibujar las cajas de texto."""
    for i, (rect, text) in enumerate(input_boxes):
        color = BLUE if i == active_index else BLACK
        pygame.draw.rect(screen, color, rect, 2)
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (rect.x + 5, rect.y + 5))


def draw_button(button_rect, text):
    """Dibujar un botón."""
    pygame.draw.rect(screen, WHITE, button_rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def main_menu():
    """Menú principal para elegir el modo de juego."""
    button_width, button_height = 200, 50
    button_margin = 20

    button_1v1 = pygame.Rect(
        (WIDTH - button_width) // 2, 250, button_width, button_height
    )
    button_vs_ai = pygame.Rect(
        (WIDTH - button_width) // 2, 250 + button_height + button_margin, button_width, button_height
    )

    while True:
        screen.fill(WHITE)

        # Dibujar botones
        pygame.draw.rect(screen, BLUE, button_1v1)
        pygame.draw.rect(screen, RED, button_vs_ai)

        # Dibujar texto en los botones
        text_1v1 = font.render("1 vs 1", True, WHITE)
        text_vs_ai = font.render("1 vs Máquina", True, WHITE)

        screen.blit(text_1v1, text_1v1.get_rect(center=button_1v1.center))
        screen.blit(text_vs_ai, text_vs_ai.get_rect(center=button_vs_ai.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1v1.collidepoint(event.pos):
                    print("Modo 1 vs 1 seleccionado")
                    return "1v1"
                elif button_vs_ai.collidepoint(event.pos):
                    print("Modo 1 vs Máquina seleccionado")
                    return "vs_ai"


def validate_input_boxes(input_boxes):
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
    return tuple(move)

# Actualizar función principal
def main(board):
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
        screen.fill((240, 240, 240))  # Fondo gris claro

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

def main_ai(board):
    raise NotImplementedError("Función aún no implementada.")

# Ejecutar el menú y el juego
game_mode = main_menu()
print(f"Modo seleccionado: {game_mode}")
if game_mode == "1v1": main(default_board)
