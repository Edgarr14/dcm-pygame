import pygame
from physics_model import PhysicsModel
from ui import GameUI

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    model = PhysicsModel()
    ui = GameUI()
    
    running = True
    while running:
        # dt en segundos (ej. ~0.016s a 60 FPS)
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        model.step(dt)
        ui.render(model)

    pygame.quit()

if __name__ == "__main__":
    main()