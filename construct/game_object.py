# ARQUIVO: construct/game_object.py

import pygame as py
import os
import re

from .global_instances import GRID_SIZE

class Game_Obj(py.sprite.Sprite):
    """Classe base para todos os objetos do jogo. (gerencia imagem, posição, animação e desenho na tela)"""
    def __init__(self, info_item, x=0, y=0):
        """ 
        Inicializa o objeto do jogo.
        ... (docstring)
        """
        super().__init__()
        self.info = info_item

        # Atributos extraídos do dicionário 'info'
        self.tamanho_grid = self.info.get('tamanho', (1, 1))
        self.nome = self.info.get('nome', 'Desconhecido')
        
        # --- LÓGICA DE ROTAÇÃO E IMAGEM ---
        self.tipo_rotacao = self.info.get('tipo_rotacao', 'transform')
        self.rotacao_atual = 0
        
        # Dicionário para guardar as imagens originais já na escala correta
        self.imagens_originais_escaladas = {}
        
        # Calcula o tamanho correto em pixels UMA VEZ
        w_pixels = self.tamanho_grid[0] * GRID_SIZE
        h_pixels = self.tamanho_grid[1] * GRID_SIZE
        
        try:
            # Carrega a imagem frontal e já a escala para o tamanho correto
            img_frente_original = py.image.load(self.info['img_path']).convert_alpha()
            self.imagens_originais_escaladas['frente'] = py.transform.scale(img_frente_original, (w_pixels, h_pixels))

            # Carrega e escala a imagem lateral, se existir
            if self.tipo_rotacao == 'swap':
                caminho_lado = self.info['img_path'].replace(".png", "_lado.png")
                img_lado_original = py.image.load(caminho_lado).convert_alpha()
                # A imagem de lado deve ter as dimensões do grid invertidas (ex: 3x2)
                self.imagens_originais_escaladas['lado'] = py.transform.scale(img_lado_original, (h_pixels, w_pixels))
        except py.error as e:
            print(f"Erro ao carregar imagem para '{self.nome}': {e}")
            self.imagens_originais_escaladas['frente'] = py.Surface((w_pixels, h_pixels))
            self.imagens_originais_escaladas['frente'].fill((255, 0, 0))

        # A imagem inicial é a imagem de frente já na escala certa
        self.image = self.imagens_originais_escaladas['frente']
        self.rect = self.image.get_rect(topleft=(x, y))

        # Lógica de animação
        self.animations = {} # Seu código de animação pode ser readaptado aqui se necessário

    def rotacionar(self, nova_rotacao):
        self.rotacao_atual = nova_rotacao
        
        if self.tipo_rotacao == 'transform':
            # Rotaciona a imagem original já escalada
            img_original = self.imagens_originais_escaladas['frente']
            self.image = py.transform.rotate(img_original, self.rotacao_atual)
        
        elif self.tipo_rotacao == 'swap':
            if self.rotacao_atual == 0:
                self.image = self.imagens_originais_escaladas['frente']
            elif self.rotacao_atual == 180:
                self.image = py.transform.flip(self.imagens_originais_escaladas['frente'], False, True)
            elif self.rotacao_atual == 270: # Direita
                self.image = self.imagens_originais_escaladas['lado']
            elif self.rotacao_atual == 90: # Esquerda
                self.image = py.transform.flip(self.imagens_originais_escaladas['lado'], True, False)
        
        centro_antigo = self.rect.center
        self.rect = self.image.get_rect(center=centro_antigo)

    def update(self):
        """
        Atualiza o estado do objeto. Animação só ocorre se não estiver rotacionado.
        A rotação é prioritária para o feedback visual durante o posicionamento.
        """
        if self.rotacao_atual == 0 and self.animations:
            self._animate()

    def _load_animations(self, path, width, height):
        try: 
            for filename in sorted(os.listdir(path)):
                match = re.match(r'([a-zA-Z]+)_(\d+)', filename)
                if match:
                    animation_name = match.group(1)
                    full_path = os.path.join(path, filename)
                    image = py.image.load(full_path).convert_alpha()
                    image = py.transform.scale(image, (width, height))

                    if animation_name not in self.animations: self.animations[animation_name] = []
                    self.animations[animation_name].append(image)
        except (py.error, FileNotFoundError) as e:
            print(f"Erro ao carregar animação de '{path}': {e}")

    def _animate(self):
        if not self.animation_state or not self.animations or self.animation_state not in self.animations:
            return
        now = py.time.get_ticks()
        frames = self.animations[self.animation_state]

        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]

    def desenhar(self, surface):
        surface.blit(self.image, self.rect)