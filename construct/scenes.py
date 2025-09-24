import pygame as py 
from sys import exit
from construct.global_instances import fonte

# Adicionada para representar os itens que podem ser colocados
class ObjetoColocavel:
    def __init__(self, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

# Classe Button (sem alterações)
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

# Classe Cena (sem alterações)
class Cena:
    def __init__(self, game, cor_fundo=(0,0,0)):
        self.game = game
        self.botões = []
        self.cor_fundo = cor_fundo
    def adicionar_botao(self, botao):
        self.botões.append(botao)
    def update(self, eventos):
        mouse = py.mouse.get_pos()
        for e in eventos:
            if e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                for b in self.botões:
                    b.click(mouse)
    def drawn(self, tela):
        tela.fill(self.cor_fundo)
        mouse = py.mouse.get_pos()
        for b in self.botões:
            b.desenhar(tela, mouse)

# SUA CLASSE EDITOR FOI RENOMEADA E CORRIGIDA PARA SER A CLASSE "MÃE"
class FaseEditavel(Cena):
    def __init__(self, game, cor_fundo=(0, 0, 0)):
        super().__init__(game, cor_fundo)
        self.GRID_SIZE = 40
        # CORREÇÃO: Padronizando nomes de estado e variáveis
        self.estado = 'NORMAL'
        self.objeto_em_mao = None
        self.objetos_do_cenario = []

        # CORREÇÃO: Adicionando itens que o código tenta usar
        self.itens_disponiveis = {
            "malboro": py.transform.scale(py.image.load("source/malboro_melancia.png").convert_alpha(),(self.GRID_SIZE,self.GRID_SIZE)),
            # Você pode adicionar uma imagem "planta.png" na sua pasta de assets para a tecla 2 funcionar
            # "planta": py.transform.scale(py.image.load("assets/planta.png").convert_alpha(),(self.GRID_SIZE,self.GRID_SIZE))
        }

    def desenhar_grid(self, tela):
        largura, altura = tela.get_size()
        for x in range(0, largura, self.GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (x, 0), (x, altura), 1)
        for y in range(0, altura, self.GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (0, y), (largura, y), 1)

    def update(self, eventos):
        super().update(eventos)
        mouse_x, mouse_y = py.mouse.get_pos()

        for e in eventos:
            if e.type == py.KEYDOWN:
                if self.estado == 'NORMAL':
                    if e.key == py.K_1 and "malboro" in self.itens_disponiveis: # Pega o item 1
                        self.estado = 'POSICIONANDO'
                        self.objeto_em_mao = ObjetoColocavel(self.itens_disponiveis["malboro"])
                        self.objeto_em_mao.imagem.set_alpha(150)
                    # if e.key == py.K_2 and "planta" in self.itens_disponiveis: # Pega o item 2
                    #     self.estado = 'POSICIONANDO'
                    #     self.objeto_em_mao = ObjetoColocavel(self.itens_disponiveis["planta"])
                    #     self.objeto_em_mao.imagem.set_alpha(150)

                elif self.estado == 'POSICIONANDO':
                    if e.key == py.K_SPACE and self.objeto_em_mao:
                        novo_objeto = ObjetoColocavel(self.objeto_em_mao.imagem.copy())
                        novo_objeto.imagem.set_alpha(255)
                        novo_objeto.rect.topleft = self.objeto_em_mao.rect.topleft
                        self.objetos_do_cenario.append(novo_objeto)
                        self.estado = 'NORMAL'
                        self.objeto_em_mao = None
                    if e.key == py.K_ESCAPE:
                        self.estado = 'NORMAL'
                        self.objeto_em_mao = None
        
        if self.estado == 'POSICIONANDO' and self.objeto_em_mao:
            snap_x = (mouse_x // self.GRID_SIZE) * self.GRID_SIZE
            snap_y = (mouse_y // self.GRID_SIZE) * self.GRID_SIZE
            self.objeto_em_mao.rect.topleft = (snap_x, snap_y)

    def drawn(self, tela):
        super().drawn(tela)
        for obj in self.objetos_do_cenario:
            obj.desenhar(tela)

        if self.estado == 'POSICIONANDO':
            self.desenhar_grid(tela)
            if self.objeto_em_mao:
                self.objeto_em_mao.desenhar(tela)
        
        info = "MODO EDIÇÃO: [1] Pega Item | [ESPAÇO] Coloca | [ESC] Cancela"
        txt_ajuda = fonte.render(info, True, (255, 255, 255))
        tela.blit(txt_ajuda, (10, 10))

# Classe Menu (sem alterações)
class Menu(Cena):
    def __init__(self, game):
        super().__init__(game, (30,100,30))
        self.adicionar_botao(Button("JOGAR", 300, 200, 200, 60,
                                   (50,150,200), (100,200,255),
                                   lambda: setattr(game, "cena_atual", game.selecao)))
        self.adicionar_botao(Button("SAIR", 300, 300, 200, 60,
                                   (200,50,50), (255,100,100),
                                   lambda: setattr(game, "running", False)))

# MUDANÇA PRINCIPAL: Fases agora herdam da classe corrigida FaseEditavel
class Fase1(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, (217, 214, 71))
    def drawn(self, tela):
        super().drawn(tela) # Desenha a grade, os objetos, etc.
        txt = fonte.render("FASE 01", True, (10,10,10))
        tela.blit(txt, (350, 250)) # Posição ajustada para exemplo

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

# Classe Selecao_Habitat (sem alterações)
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