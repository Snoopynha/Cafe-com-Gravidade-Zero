# ARQUIVO: construct/game_object.py

import pygame as py
import os
import re

# Esta é a definição completa da sua classe de objeto de jogo.
# Ela é autossuficiente e não depende de nenhuma outra classe do seu projeto.
class Game_Obj(py.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, tamanho_grid=(1, 1), animation_path=None):
        super().__init__()
        self.tamanho_grid = tamanho_grid
        self.item_key = "" # Usado para saber qual item somos (ex: "malboro")
        
        try:
            self.original_image = py.image.load(image_path).convert_alpha()
        except py.error:
            self.original_image = py.Surface((width, height))
            self.original_image.fill((255, 0, 0))
            print(f"Erro: Imagem não encontrada em '{image_path}'. Criando substituto.")

        self.image = py.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animations = {}
        self.animation_state = 'stand'
        self.current_frame = 0
        self.last_update = py.time.get_ticks()
        self.frame_rate = 150

        if animation_path:
            self._load_animations(animation_path, width, height)

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