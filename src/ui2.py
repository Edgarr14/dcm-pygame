import math
import pygame

class GameUI:
    def __init__(self, width: int = 1000, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulador de Estacionamiento - Prueba de Motor Físico")
        self.font = pygame.font.SysFont("consolas", 15)
        self.font_bold = pygame.font.SysFont("consolas", 18, bold=True)

        # Obstáculos estáticos del estacionamiento (Paredes, otros carros y columna central)
        self.obstacles = [
            pygame.Rect(0, 0, 1000, 25),       # Pared superior
            pygame.Rect(0, 575, 1000, 25),     # Pared inferior
            pygame.Rect(0, 0, 25, 600),        # Pared izquierda
            pygame.Rect(975, 0, 25, 600),      # Pared derecha
            pygame.Rect(60, 165, 155, 65),     # Carro estacionado arriba del jugador
            pygame.Rect(60, 365, 155, 65),     # Carro estacionado abajo del jugador
            pygame.Rect(450, 160, 50, 280),    # Columna / isla central
            pygame.Rect(700, 25, 150, 180),    # Bloque superior derecho
            pygame.Rect(700, 395, 150, 180),   # Bloque inferior derecho
        ]

        # Zona de meta (Salida del parking)
        self.exit_zone = pygame.Rect(830, 240, 120, 120)

    def render(self, model, won: bool = False):
        # 1. Fondo de asfalto
        self.screen.fill((38, 40, 48))

        # 2. Dibujar líneas guía del cajón de estacionamiento inicial
        pygame.draw.line(self.screen, (200, 200, 80), (55, 250), (225, 250), 3)
        pygame.draw.line(self.screen, (200, 200, 80), (55, 345), (225, 345), 3)
        pygame.draw.line(self.screen, (200, 200, 80), (55, 250), (55, 345), 3)

        # 3. Dibujar zona de salida (Meta)
        pygame.draw.rect(self.screen, (35, 110, 60), self.exit_zone, border_radius=6)
        pygame.draw.rect(self.screen, (80, 220, 120), self.exit_zone, width=2, border_radius=6)
        meta_txt = self.font_bold.render("SALIDA", True, (180, 255, 200))
        self.screen.blit(meta_txt, (self.exit_zone.centerx - 32, self.exit_zone.centery - 10))

        # 4. Dibujar obstáculos (Paredes y otros vehículos)
        for index, rect in enumerate(self.obstacles):
            # Distinguir paredes (gris) de carros estacionados (azul apagado)
            color = (75, 80, 92) if index not in (4, 5) else (65, 95, 135)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            pygame.draw.rect(self.screen, (120, 125, 140), rect, width=2, border_radius=4)

        # 5. Dibujar el vehículo del jugador usando los vértices rotados del backend
        corners = model.get_corners_pixels()
        car_color = (220, 60, 60) if model.crashed else ((60, 200, 100) if won else (235, 155, 40))
        pygame.draw.polygon(self.screen, car_color, corners)
        pygame.draw.polygon(self.screen, (255, 255, 255), corners, width=2)

        # Marcar el frente del vehículo (línea gruesa cian entre las esquinas delanteras 0 y 1)
        pygame.draw.line(self.screen, (80, 240, 255), corners[0], corners[1], 5)

        # 6. Panel de telemetría física en vivo
        self._draw_hud(model, won)
        pygame.display.flip()

    def _draw_hud(self, model, won: bool):
        steer_deg = math.degrees(model.steering_angle)
        # Radio de giro instantáneo: R = L / tan(delta)
        if abs(model.steering_angle) > 0.01:
            turn_radius_str = f"{abs(model.wheelbase / math.tan(model.steering_angle)):.2f} m"
        else:
            turn_radius_str = "Infinito (Recto)"

        lines = [
            f"Velocidad (v): {model.velocity:+.2f} m/s ({model.velocity * 3.6:+.1f} km/h)",
            f"Angulo Volante (delta): {steer_deg:+.1f} deg | Radio Giro (R): {turn_radius_str}",
            f"[1/2] Distancia Ejes (L): {model.wheelbase:.2f} m | [3/4] Friccion (mu): {model.friction_coeff:.2f}",
            "Controles: Flechas = Manejar | ESPACIO = Freno | R = Reiniciar",
        ]

        # Caja semitransparente para lectura clara
        hud_bg = pygame.Surface((680, 95), pygame.SRCALPHA)
        hud_bg.fill((15, 15, 22, 210))
        self.screen.blit(hud_bg, (30, 32))

        for i, text in enumerate(lines):
            surf = self.font.render(text, True, (230, 235, 245))
            self.screen.blit(surf, (40, 38 + i * 21))

        if model.crashed:
            msg = self.font_bold.render("¡COLISION DETECTADA! Presiona [R] para reiniciar", True, (255, 90, 90))
            self.screen.blit(msg, (280, 540))
        elif won:
            msg = self.font_bold.render("¡MANIOBRA EXITOSA! Presiona [R] para repetir", True, (100, 255, 140))
            self.screen.blit(msg, (300, 540))