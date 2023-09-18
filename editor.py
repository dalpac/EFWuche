import pygame as pg
import sys
from button import Button
import os

pg.init()

window = pg.display.set_mode((1100, 740))

class GameObject:
    def __init__(self, sprite_path, x, y, width, height, static):
        self.sprite_path = sprite_path
        self.sprite = pg.image.load(f'img/assets/{self.sprite_path}.png').convert_alpha()       
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite_rotation = 0
        self.sprite_scale = 100
        self.static = static
        self.transform_move = False
        self.transform_rotate = False
        self.transform_scale = False

    def move(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, delta):
        pass
        
    def scale(self, delta):
        pass


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
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_speed = 1
        self.scroll_x_direction = 0
        self.scroll_y_direction = 0
        self.tile_size = 46
        self.tile_count = len(os.listdir('images/tiles/'))
        self.asset_count = len(os.listdir('images/assets/'))

        # Pygame
        self.clock = pg.time.Clock()
        self.tick_rate = 60

        # Assets
        self.tile_list, self.asset_list = self.import_assets()
        self.tile_button_list, self.asset_button_list = self.create_buttons()
        self.world_data = self.get_world_data()

        self.current_tile = 0
        self.active_asset = None        

    def import_assets(self):
        tile_list = []
        for i in range(self.tile_count):
            img = pg.image.load(f'images/tiles/{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.tile_size, self.tile_size))
            tile_list.append(img) 

        asset_list = []
        for i in range(self.asset_count):
            img = pg.image.load(f'images/assets/{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.tile_size, self.tile_size))
            asset_list.append(img)

        return tile_list, asset_list
    
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
            asset_button = Button(image=self.asset_list[i], pos=((self.width- self.right_margin) + (75 * asset_col) + 50, 75 * asset_row + 400),text_input="", font=pg.font.Font('images/Fonts/foo.otf'), base_color="#000000", hovering_color="#333333")
            asset_list.append(asset_button)
            asset_col += 1
            if asset_col == 3:
                asset_row += 1
                asset_col = 0

        return tile_list, asset_list
    
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
                    self.window.blit(self.tile_list[tile], (x * self.tile_size - self.scroll_x, y * self.tile_size - self.scroll_y))

    def draw_panel(self):
        pg.draw.rect(self.window, pg.color.Color(85,107,47), (self.width - self.right_margin, 0, self.right_margin, self.height))
        self.draw_text("Tiles", pg.font.Font('images/Fonts/foo.otf', 50), "black", self.width - (self.right_margin / 2), 50)
        self.draw_text("Assets", pg.font.Font('images/Fonts/foo.otf', 50), "black", self.width - (self.right_margin / 2), 350)

        for button in self.tile_button_list:
            button.update(self.window)

        for button in self.asset_button_list:
            button.update(self.window)

        # Get Selected
        button_count = 0
        button_list = self.tile_button_list
        for button_count, i in enumerate(button_list):
            if i.draw(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                self.current_tile = button_count
                self.current_game_object = None

        # Highlight the selected tile
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
                            if self.current_game_object != None:  
                                if self.move_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                                    self.start_moving_object()                                    

                                elif self.rotate_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                                    self.start_rotating_object()                                    

                                elif self.scale_button.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):
                                    self.start_scaling_object()                                   

                            self.select_gameobject()

                        else:      
                            self.create_new_gameobject(event)

                if event.type == pg.MOUSEMOTION:
                    if self.active_asset != None:
                        if self.active_asset.transform_move:
                            self.active_asset.move(event.pos[0] + self.scroll_x, event.pos[1] + self.scroll_y)  

                        if self.active_asset.transform_rotate:
                            self.active_asset.rotate(event.pos[0] - self.active_asset.x)

                        if self.active_asset.transform_scale:
                            self.active_asset.scale(event.pos[0] - self.active_asset.x)   

    def create_new_gameobject(self, event):
        for num, asset in enumerate(self.asset_button_list):
            if asset.drag(self.window, pg.mouse.get_pos(), pg.mouse.get_pressed()):                                   
                self.active_asset = GameObject(num, event.pos[0] - self.scroll_x, event.pos[1] - self.scroll_y, self.tile_size, self.tile_size, False) 
                self.active_asset.transform_move = True

    def start_moving_object(self):
        self.active_asset = self.current_game_object
        self.active_asset.transform_move = True

        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
            self.current_game_object = None

    def start_rotating_object(self):
        self.active_asset = self.current_game_object
        self.active_asset.transform_rotate = True

        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
            self.current_game_object = None

    def start_scaling_object(self):
        self.active_asset = self.current_game_object                                    
        self.active_asset.transform_scale = True

        if self.game_objects.__contains__(self.current_game_object):
            self.game_objects.remove(self.current_game_object)
            self.current_game_object = None

    def select_gameobject(self):
        for game_object in self.game_objects:
            if game_object.static == True:
                if game_object.collidepoint(pg.mouse.get_pos()):                           
                    self.current_game_object = game_object                                       

    def run(self):
        pg.display.set_caption("Super Mario Cart")

        while True:
            # Graphics
            self.clock.tick(self.tick_rate)
            self.window.fill("black")
            self.draw_grid() 
            self.draw_world()
            self.draw_panel()          
            self.update_scroll()
            self.update_tile()

            # User Input
            self.receive_input()           
       
            pg.display.update()



editor = Editor(1100, 740, window)
editor.run()