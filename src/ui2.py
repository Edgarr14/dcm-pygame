import math
import pygame

class GameUI:
    def __init__(self, width: int = 1000, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulador de Estacionamiento - Parking Escape")
        self.font = pygame.font.SysFont("consolas", 15)
        self.font_pequeña = pygame.font.SysFont("consolas", 12)
        self.font_bold = pygame.font.SysFont("consolas", 18, bold=True)
        
        # obstaculos 
        self.obstacles = [
            pygame.Rect(0, 0, 1000, 25),      # Pared superior
            pygame.Rect(0, 575, 1000, 25),    # Pared inferior
            pygame.Rect(0, 0, 25, 600),       # Pared izquierda
            pygame.Rect(975, 0, 25, 600),     # Pared derecha
            pygame.Rect(215, 55, 70, 95),     # Carro estacionado en P2 (arriba)
            pygame.Rect(315, 450, 70, 95),    # Carro estacionado en P10 (abajo) 
            pygame.Rect(450, 160, 50, 280),   # Columna
            pygame.Rect(700, 25, 150, 180),   # Bloque superior derecho
            pygame.Rect(700, 395, 150, 180),  # Bloque inferior derecho
        ]

        # salida 
        self.exit_zone = pygame.Rect(830, 240, 120, 120)

    def draw_car(self, surface, x, y, width, height, angle, color, is_player=False):
        """
        Dibuja un carro detallado con rines, parabrisas, faros y stops.
        """
        car_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        body_color = color
        border_color = (255, 255, 255) if is_player else (30, 30, 30)
        
        pygame.draw.rect(car_surface, body_color, (0, 0, width, height), border_radius=6)
        pygame.draw.rect(car_surface, border_color, (0, 0, width, height), 2, border_radius=6)
        
        wheel_color = (20, 20, 20)
        wheel_w, wheel_h = 4, height * 0.25

        pygame.draw.rect(car_surface, wheel_color, (-2, height * 0.2, wheel_w, wheel_h), border_radius=2)
        pygame.draw.rect(car_surface, wheel_color, (-2, height * 0.55, wheel_w, wheel_h), border_radius=2)
        
        pygame.draw.rect(car_surface, wheel_color, (width - 2, height * 0.2, wheel_w, wheel_h), border_radius=2)
        pygame.draw.rect(car_surface, wheel_color, (width - 2, height * 0.55, wheel_w, wheel_h), border_radius=2)

        glass_color = (15, 25, 35, 200)
        pygame.draw.rect(car_surface, glass_color, (4, height * 0.28, width - 8, height * 0.18), border_radius=2)
        pygame.draw.rect(car_surface, glass_color, (4, height * 0.63, width - 8, height * 0.14), border_radius=2)
        
        roof_color = (max(0, body_color[0]-35), max(0, body_color[1]-35), max(0, body_color[2]-35))
        pygame.draw.rect(car_surface, roof_color, (6, height * 0.4, width - 12, height * 0.23))

        headlight_color = (255, 255, 220)
        taillight_color = (255, 40, 40)
        
        pygame.draw.rect(car_surface, headlight_color, (2, 2, 5, 4), border_radius=1)
        pygame.draw.rect(car_surface, headlight_color, (width - 7, 2, 5, 4), border_radius=1)
        
        pygame.draw.rect(car_surface, taillight_color, (2, height - 6, 5, 4), border_radius=1)
        pygame.draw.rect(car_surface, taillight_color, (width - 7, height - 6, 5, 4), border_radius=1)
        
        if is_player:
            pygame.draw.rect(car_surface, (255, 215, 0), (width * 0.42, height * 0.05, width * 0.16, height * 0.2))

        rotated_surface = pygame.transform.rotate(car_surface, -math.degrees(angle))
        new_rect = rotated_surface.get_rect(center=(x, y))
        surface.blit(rotated_surface, new_rect.topleft)

    def draw(self, screen, player_state, telemetry_data, mission_text="Misión: Maniobra y escapa del estacionamiento sin chocar"):
        # Fondo
        screen.fill((35, 38, 43))

        # puestos
        for x in range(100, 700, 100):
            pygame.draw.line(screen, (200, 200, 200), (x, 25), (x, 150), 2)
            pygame.draw.line(screen, (200, 200, 200), (x, 450), (x, 575), 2) 

        # p1, p2, p3 etc
        for i, x in enumerate(range(70, 700, 100), 1):
            txt_sup = self.font_pequena.render(f"P{i}", True, (180, 180, 180))
            screen.blit(txt_sup, (x, 30))
            txt_inf = self.font_pequena.render(f"P{i+7}", True, (180, 180, 180))
            screen.blit(txt_inf, (x, 555))

        # zona de salida
        pygame.draw.rect(screen, (46, 204, 113), self.exit_zone, border_radius=8)
        exit_text = self.font_bold.render("SALIDA", True, (255, 255, 255))
        screen.blit(exit_text, (self.exit_zone.centerx - exit_text.get_width()//2, self.exit_zone.centery - exit_text.get_height()//2))

        for idx, obs in enumerate(self.obstacles):
            if idx in [4, 5]:  #carros estacionados
                self.draw_car(screen, obs.centerx, obs.centery, obs.width, obs.height, 0, color=(70, 130, 180), is_player=False)
            else:  # paredes y columnas normales
                pygame.draw.rect(screen, (70, 75, 85) if idx < 4 else (180, 140, 100), obs, border_radius=4)

        # carro del jugador
        self.draw_car(
            screen,
            x=player_state['x_px'],
            y=player_state['y_px'],
            width=player_state['width_px'],
            height=player_state['height_px'],
            angle=player_state['angle_rad'],
            color=(0, 168, 204),
            is_player=True
        )

        # HUD Superior
        hud_box = pygame.Rect(580, 15, 400, 95)
        pygame.draw.rect(screen, (20, 22, 26), hud_box, border_radius=6)
        pygame.draw.rect(screen, (100, 110, 120), hud_box, 1, border_radius=6)

        telemetry_lines = [
            f"v: {telemetry_data.get('v', 0.0):+.1f} m/s | Giro (R): {telemetry_data.get('turn_radius', 'Infinito')}",
            f"Volante: {telemetry_data.get('steering', 0.0):+.1f} deg",
            f"Ejes (L): {telemetry_data.get('wheelbase', 2.6)}m | Fricción: {telemetry_data.get('friction', 0.7)}",
            f"Controles: WASD/Flechas | ESPACIO=Freno | R=Reset"
        ]
        for idx, line in enumerate(telemetry_lines):
            t_surf = self.font_pequena.render(line, True, (240, 240, 240))
            screen.blit(t_surf, (hud_box.x + 10, hud_box.y + 8 + (idx * 21)))

        # HUD Inferior (Misión)
        bottom_box = pygame.Rect(25, 565, 950, 30)
        pygame.draw.rect(screen, (20, 22, 26), bottom_box, border_radius=4)
        m_surf = self.font.render(mission_text, True, (255, 255, 255))
        screen.blit(m_surf, (bottom_box.x + 15, bottom_box.y + 6))

    def dibujar_mapa_estacionamiento(self):
        """Dibuja aceras perimetrales y puestos válidos (sin P5, P6, P12 y P13)."""

        pygame.draw.rect(self.screen, (60, 60, 60), (0, 0, self.width, 50))
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 46, self.width, 4))
    
        pygame.draw.rect(self.screen, (60, 60, 60), (0, self.height - 50, self.width, 50))
        pygame.draw.rect(self.screen, (100, 100, 100), (0, self.height - 50, self.width, 4))
        
        # Puestos superiores
        puestos_superiores = [(1, 100), (2, 200), (3, 300), (4, 400), (7, 750)]
        for num, x in puestos_superiores:
            pygame.draw.line(self.screen, (220, 220, 220), (x, 50), (x, 160), 2)
            label = self.font_pequeña.render(f"P{num}", True, (180, 180, 180))
            self.screen.blit(label, (x - 45, 60))

        # Puestos inferiores
        puestos_inferiores = [(8, 100), (9, 200), (10, 300), (11, 400), (14, 750)]
        for num, x in puestos_inferiores:
            pygame.draw.line(self.screen, (220, 220, 220), (x, 440), (x, 550), 2)
            label = self.font_pequeña.render(f"P{num}", True, (180, 180, 180))
            self.screen.blit(label, (x - 45, 525))
        
    def render(self, model, won: bool = False):
        # fondo de asfalto
        self.screen.fill((38, 40, 48))
        
        self.dibujar_mapa_estacionamiento()

        pygame.draw.rect(self.screen, (35, 110, 60), self.exit_zone, border_radius=6)
        pygame.draw.rect(self.screen, (80, 220, 120), self.exit_zone, width=2, border_radius=6)
        meta_txt = self.font_bold.render("SALIDA", True, (180, 255, 200))
        self.screen.blit(meta_txt, (self.exit_zone.centerx - 32, self.exit_zone.centery - 10))

        for index, rect in enumerate(self.obstacles):
            if index in (4, 5):  # Carros estacionados con detalles
                self.draw_car(self.screen, rect.centerx, rect.centery, rect.width, rect.height, 0, color=(55, 110, 160), is_player=False)
            elif index >= 7:    # Bloques grandes de la derecha
                pygame.draw.rect(self.screen, (85, 90, 105), rect, border_radius=6)
                pygame.draw.rect(self.screen, (130, 135, 155), rect, width=2, border_radius=6)
            elif index == 6:    # Columna
                pygame.draw.rect(self.screen, (100, 80, 80), rect, border_radius=4)
                pygame.draw.rect(self.screen, (150, 120, 120), rect, width=2, border_radius=4)
            else:               # Paredes perimetrales
                pygame.draw.rect(self.screen, (40, 40, 50), rect)

        # carro del jugador
        corners = model.get_corners_pixels()
        car_color = (220, 60, 60) if model.crashed else ((60, 200, 100) if won else (0, 168, 204))
        
        if len(corners) >= 4:
    
            pygame.draw.polygon(self.screen, car_color, corners)
            pygame.draw.polygon(self.screen, (255, 255, 255), corners, width=2)
        
            def get_point(t_long, t_lat):
                t_inv = 1.0 - t_long
                left_x = corners[0][0] * (1 - t_inv) + corners[3][0] * t_inv
                left_y = corners[0][1] * (1 - t_inv) + corners[3][1] * t_inv
                right_x = corners[1][0] * (1 - t_inv) + corners[2][0] * t_inv
                right_y = corners[1][1] * (1 - t_inv) + corners[2][1] * t_inv
                
                x = left_x * (1 - t_lat) + right_x * t_lat
                y = left_y * (1 - t_lat) + right_y * t_lat
                return (int(x), int(y))

            stripe1 = [get_point(0.25, 0.08), get_point(0.25, 0.92), get_point(0.42, 0.92), get_point(0.42, 0.08)]
            pygame.draw.polygon(self.screen, (25, 45, 65), stripe1)

            stripe2 = [get_point(0.58, 0.08), get_point(0.58, 0.92), get_point(0.75, 0.92), get_point(0.75, 0.08)]
            pygame.draw.polygon(self.screen, (25, 45, 65), stripe2)

            faro_i = get_point(0.92, 0.15)
            faro_d = get_point(0.92, 0.85)
            pygame.draw.circle(self.screen, (255, 255, 200), faro_i, 3)
            pygame.draw.circle(self.screen, (255, 255, 200), faro_d, 3)
            
            luz_t_i = get_point(0.08, 0.15)
            luz_t_d = get_point(0.08, 0.85)
            pygame.draw.circle(self.screen, (255, 60, 60), luz_t_i, 3)
            pygame.draw.circle(self.screen, (255, 60, 60), luz_t_d, 3)
        else:
            pygame.draw.polygon(self.screen, car_color, corners)
            pygame.draw.polygon(self.screen, (255, 255, 200), corners, width=2)

        self._draw_hud(model, won)
        pygame.display.flip()

    def _draw_hud(self, model, won: bool):
        steer_deg = math.degrees(model.steering_angle)
        if abs(model.steering_angle) > 0.01:
            turn_radius_str = f"{abs(model.wheelbase / math.tan(model.steering_angle)):.2f} m"
        else:
            turn_radius_str = "Infinito"

        lines = [
            f"v: {model.velocity:+.1f} m/s | Giro (R): {turn_radius_str}",
            f"Volante: {steer_deg:+.1f} deg",
            f"Ejes (L): {model.wheelbase:.1f}m | Fricción: {model.friction_coeff:.1f}",
            "Controles: WASD/Flechas | ESPACIO=Freno | R=Reset",
        ]

        # Caja compacta de telemetría en la esquina superior derecha
        hud_bg = pygame.Surface((410, 80), pygame.SRCALPHA)
        hud_bg.fill((15, 15, 22, 220))
        self.screen.blit(hud_bg, (570, 55))
        pygame.draw.rect(self.screen, (70, 90, 120), (570, 55, 410, 80), 1, border_radius=4)

        for i, text in enumerate(lines):
            surf = self.font_pequeña.render(text, True, (230, 235, 245))
            self.screen.blit(surf, (580, 62 + i * 17))

        # Alertas de estado o panel de misión inferior
        if model.crashed:
            msg = self.font_bold.render("¡COLISION DETECTADA! Presiona [R] para reiniciar", True, (255, 90, 90))
            self.screen.blit(msg, (280, 562))
        elif won:
            msg = self.font_bold.render("¡MANIOBRA EXITOSA! Presiona [R] para repetir", True, (100, 255, 140))
            self.screen.blit(msg, (300, 562))
        else:
            hud_mision = pygame.Rect(20, 558, self.width - 40, 32)
            pygame.draw.rect(self.screen, (30, 30, 45), hud_mision, border_radius=6)
            pygame.draw.rect(self.screen, (70, 90, 120), hud_mision, 2, border_radius=6)
            texto_mision = self.font_pequeña.render("MISION: Maniobra y escapa del estacionamiento sin chocar", True, (180, 210, 240))
            self.screen.blit(texto_mision, (35, 565))