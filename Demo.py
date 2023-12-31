import pygame as pg
import os
import csv
import ast
import sys
import math
from car import Car
from Main_Menue import Button
from Main_Menue import Main_Menu

pg.init()

window = pg.display.set_mode((1100, 740))

camera_smoothness = 0.75


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

class Demo:
    def __init__(self, width, height, window, car_index):     
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
        self.space = []

        self.counter = 3
        self.countdown_text = '3'.rjust(3)
        self.font = pg.font.Font('images/Fonts/foo.otf', 100)
        self._circle_cache = {}
        self.started = False
        self.fastest_time = 0
        self.elapsed_time_before_lap = 0
        self.checkpoints = []
        self.current_checkpoint = -1
        self.laps = 0
        self.x = False
        self.car_index = car_index

        # Buttons
        button_img = pg.transform.scale(pg.image.load('images/Button_sidemenu.png').convert_alpha(), (800, 180))

        self.continue_button = Button(image=button_img, pos=(self.width / 2,100),text_input="Continue", font=pg.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
        self.main_menue_button = Button(image=button_img, pos=(self.width / 2,300),text_input="Main Menue", font=pg.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
        self.quit_game_button = Button(image=button_img, pos=(self.width / 2,500),text_input="QUIT", font=pg.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")

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
                self.player = Car("The Oldtimer of Dracula", "purple", 1923, pg.image.load(f'images/cars/{self.car_index}.png'), 5, 0.05, 3 / self.tick_rate, 0.02, 1.5, 60, 100, new_special_object.x, new_special_object.y)
                self.cars.append(self.player)
                self.physics_objects.append(self.player)
                self.scroll_x = self.player.x_pos - 100
                self.scroll_y = self.player.y_pos - 350

            elif int(float(special_object["Sprite"])) == 1:
                new_special_object = Checkpoint(int(special_object["Index"]) + 100, position[0], position[1], True)
                self.checkpoints.append(new_special_object)

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
        
        for special_object in self.special_objects:
            if type(special_object) == Finish:
                special_object.display(self.window, self.scroll_x, self.scroll_y)

        for checkpoint in self.checkpoints:
                if self.checkpoints.index(checkpoint) == self.current_checkpoint + 1:
                    checkpoint.display(self.window, self.scroll_x, self.scroll_y)


    def receive_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.USEREVENT:
                self.counter -= 1
                if self.countdown_text == 'GO!':
                    self.started = True
                    self.font = pg.font.Font('images/Fonts/foo.otf', 25)
                else:
                    self.countdown_text = str(self.counter).rjust(3) if self.counter > 0 else 'GO!'

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    if self.x == True:
                        self.x = False
                    else: 
                        self.x = True

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
        if keys [pg.K_LEFT]:
            self.player.goal_angle = 270
            self.player.rotate_car_image()
            self.player.accelerate()
        elif keys[pg.K_RIGHT]:
            self.player.goal_angle = 90
            self.player.rotate_car_image()
            self.player.accelerate()
        elif keys[pg.K_UP]:
            self.player.goal_angle = 180
            self.player.rotate_car_image()
            self.player.accelerate()
        elif keys[pg.K_DOWN]:
            self.player.goal_angle = 0
            self.player.rotate_car_image()
            self.player.accelerate()
        #elif event.type == KEYUP:
        if keys[pg.K_SPACE]:
            self.player.brake()
  

    def update_scroll(self):
        #scroll the map
        self.scroll_x += self.player.speed[0]
        if self.scroll_x < 0:
            self.scroll_x = 0
        if self.scroll_x > ((self.columns * self.tile_size) - (self.width)):
            self.scroll_x = ((self.columns * self.tile_size) - (self.width))       

        self.scroll_y += self.player.speed[1]
        if self.scroll_y < 0:
            self.scroll_y = 0
        if self.scroll_y > ((self.columns * self.tile_size) - (self.width)):
            self.scroll_y = ((self.columns * self.tile_size) - (self.width)) 
    
    def check_collisions(self):
        for obstacle in self.obstacles:
            #obstacle_rect = pg.Rect(obstacle.x - self.scroll_x, obstacle.y - self.scroll_y, obstacle.sprite_scale, obstacle.sprite_scale)
            obstacle_rect = obstacle.sprite.get_rect()
            obstacle_rect.x = obstacle.x - self.scroll_x
            obstacle_rect.y = obstacle.y - self.scroll_y

            mask = pg.mask.from_surface(self.player.rotated_image)
            player_rect = mask.get_rect()
            player_rect.x = self.player.x_pos - self.scroll_x
            player_rect.y = self.player.y_pos -self.scroll_y

            player_rect.center = self.player.rotated_image.get_rect().center
            player_rect.center = (player_rect.center[0] + self.width / 2 + 15, player_rect.center[1] + self.height / 2 + 5)
            player_rect.size = (50, 50)
            if player_rect.colliderect(obstacle_rect):
                crash = pg.mixer.find_channel
                pg.mixer.music.load("crashing.wav")
                pg.mixer.music.set_volume(0.8)
                pg.mixer.music.play()
                self.player.total_speed *= -1
                
            
            
            #pg.draw.rect(self.window, "blue", obstacle_rect)
            #pg.draw.rect(self.window, "green", (player_rect))

        for special_object in self.special_objects:
            special_object_rect = special_object.sprite.get_rect()
            special_object_rect.x = special_object.x - self.scroll_x
            special_object_rect.y = special_object.y - self.scroll_y

            mask = pg.mask.from_surface(self.player.rotated_image)
            player_rect = mask.get_rect()
            player_rect.x = self.player.x_pos - self.scroll_x
            player_rect.y = self.player.y_pos -self.scroll_y

            if player_rect.colliderect(special_object_rect):
                if type(special_object) == Finish:
                    if self.current_checkpoint == len(self.checkpoints) - 1:
                        self.current_checkpoint = -1
                        self.laps += 1
                        
                        if self.fastest_time == 0:
                            self.fastest_time = pg.time.get_ticks()
                        else:
                            if self.fastest_time > pg.time.get_ticks() - self.elapsed_time_before_lap:
                                self.fastest_time = pg.time.get_ticks() - self.elapsed_time_before_lap

                        self.elapsed_time_before_lap = pg.time.get_ticks()

                if type(special_object) == Checkpoint:
                    if self.checkpoints.index(special_object) == self.current_checkpoint + 1:
                        self.current_checkpoint = self.checkpoints.index(special_object)

    def count_down(self):
        text = self.font.render(self.countdown_text, True, "black")
        text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
        self.window.blit(self.render(self.countdown_text, self.font, (255, 95, 31), (0, 0, 0)), text_rect)

    def _circlepoints(self, r):
        r = int(round(r))
        if r in self._circle_cache:
            return self._circle_cache[r]
        x, y, e = r, 0, 1 - r
        self._circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def render(self, text, font, gfcolor=pg.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pg.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(textsurface, (opx, opx))
        return surf

    def stopwatch(self):
        ticks=pg.time.get_ticks()
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 24)
        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        text = self.font.render(out, True, "black")
        text_rect = text.get_rect(topright=(self.width, 0))
        other_text = self.font.render('TIME ELAPSED: 00:00:000', True, "black")
        other_text_rect = other_text.get_rect(topright=(self.width, 0))
        window.blit(self.render("TIME ELAPSED: ", self.font, (255, 95, 31), (0, 0, 0)), other_text_rect)
        window.blit(self.render(out, self.font, (255, 95, 31), (0, 0, 0)), text_rect)

        lap_text = self.font.render(f"Lap: {self.laps}/3", True, "black")
        text_rect = lap_text.get_rect(topright=(self.width, 50))
        window.blit(self.render(f"Lap: {self.laps}/3", self.font, (255, 95, 31), (0, 0 ,0)), text_rect)

        millis=self.fastest_time%1000
        seconds=int(self.fastest_time/1000 % 60)
        minutes=int(self.fastest_time/60000 % 24)
        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        fastest_lap_text = self.font.render(f'Fastest Lap: {out}', True, "black")
        text_rect = fastest_lap_text.get_rect(topright=(self.width, 100))
        window.blit(self.render(f'Fastest Lap: {out}', self.font, (255, 95, 31), (0, 0, 0)), text_rect)

    def rotate(self, point):
    # First translates the point to have the origin at your sprite's center.
        origin = self.player.sprite.get_rect().center
        originPoint = (point[0] - origin[0], point[1] - origin[1])
        # Then we rotate the point using basic trigonometry.
        rotatedX = originPoint[0] * math.cos(self.player.rotation) - originPoint[1] * math.sin(self.player.rotation)
        rotatedY = originPoint[0] * math.sin(self.player.rotation) + originPoint[1] * math.cos(self.player.rotation)

        # Finally we need to translate the point back to world space.
        return [rotatedX + origin[0], rotatedY + origin[1]] 

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col) 
        img_rect = img.get_rect(center=(x, y))      
        self.window.blit(img, img_rect)

    def start_demo(self):
        self.load_level()
        #pg.mixer.music.load("driving-in-a-car-6227.mp3")
        #pg.mixer.music.set_volume(0.8)
        #pg.mixer.music.play(3,0.0,1000)
        pg.time.set_timer(pg.USEREVENT, 1000)

        while True:
            # Graphics
            self.window.fill("black")

            # Input
            self.receive_input()

            # Display World
            self.draw_grid() 
            self.draw_world()
                  
            self.display_game_objects()     
            self.update_scroll()
            self.check_collisions()          

            self.player.move(self.window, self.scroll_x, self.scroll_y)   
            self.player.decelerate()

            target_scroll_x = self.player.x_pos - (self.width / 2)
            target_scroll_y = self.player.y_pos - (self.height / 2)

            self.scroll_x += (target_scroll_x - self.scroll_x) * camera_smoothness
            self.scroll_y += (target_scroll_y - self.scroll_y) * camera_smoothness

            if self.started == False:
                self.count_down()
            else:
                self.stopwatch()

            if self.x == True:
                if self.continue_button.draw() == True:
                    self.x=False
        
                if self.main_menue_button.draw()== True:
                    main_menue = Main_Menu(1100,740,self.window)
                    main_menue.main_menu()
                
                if self.quit_game_button.draw() == True:
                    pg.quit()

            pg.display.update()    
            self.clock.tick(self.tick_rate)                              
    
if __name__ == "__main__":
    demo = Demo(1100, 740, window)
    demo.start_demo()

