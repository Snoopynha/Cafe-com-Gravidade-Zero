"""
ARQUIVO DE CONFIGURAÇÕES GLOBAIS

Este arquivo é responsável por:
1. Inicializar a biblioteca Pygame.
2. Definir as constantes essenciais que serão usadas em todo o projeto,
   como dimensões da tela, tamanho do grid e fontes.
   
Centralizar essas definições aqui torna o código mais limpo e fácil de manter,
pois qualquer ajuste de tamanho ou fonte pode ser feito em um único lugar.
"""

import pygame
pygame.init() 

# -----------------------------------------------------------------------------
# CONSTANTES DE TELA E GRID
# -----------------------------------------------------------------------------

# Define as dimensões da tela
ALTURA = 768  # Altura da tela. Múltiplo de 64 para um grid perfeito
LARGURA = 1024 # Largura da tela. Também múltiplo de 64

# --- CORREÇÕES AQUI ---
# Define o tamanho de cada célula do grid em pixels. 
# Esta é a unidade base para posicionar objetos no cenário.
GRID_SIZE = 64 

# Calcula a quantidade de células que cabem na tela, com base nas dimensões da janela e do grid.
# O operador `//` garante uma divisão inteira.
GRID_LARGURA = LARGURA // GRID_SIZE
GRID_ALTURA = ALTURA // GRID_SIZE
# -------------------------

# -----------------------------------------------------------------------------
# FONTES E TEXTO
# -----------------------------------------------------------------------------

# Cria uma fonte padrão para o jogo.
fonte = pygame.font.SysFont(None, 50)