import pygame
from pygame.locals import *
import math
import csv


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1200
MAX_FPS = 60  # Maximale Bildwiederholrate

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Car:
    def __init__(self, name, color, year, image, max_speed, brakepower, acceleration, deceleration, rotation_speed, car_width, car_height, x_pos, y_pos):
        self.angle = 90 #initial angle (car facing right)
        self.goal_angle = 90
        self.name = name
        self.color = color
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
        self.x_pos = x_pos #random werte, müssen an Karte angepasst werden
        self.y_pos = y_pos
        self.speed = pygame.Vector2((0,0))
        self.total_speed = 0



    def underground(self):
        if unknown.world_data[self.x_pos, self.y_pos] == 0:
            return 0.7
        elif unknown.world_data[self.x_pos, my_car.y_pos] == 1:
            return 1
        elif unknown.world_data[my_car.x_pos, my_car.y_pos] == 4:
            return 2

    def accelerate(self):
        if -1*self.max_speed < self.total_speed < self.max_speed:
            self.total_speed += self.acceleration #* underground.tiles()
        self.speed[0] = math.sin(math.radians(self.angle)) * self.total_speed 
        self.speed[1] = math.cos(math.radians(self.angle)) * self.total_speed
        #print("x_Speed: ", self.speed[0], "angle: ", self.angle, "cos: ", math.cos(self.angle))
        

    
    def brake(self):
        if self.total_speed-self.brakepower <= 0:
            self.total_speed = 0
        else:
            self.total_speed -= self.brakepower
        self.speed[0] = math.sin(math.radians(self.angle)) * self.total_speed 
        self.speed[1] = math.cos(math.radians(self.angle)) * self.total_speed
       
    def decelerate(self):
        # Langsames Verlangsamen, wenn keine Beschleunigung stattfindet
        if self.total_speed + self.deceleration <= 0:
            self.total_speed += self.deceleration #/ underground.tiles()
        elif self.total_speed - self.deceleration >= 0:
            self.total_speed -= self.deceleration #/ underground.tiles()
        else:
            self.total_speed = 0
        self.speed[0] = math.sin(math.radians(self.angle)) * self.total_speed 
        self.speed[1] = math.cos(math.radians(self.angle)) * self.total_speed 
 


    def move(self, screen, scroll_x, scroll_y):
        self.x_pos += self.speed[0]
        self.y_pos += self.speed[1]

        if self.x_pos > 7289:
            self.x_pos = 7289
        
        screen.blit(self.rotated_image, (self.x_pos - scroll_x, self.y_pos - scroll_y, self.car_width, self.car_height))
        print(self.x_pos, self.y_pos)
        

        # Rotieren Sie das Auto-Bild
        #print(f" {self.year} {self.name} {self.color} is moving to ({self.x_pos}, {self.y_pos}).") 

    def rotate_car_image(self):
        self.angle = 360 + self.angle #to get rid of negative numbers.
        self.angle = abs(self.angle%360)
        if round(self.angle,0) == self.goal_angle:
            self.angle == self.goal_angle
        if self.angle != self.goal_angle:
            if self.goal_angle == 0:
                if self.angle <= 180:
                    self.angle -= self.rotation_speed
                elif self.angle > 180:
                    self.angle += self.rotation_speed
            elif self.goal_angle == 90:
                if 90 < self.angle <= 270:
                    self.angle -= self.rotation_speed
                elif self.angle > 270 or self.angle < 90:
                    self.angle += self.rotation_speed
            elif self.goal_angle == 180:
                if 180 < self.angle <= 360:
                    self.angle -= self.rotation_speed
                elif 0 <= self.angle < 180:
                    self.angle += self.rotation_speed
            elif self.goal_angle == 270:
                if 270 < self.angle <= 360 or self.angle <= 90:
                    self.angle -= self.rotation_speed
                elif 90 < self.angle < 270:
                    self.angle += self.rotation_speed

        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        #print (-self.angle+90)

    def stop(self):
        self.speed[0] = 0
        self.speed[1] = 0
#        print(f"{self.color} {self.year} {self.name} {self.color} has come to a complete stop.")




########################################################################################################################

# Erstelle eine Instanz der Car-Klasse

#my_car = car.Car(self, name, color, year, image, max_speed, brakepower, acceleration, deceleration, rotation_speed, car_width, car_height)
"""violetto = Car("The Oldtimer of Dracula", "purple", 1923, pygame.image.load('images/cars/0.png'), 10, 1, 0.5, 0.2, 3, 60, 100)
blue = Car("The killer of Elon Musk", "blue", 2024, pygame.image.load('images/cars/1.png'), 17, 1, 0.9, 0.05, 2, 60, 100)
yellow = Car("The cute racer", "blue", 1990, pygame.image.load('images/cars/2.png'), 15, 1, 0.8, 0.1, 4, 60, 100)

my_car = blue 


##############################################################################################


# Erstelle das Pygame-Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")



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
        my_car.rotate_car_image()
        my_car.accelerate()
    elif keys[K_RIGHT]:
        my_car.goal_angle = 90
        my_car.rotate_car_image()
        my_car.accelerate()
    elif keys[K_UP]:
        my_car.goal_angle = 180
        my_car.rotate_car_image()
        my_car.accelerate()
    elif keys[K_DOWN]:
        my_car.goal_angle = 0
        my_car.rotate_car_image()
        my_car.accelerate()
        #elif event.type == KEYUP:
    if keys[K_SPACE]:
        my_car.brake()



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
    my_car.move() #untergrunderkennung einfügen!!!


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
pygame.quit()"""
