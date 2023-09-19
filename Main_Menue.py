import pygame
import sys   

#Display Window
SCREEN_Height = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_Height,SCREEN_WIDTH))
pygame.display.set_caption('Button demo')

#load button images
start_img = pygame.image.load('EFWuche/images/mael/start_button.png').convert_alpha()
quit_img = pygame.image.load('EFWuche/images/mael/exit_button.png').convert_alpha() 

#button class 
class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height*scale)))
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
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action 
        
    

#Button instances
start_button = Button(100,300,start_img,0.8)
exit_button = Button(10,100,quit_img,0.8)


#Game loop 
run = True
while run==True: 
    screen.fill((202,228,241))
    if start_button.draw():
        print('start game')

    if exit_button.draw():
        run = False 

    #event handler
    for event in pygame.event.get():
    #quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit 

