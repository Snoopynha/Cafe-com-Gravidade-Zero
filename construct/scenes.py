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

# Classe que trata o grid e a colocação/retirada de itens
class FaseEditavel(Cena):
    def __init__(self, game, cor_fundo=(0, 0, 0)):
        super().__init__(game, cor_fundo)
        # Define o tamanho dos quadrados do grid
        self.GRID_SIZE = GRID_SIZE
        # Define como estado padrão 'NORMAL' (onde nenhum item foi selecionado)
        self.estado = 'NORMAL'
        # Guarda o objeto qie está selecionado pelo usuário
        self.objeto_em_mao = None
        # Lista dos objetos que foram colocados na tela
        self.objetos_do_cenario = []
        # Um dicionário com todos os itens disponíveis para serem colocados
        self.mapa_da_grade = [[0 for _ in range(GRID_LARGURA)] for _ in range(GRID_ALTURA)]

        self.itens_disponiveis = {
            "malboro": { "img_path": "source/malboro_melancia.png", "tamanho": (1, 1), "anim_path": None}
        }
        self.posicao_valida = False

    # Método que desenha o grid
    def desenhar_grid(self, tela):
        largura, altura = tela.get_size()
        for x in range(0, largura, self.GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (x, 0), (x, altura), 1)
        for y in range(0, altura, self.GRID_SIZE):
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
    
    # Método que trata as ações do usuário
    def update(self, eventos):
        super().update(eventos)
        mouse_x, mouse_y = py.mouse.get_pos()

        for e in eventos:
            # Trata os eventos de teclado
            if e.type == py.KEYDOWN:
                if self.estado == 'NORMAL':
                    item_selecionado = None
                    if e.key == py.K_1: item_selecionado = "malboro"
                    if e.key == py.K_2: item_selecionado = "mesa"
                    
                    if item_selecionado and item_selecionado in self.itens_disponiveis:
                        self.estado = 'POSICIONANDO'
                        info = self.itens_disponiveis[item_selecionado]
                        w = info["tamanho"][0] * self.GRID_SIZE
                        h = info["tamanho"][1] * self.GRID_SIZE
                        
                        self.objeto_em_mao = Game_Obj(0, 0, w, h, info["img_path"], info["tamanho"], info.get("anim_path"))
                        self.objeto_em_mao.item_key = item_selecionado
                        self.objeto_em_mao.image.set_alpha(150)

                elif self.estado == 'POSICIONANDO':
                    if e.key == py.K_ESCAPE:
                        self.estado = 'NORMAL'
                        self.objeto_em_mao = None
                        
            # Trata os eventos de mouse
            if e.type == py.MOUSEBUTTONDOWN:
                if self.estado == 'POSICIONANDO' and e.button == 1 and self.objeto_em_mao and self.posicao_valida:
                    info = self.itens_disponiveis[self.objeto_em_mao.item_key]
                    x, y = self.objeto_em_mao.rect.topleft
                    w, h = self.objeto_em_mao.rect.size

                    novo_objeto = Game_Obj(x, y, w, h, info["img_path"], info["tamanho"], info.get("anim_path"))
                    novo_objeto.item_key = self.objeto_em_mao.item_key
                    self.objetos_do_cenario.append(novo_objeto)
                    
                    grid_x, grid_y = x // self.GRID_SIZE, y // self.GRID_SIZE
                    obj_w, obj_h = info["tamanho"]
                    for row in range(grid_y, grid_y + obj_h):
                        for col in range(grid_x, grid_x + obj_w):
                            self.mapa_da_grade[row][col] = 1
                    
                    self.estado = 'NORMAL'
                    self.objeto_em_mao = None

                elif self.estado == 'NORMAL' and e.button == 3: 
                    objetos_a_manter = []
                    for obj in self.objetos_do_cenario:
                        if obj.rect.collidepoint(e.pos):
                            grid_x, grid_y = obj.rect.x // self.GRID_SIZE, obj.rect.y // self.GRID_SIZE
                            obj_w, obj_h = obj.tamanho_grid
                            for row in range(grid_y, grid_y + obj_h):
                                for col in range(grid_x, grid_x + obj_w):
                                    self.mapa_da_grade[row][col] = 0
                        else:
                            objetos_a_manter.append(obj)
                    self.objetos_do_cenario = objetos_a_manter


        # Atualiza a posição do item que está sendo posicionado (mantém o item "preso" ao grid)                
        if self.estado == 'POSICIONANDO' and self.objeto_em_mao:
            snap_x = (mouse_x // self.GRID_SIZE) * self.GRID_SIZE
            snap_y = (mouse_y // self.GRID_SIZE) * self.GRID_SIZE
            self.objeto_em_mao.rect.topleft = (snap_x, snap_y)
            
            # Valida a posição para o feedback visual
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
                # ADICIONADO DE VOLTA: Feedback visual verde/vermelho
                cor = (0, 255, 0, 100) if self.posicao_valida else (255, 0, 0, 100)
                feedback_surf = py.Surface(self.objeto_em_mao.rect.size, py.SRCALPHA)
                feedback_surf.fill(cor)
                tela.blit(feedback_surf, self.objeto_em_mao.rect.topleft)
        
        info = "MODO EDIÇÃO: [1] Pega Item | Clique Esq: Coloca | Clique Dir: Remove"
        txt_ajuda = fonte.render(info, True, (255, 255, 255))
        tela.blit(txt_ajuda, (10, 10))

class Menu(Cena):
    def __init__(self, game):
        super().__init__(game, (30,100,30))
        self.adicionar_botao(Button("JOGAR", 300, 200, 200, 60,
                                   (50,150,200), (100,200,255),
                                   lambda: setattr(game, "cena_atual", game.selecao)))
        self.adicionar_botao(Button("SAIR", 300, 300, 200, 60,
                                   (200,50,50), (255,100,100),
                                   lambda: setattr(game, "running", False)))

# As Fases são herdeiras da classe FaseEditavel
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