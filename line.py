import pygame
from math import cos, sin, pi, atan2


class Seta:
    def __init__(self, cor, ox, oy, r, espessura):
        self.cor = cor
        self.ox = ox
        self.oy = oy
        self.r = r
        self.espessura = espessura
        self.a = 0

    def desenhar(self, tela, destino_x, destino_y):
        # retorna o ângulo (em radianos) cujo seno e cosseno correspondem às coordenadas y e x. Ela é usada para calcular o ângulo de rotação entre dois pontos no plano cartesiano.
        self.a = atan2(destino_y - self.oy, destino_x - self.ox)
        
        x = self.r * cos(self.a)
        y = self.r * sin(self.a)

        b = self.a - 2.35619
        c = self.a + 2.35619
        r2 = self.r / 3

        x2 = (r2 * cos(b)) + x
        y2 = (r2 * sin(b)) + y
        x3 = (r2 * cos(c)) + x
        y3 = (r2 * sin(c)) + y

        pygame.draw.line(tela, self.cor, (self.ox, self.oy), (self.ox + x, self.oy + y), self.espessura)
        pygame.draw.line(tela, self.cor, (self.ox + x, self.oy + y), (self.ox + x2, self.oy + y2), self.espessura)
        pygame.draw.line(tela, self.cor, (self.ox + x, self.oy + y), (self.ox + x3, self.oy + y3), self.espessura)

        

class Jogo:
    def __init__(self, largura = 800, altura = 800, distancia_entre_etas = 39):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("SETAS")
        self.cor_branca = (250, 250, 250)
        self.fim_jogo = False
        self.setas = []
        
        for x in range(0, largura, distancia_entre_etas):
            for y in range(0, altura, distancia_entre_etas):
                r = 15# tamanho seta
                espessura = 2  
                self.setas.append(Seta(self.cor_branca, x, y, r, espessura))
                

    def executar(self):
        while not self.fim_jogo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.fim_jogo = True
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.tela.fill(0)
            
            for seta in self.setas:
                seta.desenhar(self.tela, mouse_x, mouse_y)
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
