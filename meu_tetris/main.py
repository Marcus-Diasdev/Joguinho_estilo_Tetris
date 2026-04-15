import pygame
import sys
import random
import json

# 1. Inicialização do Pygame e do Mixer de Áudio
pygame.init()
pygame.mixer.init()

# 2. Configurações da Tela
LARGURA = 600
ALTURA = 800
flags_da_tela = pygame.FULLSCREEN | pygame.SCALED
TELA = pygame.display.set_mode((LARGURA, ALTURA), flags_da_tela)

pygame.display.set_caption("Tetris - Menu Inicial")

# --- NOVO: CARREGANDO ASSETS ---
try:
    IMAGEM_FUNDO = pygame.image.load("assets/imagens/fundo.jpg")
    # Redimensiona a imagem para caber perfeitamente na nossa tela
    IMAGEM_FUNDO = pygame.transform.scale(IMAGEM_FUNDO, (LARGURA, ALTURA))
except FileNotFoundError:
    print("Aviso: Imagem de fundo não encontrada. Usando fundo preto.")
    IMAGEM_FUNDO = None

try:
    pygame.mixer.music.load("assets/sons/musica.mp3")
    pygame.mixer.music.set_volume(0.4) # Volume de 0.0 a 1.0 (0.4 é um volume agradável)
    pygame.mixer.music.play(-1) # O -1 faz a música tocar em loop infinito!
except FileNotFoundError:
    print("Aviso: Música não encontrada. O jogo ficará sem som.")

try:
    SOM_LINHA = pygame.mixer.Sound("assets/sons/linha.wav")
    SOM_LINHA.set_volume(0.7) # Deixa o som da linha um pouco mais alto que a música
except FileNotFoundError:
    print("Aviso: Efeito sonoro de linha não encontrado.")
    SOM_LINHA = None

# 3. Cores (RGB)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL_TETRIS = (50, 150, 255)
CINZA = (150, 150, 150)

# 4. Fontes (Tamanhos ajustados para telas de 600px de largura)
FONTE_TITULO = pygame.font.SysFont('arial', 60, bold=True)
FONTE_MENU = pygame.font.SysFont('arial', 35)
FONTE_RODAPE = pygame.font.SysFont('arial', 20)

# 5. Configurações da Grade do Jogo
TAMANHO_BLOCO = 30 # Tamanho em pixels de cada "quadradinho"
COLUNAS = 10
LINHAS = 20
LARGURA_JOGO = COLUNAS * TAMANHO_BLOCO  # 300 pixels de largura
ALTURA_JOGO = LINHAS * TAMANHO_BLOCO    # 600 pixels de altura

# Para centralizar a área de jogo na tela principal de 600x800
INICIO_X = (LARGURA - LARGURA_JOGO) // 2
INICIO_Y = ALTURA - ALTURA_JOGO - 50

# 6. Formato das Peças (Tetrominós)
# S, Z, I, O, J, L, T
PECA_S = [['.....',
           '.....',
           '..00.',
           '.00..',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '...0.',
           '.....']]

PECA_Z = [['.....',
           '.....',
           '.00..',
           '..00.',
           '.....'],
          ['.....',
           '...0.',
           '..00.',
           '..0..',
           '.....']]

PECA_I = [['..0..',
           '..0..',
           '..0..',
           '..0..',
           '.....'],
          ['.....',
           '0000.',
           '.....',
           '.....',
           '.....']]

PECA_O = [['.....',
           '.....',
           '.00..',
           '.00..',
           '.....']]

PECA_J = [['.....',
           '.0...',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..00.',
           '..0..',
           '..0..',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '...0.',
           '.....'],
          ['.....',
           '..0..',
           '..0..',
           '.00..',
           '.....']]

PECA_L = [['.....',
           '...0.',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..0..',
           '..00.',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '.0...',
           '.....'],
          ['.....',
           '.00..',
           '..0..',
           '..0..',
           '.....']]

PECA_T = [['.....',
           '..0..',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '..0..',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '..0..',
           '.....'],
          ['.....',
           '..0..',
           '.00..',
           '..0..',
           '.....']]

# Lista contendo todas as peças para podermos sortear depois
FORMATOS_PECAS = [PECA_S, PECA_Z, PECA_I, PECA_O, PECA_J, PECA_L, PECA_T]

# Cores correspondentes a cada peça
CORES_PECAS = [
    (0, 255, 0),   # S - Verde
    (255, 0, 0),   # Z - Vermelho
    (0, 255, 255), # I - Ciano
    (255, 255, 0), # O - Amarelo
    (0, 0, 255),   # J - Azul
    (255, 165, 0), # L - Laranja
    (128, 0, 128)  # T - Roxo
]

class Peca:
    def __init__(self, coluna, linha, formato):
        self.x = coluna
        self.y = linha
        self.formato = formato
        self.cor = CORES_PECAS[FORMATOS_PECAS.index(formato)]
        self.rotacao = 0 # Começa na primeira posição da lista da peça


def criar_grade(posicoes_travadas={}):
    """
    Cria uma matriz 20x10.
    Se não houver peças travadas, tudo é preto.
    Se houver posições travadas no dicionário, pinta com a cor da peça.
    """
    grade = [[PRETO for _ in range(COLUNAS)] for _ in range(LINHAS)]

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            # A chave do dicionário será a tupla (coluna, linha)
            if (coluna, linha) in posicoes_travadas:
                cor_bloco = posicoes_travadas[(coluna, linha)]
                grade[linha][coluna] = cor_bloco

    return grade

def desenhar_texto(texto, fonte, cor, superficie, x, y):
    """Função auxiliar para centralizar e desenhar textos na tela"""
    objeto_texto = fonte.render(texto, True, cor)
    retangulo_texto = objeto_texto.get_rect()
    retangulo_texto.center = (x, y)
    superficie.blit(objeto_texto, retangulo_texto)
    return retangulo_texto

def obter_formato():
    """Sorteia uma peça aleatória e a posiciona no meio do topo da tela"""
    # Inicia na coluna 5 (meio) e linha 0 (topo)
    return Peca(5, 0, random.choice(FORMATOS_PECAS))


def converter_formato_peca(peca):
    """Lê a matriz 5x5 de texto da peça e converte em coordenadas (X, Y) reais da grade"""
    posicoes = []
    # Pega o desenho atual baseado na rotação
    formato = peca.formato[peca.rotacao % len(peca.formato)]

    for i, linha in enumerate(formato):
        row = list(linha)
        for j, coluna in enumerate(row):
            if coluna == '0':
                # Adiciona a posição X e Y do bloco
                posicoes.append((peca.x + j, peca.y + i))

    # Ajuste para compensar o tamanho da matriz 5x5 e centralizar a peça no seu X e Y
    for i, pos in enumerate(posicoes):
        posicoes[i] = (pos[0] - 2, pos[1] - 4)

    return posicoes


def desenhar_grade_linhas(superficie):
    """Desenha as linhas cinzas que formam o quadriculado da grade"""
    for i in range(LINHAS):
        pygame.draw.line(superficie, CINZA, (INICIO_X, INICIO_Y + i * TAMANHO_BLOCO),
                         (INICIO_X + LARGURA_JOGO, INICIO_Y + i * TAMANHO_BLOCO))
        for j in range(COLUNAS):
            pygame.draw.line(superficie, CINZA, (INICIO_X + j * TAMANHO_BLOCO, INICIO_Y),
                             (INICIO_X + j * TAMANHO_BLOCO, INICIO_Y + ALTURA_JOGO))


def desenhar_janela_jogo(superficie, grade, pontuacao=0, nivel=1, proxima_peca=None):
    # 1. Desenha o fundo (Imagem ou Preto)
    if IMAGEM_FUNDO:
        superficie.blit(IMAGEM_FUNDO, (0, 0))
    else:
        superficie.fill(PRETO)

    # 2. Cria uma "película" escura e semi-transparente atrás da área do jogo
    # para que os blocos fiquem visíveis independente da imagem de fundo
    fundo_grade = pygame.Surface((LARGURA_JOGO, ALTURA_JOGO))
    fundo_grade.set_alpha(180) # Nível de transparência (0 é invisível, 255 é sólido)
    fundo_grade.fill(PRETO)
    superficie.blit(fundo_grade, (INICIO_X, INICIO_Y))

    # Textos do HUD
    desenhar_texto("❤️ Tetris da Vida ❤️", FONTE_TITULO, AZUL_TETRIS, superficie, LARGURA // 2, 40)
    desenhar_texto(f"Pontos: {pontuacao}", FONTE_MENU, BRANCO, superficie, LARGURA // 2, 100)
    desenhar_texto(f"Nível: {nivel}", FONTE_MENU, (0, 255, 0), superficie, LARGURA // 2, 140)

    # <--- NOVO: TEXTO DO MULTIPLICADOR --->
    if nivel > 1:
        desenhar_texto(f"Mult. x{nivel}", FONTE_RODAPE, (255, 215, 0), superficie, LARGURA // 2, 180)

    # 3. Desenha OS BLOCOS COLORIDOS (Ignorando a cor preta)
    for i in range(LINHAS):
        for j in range(COLUNAS):
            cor_atual = grade[i][j]
            # SÓ DESENHA SE NÃO FOR PRETO! Isso revela a imagem e a película ao fundo.
            if cor_atual != PRETO:
                pygame.draw.rect(superficie, cor_atual,
                                 (INICIO_X + j * TAMANHO_BLOCO, INICIO_Y + i * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO),
                                 0)

    # Desenha as linhas do quadriculado
    desenhar_grade_linhas(superficie)
    # Borda vermelha do jogo
    pygame.draw.rect(superficie, (255, 0, 0), (INICIO_X, INICIO_Y, LARGURA_JOGO, ALTURA_JOGO), 5)

    if proxima_peca:
        desenhar_proxima_peca(proxima_peca, superficie)

def espaco_valido(peca, grade):
    """Verifica se a peça está dentro da tela e não está colidindo com blocos travados"""
    posicoes_peca = converter_formato_peca(peca)

    for x, y in posicoes_peca:
        # Se bater nas paredes esquerda (<0), direita (>=COLUNAS) ou passar do chão (>=LINHAS)
        if x < 0 or x >= COLUNAS or y >= LINHAS:
            return False
        # Se bater em um bloco já travado na grade (que não tem a cor PRETA)
        if y >= 0 and grade[y][x] != PRETO:
            return False

    return True


def limpar_linhas(grade, posicoes_travadas, superficie):  # <--- Adicionamos o parâmetro 'superficie'
    linhas_cheias = []

    # 1. Primeiro, mapeamos quais linhas estão totalmente cheias
    for i in range(LINHAS):
        if PRETO not in grade[i]:
            linhas_cheias.append(i)

    # 2. Se houver linhas cheias, tocamos o som e fazemos o Flash!
    if len(linhas_cheias) > 0:
        if SOM_LINHA:
            SOM_LINHA.play()

        # Pinta um retângulo branco em cima das linhas que vão explodir
        for linha in linhas_cheias:
            pygame.draw.rect(superficie, BRANCO,
                             (INICIO_X, INICIO_Y + linha * TAMANHO_BLOCO, LARGURA_JOGO, TAMANHO_BLOCO))

        pygame.display.update()  # Força a tela a desenhar o branco
        pygame.time.delay(150)  # Pausa dramática de 150 milissegundos (o "Flash")

    # 3. Lógica original: apaga as linhas do dicionário e desce o que sobrou
    linhas_limpas = 0
    linha_atual = LINHAS - 1
    while linha_atual >= 0:
        if PRETO not in grade[linha_atual]:
            linhas_limpas += 1
            for coluna in range(COLUNAS):
                if (coluna, linha_atual) in posicoes_travadas:
                    del posicoes_travadas[(coluna, linha_atual)]

            for chave in sorted(list(posicoes_travadas), key=lambda k: k[1], reverse=True):
                x, y = chave
                if y < linha_atual:
                    posicoes_travadas[(x, y + 1)] = posicoes_travadas.pop(chave)

            grade = criar_grade(posicoes_travadas)
        else:
            linha_atual -= 1

    return linhas_limpas

def jogar_partida():
    posicoes_travadas = {}
    grade = criar_grade(posicoes_travadas)

    rodando = True
    peca_atual = obter_formato()
    proxima_peca = obter_formato()
    relogio = pygame.time.Clock()

    tempo_queda = 0
    tempo_total = 0  # <--- CRONÔMETRO DE 1 MINUTO

    velocidade_normal = 0.27
    velocidade_rapida = 0.05
    mudar_peca = False

    pontuacao = 0
    nivel = 1  # <--- VARIÁVEL DE NÍVEL

    while rodando:
        grade = criar_grade(posicoes_travadas)

        # Pega o tempo que passou desde o último frame
        tempo_passado = relogio.get_rawtime()
        tempo_queda += tempo_passado
        tempo_total += tempo_passado  # Soma no cronômetro geral
        relogio.tick()

        # <--- LÓGICA DE DIFICULDADE: A cada 90.000 ms (90 segundos)
        if tempo_total >= 90000:
            tempo_total = 0
            nivel += 1
            # Aumenta a velocidade (diminuindo o tempo), com um limite para não ficar impossível
            if velocidade_normal > 0.08:
                velocidade_normal -= 0.03

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_DOWN]:
            velocidade_atual = velocidade_rapida
        else:
            velocidade_atual = velocidade_normal

        if tempo_queda / 1000 > velocidade_atual:
            tempo_queda = 0
            peca_atual.y += 1

            if not espaco_valido(peca_atual, grade):
                peca_atual.y -= 1
                mudar_peca = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                if evento.key == pygame.K_LEFT:
                    peca_atual.x -= 1
                    if not espaco_valido(peca_atual, grade):
                        peca_atual.x += 1

                if evento.key == pygame.K_RIGHT:
                    peca_atual.x += 1
                    if not espaco_valido(peca_atual, grade):
                        peca_atual.x -= 1

                if evento.key == pygame.K_UP:
                    peca_atual.rotacao += 1
                    if not espaco_valido(peca_atual, grade):
                        peca_atual.rotacao -= 1

                if evento.key == pygame.K_SPACE:
                    # Desce a peça enquanto o espaço for válido
                    while espaco_valido(peca_atual, grade):
                        peca_atual.y += 1

                    # Como o loop parou quando o espaço ficou inválido,
                    # subimos a peça 1 casa para ela ficar travada no último espaço válido
                    peca_atual.y -= 1
                    mudar_peca = True  # Trava a peça instantaneamente!

        posicoes_peca = converter_formato_peca(peca_atual)

        for i in range(len(posicoes_peca)):
            x, y = posicoes_peca[i]
            if y > -1:
                grade[y][x] = peca_atual.cor

        if mudar_peca:
            for pos in posicoes_peca:
                p = (pos[0], pos[1])
                posicoes_travadas[p] = peca_atual.cor

            peca_atual = proxima_peca
            proxima_peca = obter_formato()
            mudar_peca = False

            linhas_apagadas = limpar_linhas(grade, posicoes_travadas, TELA)

            # <--- LÓGICA DO MULTIPLICADOR: Pontos base * Nível
            if linhas_apagadas == 1:
                pontuacao += 100 * nivel
            elif linhas_apagadas == 2:
                pontuacao += 300 * nivel
            elif linhas_apagadas == 3:
                pontuacao += 500 * nivel
            elif linhas_apagadas == 4:
                pontuacao += 800 * nivel

            if verificar_derrota(posicoes_travadas):
                return pontuacao

        # Enviamos o Nível para ser desenhado na tela
        desenhar_janela_jogo(TELA, grade, pontuacao, nivel, proxima_peca)
        pygame.display.update()

    return pontuacao

def modo_solo():
    """Gerencia uma partida única para um jogador"""
    nome_jogador = tela_nome_jogador("SOLO")  # Pede o nome antes de começar
    pontos_finais = jogar_partida()

    salvar_ranking(nome_jogador, pontos_finais)  # <--- Salva os pontos!
    tela_game_over(pontos_finais)

def verificar_derrota(posicoes_travadas):
    """Se houver algum bloco travado na linha 0 (ou acima dela), o jogador perdeu"""
    for pos in posicoes_travadas:
        x, y = pos
        if y < 1:
            return True
    return False


def desenhar_proxima_peca(peca, superficie):
    """Desenha a próxima peça na lateral direita da tela"""
    fonte = pygame.font.SysFont('arial', 30)
    # Posiciona o texto à direita do quadro do jogo
    desenhar_texto("Próxima:", fonte, BRANCO, superficie, INICIO_X + LARGURA_JOGO + 75, INICIO_Y + 50)

    formato = peca.formato[peca.rotacao % len(peca.formato)]

    for i, linha in enumerate(formato):
        row = list(linha)
        for j, coluna in enumerate(row):
            if coluna == '0':
                # Desenha os quadradinhos da próxima peça
                pygame.draw.rect(superficie, peca.cor,
                                 (INICIO_X + LARGURA_JOGO + 25 + j * 30, INICIO_Y + 100 + i * 30, 30, 30), 0)


def tela_game_over(pontuacao_final):
    """Exibe a tela de derrota com um contador de 5 segundos para evitar cliques acidentais"""
    tempo_inicial = pygame.time.get_ticks()  # Marca o momento em que a tela abriu
    esperando = True

    # Limpa eventos antigos para garantir que um clique feito DURANTE o jogo não feche esta tela
    pygame.event.clear()

    while esperando:
        TELA.fill(PRETO)

        # Calcula quanto tempo passou (em milissegundos)
        tempo_atual = pygame.time.get_ticks()
        segundos_passados = (tempo_atual - tempo_inicial) // 1000
        segundos_restantes = 5 - segundos_passados

        # Desenha os textos principais
        desenhar_texto("GAME OVER", FONTE_TITULO, (255, 0, 0), TELA, LARGURA // 2, 250)
        desenhar_texto(f"Pontuação Final: {pontuacao_final}", FONTE_MENU, BRANCO, TELA, LARGURA // 2, 400)

        # Lógica do botão de ignorar/liberar
        if segundos_restantes > 0:
            # Enquanto o tempo não acaba, mostra o contador
            desenhar_texto(f"Aguarde {segundos_restantes}s...", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 550)
        else:
            # Após os 5 segundos, libera o aviso para sair
            desenhar_texto("Pressione qualquer tecla para continuar", FONTE_RODAPE, (0, 255, 0), TELA, LARGURA // 2,
                           550)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # SÓ permite fechar a tela se os 5 segundos já tiverem passado
                if segundos_restantes <= 0:
                    esperando = False

def menu_principal():
    rodando = True
    opcao_selecionada = 0
    opcoes = ["Modo Solo", "Modo Desafio", "Ranking", "Sair"]

    while rodando:
        TELA.fill(PRETO)  # <--- FUNDO APENAS PRETO AQUI

        desenhar_texto("Tetris da Vida", FONTE_TITULO, AZUL_TETRIS, TELA, LARGURA // 2, 150)

        retangulos_opcoes = []
        for i, texto_opcao in enumerate(opcoes):
            cor = BRANCO
            texto_display = texto_opcao
            if i == opcao_selecionada:
                cor = (255, 215, 0)
                texto_display = f">  {texto_opcao}  <"

            retangulo = desenhar_texto(texto_display, FONTE_MENU, cor, TELA, LARGURA // 2, 350 + (i * 70))
            retangulos_opcoes.append(retangulo)

        desenhar_texto("Use Setas/Mouse e ENTER/Clique", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 750)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                # <--- NOVO: ACEITA OS DOIS ENTERS --->
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if opcao_selecionada == 0:
                        modo_solo()
                    elif opcao_selecionada == 1:
                        modo_desafio()
                    elif opcao_selecionada == 2:
                        tela_ranking()
                    elif opcao_selecionada == 3:
                        rodando = False

            if evento.type == pygame.MOUSEMOTION:
                posicao_mouse = evento.pos
                for i, retangulo in enumerate(retangulos_opcoes):
                    if retangulo.collidepoint(posicao_mouse):
                        opcao_selecionada = i

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicao_mouse = evento.pos
                    for i, retangulo in enumerate(retangulos_opcoes):
                        if retangulo.collidepoint(posicao_mouse):
                            if i == 0:
                                modo_solo()
                            elif i == 1:
                                modo_desafio()
                            elif i == 2:
                                tela_ranking()
                            elif i == 3:
                                rodando = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

def modo_desafio():
    """Gerencia os turnos, nomes e salva as pontuações de cada jogador"""
    qtd_jogadores = tela_quantidade_jogadores()

    if qtd_jogadores == 0:
        return

        # Fase 1: Coletar os Nomes
    nomes_jogadores = []
    for i in range(1, qtd_jogadores + 1):
        nome_digitado = tela_nome_jogador(i)
        nomes_jogadores.append(nome_digitado)

    resultados = []

    # Fase 2: Jogar as partidas
    # Iteramos pela lista de nomes que acabamos de criar
    # Iteramos pela lista de nomes que acabamos de criar
    for nome_atual in nomes_jogadores:
        tela_preparacao(nome_atual)
        pontos = jogar_partida()
        resultados.append((nome_atual, pontos))

        salvar_ranking(nome_atual, pontos)  # <--- SÓ ADICIONAR ESTA LINHA AQUI!

        tela_game_over(pontos)

    # Quando todos terminarem, exibe quem ganhou!
    tela_podio(resultados)


def carregar_ranking():
    """Lê o arquivo JSON. Se não existir, retorna uma lista vazia."""
    try:
        with open("ranking.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []  # Arquivo ainda não existe, ninguém jogou


def salvar_ranking(nome, pontuacao):
    """Adiciona a nova pontuação, ordena e salva apenas os 5 melhores"""
    ranking = carregar_ranking()

    # Adiciona o jogador atual na lista
    ranking.append({"nome": nome, "pontuacao": pontuacao})

    # Ordena a lista do maior ponto para o menor
    ranking = sorted(ranking, key=lambda x: x["pontuacao"], reverse=True)

    # Mantém apenas os 5 primeiros (Top 5)
    ranking = ranking[:5]

    # Salva de volta no arquivo
    with open("ranking.json", "w") as arquivo:
        json.dump(ranking, arquivo, indent=4)


def tela_ranking():
    """Lê o arquivo e exibe os recordes na tela"""
    ranking = carregar_ranking()
    esperando = True

    pygame.time.delay(300)
    pygame.event.clear()

    while esperando:
        TELA.fill(PRETO)
        desenhar_texto("TOP 5 RECORDES", FONTE_TITULO, (255, 215, 0), TELA, LARGURA // 2, 150)

        # Se a lista estiver vazia
        if not ranking:
            desenhar_texto("Nenhum recorde registrado ainda!", FONTE_MENU, CINZA, TELA, LARGURA // 2, 350)
        else:
            y = 300
            for i, registro in enumerate(ranking):
                texto = f"{i + 1}º Lugar: {registro['nome']} - {registro['pontuacao']} pts"
                cor = (255, 215, 0) if i == 0 else BRANCO  # Pinta o 1º de dourado
                desenhar_texto(texto, FONTE_MENU, cor, TELA, LARGURA // 2, y)
                y += 60

        desenhar_texto("Pressione ESC para voltar ao menu", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 700)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    esperando = False


def tela_quantidade_jogadores():
    rodando = True
    opcao_selecionada = 0
    opcoes = [2, 3, 4]

    pygame.time.delay(300)
    pygame.event.clear()

    while rodando:
        TELA.fill(PRETO)  # <--- FUNDO APENAS PRETO E SEM AQUELA PELÍCULA

        desenhar_texto("MODO DESAFIO", FONTE_TITULO, AZUL_TETRIS, TELA, LARGURA // 2, 150)
        desenhar_texto("Quantos jogadores?", FONTE_MENU, BRANCO, TELA, LARGURA // 2, 250)

        retangulos_opcoes = []
        for i, qtd in enumerate(opcoes):
            cor = BRANCO
            texto_display = f"{qtd} Jogadores"
            if i == opcao_selecionada:
                cor = (255, 215, 0)
                texto_display = f">  {qtd} Jogadores  <"

            retangulo = desenhar_texto(texto_display, FONTE_MENU, cor, TELA, LARGURA // 2, 400 + (i * 80))
            retangulos_opcoes.append(retangulo)

        desenhar_texto("Use Setas/Mouse e ENTER/Clique", FONTE_RODAPE, AZUL_TETRIS, TELA, LARGURA // 2, 650)
        desenhar_texto("ESC para voltar", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 700)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                # <--- NOVO: ACEITA OS DOIS ENTERS --->
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return opcoes[opcao_selecionada]
                elif evento.key == pygame.K_ESCAPE:
                    return 0

            if evento.type == pygame.MOUSEMOTION:
                posicao_mouse = evento.pos
                for i, retangulo in enumerate(retangulos_opcoes):
                    if retangulo.collidepoint(posicao_mouse):
                        opcao_selecionada = i

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicao_mouse = evento.pos
                    for i, retangulo in enumerate(retangulos_opcoes):
                        if retangulo.collidepoint(posicao_mouse):
                            return opcoes[i]

def tela_nome_jogador(numero_jogador):
    """Cria um campo de digitação para o jogador inserir seu nome"""
    nome = ""
    esperando = True

    # Limpa o teclado para não digitar sem querer ao pular de tela
    pygame.time.delay(300)
    pygame.event.clear()

    while esperando:
        TELA.fill(PRETO)

        # <--- MUDANÇA AQUI: Dividimos o título em duas linhas
        desenhar_texto("NOME DO", FONTE_TITULO, AZUL_TETRIS, TELA, LARGURA // 2, 150)
        desenhar_texto(f"JOGADOR {numero_jogador}", FONTE_TITULO, BRANCO, TELA, LARGURA // 2, 230)

        # Desenha uma "caixa de texto" (descemos o Y para 350 para dar espaço)
        pygame.draw.rect(TELA, CINZA, (LARGURA // 2 - 200, 350, 400, 60), 3)

        # O texto do nome (descemos o Y para 380 para centralizar na caixa)
        if len(nome) == 0:
            desenhar_texto("Digite aqui...", FONTE_MENU, (100, 100, 100), TELA, LARGURA // 2, 380)
        else:
            desenhar_texto(nome, FONTE_MENU, BRANCO, TELA, LARGURA // 2, 380)

        # Descemos o aviso do ENTER para 550
        desenhar_texto("Pressione ENTER para confirmar", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 550)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # <--- NOVO: ACEITA OS DOIS ENTERS --->
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if nome.strip() == "":
                        nome = f"Jogador {numero_jogador}"
                    esperando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 10:
                        nome += evento.unicode

    return nome

def tela_preparacao(nome_jogador):  # <--- Agora recebe o Nome!
    esperando = True
    pygame.time.delay(300)
    pygame.event.clear()

    while esperando:
        TELA.fill(PRETO)
        desenhar_texto("PREPARE-SE", FONTE_TITULO, AZUL_TETRIS, TELA, LARGURA // 2, 250)

        # Exibe o nome que o jogador digitou, tudo em maiúsculo
        desenhar_texto(f"{nome_jogador.upper()}", FONTE_TITULO, BRANCO, TELA, LARGURA // 2, 330)

        desenhar_texto("Pressione qualquer tecla para começar", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 600)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False


def tela_podio(resultados):
    """Recebe a lista de pontos, ordena e exibe o vencedor"""
    # Ordena a lista do maior ponto para o menor
    resultados.sort(key=lambda x: x[1], reverse=True)

    esperando = True
    while esperando:
        TELA.fill(PRETO)
        desenhar_texto("PÓDIO FINAL", FONTE_TITULO, (255, 215, 0), TELA, LARGURA // 2, 150)  # Amarelo Ouro

        y = 300
        for i, (jogador, pontos) in enumerate(resultados):
            texto = f"{i + 1}º Lugar: {jogador} - {pontos} pts"
            cor = BRANCO
            if i == 0:
                cor = (255, 215, 0)  # Destaca o primeiro lugar em ouro

            desenhar_texto(texto, FONTE_MENU, cor, TELA, LARGURA // 2, y)
            y += 60  # Desce o espaço para escrever o próximo jogador

        desenhar_texto("Pressione qualquer tecla para voltar ao menu", FONTE_RODAPE, CINZA, TELA, LARGURA // 2, 700)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

# Ponto de entrada do script
if __name__ == "__main__":
    menu_principal()
