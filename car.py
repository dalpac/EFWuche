import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_SPEED = 2  # Geschwindigkeit des Autos
DECELERATION = 0.1  # Abnahme der Geschwindigkeit
MAX_FPS = 45  # Maximale Bildwiederholrate

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Car:
    def __init__(self, make, model, year,  car_width, car_height):
        self.make = make
        self.model = model
        self.year = year
        self.car_width = car_width
        self.car_height = car_height
        self.x_pos = 50 #random werte, müssen an Karte angepasst werden
        self.y_pos = 50
        self.x_speed = 0
        self.y_speed = 0

#    def start(self):
#        print(f"{self.color} {self.year} {self.make} {self.model} is starting.")

    def accelerate_x(self, mph):
        self.x_speed += mph
        print(f" {self.year} {self.make} {self.model} is accelerating in the x-direction to {self.x_speed} mph.")

    def brake_x(self, mph):
        if self.x_speed - mph >= 0:
            self.x_speed -= mph
#            print(f"{self.color} {self.year} {self.make} {self.model} is slowing down in the x-direction to {self.x_speed} mph.")
#        else:
#            print(f"{self.color} {self.year} {self.make} {self.model} has already stopped in the x-direction.")

    def accelerate_y(self, mph):
        self.y_speed += mph
#        print(f"{self.color} {self.year} {self.make} {self.model} is accelerating in the y-direction to {self.y_speed} mph.")

    def brake_y(self, mph):
        if self.y_speed - mph >= 0:
            self.y_speed -= mph
#            print(f"{self.color} {self.year} {self.make} {self.model} is slowing down in the y-direction to {self.y_speed} mph.")
#        else:
#            print(f"{self.color} {self.year} {self.make} {self.model} has already stopped in the y-direction.")

    def decelerate(self):
        # Langsames Verlangsamen, wenn keine Beschleunigung stattfindet
        if self.x_speed > DECELERATION:
            self.x_speed -= DECELERATION
        elif self.x_speed < -1*DECELERATION:
            self.x_speed += DECELERATION
        if self.y_speed > DECELERATION:
            self.y_speed -= DECELERATION
        elif self.y_speed < -1*DECELERATION:
            self.y_speed += DECELERATION

    def move(self):
        # Aktualisiere die Position des Autos basierend auf seinen x und y Geschwindigkeiten
        print(f" {self.year} {self.make} {self.model} is moving to ({self.x_pos}, {self.y_pos}).") 
    def stop(self):
        self.x_speed = 0
        self.y_speed = 0
#        print(f"{self.color} {self.year} {self.make} {self.model} has come to a complete stop.")

# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")

# Erstelle eine Instanz der Car-Klasse
my_car = Car("Toyota", "Camry", 2022, 50, 30)

# Erstelle eine Clock-Instanz, um die FPS zu steuern
clock = pygame.time.Clock()

# Spiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                my_car.accelerate_x(-CAR_SPEED)
            elif event.key == K_RIGHT:
                my_car.accelerate_x(CAR_SPEED)
            elif event.key == K_UP:
                my_car.accelerate_y(-CAR_SPEED)
            elif event.key == K_DOWN:
                my_car.accelerate_y(CAR_SPEED)
        #elif event.type == KEYUP:
            if event.key == K_SPACE:
                my_car.brake_x(CAR_SPEED)
                my_car.brake_y(CAR_SPEED)

    

    my_car.move()

    #mache dass am Feldrand das Auto stehen bleibt.
    if my_car.x_pos == 0 and my_car.x_speed < 0:
        my_car.x_speed = 0
    elif my_car.x_pos == SCREEN_WIDTH and my_car.x_speed > 0:
        my_car.x_speed = 0
    if my_car.y_pos == 0 and my_car.y_speed > 0:
        my_car.x_speed = 0
    elif my_car.y_pos == SCREEN_HEIGHT and my_car.y_speed > 0:
        my_car.y_speed = 0
    
    # Aktualisiere die Position des Autos
    my_car.x_pos += my_car.x_speed
    my_car.y_pos += my_car.y_speed

    my_car.decelerate()

    # Begrenze die Position des Autos innerhalb des Bildschirms
    my_car.x_pos = max(0, min(SCREEN_WIDTH-my_car.car_width, my_car.x_pos))
    my_car.y_pos = max(0, min(SCREEN_HEIGHT-my_car.car_height, my_car.y_pos))

    # Lösche den Bildschirm
    screen.fill(WHITE)

    # Zeichne das Auto
    pygame.draw.rect(screen, RED, (my_car.x_pos, my_car.y_pos, my_car.car_width, my_car.car_height))

    # Aktualisiere den Bildschirm
    pygame.display.flip()

    # Begrenze die Bildwiederholrate auf MAX_FPS FPS
    clock.tick(MAX_FPS)

# Beende Pygame
pygame.quit()
