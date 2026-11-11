import pygame

class GameUI:
    def __init__(self, width: int = 1000, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulación Física - Estacionamiento")
        self.font = pygame.font.SysFont("consolas", 18)
        self.font_pequeña = pygame.font.SysFont("consolas", 14)

    def render(self, model):
        #fondo
        self.screen.fill((24, 24, 36))
        #acera y borde de la pantalla
        pygame.draw.rect(self.screen, (60, 60, 60), (0, 0, self.width, 50))
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 46, self.width, 4)) #superior
        
        pygame.draw.rect(self.screen, (60, 60, 60), (0, self.height - 50, self.width, 50))
        pygame.draw.rect(self.screen, (100, 100, 100), (0, self.height - 50, self.width, 4)) #inferior
        
        #mapa del estacionamiento
        self.dibujar_mapa_estacionamiento()

        texto = self.font.render(
            f"Tiempo simulado: {model.time_elapsed:.2f} s | g = {model.gravity} m/s2",
            True,
            (220, 220, 220)
        )
        self.screen.blit(texto, (20, 20))
        
        # esta es la "mision" despues se pone mas bonito
        hud_bg = pygame.Rect(20, self.height - 42, self.width - 40, 32)
        pygame.draw.rect(self.screen, (30, 30, 45), hud_bg, border_radius=6)
        pygame.draw.rect(self.screen, (70, 90, 120), hud_bg, 2, border_radius=6)
        
        texto_mision = self.font_pequeña.render("MISION: Maniobra y escapa del estacionamiento sin chocar", True, (180, 210, 240))
        self.screen.blit(texto_mision, (35, self.height - 35))

        # el carro y obstaculos de prueba
        carro_ejemplo = pygame.Rect(100, 320, 50, 30)
        obstaculos_ejemplo = [pygame.Rect(250, 110, 60, 90), pygame.Rect(450, 110, 60, 90)]
        self.dibujar_estacionamiento(carro_ejemplo, obstaculos_ejemplo)

        pygame.display.flip()

    def dibujar_mapa_estacionamiento(self):
        """Dibuja aceras, puestos superiores e inferiores enumerados, y carriles de circulación."""
        # acera superior
        pygame.draw.rect(self.screen, (80, 80, 80), (50, 60, 900, 50))
        
        # acera inferior
        pygame.draw.rect(self.screen, (80, 80, 80), (50, 480, 900, 50))
        
        # puestos superiores (P1 a P7)
        puestos_x = range(150, 850, 100)
        for i, x in enumerate(puestos_x, start=1):
            pygame.draw.line(self.screen, (220, 220, 220), (x, 110), (x, 210), 2)
            label = self.font_pequeña.render(f"P{i}", True, (180, 180, 180))
            self.screen.blit(label, (x - 60, 120))

        # puestos inferiores (P8 a P14)
        for i, x in enumerate(puestos_x, start=8):
            pygame.draw.line(self.screen, (220, 220, 220), (x, 380), (x, 480), 2)
            label = self.font_pequeña.render(f"P{i}", True, (180, 180, 180))
            self.screen.blit(label, (x - 60, 455))

        # linea punteada del centro
        for x_linea in range(80, 920, 40):
            pygame.draw.line(self.screen, (230, 200, 50), (x_linea, 295), (x_linea + 20, 295), 2)

    def dibujar_estacionamiento(self, carro_rect, obstaculos):
        """Dibuja el vehículo principal y los carros estacionados."""
        # un carrito feito azul de prueba
        pygame.draw.rect(self.screen, (0, 150, 255), carro_rect, border_radius=4)
        
        # obstaculos horribles rojos de prueba
        for obstaculo in obstaculos:
            pygame.draw.rect(self.screen, (210, 50, 50), obstaculo, border_radius=4)