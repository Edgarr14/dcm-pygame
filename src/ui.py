import pygame

class GameUI:
    def __init__(self, width: int = 1000, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulación Física - Ready to Dev")
        self.font = pygame.font.SysFont("consolas", 18)

    def render(self, model):
        self.screen.fill((24, 24, 36))  # Fondo oscuro
        texto = self.font.render(
            f"Tiempo simulado: {model.time_elapsed:.2f} s | g = {model.gravity} m/s2",
            True,
            (220, 220, 220)
        )
        self.screen.blit(texto, (20, 20))
        pygame.display.flip()