# (: Flappy Birds :) Pink World(Flappy Doge)!
# Release v12.1.1-N
# - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Python Version : 3.9.9
# Pygame Version : 2.1.1
# - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Programmer : Mohammadreza.D
# Developer name : *_* Every Developer *_*
# Github >>> https://github.com/Every-Developer/Flappy_Birds
# ____________________________________________________________#

import pygame
import sys
import webbrowser

from random import randint
from pygame.locals import *


# Start Pygame Modules
pygame.init()

# GAME SPEED (FPS)
FPS = 60
FPSClock = pygame.time.Clock()

# Game Display setting
Screen_width = 576
Screen_height = 1024
 
Main_Screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Flappy Doge')

Icon = pygame.image.load('assets/Logo/Doge_icon.png')
pygame.display.set_icon(Icon)


# Define game variables
floor_scroll = 0
floor_height = 900
floor_speed  = 3

Fluttering = True
Game_Status = True

pass_pipe = False
Distance_pipe = 220
pipe_frequency = 2000 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

Sleep_wing = 150
Create_wing  = pygame.USEREVENT
pygame.time.set_timer(Create_wing, Sleep_wing)

# Score & High score
Score = 0
High_Score = 0
x_point = (Screen_width/2)
y_point = 140

# Colors
Beige = (245, 245, 220)
White = (255, 255, 255)
Gold  = (255, 215, 0)
Pink = (255, 192, 203)
MistyRose = (255, 228, 225)

Highlight_paint = Beige
Highlight_conter = White

# My Photos (Background and floor)
play_button = pygame.transform.scale(pygame.image.load('assets/Buttons/play.png'), (135, 75)).convert_alpha(Main_Screen)
Rate_image = pygame.transform.scale(pygame.image.load('assets/Buttons/Rate.png'), (135, 75)).convert_alpha(Main_Screen)
Menu_image = pygame.transform.scale(pygame.image.load('assets/Buttons/Menu.png'), (104, 36)).convert_alpha(Main_Screen)

ground_image = pygame.transform.scale2x(pygame.image.load('assets/Background/floor.png')).convert(Main_Screen)

pg1_image = pygame.transform.scale(pygame.image.load('assets/Buttons/Pygame_Text.png'), (135, 75)).convert_alpha(Main_Screen)
pg2_image = pygame.transform.scale(pygame.image.load('assets/Buttons/Pygame_snake.png'), (135, 75)).convert_alpha(Main_Screen)

gameover_image = pygame.transform.scale2x(pygame.image.load('assets/Message/game over.png')).convert_alpha(Main_Screen)


play_rect = play_button.get_rect(center=((Screen_width/2-100), 800))
pg_rect = pg1_image.get_rect(center=((Screen_width/2+100), 800))

# Insert High Score from MyBestScore
try:
    Data = open('assets/My Score/High_Score', 'r')
       
    High_Score = int(Data.read())
    Data.close()

except FileNotFoundError:

    with open('assets/assets/My Score/High_Score', 'w') as Data:

        High_Score = 0
        Data.write(str(High_Score))

# *___________*____________*____________*

# list of backgrounds
BACKGROUNDS_LIST = [
    
    'assets/Background/Pink_Background.png',
    'assets/Background/Dark_Background.png'   
]

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = [
    
    # doge bird
    (
        'assets/Bird/bird-up-flap.png',
        'assets/Bird/bird-mid-flap.png',
        'assets/Bird/bird-down-flap.png'    )
    
]


# pygame.mixer.init()
Audio_jump   = pygame.mixer.Sound('assets/Audio/Count.ogg')
Audio_Flight = pygame.mixer.Sound('assets/Audio/Flight.ogg')
Audio_Fall   = pygame.mixer.Sound('assets/Audio/Collision.ogg')
Audio_wing   = pygame.mixer.Sound('assets/Audio/Wind.ogg')
# pygame.mixer.music.load('Audio/examplesound')


class Bird_Animation(pygame.sprite.Sprite):
    
    '''How does my bird fly and eventually die?'''

    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.My_Birds = []
        self.index = 0
        self.counter = 0

        # Select random player
        Random_Player = randint(0, len(PLAYERS_LIST) - 1)

        # *___* *___* *___* *___* *___* My Flappy Birds Pictures *___* *___* *___* *___* *___* *___*
        for index in range(0, 3):
        
            New_Bird = pygame.transform.scale2x(pygame.image.load(PLAYERS_LIST[Random_Player][index])).convert_alpha(Main_Screen)
            self.My_Birds.append(New_Bird)


        self.image = self.My_Birds[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬ ¬_¬
        
        
        # gravity of the bird!
        self.gravity = 0
        self.check_click = False
    
                
    
    def update(self):

        # Gravity and logical rotation of the bird in ups and downs
        if Fluttering:
            self.gravity += 0.5

            if self.gravity > 10:
                self.gravity = 10

            if self.rect.bottom <= floor_height:
                self.rect.y += self.gravity

            if self.rect.bottom >= floor_height:
                
                Audio_Fall.play()
                Audio_wing.play()


        if Game_Status:
            
            self.check_click, self.gravity = Flighting(self.check_click, self.gravity, Fluttering)

            self.counter += 1
            Delay = 5

        
            if self.counter > Delay:

                self.counter = 0
                self.index += 1

                if self.index >= len(self.My_Birds):

                    self.index = 0

            self.image = self.My_Birds[self.index]
            
            self.rotation = self.gravity * -2

            if self.gravity >= 0:
                self.rotation = self.gravity * -4


            if self.gravity <= 0:
                self.rotation = self.gravity * -2
    
            # Rotation is not available in version N.
            # self.image = pygame.transform.rotate(self.My_Birds[self.index], self.rotation)
            
        
        else:
            
            if self.gravity > 6 and self.rotation < -30:
                self.rotation = -90
                
            else:
                self.rotation = self.gravity * 11.4
            
            # Rotation is not available in version N.
            # self.image = pygame.transform.rotate(self.My_Birds[self.index], self.rotation)

        # print(self.rotation)
        # print(self.gravity)


class Pipe(pygame.sprite.Sprite):
    
    '''Making pipes and creating the illusion of moving pipes and updating them'''

    def __init__(self, x, y, Position):

        pygame.sprite.Sprite.__init__(self)

        # My pipes
        self.image = pygame.transform.scale2x(pygame.image.load('assets/Pipe/pipe_1.png')).convert_alpha(Main_Screen)
        self.rect = self.image.get_rect()

        # Pipe Position >>> Top & Bottom
        if Position == "top":

            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (Distance_pipe/2)]

        if Position == "bottom":

            self.rect.topleft = [x, y + (Distance_pipe/2)]

    def update(self):

        self.rect.x -= floor_speed

        if self.rect.right < 0:

            self.kill()

# class Button():

#     '''Restart everything with just the *Restart button*'''

#     def __init__(self, x, y, image):
        
#         self.stat = False
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)

#     def draw(self):

#         action = False

#         position = pygame.mouse.get_pos()

#         if pygame.mouse.get_pressed()[0] == 1:
            
#             if self.rect.collidepoint(position):

#                 action = True
#         if self.stat == True:
#             Main_Screen.blit(self.image, (self.rect.x, self.rect.y))
        
#         self.stat = False
#         return action


# BIRD SPRITES               
PLAYERS_GROUP = pygame.sprite.Group()
Flappy_bird = Bird_Animation(100, (Screen_height/2))
PLAYERS_GROUP.add(Flappy_bird)

# PIPE SPRITES
PIPELINE = pygame.sprite.Group()

# Select random background
Random_Page = randint(0, len(BACKGROUNDS_LIST) - 1)
Background_Page = pygame.transform.scale2x(pygame.image.load(BACKGROUNDS_LIST[Random_Page])).convert(Main_Screen)

# *__* *__* *__* *__* *__* *__* *__* Welcome Page *__* *__* *__* *__* *__* *__* *__* *__*
name_image = pygame.transform.scale2x(pygame.image.load('assets/Message/flappy_name.png')).convert_alpha(Main_Screen)
name_rect  = name_image.get_rect(center=(Screen_width/2, 180))

get_ready_Page = pygame.transform.scale2x(pygame.image.load('assets/Message/get ready!.png')).convert_alpha(Main_Screen)
get_ready_rect = get_ready_Page.get_rect(center=(Screen_width/2, 370))

Tap_image = pygame.transform.scale2x(pygame.image.load('assets/Message/tap.png')).convert_alpha(Main_Screen)
Tap_rect  = Tap_image.get_rect(center=(Screen_width/2, 600))
#________________________________________________________________________________________#


# FUNCTIONS
def Welcome_Screen(Mode='Normal'):

    '''Welcome! to the Ocean Bird'''

    global floor_scroll, get_ready_rect, Tap_rect

    # if Mode == 'Normal':
        # pygame.mixer.music.play()

    # pygame button effect
    # pg_touch = False

    x = 100
    y = (Screen_height/2)

    Flight_mode = {'val': 0, 'dir': 1}

    
    if Mode == 'Restart':

        get_ready_rect = get_ready_Page.get_rect(center=(Screen_width/2, 270))
        Tap_rect  = Tap_image.get_rect(center=(Screen_width/2, 670))
    
    elif Mode == 'Normal':
        get_ready_rect = get_ready_Page.get_rect(center=(Screen_width/2, 370))
        Tap_rect  = Tap_image.get_rect(center=(Screen_width/2, 600))


    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                
                # End Pygame Modules
                pygame.quit()
                # Exit Programm
                sys.exit()
            
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and Game_Status:
                
                if Mode == 'Restart':
                    
                    Fluttering = True
                    Flappy_bird.gravity = -10
                    Main_game(Fluttering)
                

            elif event.type == MOUSEBUTTONDOWN and Game_Status == True:

                if Mode == 'Restart':

                    Fluttering = True
                    Main_game(Fluttering)


                elif Mode == 'Normal':
                
                    if play_rect.collidepoint(event.pos):
                    
                        Fluttering = True
                        Main_game(Fluttering)
  

                    if pg_rect.collidepoint(event.pos):
                        
                        webbrowser.open('https://www.pygame.org/')


            # if event.type == MOUSEMOTION and Game_Status == True:
                
            #     if pg_rect.collidepoint(event.pos):
            #         pg_touch = True

            #     else:
            #         pg_touch = False

            # Wining Bird
            if event.type == Create_wing:
                
                if Flappy_bird.index < 2:
                    Flappy_bird.index += 1
                
                else:
                    Flappy_bird.index = 0

        # Down & Up flap (Movement)
        Energy_Bird(Flight_mode)

        Main_Screen.blit(Background_Page, (0, 0))

        rectangle = Flappy_bird.My_Birds[Flappy_bird.index].get_rect(center=(x, (y + Flight_mode['val'])))
        Main_Screen.blit(Flappy_bird.My_Birds[Flappy_bird.index], rectangle)

        Main_Screen.blit(ground_image, (floor_scroll, floor_height))
        Main_Screen.blit(ground_image, (floor_scroll + Screen_width, floor_height))

        Main_Screen.blit(get_ready_Page, get_ready_rect)
        Main_Screen.blit(Tap_image, Tap_rect)


        if Mode == 'Normal':
            
            Main_Screen.blit(name_image, name_rect)
            Main_Screen.blit(play_button, play_rect)
            Pygame_web()

        floor_scroll -= floor_speed

        if (floor_scroll) <= -Screen_width:

            floor_scroll = 0

        Flappy_bird.rect.center = [x, y]
        Flappy_bird.gravity = 0

        pygame.display.update()
        
        FPSClock.tick(FPS)



def Flighting(Click_status, gravity, Fluttering):

    '''If I click, how does the bird fly?'''


    Click_Pressed = pygame.mouse.get_pressed()

    if Click_Pressed[0] == 1 and Click_status == False and Fluttering == True:
        
        Click_status = True
        gravity = -10
        Audio_Flight.play()

    # elif pygame.key.get_pressed()[pygame.K_SPACE] and Click_status == False and Fluttering == True:

    #     Click_status = True
    #     gravity = -10
    #     # Audio_Flight.play()
    
    if Click_Pressed[0] == 0:

        Click_status = False

    return Click_status, gravity



def Falling_Buttons(height = 680):
    
    '''What buttons appear on the screen when I lose?'''

    action = False

    rect_play = play_button.get_rect(midtop=((Screen_width/2)-100, height))
    rect_rate = Rate_image.get_rect(midtop=((Screen_width/2)+100, height))

    Position = pygame.mouse.get_pos()
    Click_Pressed = pygame.mouse.get_pressed()


    if Click_Pressed[0] == 1:

        if rect_play.collidepoint(Position):
            
            action = True

        if rect_rate.collidepoint(Position):

            webbrowser.open('https://github.com/Every-Developer/Flappy_Birds/issues')
            

    Main_Screen.blit(play_button, rect_play)
    Main_Screen.blit(Rate_image, rect_rate)

    return action


def Menu_button(menu_y = 790):

    '''Return to the main menu you saw at the beginning of the game'''

    action = False

    rect_menu = Menu_image.get_rect(midtop=((Screen_width/2), menu_y))

    Position = pygame.mouse.get_pos()
    Click_Pressed = pygame.mouse.get_pressed()

    if Click_Pressed[0] == 1:

        if rect_menu.collidepoint(Position):
            
            action = True

    Main_Screen.blit(Menu_image, rect_menu)

    return action

def Pygame_web(touch=False):

    '''Do you want to visit the Pygame site?
            There are a lot of interesting games there'''

    if touch == True:
        Main_Screen.blit(pg2_image, pg_rect)

    else:
        Main_Screen.blit(pg1_image, pg_rect)


def Energy_Bird(Energy):

    '''Up and down the bird on the Home screen'''

    Bird_height = 20
    Speed_of_movement = 1 # 0 to 5

    if abs(Energy['val']) == Bird_height:
        Energy['dir'] *= -1

    if Energy['dir'] == 1:
        Energy['val'] += Speed_of_movement
    
    else:
        Energy['val'] -= Speed_of_movement



def Colision():

    '''What happens if I collide with a pipe?'''

    gameover_rect = gameover_image.get_rect(center=(Screen_width/2, 350))

    # Audio_Collision.play(1)

    Main_Screen.blit(gameover_image, gameover_rect)

    Game_Status = False

    return Game_Status


def Reset_Game():

    '''Restoring everything to its original state'''

    PIPELINE.empty()
    
    Flappy_bird.rect.x = 100
    Flappy_bird.rect.y = (Screen_height/2)

    Score = 0
    return Score


def Counting_Score(Score, Color=Beige):

    '''Give me points if I go through the pipes'''

    Font_score = pygame.font.Font('assets/Font/Score.ttf', 60)

    Points = Font_score.render(f'{Score}', False, Color)
    Point_rect = Points.get_rect(center=(x_point, y_point))

    # pygame.draw.circle(Main_Screen, Beige, (x_point, y_point), 50)
    Main_Screen.blit(Points, Point_rect)



def Update_Score():

    '''Update my scores with each jump'''

    global Score, pass_pipe

    if len(PIPELINE) > 0:

        if PLAYERS_GROUP.sprites()[0].rect.left > PIPELINE.sprites()[0].rect.left\
            and PLAYERS_GROUP.sprites()[0].rect.right < PIPELINE.sprites()[0].rect.right\
            and pass_pipe == False:
            
            pass_pipe = True

        if pass_pipe == True:

            if PLAYERS_GROUP.sprites()[0].rect.right > PIPELINE.sprites()[0].rect.right:

                Score += 1
                Audio_jump.play()
                pass_pipe = False


def Final_Score(Score, Text_color, y=600):

    '''What has been my highest score ever? Show me'''

    global High_Score
    
    Font_high_score = pygame.font.Font('assets/Font/Score.ttf', 40)

    if Score > High_Score:

        High_Score = Score

        with open('assets/My Score/High_Score', 'w') as Best_score:
            Best_score.write(f'{High_Score}')


    Best_point = Font_high_score.render(f'High Score : {High_Score}', False, Text_color)
    Point_rect = Best_point.get_rect(center=((Screen_width/2), y))

    Main_Screen.blit(Best_point, Point_rect)



def Main_game(fly):

    '''Everything that happens will be on the Main Screen'''

    global floor_scroll, Fluttering, Game_Status, last_pipe, Score, High_Score, Highlight_paint, Highlight_conter

    Fluttering = fly
    
    # _____________________________________________
    # These features are not supported in version N.
    # position of Game over buttons
    # button_position = floor_height
    # High score test box height
    # HI_height = 400
    # _____________________________________________

    # pygame.mixer.music.stop()

    # GAME LOGIC
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):

                # End Pygame Modules
                pygame.quit()
                # Exit Programm
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and Fluttering == False and Game_Status == True:

                Fluttering = True


            if event.type == pygame.KEYDOWN:
                
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    
                    if Fluttering == False and Game_Status == True:

                        Fluttering = True

                    
                    if Fluttering == True and Game_Status == True:
                        
                        if Flappy_bird.check_click == False:

                            Flappy_bird.check_click = True
                            Flappy_bird.gravity = -10
                            Audio_Flight.play()

                        else:
                            Flappy_bird.check_click = False
                   
                   
        # Display & Mein Screen (background, ground)
        Main_Screen.blit(Background_Page, (0, 0))
        Main_Screen.blit(ground_image, (floor_scroll, floor_height))
        Main_Screen.blit(ground_image, (floor_scroll + Screen_width, floor_height))

        # Show My pipes!
        PIPELINE.draw(Main_Screen)
        Main_Screen.blit(ground_image, (floor_scroll, floor_height))
        Main_Screen.blit(ground_image, (floor_scroll + Screen_width, floor_height))

        # Show My Pinkly Bird!
        PLAYERS_GROUP.draw(Main_Screen)
        PLAYERS_GROUP.update()
        
        # Check if bird has hit the ground
        if Flappy_bird.rect.bottom >= floor_height:

            Game_Status = Colision()
            Fluttering = False
            

        if Game_Status == True and Fluttering == True:

            # generate New pipes
            time_now = pygame.time.get_ticks()
            
            if time_now - last_pipe > pipe_frequency:
                
                pipe_height = randint(-220, 200)
                
                bottom_pipe = Pipe((Screen_width+100), (Screen_height/2) + pipe_height, "bottom")
                top_pipe    = Pipe((Screen_width+100), (Screen_height/2) + pipe_height, "top")
                
                PIPELINE.add(bottom_pipe)
                PIPELINE.add(top_pipe)
                
                last_pipe = time_now

            PIPELINE.update()

            floor_scroll -= floor_speed

            if (floor_scroll) <= -Screen_width:

                floor_scroll = 0
        
        # Check High_Score
        if Score > High_Score:
            Highlight_conter = Pink
            Highlight_paint = Gold

        elif Score < High_Score:
            Highlight_conter = White
            Highlight_paint = Beige

        # Check to see if the bird has collided with the pipe
        if pygame.sprite.groupcollide(PLAYERS_GROUP, PIPELINE, False, False) or Flappy_bird.rect.top < -50:
            Game_Status = Colision()
            

        if Flappy_bird.rect.bottom >= floor_height and Game_Status == False:

            # if HI_height <= 590:
            #    HI_height += 20
            
            #if button_position >= 700:
            #   button_position -= 20

            Final_Score(Score, Highlight_paint)

            if Menu_button():

                Game_Status = True
                Score = Reset_Game()
                Welcome_Screen('Normal')
            
            if Falling_Buttons():
                
                Game_Status = True
                Score = Reset_Game()
                Welcome_Screen('Restart')


        Update_Score()
        Counting_Score(Score, Highlight_conter)

        
        FPSClock.tick(FPS)

        pygame.display.update()



if __name__ == '__main__':

    Welcome_Screen('Normal')

# THE END OF CODE          