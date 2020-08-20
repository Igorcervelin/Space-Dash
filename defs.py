#Tamanho da Janela
DISPLAY_W = 960
DISPLAY_H = 540

#Specs
FPS = 30
DATA_FONT_SIZE = 18
DATA_FONT_COLOR =  (255, 255, 0)
BG_FILENAME = 'images/background2.jpg'

OBSTACLE_FILENAME = 'images/Iron2.png' #Imagem do obstáculo
OBSTACLE_SPEED = 70/1000 # Velocidade
OBSTACLE_DONE = 1 # Verifica se o obstáculo já saiu da tela 
OBSTACLE_MOVING = 0 # Verifica se o obstáculo está se movendo
OBSTACLE_UPPER = 1 # Obstáculo superior
OBSTACLE_LOWER = 0 # Obstáculo inferiro
OBSTACLE_ADD_GAP = 260 # Distância entre os obstáculos
OBSTACLE_MIN = 80 # Tamanho mínimo do obstáculo
OBSTACLE_MAX = 500 # Tamanho máximo do obstáculo
OBSTACLE_START_X = DISPLAY_W # Local onde os obstáculo começam a ser criados
OBSTACLE_GAP_SIZE = 160 # Espaço entre os obstáculos
OBSTACLE_FIRST = 400 # onde o primeiro obstáculo aparece

SHIP_FILENAME = 'images/nave2.png' # Imagem da nave
SHIP_START_SPEED = -0.32 # Altura do pulo
SHIP_START_X = 200 # X inicial
SHIP_START_Y = 200 # Y inicial
SHIP_ALIVE = 1 # Verifica se a nave está viva
SHIP_DEAD = 0 # Verifica se a nave morreu
GRAVITY = 0.001 # Gravidade do mapa


# Rede neural

GENERATION_SIZE = 100

NET_INPUTS = 2
NET_HIDDEN = 5
NET_OUTPUTS = 1

JUMP_CHANCE = 0.4

MAX_Y_DIFF = DISPLAY_H - OBSTACLE_MIN - OBSTACLE_GAP_SIZE/2
MIN_Y_DIFF = OBSTACLE_GAP_SIZE/2 - OBSTACLE_MAX
Y_SHIFT = abs(MIN_Y_DIFF)
NORMALIZER = abs(MIN_Y_DIFF) + MAX_Y_DIFF

MUTATION_WEIGHT_MODIFY_CHANCE = 0.2
MUTATION_ARRAY_MIX_PERC = 0.2
MUTATION_CUT_OFF = 0.3
MUTATION_BAD_TO_KEEP = 0.2
MUTATION_MODIFY_CHANCE_LIMIT = 0.2























































