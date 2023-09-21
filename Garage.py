import pygame 
from Demo import Demo

#Display Window
SCREEN_Height = 740
SCREEN_WIDTH = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_Height))
pygame.display.set_caption('Button demo')

#load car images
car_purple_img = pygame.image.load('images/cars/0.png').convert_alpha()
car_blue_img = pygame.image.load('images/cars/1.png').convert_alpha() 
car_yellow_img = pygame.image.load('images/cars/2.png').convert_alpha()

#scale car images
car_purple_img = pygame.transform.scale(car_purple_img,(1/6*SCREEN_WIDTH, 1.87*1/6*SCREEN_WIDTH) )
car_blue_img = pygame.transform.scale(car_blue_img,(1/6*SCREEN_WIDTH, 1.87*1/6*SCREEN_WIDTH) )
car_yellow_img = pygame.transform.scale(car_yellow_img,(1/6*SCREEN_WIDTH, 1.87*1/6*SCREEN_WIDTH) )

#garage class 
class Garage():
    def __init__(self, image, pos,):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
       
        


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
        
        
        return action 


#car objects
car_purple = Garage(car_purple_img,pos=(SCREEN_WIDTH * 1/4,SCREEN_Height / 2))
car_blue = Garage(car_blue_img,pos=(SCREEN_WIDTH * 2/4,SCREEN_Height  / 2))
car_yellow = Garage(car_yellow_img,pos=(SCREEN_WIDTH *3/4 ,SCREEN_Height  / 2))

class Garage2:
    def __init__(self, width, height, screen) -> None:
        self.width = width
        self.height = height
        self.screen = screen
        self.input_active = False
        self.font =pygame.font.Font('images/Fonts/foo.otf', 50)
        self.text = self.font.render('Choose your Car',True,'white')
        self.text_rect = None


    def activate_input(self):
        self.input_active = True


    def start_garage(self):
        while True:   
            screen.fill('black')  
            self.text_rect = self.text.get_rect(center=(self.width / 2, 100))
            screen.blit(self.text,self.text_rect)       
            if car_purple.draw() == True:
                demo = Demo(self.width, self.height, self.screen, 0)
                demo.start_demo()
            if car_blue.draw() == True:
                demo = Demo(self.width, self.height, self.screen, 1)
                demo.start_demo()

            if car_yellow.draw()==True:
                demo = Demo(self.width, self.height, self.screen, 2)
                demo.start_demo()
          
            for event in pygame.event.get():
                    #quit game
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            

            pygame.display.update()
                


              



