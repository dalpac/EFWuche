import pygame
from Main_Menue import Main_Menu
import threading

pygame.init()

SCREEN_Height = 740
SCREEN_WIDTH = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_Height))
pygame.display.set_caption('Button demo')

start_img = pygame.image.load('images/Button_sidemenu.png').convert_alpha()
quit_img = pygame.image.load('images/Button_sidemenu.png').convert_alpha() 

#button class 
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False
        self.base_color = base_color
        self.text_input = text_input
        self.font = font 
        self.text = self.font.render(self.text_input, True, self.base_color)


    def draw(self): 
        action = False 
        self.font.render(self.text_input, True, self.base_color)
        #get mouse position
        position = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print('clicked')
                action = True
        if pygame.mouse.get_pressed()[0]== 0:
            self.clicked = False
        
            
        #draw button on screen
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
        return action 

button_img = pygame.transform.scale(pygame.image.load('images/Button_sidemenu.png').convert_alpha(), (800, 180))

continue_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,100),text_input="Continue", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
main_menue_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,300),text_input="Main Menue", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
quit_game_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,500),text_input="QUIT", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")

         
def side_menu():
    x = False
    while True: 
        screen.fill('black')
        #event handler
        for event in pygame.event.get():
        #quit game
            if event.type == pygame.QUIT:
                pygame.quit()  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if x==True:
                        x = False
                    else: 
                        x = True
        if x == True:
            if continue_button.draw() == True:
                x=False
        
            if main_menue_button.draw()== True:
                main_menue = Main_Menu(1100,740,screen)
                main_menue.main_menu()
                
            if quit_game_button.draw() == True:
                run = False
                print(run)

        
        pygame.display.update()
                                   
side_menu()
  
        


        
    


