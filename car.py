
from images import cars
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1200
#CAR_SPEED = 2  # Geschwindigkeit des Autos
#DECELERATION = 0.1  # Abnahme der Geschwindigkeit
MAX_FPS = 45  # Maximale Bildwiederholrate

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Car:
    def __init__(self, make, model, year, image, max_speed, brakepower, acceleration, deceleration, car_width, car_height):
        self.make = make
        self.model = model
        self.year = year
        self.image = pygame.transform.scale(image, (car_width, car_height))
        self.max_speed = max_speed
        self.brakepower = brakepower
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.car_width = car_width
        self.car_height = car_height
        self.x_pos = 50 #random werte, müssen an Karte angepasst werden
        self.y_pos = 50
        self.x_speed = 0
        self.y_speed = 0

#    def start(self):
#        print(f"{self.color} {self.year} {self.make} {self.model} is starting.")

    def accelerate_x(self, dir):
        if -1*self.max_speed < self.x_speed + self.acceleration*dir < self.max_speed:
            if self.x_speed + self.acceleration*dir <= self.max_speed or self.x_speed + self.acceleration*dir > dir*self.max_speed:
                self.x_speed += self.acceleration*dir
            else:
                self.x_speed = self.max_speed*dir
        else:
            self.x_speed = self.max_speed*dir
        print(f" {self.year} {self.make} {self.model} is accelerating in the x-direction to {self.x_speed*dir} mph.")

    def brake_x(self):
        if self.x_speed == 0:
            pass
        elif self.x_speed > 0:
            if self.x_speed - self.brakepower >= 0:
                self.x_speed -= self.brakepower
            elif self.brakepower >= self.x_speed - self.brakepower >= 0:
                self.x_speed = 0
        else:
            if self.x_speed + self.brakepower <= 0:
                self.x_speed += self.brakepower
            elif self.brakepower <= self.x_speed - self.brakepower <= 0:
                self.x_speed = 0
#            print(f"{self.color} {self.year} {self.make} {self.model} is slowing down in the x-direction to {self.x_speed} mph.")
#        else:
#            print(f"{self.color} {self.year} {self.make} {self.model} has already stopped in the x-direction.")

    def accelerate_y(self, dir):
        if -1*self.max_speed < self.y_speed + self.acceleration*dir < self.max_speed:
            if self.y_speed + self.acceleration*dir <= self.max_speed or self.y_speed + self.acceleration*dir >= dir*self.max_speed:
                self.y_speed += self.acceleration*dir
            else:
                self.y_speed = self.max_speed*dir
        else:
            self.y_speed = self.max_speed*dir
#        print(f"{self.color} {self.year} {self.make} {self.model} is accelerating in the y-direction to {self.y_speed} mph.")

    def brake_y(self):
        if self.y_speed == 0:
            pass
        elif self.y_speed > 0:
            if self.y_speed - self.brakepower >= 0:
                self.y_speed -= self.brakepower
            elif self.brakepower >= self.y_speed - self.brakepower >= 0:
                self.y_speed = 0
        else:
            if self.y_speed + self.brakepower <= 0:
                self.y_speed += self.brakepower
            elif self.brakepower <= self.y_speed - self.brakepower <= 0:
                self.y_speed = 0
            
#            print(f"{self.color} {self.year} {self.make} {self.model} is slowing down in the y-direction to {self.y_speed} mph.")
#        else:
#            print(f"{self.color} {self.year} {self.make} {self.model} has already stopped in the y-direction.")

    def decelerate(self):
        # Langsames Verlangsamen, wenn keine Beschleunigung stattfindet
        if self.x_speed - self.deceleration >= 0:
            self.x_speed -= self.deceleration
        elif self.x_speed + self.deceleration <= 0:
            self.x_speed += self.deceleration
        elif self.y_speed - self.deceleration >= 0:
            self.y_speed -= self.deceleration
        elif self.y_speed + self.deceleration <= 0:
            self.y_speed += self.deceleration
        else:
            self.y_speed = 0

    def move(self):
        # Aktualisiere die Position des Autos basierend auf seinen x und y Geschwindigkeiten
        print(f" {self.year} {self.make} {self.model} is moving to ({self.x_pos}, {self.y_pos}).") 
    def stop(self):
        self.x_speed = 0
        self.y_speed = 0
#        print(f"{self.color} {self.year} {self.make} {self.model} has come to a complete stop.")








########################################################################################################################






# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")


# Erstelle eine Instanz der Car-Klasse
car_image = pygame.image.load('images/cars/1.png')
my_car = Car("Rennauto", "Yellow", 2022, car_image, 10, 1, 0.5, 0.1, 30, 50)
car_image = pygame.transform.scale(car_image, (my_car.car_width, my_car.car_height))


# Erstelle eine Clock-Instanz, um die FPS zu steuern
clock = pygame.time.Clock()

# Spiel-Loop
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    if keys [K_LEFT]:
        my_car.accelerate_x(-1)
    elif keys[K_RIGHT]:
        my_car.accelerate_x(1)
    elif keys[K_UP]:
        my_car.accelerate_y(-1)
    elif keys[K_DOWN]:
        my_car.accelerate_y(1)
        #elif event.type == KEYUP:
    if keys[K_SPACE]:
        my_car.brake_x()
        my_car.brake_y()



    #mache dass am Feldrand das Auto stehen bleibt.
    if my_car.x_pos == 0 and my_car.x_speed < 0:
        my_car.x_speed = 0
    elif my_car.x_pos == SCREEN_WIDTH-my_car.car_width and my_car.x_speed > 0:
        my_car.x_speed = 0
    if my_car.y_pos == 0 and my_car.y_speed > 0:
        my_car.x_speed = 0
    elif my_car.y_pos == SCREEN_HEIGHT-my_car.car_height and my_car.y_speed > 0:
        my_car.y_speed = 0
    
    #Untergrunderkennung einfügen
    # Aktualisiere die Position des Autos
    #my_car.move() #nur kommentar in cmd
    my_car.x_pos += my_car.x_speed#*underground
    my_car.y_pos += my_car.y_speed#*underground

    my_car.decelerate()

    # Begrenze die Position des Autos innerhalb des Bildschirms
    my_car.x_pos = max(0, min(SCREEN_WIDTH-my_car.car_width, my_car.x_pos))
    my_car.y_pos = max(0, min(SCREEN_HEIGHT-my_car.car_height, my_car.y_pos))

    # Lösche den Bildschirm
    screen.fill(WHITE)

    # Zeichne das Auto
    #pygame.draw.rect(screen, RED, (my_car.x_pos, my_car.y_pos, my_car.car_width, my_car.car_height))
    screen.blit(car_image, (my_car.x_pos, my_car.y_pos, my_car.car_width, my_car.car_height))

    # Aktualisiere den Bildschirm
    pygame.display.flip()

    # Begrenze die Bildwiederholrate auf MAX_FPS FPS
    clock.tick(MAX_FPS)

# Beende Pygame
pygame.quit()
