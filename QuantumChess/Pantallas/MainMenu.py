from .Constants import *
from .Plays import *

def main_menu():
    """Menú principal para elegir el modo de juego."""
    button_width, button_height = 200, 50
    button_margin = 20
    is_ai = False

    button_vs_ai = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
    button_1v1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50)

    while True:
        screen.fill(WHITE)
        draw_title("Quantum Chess")
        # Dibujar botones
        draw_button(button_1v1, "1 vs 1", BLUE, WHITE) # Botón 1 vs 1
        draw_button(button_vs_ai, "1 vs AI", RED, WHITE) # Botón 1 vs Máquina

        if is_ai: #Crea los botones para elegir el color con el que jugará
            white_button_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 50, 100, 50)
            black_button_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 50, 100, 50)
            draw_button(white_button_rect, "White", WHITE, BLACK)
            draw_button(black_button_rect, "Black", BLACK, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1v1.collidepoint(event.pos):
                    print("Modo 1 vs 1 seleccionado")
                    return 1, None
                elif button_vs_ai.collidepoint(event.pos):
                    print("Modo 1 vs Máquina seleccionado")
                    is_ai = True
                    continue #Para que no tome el if que viene
                if is_ai:
                    if white_button_rect.collidepoint(event.pos):
                        print("Jugar con blancas")
                        return 0, 1
                    elif black_button_rect.collidepoint(event.pos):
                        print("Jugar con negras")
                        return 0, 0