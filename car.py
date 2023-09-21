
from images import cars
import pygame
from pygame.locals import *
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1200
#CAR_SPEED = 2  # Geschwindigkeit des Autos
#DECELERATION = 0.1  # Abnahme der Geschwindigkeit
MAX_FPS = 60  # Maximale Bildwiederholrate

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Car:
    def __init__(self, make, model, year, image, max_speed, brakepower, acceleration, deceleration, rotation_speed, car_width, car_height):
        self.angle = -90 #initial angle (car facing right)
        self.goal_angle = -90
        self.make = make
        self.model = model
        self.year = year
        self.image = pygame.transform.scale(image, (car_width, car_height))
        self.rotated_image = self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.max_speed = max_speed
        self.brakepower = brakepower
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.rotation_speed = rotation_speed
        self.car_width = car_width
        self.car_height = car_height
        self.x_pos = 50 #random werte, müssen an Karte angepasst werden
        self.y_pos = 50
        #self.speed[0] = 0
        #self.speed[1] = 0
        self.speed = pygame.Vector2((0,0))

#    def start(self):
#        print(f"{self.color} {self.year} {self.make} {self.model} is starting.")
    def accelerate_x(self, dir):
        if -1*self.max_speed < self.speed[0] + self.acceleration*dir < self.max_speed:
            if self.speed[0] + self.acceleration*dir <= self.max_speed or self.speed[0] + self.acceleration*dir > dir*self.max_speed:
                self.speed[0] += self.acceleration*dir
            else:
                self.speed[0] = self.max_speed*dir
        else:
            self.speed[0] = self.max_speed*dir
        #print(f" {self.model} is accelerating in the x-direction to {self.speed[0]*dir} mph.")

    def brake_x(self):
        if self.speed[0] == 0:
            pass
        elif self.speed[0] > 0:
            if self.speed[0] - self.brakepower >= 0:
                self.speed[0] -= self.brakepower
            elif self.brakepower >= self.speed[0] - self.brakepower >= 0:
                self.speed[0] = 0
        else:
            if self.speed[0] + self.brakepower <= 0:
                self.speed[0] += self.brakepower
            elif self.brakepower <= self.speed[0] - self.brakepower <= 0:
                self.speed[0] = 0
#            print(f"{self.color} {self.year} {self.make} {self.model} is slowing down in the x-direction to {self.speed[0]} mph.")
#        else:
#            print(f"{self.color} {self.year} {self.make} {self.model} has already stopped in the x-direction.")

    def accelerate_y(self, dir):
        if -1*self.max_speed < self.speed[1] + self.acceleration*dir < self.max_speed:
            if self.speed[1] + self.acceleration*dir <= self.max_speed or self.speed[1] + self.acceleration*dir >= dir*self.max_speed:
                self.speed[1] += self.acceleration*dir
            else:
                self.speed[1] = self.max_speed*dir
        else:
            self.speed[1] = self.max_speed*dir
        #print(f"{self.model} is accelerating in the y-direction to {self.speed[1]} mph.")

    def brake_y(self):
        if self.speed[1] == 0:
            pass
        elif self.speed[1] > 0:
            if self.speed[1] - self.brakepower >= 0:
                self.speed[1] -= self.brakepower
            elif self.brakepower >= self.speed[1] - self.brakepower >= 0:
                self.speed[1] = 0
        else:
            if self.speed[1] + self.brakepower <= 0:
                self.speed[1] += self.brakepower
            elif self.brakepower <= self.speed[1] - self.brakepower <= 0:
                self.speed[1] = 0
            
#            print(f"{self.color} {self.year} {self.make} {self.model} is slowing down in the y-direction to {self.speed[1]} mph.")
#        else:
#            print(f"{self.color} {self.year} {self.make} {self.model} has already stopped in the y-direction.")

    def decelerate(self):
        # Langsames Verlangsamen, wenn keine Beschleunigung stattfindet
        if self.speed[0] - self.deceleration >= 0:
            self.speed[0] -= self.deceleration
        elif self.speed[0] + self.deceleration <= 0:
            self.speed[0] += self.deceleration
        elif self.speed[1] - self.deceleration >= 0:
            self.speed[1] -= self.deceleration
        elif self.speed[1] + self.deceleration <= 0:
            self.speed[1] += self.deceleration
        else:
            self.speed[1] = 0

    def move(self, underground):
        my_car.x_pos += my_car.speed[0]*underground
        my_car.y_pos += my_car.speed[1]*underground
        

        # Rotieren Sie das Auto-Bild
        #print(f" {self.year} {self.make} {self.model} is moving to ({self.x_pos}, {self.y_pos}).") 

    def rotate_car_image(self):
        self.angle = self.angle%360
        if self.angle != self.goal_angle:
            if self.angle-self.rotation_speed<=self.goal_angle<=self.angle+self.rotation_speed or self.angle-self.rotation_speed>=self.goal_angle>=self.angle+self.rotation_speed:
                self.angle = self.goal_angle
            elif self.angle + 180 < self.goal_angle:
                self.angle -= self.rotation_speed
            elif self.angle+180 > self.goal_angle:
                self.angle += self.rotation_speed
            elif round(self.angle,0) + 180 == self.goal_angle:
                self.angle += self.rotation_speed
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        #print (-self.angle+90)

    def stop(self):
        self.speed[0] = 0
        self.speed[1] = 0
#        print(f"{self.color} {self.year} {self.make} {self.model} has come to a complete stop.")


    def test(self):
        pygame.Vector2.from_polar((1, self.angel))





########################################################################################################################






# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")


# Erstelle eine Instanz der Car-Klasse
car_image = pygame.image.load('images/cars/1.png')
my_car = Car("Rennauto", "Yellow", 2022, car_image, 10, 1, 0.5, 0.1, 3, 60, 100)
car_image = pygame.transform.scale(car_image, (my_car.car_width, my_car.car_height))
rotated_car_image = car_image


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
        my_car.goal_angle = 270
        print(my_car.goal_angle)
        my_car.rotate_car_image()
        my_car.accelerate_x(-1)
    elif keys[K_RIGHT]:
        my_car.goal_angle = 90
        my_car.rotate_car_image()
        my_car.accelerate_x(1)
    elif keys[K_UP]:
        my_car.goal_angle = 180
        my_car.rotate_car_image()
        my_car.accelerate_y(-1)
    elif keys[K_DOWN]:
        my_car.goal_angle = 0
        my_car.rotate_car_image()
        my_car.accelerate_y(1)
        #elif event.type == KEYUP:
    if keys[K_SPACE]:
        my_car.brake_x()
        my_car.brake_y()



    #mache dass am Feldrand das Auto stehen bleibt.
    if my_car.x_pos == 0 and my_car.speed[0] < 0:
        my_car.speed[0] = 0
    elif my_car.x_pos == SCREEN_WIDTH-my_car.car_width and my_car.speed[0] > 0:
        my_car.speed[0] = 0
    if my_car.y_pos == 0 and my_car.speed[1] > 0:
        my_car.speed[0] = 0
    elif my_car.y_pos == SCREEN_HEIGHT-my_car.car_height and my_car.speed[1] > 0:
        my_car.speed[1] = 0
    

    # Aktualisiere die Position des Autos
    my_car.move(1) #untergrunderkennung einfügen!!!


    my_car.decelerate()

    # Begrenze die Position des Autos innerhalb des Bildschirms
    my_car.x_pos = max(0, min(SCREEN_WIDTH-my_car.car_width, my_car.x_pos))
    my_car.y_pos = max(0, min(SCREEN_HEIGHT-my_car.car_height, my_car.y_pos))

    # Lösche den Bildschirm
    screen.fill(WHITE)

    # Zeichne das Auto
    #pygame.draw.rect(screen, RED, (my_car.x_pos, my_car.y_pos, my_car.car_width, my_car.car_height))
    screen.blit(my_car.rotated_image, (my_car.x_pos, my_car.y_pos, my_car.car_width, my_car.car_height))

    # Aktualisiere den Bildschirm
    pygame.display.flip()

    # Begrenze die Bildwiederholrate auf MAX_FPS FPS
    clock.tick(MAX_FPS)

# Beende Pygame
pygame.quit()
