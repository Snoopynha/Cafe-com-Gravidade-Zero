# construct/scenes.py

import pygame as py 
import json
from sys import exit
from construct.global_instances import *
from construct.game_object import *
from .regras_jogo import GameManager

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
    def desenhar(self, tela, fonte, sufixo_texto=""):
        py.draw.rect(tela, (100, 100, 100), self.rect, border_radius=5)
        py.draw.rect(tela, (200, 200, 200), self.knob_rect, border_radius=8)
        texto_val = fonte.render(f"{int(self.valor)}{sufixo_texto}", True, (255, 255, 255))
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

class ObjetoColocavel:
    def __init__(self, dados_objeto):
        """
        Inicializa o objeto com base nos dados carregados pela FaseEditavel.
        
        Args:
            dados_objeto (dict): Um dicionário contendo o tipo de rotação e as imagens originais.
        """
        self.tipo_rotacao = dados_objeto['tipo_rotacao']
        self.imagens_originais = dados_objeto['imagens']
        self.rotacao_atual = 0  # 0: Cima, 90: Esquerda, 180: Baixo, 270: Direita
        # Define a imagem inicial e o rect
        self.imagem = self.imagens_originais['frente']
        self.rect = self.imagem.get_rect()

    def rotacionar(self, nova_rotacao):
        """
        Atualiza a rotação do objeto e sua imagem correspondente.
        Sempre rotaciona a partir da imagem original para evitar perda de qualidade.
        """
        self.rotacao_atual = nova_rotacao
        
        if self.tipo_rotacao == 'transform':
            # Gira a imagem base usando a transformação do Pygame
            self.imagem = py.transform.rotate(self.imagens_originais['frente'], self.rotacao_atual)
        
        elif self.tipo_rotacao == 'swap':
            # Troca a imagem com base na direção (e inverte se necessário)
            if self.rotacao_atual == 0: # Cima
                self.imagem = self.imagens_originais['frente']
            elif self.rotacao_atual == 180: # Baixo (inverte a imagem da frente)
                self.imagem = py.transform.flip(self.imagens_originais['frente'], False, True)
            elif self.rotacao_atual == 270: # Direita
                self.imagem = self.imagens_originais['lado']
            elif self.rotacao_atual == 90: # Esquerda (inverte a imagem de lado)
                self.imagem = py.transform.flip(self.imagens_originais['lado'], True, False)

        # Atualiza o rect para o novo tamanho da imagem rotacionada
        self.rect = self.imagem.get_rect(center=self.rect.center)

    def draw(self, tela):
        """Desenha o objeto na tela."""
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
        try:
            with open("config_jogo.json", "r") as f:
                config_dados = json.load(f)
        except FileNotFoundError:
            print("AVISO: config_jogo.json não encontrado. Usando valores padrão.")
            config_dados = {"nome": "Padrão", "habitat_idx": "BUTIJAO", "volume": 1000}
            
        # 2. Cria e inicia o GameManager
        self.game_manager = GameManager(self, config_dados)

        dados_base_itens = { 
            "airlock": { "img_path": "source/itens/airlock_e_suitports.png", "tamanho": (6, 2), "anim_path": None, "nome": "Airlock", "volume": self.calcular_volume((6,2)) },
            "armario_comida": { "img_path": "source/itens/armario_comida.png", "tamanho": (2, 2), "anim_path": None, "nome": "Armário de Comida", "volume": self.calcular_volume((2,2)) },
            "armario_pessoal": { "img_path": "source/itens/armario_pessoal.png", "tamanho": (2, 2), "anim_path": None, "nome": "Armário Pessoal", "volume": self.calcular_volume((2,2)) },
            "cama_capsula": { "img_path": "source/itens/cama_capsula.png", "tamanho": (2, 3), "anim_path": None, "nome": "Cama", "volume": self.calcular_volume((2,3)) },
            "central_computador_EVA": { "img_path": "source/itens/central_computador_EVA.png", "tamanho": (1, 1), "anim_path": None, "nome": "Central de Computador EVA", "volume": self.calcular_volume((1,1)) },
            "eclss": { "img_path": "source/itens/eclss.png", "tamanho": (2, 2), "anim_path": None, "nome": "ECLSS", "volume": self.calcular_volume((2,2)) },
            "equipamento_exercicio": { "img_path": "source/itens/equipamento_exercicio.png", "tamanho": (1, 1), "anim_path": None, "nome": "Equipamento de Exercício", "volume": self.calcular_volume((1,1)) },
            "estacao_pc": { "img_path": "source/itens/estacao_pc.png", "tamanho": (2, 2), "anim_path": None, "nome": "Estação de PC", "volume": self.calcular_volume((2,2)) },
            "laboratorio": { "img_path": "source/itens/laboratorio.png", "tamanho": (3, 2), "anim_path": None, "nome": "Laboratório", "volume": self.calcular_volume((3,2)) },
            "mesa" : { "img_path": "source/itens/mesa.png", "tamanho": (2, 2), "anim_path": None, "nome": "Mesa", "volume": self.calcular_volume((2,2)) },
            "painel_de_controle": { "img_path": "source/itens/painel_de_controle.png", "tamanho": (4, 2), "anim_path": None, "nome": "Painel de Controle", "volume": self.calcular_volume((4,2)) },
            "pia": { "img_path": "source/itens/pia.png", "tamanho": (1, 1), "anim_path": None, "nome": "Pia", "volume": self.calcular_volume((1,1)) },
            "porta": { "img_path": "source/itens/porta.png", "tamanho": (1, 2), "anim_path": None, "nome": "Porta", "volume": self.calcular_volume((1,2)) },
            "privada": { "img_path": "source/itens/privada.png", "tamanho": (1, 1), "anim_path": None, "nome": "Privada", "volume": self.calcular_volume((1,1)) },
            "rack_ISPR": { "img_path": "source/itens/rack_ISPR.png", "tamanho": (2, 2), "anim_path": None, "nome": "Rack ISPR", "volume": self.calcular_volume((2,2)) },
            "workbench_e_kit_ferramentas": { "img_path": "source/itens/workbench_e_kit_ferramentas_EVA.png", "tamanho": (1, 1), "anim_path": None, "nome": "Workbench e Kit de Ferramentas", "volume": self.calcular_volume((1,1)) },
            "zona_pre_EVA": { "img_path": "source/itens/zona_pre_EVA.png", "tamanho": (3, 2), "anim_path": None, "nome": "Zona Pré-EVA", "volume": self.calcular_volume((3,2)) },
            "cama_hospitalar": { "img_path": "source/itens/cama_hospitalar.png", "tamanho": (2, 3), "anim_path": None, "nome": "Cama Hospitalar", "volume": self.calcular_volume((2,3)) },
            "monitor" : { "img_path": "source/itens/monitor.png", "tamanho": (1, 1), "anim_path": None, "nome": "Monitor", "volume": self.calcular_volume((1,1)) },
            "duto" : { "img_path": "source/itens/duto.png", "tamanho": (1, 1), "anim_path": None, "nome": "Duto", "volume": self.calcular_volume((1,1)) },
            "duto_ventilador": { "img_path": "source/itens/duto_ventilador.png", "tamanho": (1, 1), "anim_path": None, "nome": "Duto Ventilador", "volume": self.calcular_volume((1,1)) }
        }
        self.itens_disponiveis = {}
        # Lista dos nomes base dos seus itens (sem a extensão .png)
    
        for nome_item, info in dados_base_itens.items():
            dados_finais = info.copy()
            caminho_base = info['img_path']
            caminho_lado = caminho_base.replace(".png", "_lado.png")

            # 1. Pega o tamanho em blocos (ex: (2, 3)) do dicionário
            grid_w, grid_h = info['tamanho']

            # 2. Calcula o tamanho real em pixels
            pixel_w = grid_w * self.GRID_SIZE
            pixel_h = grid_h * self.GRID_SIZE
        
            # 3. Usa o tamanho em pixels correto para redimensionar a imagem de FRENTE
            try:
                imagem_original_frente = py.image.load(caminho_base).convert_alpha()
                img_frente = py.transform.scale(imagem_original_frente, (pixel_w, pixel_h))
            except FileNotFoundError:
                print(f"AVISO: Imagem não encontrada: {caminho_base}. Criando placeholder.")
                img_frente = py.Surface((pixel_w, pixel_h)); img_frente.fill((255,0,255))
        
            # Adiciona a imagem de frente já carregada (isso não estava no Game_Obj antes, mas é uma boa prática)
            dados_finais['imagens_precarregadas'] = {"frente": img_frente}

            # Verifica se a imagem de lado existe e a redimensiona com o tamanho correto
            if os.path.exists(caminho_lado):
                dados_finais["tipo_rotacao"] = "swap"
             
                # 4. Usa o tamanho em pixels correto para redimensionar a imagem de LADO
                imagem_original_lado = py.image.load(caminho_lado).convert_alpha()
                # NOTA: A imagem de lado pode ter proporções invertidas (ex: 3x2 em vez de 2x3)
                # Para simplificar, vamos assumir que ela tem o mesmo tamanho de grid.
                # Se a proporção for diferente, a lógica aqui precisaria ser mais complexa.
                img_lado = py.transform.scale(imagem_original_lado, (pixel_w, pixel_h))
                dados_finais['imagens_precarregadas']['lado'] = img_lado
            else:
                dados_finais["tipo_rotacao"] = "transform"

            dados_finais['volume'] = self.calcular_volume(info['tamanho'])
            self.itens_disponiveis[nome_item] = dados_finais

        self.posicao_valida = False
        self.botoes_inventario = []
        self.INVENTARIO_RECT = py.Rect(100, 100, LARGURA - 200, ALTURA - 200)

    @staticmethod
    def calcular_volume(tamanho, constante_por_bloco=10):
        """
        Calcula o volume de um item com base em seu tamanho em blocos.
    
        Args: 
            tamanho (tuple): Uma tupla (largura, altura) representando o tamanho em blocos.
            constante_por_bloco (int): O volume que cada bloco representa. Padrão é 10.
        """
        largura, altura = tamanho
        volume = largura * altura * constante_por_bloco
        return int(volume)
    
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
        self.game_manager.update(eventos)

        if self.game_manager.estado == GameManager.ESTADO_EDITANDO:
            mouse_x, mouse_y = py.mouse.get_pos()
            
            for e in eventos:
                if e.type == py.KEYDOWN:
                    if self.estado == self.ESTADO_POSICIONANDO and self.objeto_em_mao:
                        if e.key == py.K_w: # Rotaciona para Cima (0 graus)
                            self.objeto_em_mao.rotacionar(0)
                        elif e.key == py.K_d: # Rotaciona para Direita (270 graus)
                            self.objeto_em_mao.rotacionar(270)
                        elif e.key == py.K_s: # Rotaciona para Baixo (180 graus)
                            self.objeto_em_mao.rotacionar(180)
                        elif e.key == py.K_a: # Rotaciona para Esquerda (90 graus)
                            self.objeto_em_mao.rotacionar(90)

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
                                info_completa = self.itens_disponiveis[botao.item_key]
            
                                # Cria a instância da nova Game_Obj passando o dicionário completo
                                self.objeto_em_mao = Game_Obj(info_completa) 
                                self.objeto_em_mao.image.set_alpha(150) # Deixa transparente
                                self.objeto_em_mao.item_key = botao.item_key
                                break

                elif self.estado == self.ESTADO_POSICIONANDO:
                    if e.type == py.KEYDOWN and e.key == py.K_ESCAPE:
                        self.estado = self.ESTADO_NORMAL
                        self.objeto_em_mao = None
                    elif e.type == py.MOUSEBUTTONDOWN and e.button == 1 and self.objeto_em_mao and self.posicao_valida:
                        info = self.itens_disponiveis[self.objeto_em_mao.item_key]
                        x, y = self.objeto_em_mao.rect.topleft

                        # Cria o objeto final que será colocado no cenário
                        novo_objeto = Game_Obj(info, x=x, y=y)
                        novo_objeto.rotacionar(self.objeto_em_mao.rotacao_atual) # Aplica a rotação final
    
                        self.objetos_do_cenario.append(novo_objeto)

                        grid_x, grid_y = x // self.GRID_SIZE, y // self.GRID_SIZE
                        obj_w, obj_h = info["tamanho"]
                        for row in range(grid_y, grid_y + obj_h):
                            for col in range(grid_x, grid_x + obj_w):
                                self.mapa_da_grade[row][col] = 1
                        self.estado = self.ESTADO_NORMAL
                        self.objeto_em_mao = None
            pass
            
            if self.estado == self.ESTADO_POSICIONANDO and self.objeto_em_mao:
                snap_x = (mouse_x // self.GRID_SIZE) * self.GRID_SIZE
                snap_y = (mouse_y // self.GRID_SIZE) * self.GRID_SIZE
                self.objeto_em_mao.rect.topleft = (snap_x, snap_y)
                grid_x, grid_y = snap_x // self.GRID_SIZE, snap_y // self.GRID_SIZE
                self.posicao_valida = self.pode_colocar_aqui(grid_x, grid_y, self.objeto_em_mao.tamanho_grid)
            pass

    def reset(self):
        """Reseta a fase para seu estado inicial para um novo jogo."""
        print("Resetando a fase...")
        # Limpa os objetos colocados
        self.objetos_do_cenario = []
        # Limpa o mapa da grade
        self.mapa_da_grade = [[0 for _ in range(GRID_LARGURA)] for _ in range(GRID_ALTURA)]
        # Reseta o estado inicial e o objeto na mão
        self.estado = self.ESTADO_NORMAL
        self.objeto_em_mao = None
        
        # Recria o GameManager do zero
        try:
            with open("config_jogo.json", "r") as f:
                config_dados = json.load(f)
        except FileNotFoundError:
            config_dados = {"nome": "Padrão", "habitat_idx": "BUTIJAO", "volume": 1000}
            
        self.game_manager = GameManager(self, config_dados)

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
        self.game_manager.desenhar_hud(tela)

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
        VOLUME_HABITAT_MINIMO = 500
        VOLUME_HABITAT_MAXIMO = 3000
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
        self.slider_volume = Slider(largura_tela * 0.2, altura_tela * 0.6, 300, 10, 
                                    min_val=VOLUME_HABITAT_MINIMO, 
                                    max_val=VOLUME_HABITAT_MAXIMO, 
                                    val_inicial=VOLUME_HABITAT_MINIMO)
        self.adicionar_botao(Button(x=largura_tela * 0.2, y=altura_tela * 0.8, w=150, h=50,
                                   texto="Iniciar", cor=(50,205,50), cor_hover=(0,255,0),
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
        proxima_fase = self.habitats_disponiveis[self.habitat_selecionado]
        # CHAMA O NOVO MÉTODO RESET NELA!
        proxima_fase.reset()
        # Agora sim, define como a cena atual
        self.game.cena_atual = proxima_fase

        if self.habitat_selecionado == 0:
            self.inf = "BUTIJAO"
        if self.habitat_selecionado == 1:
            self.inf = "CIRCULAR"
        if self.habitat_selecionado == 2:
            self.inf = "PILULA"
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
        self.slider_volume.desenhar(tela, self.fonte_form, sufixo_texto=" m³")
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
        super().__init__(game, image_path="source/habitat_2_preview.png")
    def drawn(self, tela):
        super().drawn(tela)

class Fase3(FaseEditavel):
    def __init__(self, game):
        super().__init__(game, image_path="source/habitat_3_preview.png")
    def drawn(self, tela):
        super().drawn(tela)