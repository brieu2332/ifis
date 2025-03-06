import pygame
import math

pygame.init()
largura, altura = 1100, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação IFIS: Sol e Terra")
clock = pygame.time.Clock()

# Classe que representa um corpo celeste (como o Sol ou a Terra)
class CorpoCeleste:
    def __init__(self, pos, vel, massa, cor, raio_desenho, raio_influencia, raio_poco):
        self.pos = pygame.Vector2(pos)        # Posição do corpo
        self.vel = pygame.Vector2(vel)        # Velocidade do corpo
        self.massa = massa                    # Massa (importante para a força gravitacional)
        self.cor = cor                        # Cor para desenho
        self.raio_desenho = raio_desenho      # Tamanho visual do corpo
        self.raio_influencia = raio_influencia  # Raio visual para a "zona de influência"
        self.raio_poco = raio_poco            # Raio visual para o "poço gravitacional"

    def update(self, forca, dt):
        # Atualiza a velocidade e posição com base na força aplicada
        # Aceleração = forca / massa
        acel = forca / self.massa
        self.vel += acel * dt  # Atualiza velocidade
        self.pos += self.vel * dt  # Atualiza posição

    def draw(self, surface):
        # Desenha o corpo como um círculo preenchido
        pygame.draw.circle(surface, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio_desenho)
        # Desenha o círculo de influência (apenas contorno) - serve só para visualização
        pygame.draw.circle(surface, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio_influencia, 1)
        # Desenha o poço gravitacional (apenas contorno) - serve só para visualização
        pygame.draw.circle(surface, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio_poco, 1)

def calcular_forca(corpo1, corpo2):
    # Calcula a força gravitacional que o corpo1 exerce sobre o corpo2
    G = 1  # Constante gravitacional ajustada para a simulação
    direcao = corpo1.pos - corpo2.pos  # Vetor que aponta do corpo2 para o corpo1
    distancia = direcao.length()  # Distância entre os corpos
    if distancia == 0:
        return pygame.Vector2(0, 0)
    # Fórmula da gravitação universal: F = G * (m1 * m2) / (distancia^2)
    forca_magnitude = G * corpo1.massa * corpo2.massa / (distancia ** 2)
    # Normaliza o vetor de direção para aplicar a magnitude da força
    forca = direcao.normalize() * forca_magnitude
    return forca

# Instanciando os corpos
# Sol: posicionado no centro, sem velocidade
sol = CorpoCeleste(
    pos=(largura - 100, altura / 2),
    vel=(0, 0),
    massa=10000,
    cor=(255, 255, 255),
    raio_desenho=10,         # Tamanho visual menor
    raio_influencia=150,     # Zona de influência visual (não afeta o cálculo da força)
    raio_poco=30             # Poço gravitacional visual (usado para detectar "colisão" ou captura)
)

# Terra: posicionada acima do Sol, com velocidade horizontal para orbitar
terra = CorpoCeleste(
    pos=(700, altura / 3),   # (100, altura / 3) // (700, altura / 3) //
    vel=(0, 3),              # (2,2) // (0, 3) //
    massa=10,
    cor=(255, 255, 255),
    raio_desenho=5,          # Tamanho visual menor
    raio_influencia=100,
    raio_poco=20
)

dt = 0.1  # Intervalo de tempo para cada atualização
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Calcula a força gravitacional exercida pelo Sol sobre a Terra com base na distância real
    forca = calcular_forca(sol, terra)
    terra.update(forca, dt)

    # Se a Terra entrar no "poço gravitacional" do Sol (definido visualmente), 
    # pode ser considerado uma colisão ou captura
    if (terra.pos - sol.pos).length() < sol.raio_poco:
        print("Colisão ou captura!")
        rodando = False

    # Atualiza a visualização
    tela.fill((0, 0, 0))
    sol.draw(tela)
    terra.draw(tela)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
