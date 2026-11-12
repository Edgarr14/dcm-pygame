import pygame
from physics_model import CarPhysicsModel
from ui2 import GameUI

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Inicializar el carro dentro del cajón de estacionamiento (x=4.0m, y=8.5m, mirando a la derecha)
    model = CarPhysicsModel(start_x_m=4.0, start_y_m=8.5, start_angle_rad=0.0)
    ui = GameUI()
    won = False

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        # 1. Eventos discretos (Cerrar ventana, reiniciar y cambiar parámetros del modelo)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    model.reset()
                    won = False
                # Modificar distancia entre ejes L (Requisito de rúbrica)
                elif event.key == pygame.K_1:
                    model.wheelbase = max(1.8, round(model.wheelbase - 0.2, 2))
                elif event.key == pygame.K_2:
                    model.wheelbase = min(4.2, round(model.wheelbase + 0.2, 2))
                # Modificar coeficiente de fricción mu (Requisito de rúbrica)
                elif event.key == pygame.K_3:
                    model.friction_coeff = max(0.1, round(model.friction_coeff - 0.1, 2))
                elif event.key == pygame.K_4:
                    model.friction_coeff = min(1.2, round(model.friction_coeff + 0.1, 2))

        # 2. Estado continuo del teclado para conducción suave
        keys = pygame.key.get_pressed()
        throttle = 0.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1.0
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            throttle = -1.0

        steer = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steer = -1.0
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steer = 1.0

        controls = {
            "throttle": throttle,
            "steer": steer,
            "brake": keys[pygame.K_SPACE]
        }

        # 3. Actualizar física si aún no ha ganado
        if not won:
            model.step(dt, controls, ui.obstacles)
            # Comprobar si el centro del carro llegó a la zona de salida sin chocar
            if not model.crashed and ui.exit_zone.collidepoint(model.get_center_pixels()):
                won = True
                model.velocity = 0.0

        # 4. Renderizar frame
        ui.render(model, won)

    pygame.quit()

if __name__ == "__main__":
    main()