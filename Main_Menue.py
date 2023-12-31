import pygame  
from editor import Editor
import threading
import Garage



#Display Window
SCREEN_Height = 740
SCREEN_WIDTH = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_Height))
pygame.display.set_caption('Button demo')

#load button images
start_img = pygame.image.load('images/Button_dalia.png').convert_alpha()
quit_img = pygame.image.load('images/Button_dalia.png').convert_alpha() 

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
        
    

#Button instances
button_img = pygame.transform.scale(pygame.image.load('images/Button_dalia.png').convert_alpha(), (800, 180))
start_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,SCREEN_Height  *2/ 4),text_input="Editor", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
exit_button = Button(image=button_img, pos=(SCREEN_WIDTH / 2,SCREEN_Height * 3/ 4),text_input="Exit", font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color="#000000", hovering_color="#333333")
play_button= Button(image = button_img, pos=(SCREEN_WIDTH/2,SCREEN_Height*1/4),text_input="Play",font=pygame.font.Font('images/Fonts/foo.otf', 50), base_color ='#000000', hovering_color='#333333' )


class Main_Menu:
    def __init__(self, width, height, screen) -> None:
        self.width = width
        self.height = height
        self.screen = screen
        self.input_active = False

    def activate_input(self):
        self.input_active = True



    #Game loop 
    def main_menu(self):
        threading.Timer(1, self.activate_input).start()
        pygame.mixer.music.load("theme_mainmenu.wav")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(10)
        while True: 
            
            screen.fill((202,228,241))

            if self.input_active:
                if start_button.draw():
                    editor = Editor(self.width, self.height, self.screen)
                    editor.run()
                if play_button.draw():
                    garage = Garage.Garage2(self.width, self.height, self.screen)
                    garage.start_garage()
                if exit_button.draw():
                    pygame.quit()

            #event handler
            for event in pygame.event.get():
            #quit game
                if event.type == pygame.QUIT:
                    pygame.quit()

                    pygame.quit()
            pygame.display.update()


if __name__ == "__main__":
    main_menu = Main_Menu(1100, 740, screen)
    main_menu.main_menu()