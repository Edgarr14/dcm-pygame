import math
import pygame
from pygame.math import Vector2

class CarPhysicsModel:
    # Escala de conversión: 1 metro de la vida real = 35 píxeles en pantalla
    PIXELS_PER_METER = 35.0

    def __init__(self, start_x_m: float = 5.0, start_y_m: float = 5.0, start_angle_rad: float = 0.0):
        # --- PARÁMETROS MODIFICABLES (Para los controles de la rúbrica) ---
        self.mass = 1200.0           # Masa del vehículo (kg)
        self.wheelbase = 2.6         # Distancia entre ejes L (m) - define el radio de giro
        self.friction_coeff = 0.7    # Coeficiente de rozamiento (asfalto seco ~0.7, mojado ~0.3)
        self.max_steer_deg = 35.0    # Ángulo máximo de las ruedas delanteras (grados)

        # Dimensiones reales del carro (metros)
        self.car_length = 4.2
        self.car_width = 1.8

        # Constantes físicas y del motor
        self.gravity = 9.81
        self.engine_force = 6500.0   # Fuerza de tracción (N)
        self.brake_force = 12000.0   # Fuerza de frenado (N)
        self.steer_speed = 1.8       # Velocidad con la que gira el volante (rad/s)

        # Estado inicial para poder reiniciar
        self.initial_state = (start_x_m, start_y_m, start_angle_rad)
        self.reset()

    def reset(self):
        """Reinicia la posición y variables cinemáticas del vehículo."""
        self.x, self.y, self.heading = self.initial_state
        self.velocity = 0.0          # Velocidad longitudinal v (m/s)
        self.acceleration = 0.0      # Aceleración actual (m/s^2)
        self.steering_angle = 0.0    # Ángulo actual de las ruedas delanteras delta (rad)
        self.crashed = False

    def step(self, dt: float, controls: dict, obstacles_rects_px: list[pygame.Rect] = None):
        """
        Avanza la simulación un paso dt (segundos).
        controls: {'throttle': float (-1 a 1), 'steer': float (-1 a 1), 'brake': bool}
        """
        if self.crashed:
            return

        # 1. Actualizar dirección de las ruedas delanteras (delta)
        max_steer_rad = math.radians(self.max_steer_deg)
        steer_input = controls.get("steer", 0.0)
        if steer_input != 0:
            self.steering_angle += steer_input * self.steer_speed * dt
            self.steering_angle = max(-max_steer_rad, min(max_steer_rad, self.steering_angle))
        else:
            # Retorno gradual del volante al centro
            self.steering_angle *= max(0.0, 1.0 - 6.0 * dt)

        # 2. Calcular fuerzas longitudinales (Motor, Freno y Fricción)
        throttle = controls.get("throttle", 0.0)  # 1.0 adelante, -1.0 reversa
        braking = controls.get("brake", False)

        f_traction = throttle * self.engine_force

        # Fuerza de fricción oponiéndose al movimiento
        if abs(self.velocity) > 0.05:
            sign_v = 1.0 if self.velocity > 0 else -1.0
            f_friction = self.friction_coeff * self.mass * self.gravity * 0.15 * sign_v
            f_brake = (self.brake_force * self.friction_coeff * sign_v) if braking else 0.0
        else:
            f_friction = 0.0
            f_brake = 0.0
            if throttle == 0.0 or braking:
                self.velocity = 0.0

        # Segunda Ley de Newton: a = F_neta / m
        f_net = f_traction - f_friction - f_brake
        self.acceleration = f_net / self.mass

        # 3. Integración de Euler Semi-Implícito
        self.velocity += self.acceleration * dt
        # Limitar velocidad máxima en parking (ej. 8 m/s Adelante, 4 m/s Reversa)
        self.velocity = max(-4.0, min(8.0, self.velocity))

        # Modelo Cinemático de Bicicleta
        # El carro solo cambia su orientación (heading) si se está moviendo (v != 0)
        angular_velocity = (self.velocity / self.wheelbase) * math.tan(self.steering_angle)
        self.heading += angular_velocity * dt

        self.x += self.velocity * math.cos(self.heading) * dt
        self.y += self.velocity * math.sin(self.heading) * dt

        # 4. Verificar colisiones si el frontend envía obstáculos
        if obstacles_rects_px:
            self.crashed = self.check_collision(obstacles_rects_px)
            if self.crashed:
                self.velocity = 0.0

    # --- CONTRATO PARA EL FRONTEND (UI) ---

    def get_center_pixels(self) -> tuple[float, float]:
        """Devuelve el centro (x, y) del carro convertido a píxeles."""
        return (self.x * self.PIXELS_PER_METER, self.y * self.PIXELS_PER_METER)

    def get_corners_pixels(self) -> list[tuple[float, float]]:
        """
        Calcula las 4 esquinas rotadas del carro en píxeles (Oriented Bounding Box).
        Tu compañera puede usar esto directamente con pygame.draw.polygon() y para colisiones.
        """
        cx, cy = self.get_center_pixels()
        half_l = (self.car_length * self.PIXELS_PER_METER) / 2.0
        half_w = (self.car_width * self.PIXELS_PER_METER) / 2.0
        angle_deg = math.degrees(self.heading)

        # Vértices locales respecto al centro antes de rotar
        local_corners = [
            Vector2( half_l, -half_w),  # Delantera izquierda
            Vector2( half_l,  half_w),  # Delantera derecha
            Vector2(-half_l,  half_w),  # Trasera derecha
            Vector2(-half_l, -half_w),  # Trasera izquierda
        ]

        # Rotar cada esquina y trasladar al centro en píxeles
        return [(cx + c.rotate(angle_deg).x, cy + c.rotate(angle_deg).y) for c in local_corners]

    def check_collision(self, obstacles_rects_px: list[pygame.Rect]) -> bool:
        """
        Verifica si alguna esquina o borde del carro choca contra los rectángulos
        de paredes u otros carros estacionados.
        """
        corners = self.get_corners_pixels()
        for rect in obstacles_rects_px:
            # 1. ¿Alguna de las 4 esquinas del carro entró en el obstáculo?
            for pt in corners:
                if rect.collidepoint(pt):
                    return True
            # 2. ¿Alguna de las 4 líneas del chasis corta el rectángulo del obstáculo?
            for i in range(4):
                p1 = corners[i]
                p2 = corners[(i + 1) % 4]
                if rect.clipline(p1, p2):
                    return True
        return False