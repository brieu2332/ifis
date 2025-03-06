import pygame
import math

pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação IFIS: Captura Orbital - Terra Parte da Esquerda")
clock = pygame.time.Clock()

# Classe que representa um corpo celeste
class CorpoCeleste:
    def __init__(self, pos, vel, massa, cor, raio_desenho, raio_influencia, raio_poco):
        self.pos = pygame.Vector2(pos)          # Posição do corpo
        self.vel = pygame.Vector2(vel)          # Velocidade do corpo
        self.massa = massa                      # Massa usada para calcular a gravidade
        self.cor = cor                          # Cor para o desenho
        self.raio_desenho = raio_desenho        # Tamanho visual do corpo
        self.raio_influencia = raio_influencia  # Zona de influência visual (para escalonar a atração)
        self.raio_poco = raio_poco              # Poço gravitacional visual (para detecção de colisão)

    def update(self, forca, dt):
        # Atualiza velocidade e posição com o método de Euler
        acel = forca / self.massa
        self.vel += acel * dt
        self.pos += self.vel * dt

    def draw(self, surface):
        # Desenha o corpo e as zonas de influência (apenas para visualização)
        pygame.draw.circle(surface, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio_desenho)
        pygame.draw.circle(surface, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio_influencia, 1)
        pygame.draw.circle(surface, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio_poco, 1)

def calcular_forca(sun, planet):
    G = 1  # Constante gravitacional para a simulação
    d_vec = sun.pos - planet.pos          # Vetor que aponta do planeta para o Sol
    distance = d_vec.length()
    if distance == 0:
        return pygame.Vector2(0, 0)
    # Força gravitacional pura
    force_magnitude = G * sun.massa * planet.massa / (distance ** 2)
    force = d_vec.normalize() * force_magnitude

    # Escalonamento da força de forma gradual:
    # Se o planeta estiver fora do "raio_influencia", a força é zero.
    # Dentro desse raio, a força é aplicada de forma linear (de 0 a 1)
    threshold = sun.raio_influencia
    if distance > threshold:
        factor = 0
    else:
        factor = 1 - (distance / threshold)
    return force * factor

# Configuração do Sol (posicionado à direita, mas não na borda)
sun = CorpoCeleste(
    pos=(600, 300),
    vel=(0, 0),
    massa=10000,
    cor=(255, 255, 0),
    raio_desenho=10,
    raio_influencia=500,  # Aumentado para que a atração comece a agir gradualmente
    raio_poco=30
)

# Configuração da Terra (parte da esquerda da tela)
# A Terra inicia em (100, 350) para que a linha que une os corpos não seja perfeitamente horizontal,
# permitindo que haja um componente tangencial na força quando ela entrar na zona de influência.
terra = CorpoCeleste(
    pos=(100, 350),
    vel=(3, -2),  # Velocidade inicial com componente horizontal e vertical
    massa=10,
    cor=(0, 0, 255),
    raio_desenho=5,
    raio_influencia=100,
    raio_poco=20
)

dt = 0.1  # Intervalo de tempo para as atualizações
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Calcula a força gravitacional do Sol sobre a Terra (aplicada gradualmente)
    forca = calcular_forca(sun, terra)
    terra.update(forca, dt)

    # Se a Terra atingir o poço gravitacional do Sol, consideramos uma captura ou colisão
    if (terra.pos - sun.pos).length() < sun.raio_poco:
        print("Colisão ou captura!")
        rodando = False

    tela.fill((0, 0, 0))
    sun.draw(tela)
    terra.draw(tela)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
