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
    def __init__(self,x,y,image,scale):
        self.width = image.get_width()
        self.height = image.get_height()     
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height*scale)))
        self.scale = self.width * scale
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
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
        screen.blit(self.image, (self.rect.x - self.scale / 2, self.rect.y))
        
        return action 
        
    

#Button instances
start_button = Button(SCREEN_WIDTH / 2,300,start_img,1)
exit_button = Button(SCREEN_WIDTH / 2,100,quit_img,1)


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

