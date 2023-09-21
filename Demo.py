import pygame as pg
import os
import csv
import ast
import sys
import threading
from particles import Particle

pg.init()

window = pg.display.set_mode((1100, 740))

camera_smoothness = 0.75

class Car:
    def __init__(self, manufacturer, model, year, sprite_path, position, rotation, static):
        self.manufacturer = manufacturer
        self.model = model
        self.year = year
        self.sprite_path = sprite_path
        self.sprite = pg.transform.scale(pg.image.load(f'images/cars/{self.sprite_path}.png').convert_alpha(), (50, 100))
        self.position = position
        self.rotation = 0
        self.sprite_scale = 100
        self.static = static

        self.velocity = pg.Vector2()
        self.force = pg.Vector2()
        self.torque = 0
        self.angular_velocity = 0
        self.vector = pg.Vector2.from_polar((1, self.rotation))
        self.drag_coefficient = 0.03
        self.angular_drag_coefficient = 0.1

    def step(self, tick_rate):
        self.velocity = pg.Vector2.__add__(self.velocity, (self.force / tick_rate))

        drag_force = pg.Vector2()
        drag_magnitude = -0.5 * self.drag_coefficient * self.velocity.magnitude()**2
        if self.velocity != pg.Vector2():
            drag_direction = self.velocity.normalize()  # Normalize the velocity to get the direction
            drag_force = drag_direction * drag_magnitude
        
        self.velocity = pg.Vector2.__add__(self.velocity, (drag_force))

        
        self.angular_velocity += (self.torque / tick_rate)
        angular_drag_torque = -0.5 * self.angular_drag_coefficient * self.angular_velocity

        self.angular_velocity += angular_drag_torque

        self.position += self.velocity
        self.rotation -= self.angular_velocity        

        self.force = pg.Vector2()
        self.torque = 0

    def add_force(self, force):
        self.vector = pg.Vector2.from_polar((1, self.rotation - 90))
        self.force = pg.Vector2(self.vector[0] * int(force), - self.vector[1] * int(force))

    def add_torque(self, torque):
        self.torque = torque

    def draw(self, scroll_x, scroll_y):
        if self.sprite.get_locked() != True:
            top_left = [0, 0]
            top_left[0] = self.position[0] - scroll_x
            top_left[1] = self.position[1] - scroll_y
            rotated_image = pg.transform.rotate(self.sprite, self.rotation + 180)
            new_rect = rotated_image.get_rect(center = self.sprite.get_rect(topleft = top_left).center)
            window.blit(rotated_image, new_rect.topleft)
        

class GameObject():
    def __init__(self, index, sprite_path, x, y, static):
        self.index = index
        self.sprite_path = sprite_path
        self.sprite = pg.transform.scale(pg.image.load(f'images/assets/{self.sprite_path}.png').convert_alpha(), (100, 100))   
        self.x = x
        self.y = y
        self.sprite_rotation = 0
        self.sprite_scale = 100
        self.static = static
        self.transform_move = False
        self.transform_rotate = False
        self.transform_scale = False

    def move(self, x, y):
        self.x = x - self.sprite_scale / 2
        self.y = y - self.sprite_scale / 2

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def rotate(self, delta):
        self.sprite_rotation = delta
        sprite = pg.image.load(f'images/assets/{self.sprite_path}.png').convert_alpha()
        sprite = pg.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
        self.sprite = pg.transform.rotate(sprite, delta)

        
    def scale(self, delta):
        if delta > 0:
            self.sprite_scale = delta
            sprite = pg.image.load(f'images/assets/{self.sprite_path}.png').convert_alpha()
            sprite = pg.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.sprite = pg.transform.rotate(sprite, self.sprite_rotation)

    def collidepoint(self, position):
        rect = pg.Rect(self.x, self.y, self.sprite_scale, self.sprite_scale)
        if rect.collidepoint(position):
            return True
        return False

    def display(self, window, scroll_x, scroll_y):
        window.blit(self.sprite, ((self.x - scroll_x), (self.y - scroll_y)))
        
class SpecialObject:
    def __init__(self, index, sprite_path, x, y, static):
        self.index = index
        self.sprite_path = sprite_path
        self.sprite = pg.transform.scale(pg.image.load(f'images/special/{self.sprite_path}.png').convert_alpha(), (100, 100))   
        self.x = x
        self.y = y
        self.sprite_rotation = 0
        self.sprite_scale = 100
        self.static = static
        self.transform_move = False
        self.transform_rotate = False
        self.transform_scale = False

    def move(self, x, y):
        self.x = x - self.sprite_scale / 2
        self.y = y - self.sprite_scale / 2

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def rotate(self, delta):
        self.sprite_rotation = delta
        sprite = pg.image.load(f'images/special/{self.sprite_path}.png').convert_alpha()
        sprite = pg.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
        self.sprite = pg.transform.rotate(sprite, delta)
        
    def scale(self, delta):
        if delta > 0:
            self.sprite_scale = delta
            sprite = pg.image.load(f'images/special/{self.sprite_path}.png').convert_alpha()
            sprite = pg.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.sprite = pg.transform.rotate(sprite, self.sprite_rotation)

    def collidepoint(self, position):
        rect = pg.Rect(self.x, self.y, self.sprite_scale, self.sprite_scale)
        if rect.collidepoint(position):
            return True
        return False
    
    def display(self, window, scroll_x, scroll_y):
        window.blit(self.sprite, ((self.x - scroll_x), (self.y - scroll_y)))

class Finish(SpecialObject):
    def __init__(self, index, x, y, static):
        super().__init__(index, 0, x, y, static)

class Checkpoint(SpecialObject):
    def __init__(self, index, x, y, static):
        super().__init__(index, 1, x, y, static)

class Spawnpoint(SpecialObject):
    def __init__(self, index, x, y, static):
        super().__init__(index, 2, x, y, static)

class Demo:
    def __init__(self, width, height, window):     
        self.width = width
        self.height = height
        self.window = window

        # Grid
        self.rows = 150
        self.columns = 150
        self.scroll_x = 75*80
        self.scroll_y = 75*80
        self.scroll_x_direction = 0
        self.scroll_y_direction = 0
        self.tile_size = 80

        # Pygame
        self.clock = pg.time.Clock()
        self.tick_rate = 60

        self.world_data = self.get_world_data()

        self.current_game_object = None
        self.tile_count = len(os.listdir('images/tiles/')) 
        self.tile_list = self.get_tiles()
        self.game_objects = []
        self.special_objects = []
        self.object_id = 0

        self.physics_objects = []
        self.obstacles = []
        self.player = None
        self.cars = []

        # Particles
        self.particle1 = None
        self.PARTICLE_EVENT = None

    def get_tiles(self):
        tile_list = []
        for i in range(self.tile_count):
            img = pg.image.load(f'images/tiles/{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.tile_size, self.tile_size))
            tile_list.append(img)

        return tile_list

    def get_world_data(self):
        world_data = []
        for row in range(self.rows):
            r = [-1] * self.columns
            world_data.append(r)

        for tile in range(0, self.columns):
            world_data[self.rows - 1][tile] = 0
        
        return world_data

    def load_level(self):
        self.scroll = 0
        with open(f'level_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)  

        csv_file_path = "level_object_data.csv"

        # Initialize an empty list to store the loaded data
        loaded_game_objects = []

        # Read the CSV file and populate the list of dictionaries
        with open(csv_file_path, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
        
            # Iterate through the rows in the CSV file
            for row in reader:
                # Append each row (as a dictionary) to the loaded_game_objects list
                loaded_game_objects.append(dict(row))

        # Print the loaded data
        for game_object in loaded_game_objects:
            position = ()
            try:
                result_tuple = ast.literal_eval(game_object["Position"])
                if isinstance(result_tuple, tuple):
                    position = result_tuple
                else:
                    print("The input string did not represent a valid tuple.")
            except (ValueError, SyntaxError):
                print("An error occurred while converting the string.") 

            new_game_object = GameObject(int(game_object["Index"]) + 100, int(game_object["Sprite"]), position[0], position[1], True)
            new_game_object.rotate(int(float(game_object["Rotation"])))
            new_game_object.scale(int(float(game_object["Scale"])))
            self.game_objects.append(new_game_object)
            if int(game_object["Sprite"]) != 2:
                self.obstacles.append(new_game_object)

        csv_file_path = "level_special_object_data.csv"

        loaded_special_objects = []

        # Read the CSV file and populate the list of dictionaries
        with open(csv_file_path, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
        
            # Iterate through the rows in the CSV file
            for row in reader:
                # Append each row (as a dictionary) to the loaded_game_objects list
                loaded_special_objects.append(dict(row))

        # Print the loaded data
        for special_object in loaded_special_objects:
            position = ()
            try:
                result_tuple = ast.literal_eval(special_object["Position"])
                if isinstance(result_tuple, tuple):
                    position = result_tuple
                else:
                    print("The input string did not represent a valid tuple.")
            except (ValueError, SyntaxError):
                print("An error occurred while converting the string.") 

            if int(float(special_object["Sprite"])) == 0:
                new_special_object = Finish(int(special_object["Index"]) + 100, position[0], position[1], True)
                self.player = Car("Honda", "Civic Type R", 2018, 0, pg.Vector2(new_special_object.x, new_special_object.y), 0, False)
                self.cars.append(self.player)
                self.physics_objects.append(self.player)
                self.scroll_x = self.player.position[0] - 100
                self.scroll_y = self.player.position[1] - 350

            elif int(float(special_object["Sprite"])) == 1:
                new_special_object = Checkpoint(int(special_object["Index"]) + 100, position[0], position[1], True)
            else:
                new_special_object = Spawnpoint(int(special_object["Index"]) + 100, position[0], position[1], True)

            new_special_object.rotate(int(float(special_object["Rotation"])))
            new_special_object.scale(int(float(special_object["Scale"])))
            self.special_objects.append(new_special_object)

    def draw_grid(self):
        for c in range(self.columns + 1):
            pg.draw.line(self.window, "white", (c * self.tile_size - self.scroll_x, 0), (c * self.tile_size - self.scroll_x, self.height))

        for c in range(self.rows + 1):
            pg.draw.line(self.window, "white", (0, c * self.tile_size - self.scroll_y), ((self.width), c * self.tile_size - self.scroll_y))

    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.window.blit(self.tile_list[tile], (x * self.tile_size - self.scroll_x, y * self.tile_size - self.scroll_y)) 

    def display_game_objects(self):
        for game_object in self.game_objects:
            game_object.display(self.window, self.scroll_x, self.scroll_y) 
        
        """for special_object in self.special_objects:
            special_object.display(self.window, self.scroll_x, self.scroll_y)"""

    def receive_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == self.PARTICLE_EVENT:
                self.particle1.add_particles(self.player.position)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.scroll_x_direction = -1
                if event.key == pg.K_RIGHT:
                    self.scroll_x_direction = 1
                if event.key == pg.K_UP:
                    self.scroll_y_direction = -1
                if event.key == pg.K_DOWN:
                    self.scroll_y_direction = 1

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.scroll_x_direction = 0
                if event.key == pg.K_RIGHT:
                    self.scroll_x_direction = 0
                if event.key == pg.K_UP:
                    self.scroll_y_direction = 0
                if event.key == pg.K_DOWN:
                    self.scroll_y_direction = 0
            
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.player.add_force(-20)
        if keys[pg.K_s]:
            self.player.add_force(20)   

        if keys[pg.K_a]:
            self.player.add_torque(-5)          
        
        if keys[pg.K_d]:
            self.player.add_torque(5)       

    def update_scroll(self):
        #scroll the map
        self.scroll_x += self.player.velocity[0]
        if self.scroll_x < 0:
            self.scroll_x = 0
        if self.scroll_x > ((self.columns * self.tile_size) - (self.width)):
            self.scroll_x = ((self.columns * self.tile_size) - (self.width))       

        self.scroll_y += self.player.velocity[1]
        if self.scroll_y < 0:
            self.scroll_y = 0
        if self.scroll_y > ((self.columns * self.tile_size) - (self.width)):
            self.scroll_y = ((self.columns * self.tile_size) - (self.width)) 
    
    def draw_collider(self):
        for obstacle in self.obstacles:
            #obstacle_rect = pg.Rect(obstacle.x - self.scroll_x, obstacle.y - self.scroll_y, obstacle.sprite_scale, obstacle.sprite_scale)
            obstacle_rect = obstacle.sprite.get_rect()
            obstacle_rect.x = obstacle.x - self.scroll_x
            obstacle_rect.y = obstacle.y - self.scroll_y

            player_rect = self.player.sprite.get_rect()
            player_rect.x = self.player.position[0] -self.scroll_x
            player_rect.y = self.player.position[1] -self.scroll_y
            if player_rect.colliderect(obstacle_rect):
                self.player.velocity *= -1

            pg.draw.rect(self.window, "blue", obstacle_rect)

    def start_demo(self):
        self.load_level()

        self.particle1 = Particle()
        self.PARTICLE_EVENT = pg.USEREVENT + 1
        pg.time.set_timer(self.PARTICLE_EVENT, 40)

        while True:
            # Graphics
            self.clock.tick(self.tick_rate)
            self.window.fill("black")

            # Input
            self.receive_input()

            for physics_object in self.physics_objects:
                if physics_object.static != True:
                    physics_object.step(self.tick_rate)

            # Display World
            self.draw_grid() 
            self.draw_world()      
            self.display_game_objects()     
            self.update_scroll()
            self.draw_collider()

            for car in self.cars:
                car.draw(self.scroll_x, self.scroll_y)      

            target_scroll_x = self.player.position[0] - (self.width / 2)
            target_scroll_y = self.player.position[1] - (self.height / 2)

            self.scroll_x += (target_scroll_x - self.scroll_x) * camera_smoothness
            self.scroll_y += (target_scroll_y - self.scroll_y) * camera_smoothness

            pg.display.update()                                  
    
if __name__ == "__main__":
    demo = Demo(1100, 740, window)
    demo.start_demo()
