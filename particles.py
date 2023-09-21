class Particle:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            for particle in self.particles:
                # Move
                # Shrink
                # Draw
                pass

    def add_particles(self, position):
        pos_x = position[0]
        pos_y = position[1]
        radius = 10
        direction = -1
        particle_circle = [[pos_x, pos_y], radius, direction]
        self.particles.append(particle_circle)

    def delete_particles(self):
        pass

