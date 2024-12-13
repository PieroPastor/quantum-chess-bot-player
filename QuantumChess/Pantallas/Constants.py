from Utils import *
from Piezas import BColors

# Configuración inicial
pygame.init()
# Dimensiones de la ventana
WIDTH, HEIGHT = 580, 700
SQUARE_SIZE = 60
BOARD_OFFSET = 50
FONT_SIZE = 20

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (240, 240, 240)

#Longitudes
max_lengths = [1, 2, 2, 2, 2, 1]

# Inicializar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Chess")
# Fuente para texto
titles = pygame.font.Font("Fonts/Xolonium-Bold.ttf", 36)
font = pygame.font.Font("Fonts/Xolonium-Regular.ttf", FONT_SIZE)

# Cargar piezas os.path.join(os.path.dirname(__file__), '..', 'Images', 'br.png')
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