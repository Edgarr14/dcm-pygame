class PhysicsModel:
    def __init__(self):
        # Parámetros configurables del fenómeno (se definirán al elegir el tema)
        self.gravity = 9.81
        self.time_elapsed = 0.0

    def reset(self):
        self.time_elapsed = 0.0

    def step(self, dt: float):
        """Avanza la simulación un paso de tiempo dt (en segundos)."""
        self.time_elapsed += dt