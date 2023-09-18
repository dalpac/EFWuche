import pygame, sys

#Display Window
SCREEN_Height = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_Height,SCREEN_WIDTH))
pygame.display.set_caption('Button demo')

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
