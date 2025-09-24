import pygame
pygame.init() 

# Variaveis de tela
ALTURA = 600
LARGURA = 800
# Fonte
fonte = pygame.font.SysFont(None, 50)
#variaveis de estado
GAME_RUN = None
MENU = "menu"
SELECAO = "selecao"
FASE = "fase"
EDITOR_MODE = None
ON_FIXED = None
SCENE_STATE = None