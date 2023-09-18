import pygame, sys

#Display Window
SCREEN_Height = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_Height,SCREEN_WIDTH))
pygame.display.set_caption('Button demo')

#load button images
start_img = pygame.img.load('/images/png-transparent-game-buttons-3d-three-dimensional-orange-thumbnail.png').convert_alpha()

#Game loop 
run = True
while run==True: 
    #event handler
    for event in pygame.event.get():
    #quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit 

