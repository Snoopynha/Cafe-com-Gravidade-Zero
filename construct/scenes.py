import pygame as py 
from sys import exit
from construct.global_instances import *
from construct.game_object import *

# ---------------------Classe dos itens que podem ser colocados------------------------
class ObjetoColocavel:
    def __init__(self, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

class Button:
    def __init__(self, texto, x, y, w, h, cor, cor_hover, acao):
        self.texto = texto
        self.rect = py.Rect(x, y, w, h)
        self.cor = cor
        self.cor_hover = cor_hover
        self.acao = acao
    def desenhar(self, tela, mouse):
        cor = self.cor_hover if self.rect.collidepoint(mouse) else self.cor
        py.draw.rect(tela, cor, self.rect)
        txt = fonte.render(self.texto, True, (255,255,255))
        tela.blit(txt, (self.rect.x + (self.rect.w - txt.get_width())//2,
                        self.rect.y + (self.rect.h - txt.get_height())//2))
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
    def __init__(self, game, cor_fundo=(0,0,0)):
        self.game = game
        self.botoes = []
        self.cor_fundo = cor_fundo
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
        mouse = py.mouse.get_pos()
        for b in self.botoes:
            b.desenhar(tela, mouse)
            
# ---------------------Classe de Ediçao do Cenario------------------------

class FaseEditavel(Cena):
    def __init__(self, game, cor_fundo=(0, 0, 0)):
        super().__init__(game, cor_fundo)
        self.GRID_SIZE = GRID_SIZE
        self.estado = 'NORMAL'  # NORMAL, INVENTARIO, POSICIONANDO
        self.objeto_em_mao = None
        self.objetos_do_cenario = []
        self.mapa_da_grade = [[0 for _ in range(GRID_LARGURA)] for _ in range(GRID_ALTURA)]

        self.itens_disponiveis = {
            "malboro": { "img_path": "Cafe-com-Gravidade-Zero/source/malboro_melancia.png", "tamanho": (1, 1), "anim_path": None },
            "gato": { "img_path": "Cafe-com-Gravidade-Zero/source/gato.png", "tamanho": (2, 2), "anim_path": None },
            "isac": { "img_path": "Cafe-com-Gravidade-Zero/source/isac.png", "tamanho": (5, 3), "anim_path": None }
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
                if self.mapa_da_grade[y][x] == 1:
                    return False
        return True
    
    def update(self, eventos):
        super().update(eventos)
        mouse_x, mouse_y = py.mouse.get_pos()

        for e in eventos:
            # --- Estado NORMAL ---
            if self.estado == 'NORMAL':
                if e.type == py.KEYDOWN and e.key == py.K_e:
                    self.estado = 'INVENTARIO'
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

            # --- Estado INVENTARIO ---
            elif self.estado == 'INVENTARIO':
                if e.type == py.KEYDOWN and (e.key == py.K_e or e.key == py.K_ESCAPE):
                    self.estado = 'NORMAL'

                elif e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                    for botao in self.botoes_inventario:
                        if botao.rect.collidepoint(e.pos):
                            self.estado = 'POSICIONANDO'
                            info = botao.info
                            w = info["tamanho"][0] * self.GRID_SIZE
                            h = info["tamanho"][1] * self.GRID_SIZE
                            self.objeto_em_mao = Game_Obj(0, 0, w, h, info["img_path"], info["tamanho"], info.get("anim_path"))
                            self.objeto_em_mao.item_key = botao.item_key
                            self.objeto_em_mao.image.set_alpha(150)
                            break

            # --- Estado POSICIONANDO ---
            elif self.estado == 'POSICIONANDO':
                if e.type == py.KEYDOWN and e.key == py.K_ESCAPE:
                    self.estado = 'NORMAL'
                    self.objeto_em_mao = None

                elif e.type == py.MOUSEBUTTONDOWN and e.button == 1 and self.objeto_em_mao and self.posicao_valida:
                    info = self.itens_disponiveis[self.objeto_em_mao.item_key]
                    x, y = self.objeto_em_mao.rect.topleft
                    w, h = self.objeto_em_mao.rect.size
                    novo_objeto = Game_Obj(x, y, w, h, info["img_path"], info["tamanho"], info.get("anim_path"))
                    self.objetos_do_cenario.append(novo_objeto)

                    grid_x, grid_y = x // self.GRID_SIZE, y // self.GRID_SIZE
                    obj_w, obj_h = info["tamanho"]
                    for row in range(grid_y, grid_y + obj_h):
                        for col in range(grid_x, grid_x + obj_w):
                            self.mapa_da_grade[row][col] = 1

                    self.estado = 'NORMAL'
                    self.objeto_em_mao = None

        # Snap
        if self.estado == 'POSICIONANDO' and self.objeto_em_mao:
            snap_x = (mouse_x // self.GRID_SIZE) * self.GRID_SIZE
            snap_y = (mouse_y // self.GRID_SIZE) * self.GRID_SIZE
            self.objeto_em_mao.rect.topleft = (snap_x, snap_y)

            grid_x, grid_y = snap_x // self.GRID_SIZE, snap_y // self.GRID_SIZE
            self.posicao_valida = self.pode_colocar_aqui(grid_x, grid_y, self.objeto_em_mao.tamanho_grid)

    def drawn(self, tela):
        super().drawn(tela)
        for obj in self.objetos_do_cenario:
            obj.desenhar(tela)

        if self.estado == 'POSICIONANDO':
            self.desenhar_grid(tela)
            if self.objeto_em_mao:
                self.objeto_em_mao.desenhar(tela)
                cor = (0, 255, 0, 100) if self.posicao_valida else (255, 0, 0, 100)
                feedback_surf = py.Surface(self.objeto_em_mao.rect.size, py.SRCALPHA)
                feedback_surf.fill(cor)
                tela.blit(feedback_surf, self.objeto_em_mao.rect.topleft)

        elif self.estado == 'INVENTARIO':
            fundo_inventario = py.Surface(self.INVENTARIO_RECT.size, py.SRCALPHA)
            fundo_inventario.fill((10, 20, 40, 220))
            tela.blit(fundo_inventario, self.INVENTARIO_RECT.topleft)
            py.draw.rect(tela, (100, 120, 150), self.INVENTARIO_RECT, 3)

            txt_titulo = fonte.render("Inventário", True, (255, 255, 255))
            tela.blit(txt_titulo, (self.INVENTARIO_RECT.centerx - txt_titulo.get_width() // 2, self.INVENTARIO_RECT.top + 15))

            for botao in self.botoes_inventario:
                botao.desenhar(tela)

        info = ""
        if self.estado == 'NORMAL': info = "Pressione [E] para abrir o inventário"
        elif self.estado == 'INVENTARIO': info = "Pressione [E] ou [ESC] para fechar"
        elif self.estado == 'POSICIONANDO': info = "Clique para colocar | [ESC] para cancelar"

        txt_ajuda = fonte.render(info, True, (255, 255, 255))
        tela.blit(txt_ajuda, (10, 10))

# ---------------------Demais Cenas------------------------

class Menu(Cena):
    def __init__(self, game):
        super().__init__(game, (30,100,30))
        self.adicionar_botao(Button("JOGAR", 300, 200, 200, 60,
                                   (50,150,200), (100,200,255),
                                   lambda: setattr(game, "cena_atual", game.selecao)))
        self.adicionar_botao(Button("SAIR", 300, 300, 200, 60,
                                   (200,50,50), (255,100,100),
                                   lambda: setattr(game, "running", False)))

class Fase1(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, (217, 214, 71))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("FASE 01", True, (10,10,10))
        tela.blit(txt, (350, 250))

class Fase2(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, (137, 230, 227))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("FASE 02", True, (10,10,10))
        tela.blit(txt, (350, 250))

class Fase3(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, (0, 18, 64))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("FASE 03", True, (10,10,10))
        tela.blit(txt, (350, 250))

class Selecao_Habitat(Cena):
    def __init__(self, game):
        super().__init__(game, (141, 45, 237))
        self.adicionar_botao(Button("HABITATE 1", 300, 150, 200, 60,
                                   (50,150,200), (100,200,255),
                                   lambda: setattr(game, "cena_atual", game.fase1)))
        self.adicionar_botao(Button("HABITATE 2", 300, 230, 200, 60,
                                   (50,150,200), (100,200,255),
                                   lambda: setattr(game, "cena_atual", game.fase2)))
        self.adicionar_botao(Button("HABITATE 3", 300, 310, 200, 60,
                                   (50,150,200), (100,200,255),
                                   lambda: setattr(game, "cena_atual", game.fase3)))
        self.adicionar_botao(Button("VOLTAR", 300, 450, 200, 60,
                                   (200,50,50), (255,100,100),
                                   lambda: setattr(game, "cena_atual", game.menu)))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("Selecione o seu Habitat", True, (10,10,10))
        tela.blit(txt, (30, 70))
