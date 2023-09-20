import pygame
import sys  
from editor import Editor

#Display Window
SCREEN_Height = 740
SCREEN_WIDTH = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_Height))
pygame.display.set_caption('Button demo')

#load button images
start_img = pygame.image.load('images/button.png').convert_alpha()
quit_img = pygame.image.load('images/button.png').convert_alpha() 

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

    def draw(self): 
        action = False 
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
        
    

#Button instances
button_img = pygame.transform.scale(pygame.image.load('images/button.png').convert_alpha(), (800, 180))
start_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,SCREEN_Height  *1/ 4),text_input="Editor", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
exit_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,SCREEN_Height * 2/ 4),text_input="Exit", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")



#Game loop 
run = True
while run==True: 
    screen.fill((202,228,241))
    if start_button.draw():
        editor = Editor(1100, 740, screen)
        editor.run()

    if exit_button.draw():
        run = False 

    #event handler
    for event in pygame.event.get():
    #quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit 

