import pygame as pg
import sys
from button import Button
import os
import csv
import ast

pg.init()

window = pg.display.set_mode((1100, 740))

class GameObject:
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

class Editor:
    def __init__(self, width, height, window):
        # Editor Layout     
        self.width = width
        self.height = height
        self.window = window
        self.bottom_margin = 100
        self.right_margin = 300

        # Grid
        self.rows = 150
        self.columns = 150
        self.scroll_x = 75*80
        self.scroll_y = 75*80
        self.scroll_speed = 1
        self.scroll_x_direction = 0
        self.scroll_y_direction = 0
        self.tile_size = 80
        self.tile_count = len(os.listdir('images/tiles/'))
        self.asset_count = len(os.listdir('images/assets/'))
        self.special_count= len(os.listdir('images/special'))
        self.draw = False

        # Pygame
        self.clock = pg.time.Clock()
        self.tick_rate = 60

        # Assets
        self.tile_list, self.asset_list, self.special_list = self.import_assets()
        self.tile_button_list, self.asset_button_list, self.special_button_list = self.create_buttons()
        self.world_data = self.get_world_data()

        self.current_tile = 0
        self.active_asset = None
        self.current_game_object = None 
        self.game_objects = []
        self.special_objects = []
        self.object_id = 0

        # Transform
        self.move_img = pg.transform.scale(pg.image.load('images/move.png'), (50, 50))
        self.rotate_img = pg.transform.scale(pg.image.load('images/rotate.png'), (50, 50))
        self.scale_img = pg.transform.scale(pg.image.load('images/scale.png'), (50, 50))

        # Save / Load
        self.button_img = pg.transform.scale(pg.image.load('images/button.png').convert_alpha(), (300, 50))
        self.save_button = Button(image=self.button_img, 
                             pos=(self.width - (self.right_margin / 2), 650), 
                             text_input="SAVE", font=pg.font.Font('images/Fonts/foo.otf', 30), 
                             base_color="#000000", hovering_color="#333333")
        
        self.load_button = Button(image=self.button_img, 
                             pos=(self.width - (self.right_margin / 2), 700), 
                             text_input="LOAD", font=pg.font.Font('images/Fonts/foo.otf', 30), 
                             base_color="#000000", hovering_color="#333333")

    def import_assets(self):
        tile_list = []
        for i in range(self.tile_count):
            img = pg.image.load(f'images/tiles/{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.tile_size / 2, self.tile_size / 2))
            tile_list.append(img) 

        asset_list = []
        for i in range(self.asset_count):
            img = pg.image.load(f'images/assets/{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.tile_size  / 2, self.tile_size / 2))
            asset_list.append(img)

        special_list = []
        for i in range(self.special_count):
            img = pg.image.load(f'images/special/{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.tile_size / 2, self.tile_size / 2))
            special_list.append(img)

        return tile_list, asset_list, special_list
    
    def create_buttons(self):
        #make a button list
        tile_list = []
        tile_col = 0
        tile_row = 0       
        for i in range(len(self.tile_list)):
            tile_button = Button(image=self.tile_list[i], pos=((self.width- self.right_margin) + (75 * tile_col) + 50, 75 * tile_row + 100),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")
            tile_list.append(tile_button)
            tile_col += 1
            if tile_col == 3:
                tile_row += 1
                tile_col = 0

        asset_list = []
        asset_col = 0
        asset_row = 0
        for i in range(len(self.asset_list)):
            asset_button = Button(image=self.asset_list[i], pos=((self.width- self.right_margin) + (75 * asset_col) + 50, 75 * asset_row + 300),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")
            asset_list.append(asset_button)
            asset_col += 1
            if asset_col == 3:
                asset_row += 1
                asset_col = 0

        special_list = []
        special_col = 0
        special_row = 0
        for i in range(len(self.special_list)):
            special_button = Button(image=self.special_list[i], pos=((self.width- self.right_margin) + (75 * special_col) + 50, 75 * special_row + 500),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")
            special_list.append(special_button)
            special_col += 1
            if special_col == 3:
                special_row += 1
                special_col = 0

        return tile_list, asset_list, special_list
    
    def get_world_data(self):
        world_data = []
        for row in range(self.rows):
            r = [-1] * self.columns
            world_data.append(r)

        for tile in range(0, self.columns):
            world_data[self.rows - 1][tile] = 0
        
        return world_data
        
    def draw_grid(self):
        for c in range(self.columns + 1):
            pg.draw.line(self.window, "white", (c * self.tile_size - self.scroll_x, 0), (c * self.tile_size - self.scroll_x, self.height))

        for c in range(self.rows + 1):
            pg.draw.line(self.window, "white", (0, c * self.tile_size - self.scroll_y), ((self.width - self.right_margin), c * self.tile_size - self.scroll_y))

    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.window.blit(pg.transform.scale(self.tile_list[tile], (self.tile_size, self.tile_size)), (x * self.tile_size - self.scroll_x, y * self.tile_size - self.scroll_y))

    def draw_panel(self):
        pg.draw.rect(self.window, pg.color.Color(85,107,47), (self.width - self.right_margin, 0, self.right_margin, self.height))
        self.draw_text("Tiles", pg.font.Font('images/Fonts/foo.otf', 50), "black", self.width - (self.right_margin / 2), 50)
        self.draw_text("Assets", pg.font.Font('images/Fonts/foo.otf', 50), "black", self.width - (self.right_margin / 2), 250)
        self.draw_text("Special", pg.font.Font('images/Fonts/foo.otf', 50), "black", self.width - (self.right_margin / 2), 450)

        for button in self.tile_button_list:
            button.update(self.window)

        for button in self.asset_button_list:
            button.update(self.window)

        for button in self.special_button_list:
            button.update(self.window)

        # Get Selected
        button_count = 0
        button_list = self.tile_button_list
        for button_count, i in enumerate(button_list):
            if i.draw(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                self.current_tile = button_count
                self.current_game_object = None
                self.draw = True                

        # Highlight the selected tile
        if self.draw == True:
            pg.draw.rect(self.window, "red", button_list[self.current_tile].rect, 3)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col) 
        img_rect = img.get_rect(center=(x, y))      
        self.window.blit(img, img_rect)

    def update_scroll(self):
        #scroll the map
        self.scroll_x += 5 * self.scroll_x_direction
        if self.scroll_x < 0:
            self.scroll_x = 0
        if self.scroll_x > ((self.columns * self.tile_size) - (self.width - self.right_margin)):
            self.scroll_x = ((self.columns * self.tile_size) - (self.width - self.right_margin))       

        self.scroll_y += 5 * self.scroll_y_direction
        if self.scroll_y < 0:
            self.scroll_y = 0
        if self.scroll_y > ((self.columns * self.tile_size) - (self.width - self.right_margin)):
            self.scroll_y = ((self.columns * self.tile_size) - (self.width - self.right_margin))           
            
    def update_tile(self):           
        pos = pg.mouse.get_pos()
        x = (pos[0] + self.scroll_x) // self.tile_size
        y = (pos[1] + self.scroll_y) // self.tile_size    

        if (self.draw == True):
            #check that the coordinates are within the tile area
            if (self.active_asset == None):
                if pos[0] < (self.width - self.right_margin) and pos[1] < self.height:
                    #update tile value                
                    if pg.mouse.get_pressed()[0] == 1:
                        if self.world_data[y][x] != self.current_tile:
                            self.world_data[y][x] = self.current_tile
                    if pg.mouse.get_pressed()[2] == 1:
                        self.world_data[y][x] = -1  

    def receive_input(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DELETE:
                        self.delete_game_object()

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

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.active_asset == None:  
                            self.drag(event) 

                    if self.save_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                        self.save_level()

                    if self.load_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                        self.load_level()                               
                                                                
                if event.type == pg.MOUSEMOTION:
                    if self.active_asset != None:
                        if self.active_asset.transform_move:
                            self.active_asset.move(event.pos[0] + self.scroll_x, event.pos[1] + self.scroll_y)  

                        if self.active_asset.transform_rotate:
                            self.active_asset.rotate(event.pos[0] + self.scroll_x - self.active_asset.x)

                        if self.active_asset.transform_scale:
                            self.active_asset.scale((event.pos[0] + self.scroll_x - self.active_asset.x) + (event.pos[1] + self.scroll_y - self.active_asset.y))  

                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.active_asset != None:
                            self.drop()             

    def drag(self, event):
        if self.current_game_object != None:  
            if self.move_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                self.start_moving_object()                                    

            elif self.rotate_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                self.start_rotating_object()                                    

            elif self.scale_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                self.start_scaling_object()

            else:
                self.current_game_object = None

        else:  
            self.select_gameobject()    
            # Or                               
            self.create_new_gameobject(event) 

    def drop(self):  

        if pg.mouse.get_pos()[0] < self.width - self.right_margin:                                
            self.active_asset.transform_move = False
            self.active_asset.transform_rotate = False
            self.active_asset.transform_scale = False                                
            self.current_game_object = self.active_asset
            self.current_game_object.static = True
            if type(self.current_game_object) == GameObject:
                self.game_objects.append(self.current_game_object)
                self.object_id += 1
                self.active_asset = None
            else:
                self.special_objects.append(self.current_game_object)
                self.object_id += 1
                self.active_asset = None           

    def create_new_gameobject(self, event):
        for num, asset in enumerate(self.asset_button_list):
            if asset.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):                                   
                self.active_asset = GameObject(self.object_id, num, event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y, False) 
                self.object_id += 1
                self.active_asset.transform_move = True
                self.draw = False

        for  num, special_object in enumerate(self.special_button_list):
            if special_object.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                if num == 0:
                    self.active_asset = Finish(self.object_id, event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y, False)
                
                elif num == 1:               
                    self.active_asset = Checkpoint(self.object_id, event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y, False)

                else:
                    self.active_asset = Spawnpoint(self.object_id, event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y, False)

                self.object_id += 1
                self.active_asset.transform_move = True
                self.draw = False

    def start_moving_object(self):
        self.active_asset = self.current_game_object
        self.object_id += 1
        self.active_asset.transform_move = True

        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
            self.current_game_object = None

    def start_rotating_object(self):
        self.active_asset = self.current_game_object
        self.object_id += 1
        self.active_asset.transform_rotate = True

        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
            self.current_game_object = None

        if self.special_objects.__contains__(self.current_game_object):
            self.special_objects.remove(self.current_game_object)
            self.current_game_object = None

    def start_scaling_object(self):
        self.active_asset = self.current_game_object 
        self.object_id += 1                                   
        self.active_asset.transform_scale = True

        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
            self.current_game_object = None

        if self.special_objects.__contains__(self.current_game_object):
            self.special_objects.remove(self.current_game_object)
            self.current_game_object = None

    def select_gameobject(self):
        for game_object in self.game_objects:
            if game_object.static == True:
                mouse_pos = (pg.mouse.get_pos()[0] + self.scroll_x, pg.mouse.get_pos()[1] + self.scroll_y)
                if game_object.collidepoint(mouse_pos):                           
                    self.current_game_object = game_object
                    self.draw = False

        for special_object in self.special_objects:
            if special_object.static == True:
                mouse_pos = (pg.mouse.get_pos()[0] + self.scroll_x, pg.mouse.get_pos()[1] + self.scroll_y)
                if special_object.collidepoint(mouse_pos):                           
                    self.current_game_object = special_object
                    self.draw = False   

    def delete_game_object(self):
        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
        else:
            self.special_objects.remove(self.current_game_object)
        self.current_game_object = None

    def display_game_objects(self):
        for game_object in self.game_objects:
            game_object.display(self.window, self.scroll_x, self.scroll_y) 

        for special_object in self.special_objects:
            special_object.display(self.window, self.scroll_x, self.scroll_y)

    def display_transform(self):
        if self.current_game_object != None:
            self.move_button = Button(image=self.move_img, pos=(self.current_game_object.x - self.scroll_x + (self.current_game_object.sprite_scale / 2), self.current_game_object.y + (self.current_game_object.sprite_scale / 2) - self.scroll_y- 50),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")
            self.rotate_button = Button(image=self.rotate_img, pos=(self.current_game_object.x + 75 - self.scroll_x + (self.current_game_object.sprite_scale / 2), self.current_game_object.y + (self.current_game_object.sprite_scale / 2) - self.scroll_y - 50),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")
            self.scale_button = Button(image=self.scale_img, pos=(self.current_game_object.x + 150 - self.scroll_x + (self.current_game_object.sprite_scale / 2), self.current_game_object.y + (self.current_game_object.sprite_scale / 2) - self.scroll_y - 50),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")

            self.move_button.update(self.window)
            self.rotate_button.update(self.window)
            self.scale_button.update(self.window)

    def display_buttons(self):               
        self.save_button.update(self.window)
        self.load_button.update(self.window)

    def save_level(self):
        # Save Tiles
        with open(f'level_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in self.world_data:
                writer.writerow(row)

        # Save Game Object
        game_objects = []
        for game_object in self.game_objects:
            game_objects.append({"Index" : game_object.index, "Sprite": game_object.sprite_path, "Position" : (game_object.x, game_object.y), "Rotation" : game_object.sprite_rotation, "Scale" : game_object.sprite_scale})

        game_objects_list = []
        for game_object in game_objects:
            game_objects_list.append(game_object)

        fieldnames = ["Index", "Sprite", "Position", "Rotation", "Scale"]
        with open(f'level_object_data.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  

            for game_object in game_objects_list:
                writer.writerow(game_object)   

        # Save Special Object
        special_objects = []
        for special_object in self.special_objects:
            special_objects.append({"Index" : special_object.index, "Sprite" : special_object.sprite_path, "Position" : (special_object.x, special_object.y), "Rotation" : special_object.sprite_rotation, "Scale" : special_object.sprite_scale})  

        special_objects_list = []
        for special_object in special_objects:
            special_objects_list.append(special_object)

        fieldnames = ["Index", "Sprite", "Position", "Rotation", "Scale"]
        with open(f'level_special_object_data.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for special_object in special_objects_list:
                writer.writerow(special_object)

        print("Saved")
        
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
            elif int(float(special_object["Sprite"])) == 1:
                new_special_object = Checkpoint(int(special_object["Index"]) + 100, position[0], position[1], True)
            else:
                new_special_object = Spawnpoint(int(special_object["Index"]) + 100, position[0], position[1], True)

            new_special_object.rotate(int(float(special_object["Rotation"])))
            new_special_object.scale(int(float(special_object["Scale"])))
            self.special_objects.append(new_special_object)
               
    def run(self):
        pg.display.set_caption("Super Mario Cart")

        while True:
            # Graphics
            self.clock.tick(self.tick_rate)
            self.window.fill("black")

            # Display World
            self.draw_grid() 
            self.draw_world()
            self.display_game_objects()           

            # Display Panel
            self.draw_panel()          
            self.update_scroll()
            self.update_tile()
            self.display_buttons()
            self.display_transform()

            if self.active_asset != None:
                self.active_asset.display(self.window, self.scroll_x, self.scroll_y)

            # User Input
            self.receive_input()           
       
            pg.display.update()



#editor = Editor(1100, 740, window)
#editor.run()