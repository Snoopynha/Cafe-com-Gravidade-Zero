# core.py

import pygame as py
from construct.global_instances import ALTURA, LARGURA
from construct.scenes import * # <- scenes.py agora exporta FormularioSelecao
py.init()

tela = py.display.set_mode((LARGURA, ALTURA))
relogio = py.time.Clock()

class Game:
    def __init__(self):
        self.tela = tela
        self.menu = Menu(self)
        self.fase1 = Fase1(self)
        self.fase2 = Fase2(self)
        self.fase3 = Fase3(self)
        # --- ALTERAÇÃO AQUI ---
        # Trocamos a antiga classe 'Selecao_Habitat' pela nova 'FormularioSelecao'
        self.selecao = FormularioSelecao(self)
        # --------------------
        self.cena_atual = self.menu
        self.running = True
    
    def run(self):
        while self.running:
            events = py.event.get()
            for e in events:
                if e.type == py.QUIT:
                    self.running = False
            self.cena_atual.update(events) 
            self.cena_atual.drawn(tela)
            py.display.flip()
Game().run()
py.quit()