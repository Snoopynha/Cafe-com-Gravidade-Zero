# construct/scenes.py

import pygame as py 
import json
from sys import exit
from construct.global_instances import *
from construct.game_object import *

# ... (Classes de UI como TextInputBox, Slider, Button, etc. não mudam) ...
class TextInputBox:
    def __init__(self, x, y, w, h, fonte, texto_inicial=''):
        self.rect = py.Rect(x, y, w, h)
        self.cor_inativa = py.Color('lightskyblue3')
        self.cor_ativa = py.Color('dodgerblue2')
        self.cor = self.cor_inativa
        self.texto = texto_inicial
        self.fonte = fonte
        self.surface_texto = self.fonte.render(self.texto, True, (255, 255, 255))
        self.ativo = False
    def handle_event(self, evento):
        if evento.type == py.MOUSEBUTTONDOWN:
            self.ativo = self.rect.collidepoint(evento.pos)
            self.cor = self.cor_ativa if self.ativo else self.cor_inativa
        if evento.type == py.KEYDOWN and self.ativo:
            if evento.key == py.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                self.texto += evento.unicode
            self.surface_texto = self.fonte.render(self.texto, True, (255, 255, 255))
    def desenhar(self, tela):
        py.draw.rect(tela, self.cor, self.rect, 2)
        tela.blit(self.surface_texto, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(200, self.surface_texto.get_width() + 10)
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, val_inicial):
        self.rect = py.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.valor = val_inicial
        self.knob_rect = py.Rect(0, 0, 20, h + 10)
        self.knob_rect.centery = self.rect.centery
        self._atualizar_pos_knob()
        self.arrastando = False
    def _atualizar_pos_knob(self):
        range_pixels = self.rect.width - self.knob_rect.width
        range_valores = self.max_val - self.min_val
        if range_valores == 0: return
        percentual = (self.valor - self.min_val) / range_valores
        self.knob_rect.x = self.rect.x + (percentual * range_pixels)
    def _atualizar_valor_pela_pos(self, pos_mouse_x):
        pos_x = max(self.rect.left, min(pos_mouse_x, self.rect.right - self.knob_rect.width))
        range_pixels = self.rect.width - self.knob_rect.width
        if range_pixels == 0: return
        percentual = (pos_x - self.rect.x) / range_pixels
        self.valor = self.min_val + percentual * (self.max_val - self.min_val)
        self.knob_rect.x = pos_x
    def handle_event(self, evento):
        if evento.type == py.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(evento.pos):
                self.arrastando = True
        elif evento.type == py.MOUSEBUTTONUP:
            self.arrastando = False
        elif evento.type == py.MOUSEMOTION and self.arrastando:
            self._atualizar_valor_pela_pos(evento.pos[0])
    def desenhar(self, tela, fonte):
        py.draw.rect(tela, (100, 100, 100), self.rect, border_radius=5)
        py.draw.rect(tela, (200, 200, 200), self.knob_rect, border_radius=8)
        texto_val = fonte.render(f"{int(self.valor)}%", True, (255, 255, 255))
        tela.blit(texto_val, (self.rect.right + 15, self.rect.centery - texto_val.get_height() // 2))
class Button:
    def __init__(self, x, y, acao, w=0, h=0, texto=None, cor=None, cor_hover=None, imagem_surface=None):
        self.acao = acao
        if imagem_surface is not None:
            self.tipo = 'imagem'
            self.imagem = imagem_surface
            self.rect = self.imagem.get_rect(topleft=(x, y))
        elif texto is not None:
            self.tipo = 'retangulo'
            self.texto = texto
            self.rect = py.Rect(x, y, w, h)
            self.cor = cor
            self.cor_hover = cor_hover
        else:
            raise ValueError("Para criar um botão, você precisa fornecer um 'texto' ou uma 'imagem_surface'.")
    def desenhar(self, tela, mouse):
        mouse_sobre = self.rect.collidepoint(mouse)
        if self.tipo == 'imagem':
            if mouse_sobre:
                imagem_hover = self.imagem.copy()
                imagem_hover.fill((50, 50, 50), special_flags=py.BLEND_RGB_ADD) 
                tela.blit(imagem_hover, self.rect)
            else:
                tela.blit(self.imagem, self.rect)
        else:
            cor = self.cor_hover if self.rect.collidepoint(mouse) else self.cor
            py.draw.rect(tela, cor, self.rect)
            txt = fonte.render(self.texto, True, (255,255,255))
            tela.blit(txt, (self.rect.x + (self.rect.w - txt.get_width())//2, self.rect.y + (self.rect.h - txt.get_height())//2))
    def click(self, mouse):
        if self.rect.collidepoint(mouse) and self.acao:
            self.acao()
class BotaoInventario:
    def __init__(self, item_key, item_info, pos):
        self.item_key = item_key 
        self.info = item_info
        self.imagem = py.transform.scale(py.image.load(item_info["img_path"]).convert_alpha(), (50, 50))
        self.rect = self.imagem.get_rect(topleft=pos)
    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

class Cena:
    def __init__(self, game, cor_fundo=(0,0,0), image_path=None):
        self.game = game
        self.botoes = []
        self.cor_fundo = cor_fundo
        self.imagem_fundo = None
        if image_path:
            try:
                imagem_original = py.image.load(image_path).convert_alpha()
                self.imagem_fundo = py.transform.scale(imagem_original, (LARGURA, ALTURA))
            except FileNotFoundError:
                print(f"AVISO: Imagem de fundo não encontrada em '{image_path}'. Usando cor sólida.")
    def adicionar_botao(self, botao):
        self.botoes.append(botao)
    def update(self, eventos):
        mouse = py.mouse.get_pos()
        for e in eventos:
            if e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                for b in self.botoes:
                    b.click(mouse)
    def drawn(self, tela):
        tela.fill(self.cor_fundo)
        if self.imagem_fundo:
            tela.blit(self.imagem_fundo, (0, 0))
        mouse = py.mouse.get_pos()
        for b in self.botoes:
            b.desenhar(tela, mouse)

class FaseEditavel(Cena):
    ESTADO_NORMAL = 'NORMAL'
    ESTADO_INVENTARIO = 'INVENTARIO'
    ESTADO_POSICIONANDO = 'POSICIONANDO'
    def __init__(self, game, cor_fundo=(0, 0, 0), image_path=None):
        super().__init__(game, cor_fundo, image_path=image_path)
        self.GRID_SIZE = GRID_SIZE
        self.estado = self.ESTADO_NORMAL
        self.objeto_em_mao = None
        self.objetos_do_cenario = []
        self.mapa_da_grade = [[0 for _ in range(GRID_LARGURA)] for _ in range(GRID_ALTURA)]
        self.itens_disponiveis = {
            "malboro": { "img_path": "source/malboro_melancia.png", "tamanho": (1, 1), "anim_path": None, "nome": "Malboro", "volume": 10 },
            "gato": { "img_path": "source/gato.png", "tamanho": (2, 2), "anim_path": None, "nome": "Gato Niko", "volume": 50 },
            "isac": { "img_path": "source/isac.png", "tamanho": (5, 3), "anim_path": None, "nome": "Isac", "volume": 150 },
            "momo": { "img_path": "source/momo.png", "tamanho": (1, 2), "anim_path": None, "nome": "Momo", "volume": 25 }
        }
        self.posicao_valida = False
        self.botoes_inventario = []
        self.INVENTARIO_RECT = py.Rect(100, 100, LARGURA - 200, ALTURA - 200)
    def _criar_botoes_inventario(self):
        self.botoes_inventario = []
        padding = 20
        x_inicial = self.INVENTARIO_RECT.left + padding
        y_inicial = self.INVENTARIO_RECT.top + padding + 40
        x, y = x_inicial, y_inicial
        for key, info in self.itens_disponiveis.items():
            botao = BotaoInventario(key, info, (x, y))
            self.botoes_inventario.append(botao)
            x += botao.rect.width + padding
            if x + botao.rect.width > self.INVENTARIO_RECT.right:
                x = x_inicial
                y += botao.rect.height + padding
    def desenhar_grid(self, tela):
        largura, altura = tela.get_size()
        for x in range(0, largura, GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (x, 0), (x, altura), 1)
        for y in range(0, altura, GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (0, y), (largura, y), 1)
    def pode_colocar_aqui(self, grid_x, grid_y, tamanho_obj):
        obj_w, obj_h = tamanho_obj
        if not (0 <= grid_x < GRID_LARGURA - obj_w + 1 and 0 <= grid_y < GRID_ALTURA - obj_h + 1):
            return False
        for y in range(grid_y, grid_y + obj_h):
            for x in range(grid_x, grid_x + obj_w):
                if self.mapa_da_grade[y][x] != 0:
                    return False
        return True
    def update(self, eventos):
        super().update(eventos)
        mouse_x, mouse_y = py.mouse.get_pos()
        for e in eventos:
            if self.estado == self.ESTADO_NORMAL:
                if e.type == py.KEYDOWN and e.key == py.K_e:
                    self.estado = self.ESTADO_INVENTARIO
                    self._criar_botoes_inventario()
                elif e.type == py.MOUSEBUTTONDOWN and e.button == 3:
                    objetos_a_manter = []
                    for obj in self.objetos_do_cenario:
                        if not obj.rect.collidepoint(e.pos):
                            objetos_a_manter.append(obj)
                        else:
                            grid_x, grid_y = obj.rect.x // self.GRID_SIZE, obj.rect.y // self.GRID_SIZE
                            obj_w, obj_h = obj.tamanho_grid
                            for row in range(grid_y, grid_y + obj_h):
                                for col in range(grid_x, grid_x + obj_w):
                                    self.mapa_da_grade[row][col] = 0
                    self.objetos_do_cenario = objetos_a_manter
            elif self.estado == self.ESTADO_INVENTARIO:
                if e.type == py.KEYDOWN and (e.key == py.K_e or e.key == py.K_ESCAPE):
                    self.estado = self.ESTADO_NORMAL
                elif e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                    for botao in self.botoes_inventario:
                        if botao.rect.collidepoint(e.pos):
                            self.estado = self.ESTADO_POSICIONANDO
                            info = botao.info
                            w = info["tamanho"][0] * self.GRID_SIZE
                            h = info["tamanho"][1] * self.GRID_SIZE
                            self.objeto_em_mao = Game_Obj(0, 0, w, h, info["img_path"], info["tamanho"], 
                                                          info.get("anim_path"), nome=info["nome"], volume=info["volume"])
                            self.objeto_em_mao.item_key = botao.item_key
                            self.objeto_em_mao.image.set_alpha(90)
                            break
            elif self.estado == self.ESTADO_POSICIONANDO:
                if e.type == py.KEYDOWN and e.key == py.K_ESCAPE:
                    self.estado = self.ESTADO_NORMAL
                    self.objeto_em_mao = None
                elif e.type == py.MOUSEBUTTONDOWN and e.button == 1 and self.objeto_em_mao and self.posicao_valida:
                    info = self.itens_disponiveis[self.objeto_em_mao.item_key]
                    x, y = self.objeto_em_mao.rect.topleft
                    w, h = self.objeto_em_mao.rect.size
                    novo_objeto = Game_Obj(x, y, w, h, info["img_path"], info["tamanho"], 
                                           info.get("anim_path"), nome=info["nome"], volume=info["volume"])
                    self.objetos_do_cenario.append(novo_objeto)
                    grid_x, grid_y = x // self.GRID_SIZE, y // self.GRID_SIZE
                    obj_w, obj_h = info["tamanho"]
                    for row in range(grid_y, grid_y + obj_h):
                        for col in range(grid_x, grid_x + obj_w):
                            self.mapa_da_grade[row][col] = 1
                    self.estado = self.ESTADO_NORMAL
                    self.objeto_em_mao = None
        if self.estado == self.ESTADO_POSICIONANDO and self.objeto_em_mao:
            snap_x = (mouse_x // self.GRID_SIZE) * self.GRID_SIZE
            snap_y = (mouse_y // self.GRID_SIZE) * self.GRID_SIZE
            self.objeto_em_mao.rect.topleft = (snap_x, snap_y)
            grid_x, grid_y = snap_x // self.GRID_SIZE, snap_y // self.GRID_SIZE
            self.posicao_valida = self.pode_colocar_aqui(grid_x, grid_y, self.objeto_em_mao.tamanho_grid)
    def drawn(self, tela):
        super().drawn(tela)
        for obj in self.objetos_do_cenario:
            obj.desenhar(tela)
        if self.estado == self.ESTADO_POSICIONANDO:
            self.desenhar_grid(tela)
            if self.objeto_em_mao:
                self.objeto_em_mao.desenhar(tela)
                cor = (0, 255, 0, 100) if self.posicao_valida else (255, 0, 0, 100)
                feedback_surf = py.Surface(self.objeto_em_mao.rect.size, py.SRCALPHA)
                feedback_surf.fill(cor)
                tela.blit(feedback_surf, self.objeto_em_mao.rect.topleft)
        elif self.estado == self.ESTADO_INVENTARIO:
            fundo_inventario = py.Surface(self.INVENTARIO_RECT.size, py.SRCALPHA)
            fundo_inventario.fill((10, 20, 40, 220))
            tela.blit(fundo_inventario, self.INVENTARIO_RECT.topleft)
            py.draw.rect(tela, (100, 120, 150), self.INVENTARIO_RECT, 3)
            txt_titulo = fonte.render("Inventário", True, (255, 255, 255))
            tela.blit(txt_titulo, (self.INVENTARIO_RECT.centerx - txt_titulo.get_width() // 2, self.INVENTARIO_RECT.top + 15))
            for botao in self.botoes_inventario:
                botao.desenhar(tela)
        info = ""
        if self.estado == self.ESTADO_NORMAL: info = "Pressione [E] para abrir o inventário"
        elif self.estado == self.ESTADO_INVENTARIO: info = "Pressione [E] ou [ESC] para fechar"
        elif self.estado == self.ESTADO_POSICIONANDO: info = "Clique para colocar | [ESC] para cancelar"
        txt_ajuda = fonte.render(info, True, (255, 255, 255))
        tela.blit(txt_ajuda, (10, 10))

# ... (Menu e FormularioSelecao não mudam) ...
class Menu(Cena):
    def __init__(self, game):
        super().__init__(game, (0,0,0))
        largura_tela, altura_tela = self.game.tela.get_width(), self.game.tela.get_height()
        largura_botao, altura_botao = largura_tela * 0.4, altura_tela // 10
        espacamento = 20
        pos_x = (largura_tela - largura_botao) // 2
        pos_y = (altura_tela - (2 * altura_botao + espacamento)) // 2
        self.adicionar_botao(Button(x=pos_x, y=pos_y, w=largura_botao, h=altura_botao, texto="Jogar", 
                                   cor=(50,205,50), cor_hover=(0,255,0),
                                   acao=lambda: setattr(game, "cena_atual", game.selecao)))
        self.adicionar_botao(Button(x=pos_x, y=pos_y + altura_botao + espacamento, w=largura_botao, h=altura_botao,
                                   texto="Sair", cor=(200,50,50), cor_hover=(255,100,100),
                                   acao=lambda: setattr(game, "running", False)))
class FormularioSelecao(Cena):
    def __init__(self, game):
        self.caminhos_fundo = ["source/fundo_fase1.png","source/fundo_fase2.png","source/fundo_fase3.png"]
        super().__init__(game, (20, 30, 50), image_path=self.caminhos_fundo[0])
        self.fonte_form = py.font.SysFont(None, 32)
        self.habitat_selecionado = 0
        self.habitats_disponiveis = [game.fase1, game.fase2, game.fase3]
        self.imagens_habitat = []
        try:
            for i in range(1, 4):
                path = f"source/habitat_{i}_preview.png"
                img = py.image.load(path).convert_alpha()
                self.imagens_habitat.append(py.transform.scale(img, (150, 150)))
        except FileNotFoundError:
            print("AVISO: Imagens de preview do habitat não encontradas. Usando placeholders.")
            for _ in range(3):
                placeholder = py.Surface((150, 150))
                placeholder.fill((80,80,80))
                self.imagens_habitat.append(placeholder)
        largura_tela, altura_tela = self.game.tela.get_size()
        self.input_nome = TextInputBox(largura_tela * 0.2, altura_tela * 0.15, 400, 40, self.fonte_form, texto_inicial="Meu Habitat")
        self.botoes_habitat_rects = []
        x_inicial = largura_tela * 0.2
        y_pos = altura_tela * 0.3
        for i in range(3):
            rect = py.Rect(x_inicial + i * (150 + 20), y_pos, 150, 150)
            self.botoes_habitat_rects.append(rect)
        self.slider_volume = Slider(largura_tela * 0.2, altura_tela * 0.6, 300, 10, 0, 100, 50)
        self.adicionar_botao(Button(x=largura_tela * 0.2, y=altura_tela * 0.8, w=150, h=50,
                                   texto="Jogar", cor=(50,205,50), cor_hover=(0,255,0),
                                   acao=self._iniciar_jogo))
        self.adicionar_botao(Button(x=30, y=30, imagem_surface=py.transform.scale(py.image.load("source/seta_voltar.png").convert_alpha(), (50, 50)), acao=lambda: setattr(game, "cena_atual", game.menu)))
    def _atualizar_fundo(self):
        caminho_img = self.caminhos_fundo[self.habitat_selecionado]
        try:
            imagem_original = py.image.load(caminho_img).convert_alpha()
            self.imagem_fundo = py.transform.scale(imagem_original, (LARGURA, ALTURA))
        except FileNotFoundError:
            print(f"AVISO: Imagem de fundo não encontrada em '{caminho_img}'. Usando cor sólida.")
            self.imagem_fundo = None
            self.cor_fundo = (20, 30, 50)
    def _iniciar_jogo(self):
        if self.habitat_selecionado == 0:
            self.inf = "BUTIJAO"
        if self.habitat_selecionado == 1:
            self.inf = "PIRULA"
        if self.habitat_selecionado == 2:
            self.inf = "CIRCULAR"
        dados_config = { "nome": self.input_nome.texto, "habitat_idx": self.inf, "volume": int(self.slider_volume.valor) }
        with open("config_jogo.json", "w") as f:
            json.dump(dados_config, f, indent=4)
            print(f"Configurações salvas: {dados_config}")
        self.game.cena_atual = self.habitats_disponiveis[self.habitat_selecionado]
    def update(self, eventos):
        super().update(eventos)
        for e in eventos:
            self.input_nome.handle_event(e)
            self.slider_volume.handle_event(e)
            if e.type == py.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.botoes_habitat_rects):
                    if rect.collidepoint(e.pos):
                        if self.habitat_selecionado != i:
                            self.habitat_selecionado = i
                            self._atualizar_fundo()
    def drawn(self, tela):
        super().drawn(tela)
        txt_nome = self.fonte_form.render("Nome:", True, (255, 255, 255))
        tela.blit(txt_nome, (self.input_nome.rect.x, self.input_nome.rect.y - 30))
        txt_habitat = self.fonte_form.render("Selecione o Habitat:", True, (255, 255, 255))
        tela.blit(txt_habitat, (self.botoes_habitat_rects[0].x, self.botoes_habitat_rects[0].y - 30))
        txt_volume = self.fonte_form.render("Volume:", True, (255, 255, 255))
        tela.blit(txt_volume, (self.slider_volume.rect.x, self.slider_volume.rect.y - 30))
        self.input_nome.desenhar(tela)
        self.slider_volume.desenhar(tela, self.fonte_form)
        for i, rect in enumerate(self.botoes_habitat_rects):
            tela.blit(self.imagens_habitat[i], rect)
            if i == self.habitat_selecionado:
                py.draw.rect(tela, (255, 223, 0), rect, 4)

class Fase1(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, image_path="source/habitat_1_preview.png")
        CELULA_BLOQUEADA = 2
        for y in range(2):
            for x in range(GRID_LARGURA):
                self.mapa_da_grade[y][x] = CELULA_BLOQUEADA
        for y in range(GRID_ALTURA):
            self.mapa_da_grade[y][0] = CELULA_BLOQUEADA
            self.mapa_da_grade[y][1] = CELULA_BLOQUEADA
            self.mapa_da_grade[y][GRID_LARGURA - 1] = CELULA_BLOQUEADA
        for x in range(GRID_LARGURA):
            self.mapa_da_grade[GRID_ALTURA - 1][x] = CELULA_BLOQUEADA
    def drawn(self, tela):
        super().drawn(tela)

class Fase2(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, image_path="source/fundo_fase2.png")
    def drawn(self, tela):
        super().drawn(tela)

class Fase3(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, image_path="source/fundo_fase3.png")
    def drawn(self, tela):
        super().drawn(tela)