import pygame
pygame.init() 

# Variaveis de tela
ALTURA = 768  # Múltiplo de 64 para um grid perfeito
LARGURA = 1024 # Múltiplo de 64

# --- CORREÇÕES AQUI ---
# Define o tamanho da célula do grid aqui
GRID_SIZE = 64 

# Calcula a quantidade de células na tela
GRID_LARGURA = LARGURA // GRID_SIZE
GRID_ALTURA = ALTURA // GRID_SIZE
# -------------------------

# Fonte
fonte = pygame.font.SysFont(None, 50)