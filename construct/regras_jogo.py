import pygame as py
import json

from .global_instances import fonte

class Popup:
    """Uma janela de popup para exibir informações no final do jogo."""
    def __init__(self, game, titulo, linhas_texto):
        from .scenes import Button  # Importa aqui para evitar dependência circular
        largura_tela, altura_tela = game.tela.get_size()
        self.largura = 600
        self.altura = 350
        self.rect = py.Rect((largura_tela - self.largura) // 2, (altura_tela - self.altura) // 2, self.largura, self.altura)
        
        self.titulo = titulo
        self.linhas_texto = linhas_texto
        
        # Botão para voltar ao menu
        self.botao_menu = Button(x=self.rect.centerx - 75, y=self.rect.bottom - 70, w=150, h=50,
                                 texto="Menu", cor=(100, 100, 200), cor_hover=(150, 150, 255),
                                 acao=lambda: setattr(game, "cena_atual", game.menu))

    def handle_event(self, evento):
        if evento.type == py.MOUSEBUTTONUP and evento.button == 1:
            self.botao_menu.click(evento.pos)

    def desenhar(self, tela):
        # 1. Fundo semi-transparente sobre o jogo todo
        overlay = py.Surface(tela.get_size(), py.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))
        
        # 2. A "caixinha bonitinha" de fundo do popup
        py.draw.rect(tela, (20, 30, 50), self.rect, border_radius=15)
        py.draw.rect(tela, (100, 120, 150), self.rect, 3, border_radius=15)

        # 3. Título
        txt_titulo = fonte.render(self.titulo, True, (255, 223, 0))
        tela.blit(txt_titulo, (self.rect.centerx - txt_titulo.get_width() // 2, self.rect.top + 20))

        # 4. Corpo do texto com layout dinâmico
        linha_resultado = self.linhas_texto[-1]
        linhas_info = self.linhas_texto[:-1]

        y_pos = self.rect.top + 80
        padding_linha = 5

        for linha in linhas_info:
            txt_surf = fonte.render(linha, True, (255, 255, 255))
            tela.blit(txt_surf, (self.rect.left + 30, y_pos))
            y_pos += txt_surf.get_height() + padding_linha

        cor_resultado = (100, 255, 100) if "Atingida" in linha_resultado else (255, 100, 100)
        txt_resultado_surf = fonte.render(linha_resultado, True, cor_resultado)
        pos_resultado_y = y_pos + 5
        tela.blit(txt_resultado_surf, (self.rect.centerx - txt_resultado_surf.get_width() // 2, pos_resultado_y))
        
        # 5. Botão "Menu"
        self.botao_menu.desenhar(tela, py.mouse.get_pos())

class GameManager:
    """Controla o tempo, volume e o estado da fase de edição."""
    ESTADO_EDITANDO = 'EDITANDO'
    ESTADO_FINALIZADO = 'FINALIZADO'
    
    def __init__(self, fase_editavel, config_jogo):
        self.fase = fase_editavel
        self.game = fase_editavel.game
        self.config = config_jogo
        
        self.estado = self.ESTADO_EDITANDO
        self.popup = None
        
        self.tempo_total = 60  # 60 segundos
        self.tempo_inicio = py.time.get_ticks()
        
        self.volume_total_habitat = self.config['volume']
        self.volume_ocupado = 0

    def update(self, eventos):
        if self.estado == self.ESTADO_EDITANDO:
            self.recalcular_volume()
            
            tempo_decorrido = (py.time.get_ticks() - self.tempo_inicio) / 1000
            if tempo_decorrido >= self.tempo_total:
                self.finalizar_jogo()
        
        elif self.estado == self.ESTADO_FINALIZADO and self.popup:
            for e in eventos:
                self.popup.handle_event(e)

    def desenhar_hud(self, tela):
        # Timer
        tempo_restante = self.tempo_total - (py.time.get_ticks() - self.tempo_inicio) / 1000
        if tempo_restante < 0:
            tempo_restante = 0
        texto_timer = f"Tempo: {int(tempo_restante // 60):02}:{int(tempo_restante % 60):02}"
        surf_timer = fonte.render(texto_timer, True, (255, 255, 255))
        tela.blit(surf_timer, (tela.get_width() - surf_timer.get_width() - 20, 20))

        # Volume
        texto_volume = f"Volume: {self.volume_ocupado} / {self.volume_total_habitat} m³"
        surf_volume = fonte.render(texto_volume, True, (255, 255, 255))
        tela.blit(surf_volume, (tela.get_width() - surf_volume.get_width() - 20, 50))
        
        # Desenha o popup se o jogo tiver acabado
        if self.estado == self.ESTADO_FINALIZADO and self.popup:
            self.popup.desenhar(tela)

    def recalcular_volume(self):
        self.volume_ocupado = sum(obj.volume for obj in self.fase.objetos_do_cenario)

    def finalizar_jogo(self):
        if self.estado != self.ESTADO_FINALIZADO:
            self.estado = self.ESTADO_FINALIZADO
            print("Tempo esgotado! Finalizando o jogo.")
            
            # --- Monta o resultado e salva em JSON ---
            itens_colocados = [obj.nome for obj in self.fase.objetos_do_cenario]
            
            # Define uma meta de volume, por exemplo, 80% da capacidade
            meta_volume = self.volume_total_habitat * 0.8
            cumpriu_meta = self.volume_ocupado >= meta_volume
            
            resultado = {
                "configuracao_inicial": self.config,
                "resultado_final": {
                    "volume_ocupado": self.volume_ocupado,
                    "cumpriu_meta_de_volume": cumpriu_meta,
                    "itens_colocados": itens_colocados
                }
            }
            
            with open("resultado_jogo.json", "w") as f:
                json.dump(resultado, f, indent=4)
            print(f"Resultado salvo em resultado_jogo.json")
            
            # --- Prepara o texto para o Popup ---
            titulo_popup = "Tempo Esgotado!"
            resultado_str = "Meta Atingida!" if cumpriu_meta else "Meta não atingida."

            linhas_popup = [
                f"Nome: {self.config['nome']}",
                f"Habitat: {self.config['habitat_idx']}",
                f"Volume Ocupado: {self.volume_ocupado} / {self.volume_total_habitat} m³",
                "", # Linha vazia para espaçamento
                resultado_str # Apenas o resultado, para darmos um tratamento especial
            ] 
            
            self.popup = Popup(self.game, titulo_popup, linhas_popup)