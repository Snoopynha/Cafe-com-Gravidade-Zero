import pygame as py 
from sys import exit
from construct.global_instances import *
from construct.game_object import *

# -----------------------------------------------------------------------------
# Classes de UI e Objetos Básicos
# -----------------------------------------------------------------------------

class ObjetoColocavel:
    """Classe base para os itens/objetos que pode ser colocados na tela."""
    def __init__(self, imagem):
        """ 
        Inicializa o objeto com uma imagem.
        
        Args:
            imagem (Surface): A imagem do objeto.
        """
        self.imagem = imagem
        self.rect = self.imagem.get_rect()

    def desenhar(self, tela):
        """
        Desenha o objeto na tela.

        Args:
            tela (Surface): A superfície onde o objeto será desenhado.
        """
        tela.blit(self.imagem, self.rect)

class Button:
    """
    Classe de botão genérica e unificada.
    Pode ser um botão retangular com cor ou um botão com imagem.
    """
    def __init__(self, x, y, acao, w=0, h=0, texto=None, cor=None, cor_hover=None, imagem_surface=None):
        """
        Inicializa o botão.

        Args:
            texto (str): Texto do botão (opcional).
            x, y (int): Posição do botão.
            w, h (int): Largura e altura do botão.
            cor (tuple): Cor padrão do botão (opcional).
            cor_hover (tuple): Cor do botão quando o mouse está sobre ele (opcional).
            imagem (Surface): Imagem do botão (opcional).
            acao (function): Função a ser chamada quando o botão é clicado.
        """
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
            # Erro se nenhum tipo for especificado
            raise ValueError("Para criar um botão, você precisa fornecer um 'texto' ou uma 'imagem_surface'.")

    def desenhar(self, tela, mouse):
        """
        Desenha o botão na tela, tratando os diferentes tipos de botão.

        Args:
            tela (Surface): A superfície onde o botão será desenhado.
            mouse (tuple): Posição atual do mouse.
        """

        mouse_sobre = self.rect.collidepoint(mouse)
        if self.tipo == 'imagem':
            if mouse_sobre:
                # Adiciona um efeito de "brilho" ou transparência quando o mouse está sobre o botão
                imagem_hover = self.imagem.copy()
                imagem_hover.fill((50, 50, 50), special_flags=py.BLEND_RGB_ADD) 
                tela.blit(imagem_hover, self.rect)
            else:
                tela.blit(self.imagem, self.rect)
        else:
            # Muda a cor do botão caso o mouse esteja sobre o botão
            cor = self.cor_hover if self.rect.collidepoint(mouse) else self.cor
            py.draw.rect(tela, cor, self.rect)
            txt = fonte.render(self.texto, True, (255,255,255))
            # Centraliza o texto no botão
            tela.blit(txt, (self.rect.x + (self.rect.w - txt.get_width())//2,
                        self.rect.y + (self.rect.h - txt.get_height())//2))
        
    def click(self, mouse):
        """
        Verifica se o botão foi clicado e executa a ação associada.

        Args:
            mouse (tuple): Posição atual do mouse.
        """
        if self.rect.collidepoint(mouse) and self.acao:
            # Executa a ação associada ao botão
            self.acao()

class BotaoInventario:
    """Um botão específico para o inventário , representando um dos itens que podem ser selecionado."""
    def __init__(self, item_key, item_info, pos):
        """
        Inicializa o botão do inventário.

        Args:
            item_key (str): Chave identificadora do item.
            item_info (dict): Dicionário contendo informações do item (imagem, tamanho, etc).
            pos (tuple): Posição (x, y) onde o botão será desenhado.
        """
        self.item_key = item_key 
        self.info = item_info
        
        # Carrega e escala a imagem do item
        self.imagem = py.transform.scale(py.image.load(item_info["img_path"]).convert_alpha(), (50, 50))
        self.rect = self.imagem.get_rect(topleft=pos)

    def desenhar(self, tela):
        """ 
        Desenha o botão do inventário na tela.

        Args:
            tela (Surface): A superfície onde o botão será desenhado.
        """
        tela.blit(self.imagem, self.rect)

# -----------------------------------------------------------------------------
# Classes de Cenas (Telas do Jogo)
# -----------------------------------------------------------------------------

class Cena:
    """Classe base para as cenas do jogo."""
    def __init__(self, game, cor_fundo=(0,0,0)):
        """ 
        Inicializa a cena.

        Args:
            game (Game): Instância do jogo.
            cor_fundo (tuple): Cor de fundo da cena.
        """
        self.game = game
        self.botoes = []
        self.cor_fundo = cor_fundo

    def adicionar_botao(self, botao):
        """Adiciona um botão à cena."""
        self.botoes.append(botao)

    def update(self, eventos):
        """
        Atualiza o estado da cena.

        Args:
            eventos (list): Lista de eventos do Pygame.
        """
        mouse = py.mouse.get_pos()
        for e in eventos:
            # Verifica se teve algum click com o botão esquerdo do mouse
            if e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                # Verifica cada botão na cena
                for b in self.botoes:
                    b.click(mouse)

    def drawn(self, tela):
        """
        Desenha a cena na tela.

        Args:
            tela (Surface): A superfície onde a cena será desenhada.
        """
        tela.fill(self.cor_fundo)
        mouse = py.mouse.get_pos()
        for b in self.botoes:
            b.desenhar(tela, mouse)
            
# Classe de edição de cenário
# -----------------------------------------------------------------------------

class FaseEditavel(Cena):
    """Uma fase que pode ser editada, permitindo adicionar/remover objetos."""

    # Constantes para os estados da fase
    ESTADO_NORMAL = 'NORMAL'
    ESTADO_INVENTARIO = 'INVENTARIO'
    ESTADO_POSICIONANDO = 'POSICIONANDO'

    def __init__(self, game, cor_fundo=(0, 0, 0)):
        super().__init__(game, cor_fundo)
        self.GRID_SIZE = GRID_SIZE
        # O estado atual da fase
        self.estado = self.ESTADO_NORMAL
        self.objeto_em_mao = None
        self.objetos_do_cenario = []
        # Mapa da grade para controle de ocupação (0 = livre, 1 = ocupado)
        self.mapa_da_grade = [[0 for _ in range(GRID_LARGURA)] for _ in range(GRID_ALTURA)]

        # Itens disponíveis para colocar no cenário
        self.itens_disponiveis = {
            "malboro": { "img_path": "source/malboro_melancia.png", "tamanho": (1, 1), "anim_path": None },
            "gato": { "img_path": "source/gato.png", "tamanho": (2, 2), "anim_path": None },
            "isac": { "img_path": "source/isac.png", "tamanho": (5, 3), "anim_path": None },
            "momo": { "img_path": "source/momo.png", "tamanho": (1, 2), "anim_path": None }
        }
        self.posicao_valida = False
        self.botoes_inventario = []
        self.INVENTARIO_RECT = py.Rect(100, 100, LARGURA - 200, ALTURA - 200)

    def _criar_botoes_inventario(self):
        """Cria os botões do inventário com base nos itens disponíveis."""
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
        """Desenha a grade na tela."""
        largura, altura = tela.get_size()
        for x in range(0, largura, GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (x, 0), (x, altura), 1)
        for y in range(0, altura, GRID_SIZE):
            py.draw.line(tela, (200, 200, 200), (0, y), (largura, y), 1)

    def pode_colocar_aqui(self, grid_x, grid_y, tamanho_obj):
        """Verifica se um objeto pode ser colocado na posição da grade especificada."""
        obj_w, obj_h = tamanho_obj
        if not (0 <= grid_x < GRID_LARGURA - obj_w + 1 and 0 <= grid_y < GRID_ALTURA - obj_h + 1):
            return False
        for y in range(grid_y, grid_y + obj_h):
            for x in range(grid_x, grid_x + obj_w):
                if self.mapa_da_grade[y][x] == 1:
                    return False
        return True
    
    def update(self, eventos):
        """Atualiza o estado da fase editável com base nos eventos."""
        super().update(eventos)
        mouse_x, mouse_y = py.mouse.get_pos()

        for e in eventos:
            # --- Estado NORMAL ---
            # Onde o jogador pode abrir o inventário ou remover objetos
            if self.estado == self.ESTADO_NORMAL:
                # Pressiona E para abrir o inventário
                if e.type == py.KEYDOWN and e.key == py.K_e:
                    self.estado = self.ESTADO_INVENTARIO
                    self._criar_botoes_inventario()

                # Clique com o botão direito para remover um objeto
                elif e.type == py.MOUSEBUTTONDOWN and e.button == 3:
                    objetos_a_manter = []
                    for obj in self.objetos_do_cenario:
                        # Se o clique não colidir com o objeto, mantém ele
                        if not obj.rect.collidepoint(e.pos):
                            objetos_a_manter.append(obj)
                        # Se colidir, remove o objeto e libera a área na grade
                        else:
                            # Libera a área ocupada na grade
                            grid_x, grid_y = obj.rect.x // self.GRID_SIZE, obj.rect.y // self.GRID_SIZE
                            obj_w, obj_h = obj.tamanho_grid
                            for row in range(grid_y, grid_y + obj_h):
                                for col in range(grid_x, grid_x + obj_w):
                                    self.mapa_da_grade[row][col] = 0
                    # Atualiza a lista de objetos do cenário
                    self.objetos_do_cenario = objetos_a_manter

            # --- Estado INVENTARIO ---
            # Onde o jogador pode selecionar um item para posicionar
            elif self.estado == self.ESTADO_INVENTARIO:
                # Pressiona E ou ESC para fechar o inventário
                if e.type == py.KEYDOWN and (e.key == py.K_e or e.key == py.K_ESCAPE):
                    self.estado = self.ESTADO_NORMAL

                # Clica em um item do inventário para começar a posicionar
                elif e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                    for botao in self.botoes_inventario:
                        if botao.rect.collidepoint(e.pos):
                            # Começa a posicionar o item selecionado
                            self.estado = self.ESTADO_POSICIONANDO
                            # Cria o objeto em mão com transparência
                            info = botao.info
                            w = info["tamanho"][0] * self.GRID_SIZE
                            h = info["tamanho"][1] * self.GRID_SIZE
                            self.objeto_em_mao = Game_Obj(0, 0, w, h, info["img_path"], info["tamanho"], info.get("anim_path"))
                            self.objeto_em_mao.item_key = botao.item_key
                            # Define a transparência do objeto em mão
                            self.objeto_em_mao.image.set_alpha(150)
                            break

            # --- Estado POSICIONANDO ---
            # Onde o jogador pode posicionar o item selecionado
            elif self.estado == self.ESTADO_POSICIONANDO:
                # Pressiona ESC para cancelar o posicionamento
                if e.type == py.KEYDOWN and e.key == py.K_ESCAPE:
                    self.estado = self.ESTADO_NORMAL
                    self.objeto_em_mao = None # Descarta o objeto em mão

                # Clica com o botão esquerdo para colocar o objeto, se a posição for válida
                elif e.type == py.MOUSEBUTTONDOWN and e.button == 1 and self.objeto_em_mao and self.posicao_valida:
                    info = self.itens_disponiveis[self.objeto_em_mao.item_key]
                    x, y = self.objeto_em_mao.rect.topleft
                    w, h = self.objeto_em_mao.rect.size
                    novo_objeto = Game_Obj(x, y, w, h, info["img_path"], info["tamanho"], info.get("anim_path"))
                    self.objetos_do_cenario.append(novo_objeto)

                    # Marca a área ocupada na grade
                    grid_x, grid_y = x // self.GRID_SIZE, y // self.GRID_SIZE
                    obj_w, obj_h = info["tamanho"]
                    for row in range(grid_y, grid_y + obj_h):
                        for col in range(grid_x, grid_x + obj_w):
                            self.mapa_da_grade[row][col] = 1

                    # Volta ao estado normal
                    self.estado = self.ESTADO_NORMAL
                    self.objeto_em_mao = None

        # Lógica de "Snap" para o objeto em mão para seguir o mouse
        # Acompanha o mouse, mas "encaixa" na grade
        if self.estado == self.ESTADO_POSICIONANDO and self.objeto_em_mao:
            # Calcula a posição "snap" baseada na grade
            snap_x = (mouse_x // self.GRID_SIZE) * self.GRID_SIZE
            snap_y = (mouse_y // self.GRID_SIZE) * self.GRID_SIZE
            self.objeto_em_mao.rect.topleft = (snap_x, snap_y)

            # Verifica se a posição é válida para colocar o objeto
            grid_x, grid_y = snap_x // self.GRID_SIZE, snap_y // self.GRID_SIZE
            self.posicao_valida = self.pode_colocar_aqui(grid_x, grid_y, self.objeto_em_mao.tamanho_grid)

    def drawn(self, tela):
        """Desenha os objetos do cenário na tela."""
        super().drawn(tela)
        for obj in self.objetos_do_cenario:
            obj.desenhar(tela)

        # Desenha a grade e o objeto em mão, se estiver posicionando
        if self.estado == self.ESTADO_POSICIONANDO:
            self.desenhar_grid(tela)
            if self.objeto_em_mao:
                self.objeto_em_mao.desenhar(tela)
                # Desenha o objeto em mão com feedback visual (verde = válido, vermelho = inválido)
                cor = (0, 255, 0, 100) if self.posicao_valida else (255, 0, 0, 100)
                # Cria uma superfície semi-transparente para o feedback
                feedback_surf = py.Surface(self.objeto_em_mao.rect.size, py.SRCALPHA)
                feedback_surf.fill(cor)
                tela.blit(feedback_surf, self.objeto_em_mao.rect.topleft)

        # Desenha a interface do inventário, se estiver no estado INVENTARIO
        elif self.estado == self.ESTADO_INVENTARIO:
            fundo_inventario = py.Surface(self.INVENTARIO_RECT.size, py.SRCALPHA)
            fundo_inventario.fill((10, 20, 40, 220))
            tela.blit(fundo_inventario, self.INVENTARIO_RECT.topleft)
            py.draw.rect(tela, (100, 120, 150), self.INVENTARIO_RECT, 3)

            txt_titulo = fonte.render("Inventário", True, (255, 255, 255))
            tela.blit(txt_titulo, (self.INVENTARIO_RECT.centerx - txt_titulo.get_width() // 2, self.INVENTARIO_RECT.top + 15))

            # Desenha os botões do inventário
            for botao in self.botoes_inventario:
                botao.desenhar(tela)

        # Desenha as instruções na tela
        info = ""
        if self.estado == self.ESTADO_NORMAL: info = "Pressione [E] para abrir o inventário"
        elif self.estado == self.ESTADO_INVENTARIO: info = "Pressione [E] ou [ESC] para fechar"
        elif self.estado == self.ESTADO_POSICIONANDO: info = "Clique para colocar | [ESC] para cancelar"

        txt_ajuda = fonte.render(info, True, (255, 255, 255))
        tela.blit(txt_ajuda, (10, 10))

# -----------------------------------------------------------------------------
# Implementações Específicas das Cenas
# -----------------------------------------------------------------------------

class Menu(Cena):
    """Tela de menu principal do jogo."""
    def __init__(self, game):
        super().__init__(game, (0,0,0))
        # O lambda usa setattr para mudar a cena atual do jogo

        # Centralização automática
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

class Selecao_Habitat(Cena):
    """A tela de seleção de habitat (fase)."""
    def __init__(self, game):
        super().__init__(game, (141, 45, 237))

        # Centralização automática
        largura_tela, altura_tela = self.game.tela.get_width(), self.game.tela.get_height()
        largura_botao, altura_botao = largura_tela * 0.4, altura_tela * 0.1
        pos_x_central = (largura_tela - largura_botao) / 2

        self.adicionar_botao(Button(x=pos_x_central, y=altura_tela * 0.25, w=largura_botao, h=altura_botao,
                                   texto="HABITAT 1", cor=(50,150,200), cor_hover=(100,200,255),
                                   acao=lambda: setattr(game, "cena_atual", game.fase1)))
        self.adicionar_botao(Button(x=pos_x_central, y=altura_tela * 0.4, w=largura_botao, h=altura_botao,
                                   texto="HABITAT 2", cor=(50,150,200), cor_hover=(100,200,255),
                                   acao=lambda: setattr(game, "cena_atual", game.fase2)))
        self.adicionar_botao(Button(x=pos_x_central, y=altura_tela * 0.55, w=largura_botao, h=altura_botao,
                                   texto="HABITAT 3", cor=(50,150,200), cor_hover=(100,200,255),
                                   acao=lambda: setattr(game, "cena_atual", game.fase3)))
        # Botão de voltar
        self.adicionar_botao(Button(x=30, y=30, imagem_surface=py.transform.scale(py.image.load("source/seta_voltar.png").convert_alpha(), (50, 50)), acao=lambda: setattr(game, "cena_atual", game.menu)))

    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("Selecione o seu Habitat", True, (10,10,10))
        tela.blit(txt, (30, 70))

# Cenas de Fases do Jogo
# -----------------------------------------------------------------------------
# elas herdam de FaseEditavel para permitir edição

class Fase1(FaseEditavel):
    """A primeira fase do jogo."""
    def __init__(self, game):
        super().__init__(game, (217, 214, 71))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("FASE 01", True, (10,10,10))
        tela.blit(txt, (350, 250))

class Fase2(FaseEditavel):
    """A segunda fase do jogo."""
    def __init__(self, game):
        super().__init__(game, (137, 230, 227))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("FASE 02", True, (10,10,10))
        tela.blit(txt, (350, 250))

class Fase3(FaseEditavel):
    """A terceira fase do jogo."""
    def __init__(self, game):
        super().__init__(game, (0, 18, 64))
    def drawn(self, tela):
        super().drawn(tela)
        txt = fonte.render("FASE 03", True, (10,10,10))
        tela.blit(txt, (350, 250))