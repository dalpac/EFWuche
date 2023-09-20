import pygame

SCREEN_Height = 740
SCREEN_WIDTH = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_Height))
pygame.display.set_caption('Button demo')

start_img = pygame.image.load('images/button.png').convert_alpha()
quit_img = pygame.image.load('images/button.png').convert_alpha() 

#button class 
class Button():
    def __init__(self,x,y,image,scale,base_color, font,text_input):
        self.width = image.get_width()
        self.height = image.get_height()     
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height*scale)))
        self.scale = self.width * scale
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
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
            screen.blit(self.image, (self.rect.x - self.scale / 2, self.rect.y))
            
            return action 

continue_button = Button(SCREEN_WIDTH / 2,300,start_img,1,'black',pygame.font.Font('images/Fonts/foo.otf', 50),'PLAY')
main_menue_button = Button(SCREEN_WIDTH / 2,200,quit_img,1,'black',pygame.font.Font('images/Fonts/foo.otf', 50),'EXIT')
quit_game_button = Button(SCREEN_WIDTH / 2,100,start_img,'black',pygame.font.Font('images/Fonts/foo.otf', 50),'PLAY')






for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            continue_button.draw()
            
              
             
             



run = True
while run==True: 
    screen.fill((202,228,241))

    if quit_game_button.draw():
        run = False 

    #event handler
    for event in pygame.event.get():
    #quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit 