# ARQUIVO: construct/game_object.py

import pygame as py
import os
import re

# -----------------------------------------------------------------------------
# Classes de UI e Objetos Básicos
# -----------------------------------------------------------------------------

class Game_Obj(py.sprite.Sprite):
    """Classe base para todos os objetos do jogo. (gerencia imagem, posição, animação e desenho na tela)"""
    def __init__(self, x, y, width, height, image_path, tamanho_grid=(1, 1), animation_path=None):
        """ 
        Inicializa o objeto do jogo.

        Args:
            x, y (int): Posição do objeto.
            width, height (int): Largura e altura do objeto.
            image_path (str): Caminho para a imagem do objeto. 
            tamanho_grid (tuple): Tamanho do objeto em unidades de grid (largura, altura).
            animation_path (str): Caminho para a pasta de animações do objeto.
        """
        super().__init__()
        self.tamanho_grid = tamanho_grid
        self.item_key = "" # Utilizado para inventário e identificação de itens
        
        # Tenta carregar a imagem, se falhar cria uma superfície vermelha
        try:
            self.original_image = py.image.load(image_path).convert_alpha()
        except py.error:
            self.original_image = py.Surface((width, height))
            self.original_image.fill((255, 0, 0))
            print(f"Erro: Imagem não encontrada em '{image_path}'. Criando substituto.")

        # Redimensiona a imagem e define o retângulo do objeto
        self.image = py.transform.scale(self.original_image, (width, height))
        # Define o retângulo do objeto na posição (x, y)
        self.rect = self.image.get_rect(topleft=(x, y))

        # --- Animação ---
        # Dicionário para armazenar animações
        self.animations = {}
        # Estado atual da animação
        self.animation_state = 'stand'
        # Quadro atual da animação
        self.current_frame = 0
        # Controle de tempo para animação
        self.last_update = py.time.get_ticks()
        # Velocidade da animação (milissegundos por quadro)
        self.frame_rate = 150

        # Carrega animações se o caminho for fornecido
        if animation_path:
            self._load_animations(animation_path, width, height)

    # --- Métodos Internos de Animação ---
    def _load_animations(self, path, width, height):
        """
        Carrega as animações a partir de arquivos de imagem em um diretório.
        Os arquivos devem seguir o padrão 'nome_0.png', 'nome_1.png', etc.
        onde 'nome' é o nome da animação.
        """
        # Tenta carregar as imagens de animação
        try: 
            # Percorre os arquivos no diretório
            for filename in sorted(os.listdir(path)):
                # Usa expressão regular para extrair o nome da animação
                match = re.match(r'([a-zA-Z]+)_(\d+)', filename)
                if match:
                    animation_name = match.group(1)
                    # Monta o caminho completo do arquivo
                    full_path = os.path.join(path, filename)
                    image = py.image.load(full_path).convert_alpha()
                    image = py.transform.scale(image, (width, height))

                    # Se a animação não existir, cria uma nova lista
                    if animation_name not in self.animations: self.animations[animation_name] = []
                    self.animations[animation_name].append(image)
        except (py.error, FileNotFoundError) as e:
            print(f"Erro ao carregar animação de '{path}': {e}")

    def _animate(self):
        """Atualiza a animação do objeto."""
        # Se não houver animação, retorna
        if not self.animation_state or not self.animations or self.animation_state not in self.animations:
            return
        now = py.time.get_ticks() # Tempo atual em milissegundos
        frames = self.animations[self.animation_state] # Quadro atual da animação

        # Se passou tempo suficiente, atualiza o quadro
        if now - self.last_update > self.frame_rate:
            # Atualiza o tempo do último quadro
            self.last_update = now
            # Avança para o próximo quadro (loopando se necessário)
            self.current_frame = (self.current_frame + 1) % len(frames)
            # Atualiza a imagem do objeto
            self.image = frames[self.current_frame]

    def desenhar(self, surface):
        """
        Desenha o objeto na superfície fornecida.

        Args:
            surface (pygame.Surface): A superfície onde o objeto será desenhado.
        """
        surface.blit(self.image, self.rect)