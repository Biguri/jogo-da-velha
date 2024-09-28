import pygame
import sys
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 400, 400
LARGURA_LINHA = 5
LARGURA_LINHA_VITORIA = 15
LINHAS_TABULEIRO = 3
COLUNAS_TABULEIRO = 3
TAMANHO_QUADRADO = LARGURA // COLUNAS_TABULEIRO
RAIO_CIRCULO = TAMANHO_QUADRADO // 3
LARGURA_CIRCULO = 15
LARGURA_X = 25
ESPACO = TAMANHO_QUADRADO // 4

# Cores
COR_FUNDO = (28, 170, 156)
COR_LINHA = (23, 145, 135)
COR_CIRCULO = (239, 231, 200)
COR_X = (84, 84, 84)
COR_VITORIA = (255, 0, 0)  # Cor para destacar a vitória

# Tela de exibição
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha')


class Jogo:
    def __init__(self, modo='PvP', dificuldade='dificil'):
        self.tabuleiro = Tabuleiro()
        # Define o jogador atual (1 ou 2)
        self.jogador = 1
        # Indica se o jogo acabou
        self.jogo_acabou = False
        # Define o modo de jogo ('PvP' para jogador vs jogador, 'IA' para jogar contra a IA)
        self.modo = modo
        # Define a dificuldade da IA ('facil' ou 'dificil')
        self.dificuldade = dificuldade

    def rodar(self):
        self.tabuleiro.desenhar_linhas()

        # Loop principal do jogo
        while True:
            # Captura eventos do Pygame (como cliques do mouse, teclas pressionadas, etc.)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Se o jogador fechar a janela, encerra o jogo
                    pygame.quit()
                    sys.exit()

                # Se o jogo não acabou
                if not self.jogo_acabou:
                    # Se for modo PvP ou se for a vez do jogador humano no modo IA
                    if self.modo == 'PvP' or (self.modo == 'IA' and self.jogador == 1):
                        if evento.type == pygame.MOUSEBUTTONDOWN:
                            # Obtém as coordenadas do clique do mouse
                            mouseX = evento.pos[0]
                            mouseY = evento.pos[1]

                            # Calcula em qual linha e coluna o jogador clicou
                            linha = mouseY // TAMANHO_QUADRADO
                            coluna = mouseX // TAMANHO_QUADRADO

                            # Verifica se o quadrado está disponível
                            if self.tabuleiro.quadrado_disponivel(linha, coluna):
                                # Marca o quadrado para o jogador atual
                                self.tabuleiro.marcar_quadrado(linha, coluna, self.jogador)
                                # Verifica se o jogador atual venceu o jogo
                                if self.tabuleiro.verificar_vitoria(self.jogador):
                                    self.jogo_acabou = True
                                    # Destaca a linha de vitória
                                    self.tabuleiro.destacar_linha_vitoria(self.jogador)
                                # Alterna para o outro jogador (1 se for 2, 2 se for 1)
                                self.jogador = 3 - self.jogador
                                # Atualiza as figuras desenhadas no tabuleiro
                                self.tabuleiro.desenhar_figuras()

                    # Se for a vez da IA no modo 'IA'
                    elif self.modo == 'IA' and self.jogador == 2:
                        # Realiza a jogada da IA
                        self.jogada_ia()
                        # Atualiza as figuras desenhadas no tabuleiro
                        self.tabuleiro.desenhar_figuras()

                # Se uma tecla for pressionada
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        # Reinicia o jogo se a tecla 'R' for pressionada
                        self.reiniciar()

            # Atualiza a tela com as mudanças
            pygame.display.update()

    def jogada_ia(self):
        if self.dificuldade == 'facil':
            # Tenta bloquear a vitória do jogador humano
            bloqueou = False
            for linha in range(LINHAS_TABULEIRO):
                for coluna in range(COLUNAS_TABULEIRO):
                    if self.tabuleiro.quadrado_disponivel(linha, coluna):
                        # Simula uma jogada do jogador humano
                        self.tabuleiro.marcar_quadrado(linha, coluna, 1)
                        if self.tabuleiro.verificar_vitoria(1):
                            # Se o jogador humano venceria com essa jogada, a IA bloqueia
                            self.tabuleiro.marcar_quadrado(linha, coluna, 2)
                            bloqueou = True
                            print(f"IA bloqueou a jogada do jogador na posição ({linha}, {coluna})")
                            break
                        # Desfaz a simulação
                        self.tabuleiro.marcar_quadrado(linha, coluna, 0)
                if bloqueou:
                    break

            if not bloqueou:
                # Se não precisou bloquear, a IA escolhe uma posição preferencial
                # Ordem de preferência: Centro > Cantos > Laterais
                for (linha, coluna) in [
                    (1, 1),  # Centro
                    (0, 0), (0, 2), (2, 0), (2, 2),  # Cantos
                    (0, 1), (1, 0), (1, 2), (2, 1)  # Laterais
                ]:
                    if self.tabuleiro.quadrado_disponivel(linha, coluna):
                        # Marca o quadrado para a IA
                        self.tabuleiro.marcar_quadrado(linha, coluna, 2)
                        print(f"IA escolheu a jogada na posição preferencial ({linha}, {coluna})")
                        break

        else:
            # Se a dificuldade for 'dificil', utiliza o algoritmo Minimax
            _, jogada = self.minimax(self.tabuleiro, 2, True, -float('inf'), float('inf'))
            if jogada:
                linha, coluna = jogada
                # Marca o melhor movimento encontrado
                self.tabuleiro.marcar_quadrado(linha, coluna, 2)
                print(f"IA escolheu a jogada minimax na posição ({linha}, {coluna})")
            else:
                # Se não houver jogadas válidas, declara empate
                self.jogo_acabou = True
                return

        # Verifica se a IA venceu após sua jogada
        if self.tabuleiro.verificar_vitoria(2):
            self.jogo_acabou = True
            # Destaca a linha de vitória
            self.tabuleiro.destacar_linha_vitoria(2)
        elif self.tabuleiro.tabuleiro_cheio():
            # Se o tabuleiro estiver cheio e ninguém venceu, é empate
            self.jogo_acabou = True
            print("Empate: Tabuleiro cheio")
        else:
            # Alterna para o jogador humano
            self.jogador = 1

    def minimax(self, tabuleiro, jogador, maximizando, alfa, beta):
        # Verifica se há uma vitória para o jogador 2 (IA)
        if tabuleiro.verificar_vitoria(2):
            return 1, None  # Retorna uma pontuação positiva se a IA venceu
        # Verifica se há uma vitória para o jogador 1 (humano)
        elif tabuleiro.verificar_vitoria(1):
            return -1, None  # Retorna uma pontuação negativa se o humano venceu
        # Verifica se o tabuleiro está cheio (empate)
        elif tabuleiro.tabuleiro_cheio():
            return 0, None  # Retorna zero em caso de empate
        # Se for o turno do jogador maximizador (IA)
        if maximizando:
            max_avaliacao = -float('inf')  # Inicializa com o pior caso para maximização
            melhor_jogada = None
            # Percorre todas as posições do tabuleiro
            for linha in range(LINHAS_TABULEIRO):
                for coluna in range(COLUNAS_TABULEIRO):
                    if tabuleiro.quadrado_disponivel(linha, coluna):
                        # Faz uma jogada teste
                        tabuleiro.marcar_quadrado(linha, coluna, jogador)
                        # Chama recursivamente o minimax para o jogador oponente
                        avaliacao, _ = self.minimax(tabuleiro, 3 - jogador, False, alfa, beta)
                        # Desfaz a jogada
                        tabuleiro.marcar_quadrado(linha, coluna, 0)  # Desfaz a jogada
                        # Atualiza a melhor avaliação e jogada se necessário
                        if avaliacao > max_avaliacao:
                            max_avaliacao = avaliacao
                            melhor_jogada = (linha, coluna)
                        # Atualiza o alfa para a poda alfa-beta
                        alfa = max(alfa, avaliacao)
                        if beta <= alfa:
                            # Poda a árvore de possibilidades
                            break
            return max_avaliacao, melhor_jogada
        else:
            # Turno do jogador minimizador (humano)
            min_avaliacao = float('inf')  # Inicializa com o pior caso para minimização
            melhor_jogada = None
            # Percorre todas as posições do tabuleiro
            for linha in range(LINHAS_TABULEIRO):
                for coluna in range(COLUNAS_TABULEIRO):
                    if tabuleiro.quadrado_disponivel(linha, coluna):
                        # Faz uma jogada hipotética
                        tabuleiro.marcar_quadrado(linha, coluna, jogador)
                        # Chama recursivamente o minimax para o jogador oponente
                        avaliacao, _ = self.minimax(tabuleiro, 3 - jogador, True, alfa, beta)
                        # Desfaz a jogada
                        tabuleiro.marcar_quadrado(linha, coluna, 0)
                        # Atualiza a melhor avaliação e jogada se necessário
                        if avaliacao < min_avaliacao:
                            min_avaliacao = avaliacao
                            melhor_jogada = (linha, coluna)
                        # Atualiza o beta para a poda alfa-beta
                        beta = min(beta, avaliacao)
                        if beta <= alfa:
                            break  # Poda a árvore de possibilidades
            return min_avaliacao, melhor_jogada

    def reiniciar(self):
        # Limpa a tela com a cor de fundo
        tela.fill(COR_FUNDO)
        # Reinicia o tabuleiro
        self.tabuleiro.reiniciar()
        # Desenha as linhas do tabuleiro
        self.tabuleiro.desenhar_linhas()
        # Reseta o estado do jogo
        self.jogo_acabou = False
        self.jogador = 1  # Define o jogador inicial


class Tabuleiro:
    def __init__(self):
        # Cria uma matriz 3x3 para representar o tabuleiro, inicializando com zeros
        self.quadrados = [[0 for _ in range(COLUNAS_TABULEIRO)] for _ in range(LINHAS_TABULEIRO)]
        # Armazena a linha vencedora para destaque
        self.linha_destacada = None

    def desenhar_linhas(self):
        # Preenche a tela com a cor de fundo
        tela.fill(COR_FUNDO)
        # Desenha as linhas horizontais
        for linha in range(1, LINHAS_TABULEIRO):
            pygame.draw.line(tela, COR_LINHA, (0, TAMANHO_QUADRADO * linha), (LARGURA, TAMANHO_QUADRADO * linha), LARGURA_LINHA)
        # Desenha as linhas verticais
        for coluna in range(1, COLUNAS_TABULEIRO):
            pygame.draw.line(tela, COR_LINHA, (TAMANHO_QUADRADO * coluna, 0), (TAMANHO_QUADRADO * coluna, ALTURA), LARGURA_LINHA)

    def desenhar_figuras(self):
        # Percorre o tabuleiro para desenhar as figuras
        for linha in range(LINHAS_TABULEIRO):
            for coluna in range(COLUNAS_TABULEIRO):
                if self.quadrados[linha][coluna] == 1:
                    # Desenha um círculo para o jogador 1
                    pygame.draw.circle(
                        tela, COR_CIRCULO,
                        (int(coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2),
                         int(linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2)),
                        RAIO_CIRCULO, LARGURA_CIRCULO) # Coordenadas do centro do círculo
                elif self.quadrados[linha][coluna] == 2:
                    # Desenha um "X" para o jogador 2
                    pygame.draw.line(
                        tela, COR_X,
                        (coluna * TAMANHO_QUADRADO + ESPACO, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO - ESPACO),# Ponto inicial
                        (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO - ESPACO, linha * TAMANHO_QUADRADO + ESPACO),# Ponto final
                        LARGURA_X)
                    pygame.draw.line(
                        tela, COR_X,
                        (coluna * TAMANHO_QUADRADO + ESPACO, linha * TAMANHO_QUADRADO + ESPACO),
                        (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO - ESPACO, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO - ESPACO),
                        LARGURA_X)

    def marcar_quadrado(self, linha, coluna, jogador):
        # Marca o quadrado com o número do jogador (1 ou 2)
        self.quadrados[linha][coluna] = jogador

    def quadrado_disponivel(self, linha, coluna):
        # Verifica se o quadrado está vazio (valor zero)
        return self.quadrados[linha][coluna] == 0

    def tabuleiro_cheio(self):
        # Verifica se todos os quadrados estão preenchidos
        for linha in self.quadrados:
            if 0 in linha:
                return False  # Ainda há espaços disponíveis
        return True  # Todos os quadrados estão preenchidos

    def verificar_vitoria(self, jogador):
        # Verifica as linhas para uma vitória
        for linha in range(LINHAS_TABULEIRO):
            if self.quadrados[linha][0] == self.quadrados[linha][1] == self.quadrados[linha][2] == jogador:
                self.linha_destacada = ('linha', linha)
                return True
        # Verifica as colunas para uma vitória
        for coluna in range(COLUNAS_TABULEIRO):
            if self.quadrados[0][coluna] == self.quadrados[1][coluna] == self.quadrados[2][coluna] == jogador:
                self.linha_destacada = ('coluna', coluna)
                return True
        # Verifica a diagonal principal
        if self.quadrados[0][0] == self.quadrados[1][1] == self.quadrados[2][2] == jogador:
            self.linha_destacada = ('diagonal1', 0)
            return True
        # Verifica a diagonal secundária
        if self.quadrados[2][0] == self.quadrados[1][1] == self.quadrados[0][2] == jogador:
            self.linha_destacada = ('diagonal2', 0)
            return True
        # Se não houve vitória
        return False

    def destacar_linha_vitoria(self, jogador):
        # Destaca a linha, coluna ou diagonal vencedora
        if self.linha_destacada:
            if self.linha_destacada[0] == 'linha':
                linha = self.linha_destacada[1]
                posY = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                # Desenha uma linha horizontal para destacar a vitória
                pygame.draw.line(tela, COR_VITORIA, (15, posY), (LARGURA - 15, posY), LARGURA_LINHA_VITORIA)
            elif self.linha_destacada[0] == 'coluna':
                coluna = self.linha_destacada[1]
                posX = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                # Desenha uma linha vertical para destacar a vitória
                pygame.draw.line(tela, COR_VITORIA, (posX, 15), (posX, ALTURA - 15), LARGURA_LINHA_VITORIA)
            elif self.linha_destacada[0] == 'diagonal1':
                # Desenha uma linha na diagonal principal
                pygame.draw.line(tela, COR_VITORIA, (15, 15), (LARGURA - 15, ALTURA - 15), LARGURA_LINHA_VITORIA)
            elif self.linha_destacada[0] == 'diagonal2':
                # Desenha uma linha na diagonal secundária
                pygame.draw.line(tela, COR_VITORIA, (15, ALTURA - 15), (LARGURA - 15, 15), LARGURA_LINHA_VITORIA)

    def reiniciar(self):
        # Reinicia o tabuleiro para o estado inicial
        self.quadrados = [[0 for _ in range(COLUNAS_TABULEIRO)] for _ in range(LINHAS_TABULEIRO)]
        self.linha_destacada = None


class Menu:
    def __init__(self):
        self.rodando = True  # Controle do loop do menu

    def exibir_menu(self):
        # Loop do menu principal
        while self.rodando:
            # Preenche a tela com a cor de fundo
            tela.fill(COR_FUNDO)
            # Desenha as opções do menu
            self.desenhar_opcoes_menu()
            # Atualiza a tela
            pygame.display.update()

            # Captura eventos do Pygame
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica se o jogador clicou em "2 Jogadores"
                    if self.verificar_clique(evento.pos, (50, 100, 200, 50)):
                        self.iniciar_jogo('PvP')
                    # Verifica se o jogador clicou em "Contra IA"
                    elif self.verificar_clique(evento.pos, (50, 200, 200, 50)):
                        self.exibir_menu_dificuldade()

    def desenhar_opcoes_menu(self):
        # Define a fonte e renderiza o título
        fonte = pygame.font.Font(None, 74)
        texto = fonte.render("Jogo da Velha", True, (255, 255, 255))
        tela.blit(texto, (30, 30))
        # Desenha os botões do menu
        self.desenhar_botao((50, 100, 200, 50), "2 Jogadores")
        self.desenhar_botao((50, 200, 200, 50), "Contra IA")

    def desenhar_botao(self, rect, texto):
        # Desenha um retângulo para o botão
        pygame.draw.rect(tela, COR_LINHA, rect)
        # Define a fonte e renderiza o texto do botão
        fonte = pygame.font.Font(None, 36)
        texto_surface = fonte.render(texto, True, (255, 255, 255))
        tela.blit(texto_surface, (rect[0] + 10, rect[1] + 10))

    def verificar_clique(self, pos, rect):
        # Verifica se o clique do mouse está dentro do retângulo do botão
        x, y, w, h = rect
        return x <= pos[0] <= x + w and y <= pos[1] <= y + h

    def iniciar_jogo(self, modo, dificuldade='dificil'):
        self.rodando = False  # Sai do loop do menu
        jogo = Jogo(modo, dificuldade)  # Cria uma instância do jogo com o modo e dificuldade selecionados
        jogo.rodar()  # Inicia o loop principal do jogo

    def exibir_menu_dificuldade(self):
        # Exibe o menu para selecionar a dificuldade
        self.rodando = True
        while self.rodando:
            tela.fill(COR_FUNDO)
            self.desenhar_opcoes_dificuldade()
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica se o jogador clicou em "Fácil"
                    if self.verificar_clique(evento.pos, (50, 100, 200, 50)):
                        self.iniciar_jogo('IA', 'facil')
                    # Verifica se o jogador clicou em "Difícil"
                    elif self.verificar_clique(evento.pos, (50, 200, 200, 50)):
                        self.iniciar_jogo('IA', 'dificil')

    def desenhar_opcoes_dificuldade(self):
        # Renderiza o título do menu de dificuldade
        fonte = pygame.font.Font(None, 74)
        texto = fonte.render("Dificuldade", True, (255, 255, 255))
        tela.blit(texto, (30, 30))
        # Desenha os botões de seleção de dificuldade
        self.desenhar_botao((50, 100, 200, 50), "Fácil")
        self.desenhar_botao((50, 200, 200, 50), "Difícil")


if __name__ == "__main__":
    menu = Menu()  # Cria uma instância do menu
    menu.exibir_menu()  # Exibe o menu e aguarda a escolha do jogador
