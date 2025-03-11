import pygame
import math

pygame.init()
largura, altura = 1100, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação IFIS: Sol e Terra")
clock = pygame.time.Clock()

# Classe pai para corpos celestes
class CorpoCeleste:
    def __init__(self, posicao, vel, massa, cor, raio_desenho, raio_influencia, raio_poco):
        self.posicao = pygame.Vector2(posicao)
        self.vel = pygame.Vector2(vel)        # Vector2: é uma classe do Pygame que representa vetores bidimensionais. Ele é usado para facilitar cálculos com posição, velocidade e força sem precisar manipular manualmente os valores de x e y separadamente.
        self.massa = massa
        self.cor = cor
        self.raio_desenho = raio_desenho
        self.raio_influencia = raio_influencia
        self.raio_poco = raio_poco

    def update(self, forca, tempoDecorrido):
        acel = forca / self.massa # a = f / m
        self.vel = self.vel + acel * tempoDecorrido  # Atualiza velocidade (Vf - Vi + a * ◬T) movimento uniformemente variado  
        self.posicao += self.vel * tempoDecorrido  

    def draw(self, surface):
        # Desenha a bolinha (pleneta)
        pygame.draw.circle(surface, self.cor, (int(self.posicao.x), int(self.posicao.y)), self.raio_desenho)
        # Desenha o poço gravitacional (atmosfera) - serve só para visualização
        pygame.draw.circle(surface, self.cor, (int(self.posicao.x), int(self.posicao.y)), self.raio_influencia, 1)
        # Desenha o círculo de influência (a gravidade) - serve só para visualização
        pygame.draw.circle(surface, self.cor, (int(self.posicao.x), int(self.posicao.y)), self.raio_poco, 1)

# classeFilha Sol
class Sol(CorpoCeleste):
    def __init__(self, posicao):
        super().__init__(posicao, vel=(0, 0), massa=10000, cor=(255, 255, 255),raio_desenho=10, raio_influencia=150, raio_poco=30)

# classefilha Terra
class Terra(CorpoCeleste):
    def __init__(self, posicao):
        super().__init__(posicao, vel=(2, 2), massa=10, cor=(255, 255, 255),raio_desenho=5, raio_influencia=100, raio_poco=20)


def calcular_forca(corpo1, corpo2):
    G = 1  
    direcao = corpo1.posicao - corpo2.posicao  
    distancia = direcao.length()  
    if distancia == 0:
        return pygame.Vector2(0, 0)
    forca_magnitude = G * corpo1.massa * corpo2.massa / (distancia ** 2) # Fórmula da gravitação universal: F = G * (m1 * m2) / (distancia^2)
    return direcao.normalize() * forca_magnitude # Normaliza o vetor de direção para aplicar a magnitude da força

# Criando instâncias dos corpo celeste
sol = Sol(posicao=(largura - 300, altura / 2))
terra = Terra(posicao=(150, altura / 1.5))

dt = 0.1  
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    #calcula apenas a força do sol sobre a terra
    forca = calcular_forca(sol, terra)
    print(forca)
    terra.update(forca, dt)

    #pequena colisão para simular a colisão dos planetas
    if (terra.posicao - sol.posicao).length() < sol.raio_poco:
        print("Colisão")
        rodando = False

    tela.fill((0, 0, 0))
    sol.draw(tela)
    terra.draw(tela)
    pygame.display.flip()
    clock.tick(60)

    if rodando == False:
        print('programa fechado')

pygame.quit()
# 1° lei de Kepler, as orbitas nao sao circulares mas sim elipticas( mais achatadas), 
# 2° lei de Kepler(lei das areas) em uma orbita areas iguais sao percorridas em tempos iguais ou seja a area do arco do Periélio é percorrido no mesmo tempo do  afélio ( a velocidade da area do perielio é maior para percorrer no mesmo tempo do afelio)
# 3° lei de Newton, lei da ação e reação onde cada um dos corpos celestes causam uma ação e reação os dois em cada um