# *__* Flappy Birds *__* :( Flappy fish!
# Release v11.0 (September 2021 Update)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Python Version : 3.9.6
# Pygame Version : 2.0.1
# - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Programmer : Mohammadreza.D
# Developer name : *_* Every Developer *_*
# Github >>> https://github.com/Every-Developer/Flappy_Birds
# ____________________________________________________________#


import pygame
import sys
from random import randint
from pygame.locals import *

# Start Pygame Modules
pygame.init()

# GAME SPEED (FPS)
FPS = 60
FPSClock = pygame.time.Clock()

# Game Display setting
Screen_width = 288
Screen_height = 512
 
Main_Screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Flappy Fish')

Icon = pygame.image.load('Assets/Logo/Fish_icon.png')
pygame.display.set_icon(Icon)


# Define game variables
floor_scroll = 0
floor_height = 440
floor_speed  = 2

Fluttering = True
Game_Status = True

pass_pipe = False
Distance_pipe = 120
pipe_frequency = 1400 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

Sleep_wing = 130
Create_wing  = pygame.USEREVENT
pygame.time.set_timer(Create_wing, Sleep_wing)

# Points
Score = 0
x_point = (Screen_width/2)
y_point = 70

# Colors
Beige = (245, 245, 220)
White = (255, 255, 255)
Gold  = (255, 215, 0)
CornflowerBlue = (100, 149, 237)


# My Photos (Background and floor)
ground_image = pygame.transform.scale(pygame.image.load('Assets/Background/floor.png'), (336, 112)).convert(Main_Screen)
restart_image = pygame.transform.scale(pygame.image.load('Assets/Buttons/restart.png'), (60, 21)).convert(Main_Screen)

gameover_image = pygame.image.load('Assets/Message/game over.png').convert_alpha(Main_Screen)
gameover_rect  = gameover_image.get_rect(center=(Screen_width/2, 200))


# list of backgrounds
BACKGROUNDS_LIST = [
    
    'Assets/Background/Dark_Sea.png',
    'Assets/Background/Light_Sea.png'   
]

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = [
    
    # Aque bird
    (
        'Assets/Bird/red-fish-up-flap.png',
        'Assets/Bird/red-fish-mid-flap.png',
        'Assets/Bird/red-fish-down-flap.png'
    ),
    # Purple bird
    (
        'Assets/Bird/yellow-fish-up-flap.png',
        'Assets/Bird/yellow-fish-mid-flap.png',
        'Assets/Bird/yellow-fish-down-flap.png'
    ),
    
]

# list of pipes
PIPES_LIST = [
    
    'Assets/Pipe/yellow_pipe.png',
    'Assets/Pipe/red_pipe.png'
]

# Select random pipe
Random_Pipe = randint(0, len(PIPES_LIST) - 1)

# Music & Sounds
FALLING_LIST = [
    
    'Assets/Audio/Fall (1).mp3',
    'Assets/Audio/Fall (2).mp3',
    'Assets/Audio/Fall (3).mp3'
]

Random_music = randint(0, len(FALLING_LIST) - 1)

# pygame.mixer.init()
Audio_jump      = pygame.mixer.Sound('Assets/Audio/jump.wav')
Audio_Flight    = pygame.mixer.Sound('Assets/Audio/Flight.mp3')
Audio_Fall      = pygame.mixer.Sound(FALLING_LIST[Random_music])
pygame.mixer.music.load('Assets/Audio/Sea.mp3')


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
        
            New_Bird = pygame.image.load(PLAYERS_LIST[Random_Player][index])
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
            self.gravity += 0.25

            if self.gravity > 6:
                self.gravity = 6

            if self.rect.bottom <= (floor_height + 10):
                self.rect.y += self.gravity

            if self.rect.bottom >= (floor_height + 10):

                Random_music = randint(0, len(FALLING_LIST) - 1)
                Audio_Fall = pygame.mixer.Sound(FALLING_LIST[Random_music])
                Audio_Fall.play()


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
            
            self.rotation = self.gravity * -3

            if self.gravity >= 0:
                self.rotation = self.gravity * -5


            if self.gravity <= 0:
                self.rotation = self.gravity * -4
    
            
            self.image = pygame.transform.rotate(self.My_Birds[self.index], self.rotation)
            
        
        else:
            
            self.rotation = -90

            self.image = pygame.transform.rotate(self.My_Birds[self.index], self.rotation)



class Pipe(pygame.sprite.Sprite):
    
    '''Making pipes and creating the illusion of moving pipes and updating them'''

    def __init__(self, x, y, Position):

        pygame.sprite.Sprite.__init__(self)

        # My pipes
        self.image = pygame.transform.scale(pygame.image.load(PIPES_LIST[Random_Pipe]), (52, 320)).convert_alpha(Main_Screen)
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

class Button():

    '''Restart everything with just the *Restart button*'''

    def __init__(self, x, y, image):
        
        self.stat = False
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        position = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] == 1:
            
            if self.rect.collidepoint(position) and self.stat:

                action = True
        
        if self.stat == True:
            Main_Screen.blit(self.image, (self.rect.x, self.rect.y))
        
        self.stat = False
        return action



# BIRD SPRITES               
PLAYERS_GROUP = pygame.sprite.Group()
Flappy_bird = Bird_Animation(70, (Screen_height/2))
PLAYERS_GROUP.add(Flappy_bird)

# PIPE SPRITES
PIPELINE = pygame.sprite.Group()

Restart_button = Button((Screen_width/2-30), (Screen_height/2), restart_image)


# Select random background
Random_Page = randint(0, len(BACKGROUNDS_LIST) - 1)
Background_Page = pygame.transform.scale(pygame.image.load(BACKGROUNDS_LIST[Random_Page]), (Screen_width, Screen_height)).convert(Main_Screen)

# *__* *__* *__* *__* *__* *__* *__* Welcome Page *__* *__* *__* *__* *__* *__* *__* *__*
name_image = pygame.image.load('Assets/Message/bird_name.png')
name_rect  = name_image.get_rect(center=(Screen_width/2, 80))

get_ready_Page = pygame.image.load('Assets/Message/get ready!.png')
get_ready_rect = get_ready_Page.get_rect(center=(Screen_width/2, 180))

Tap_image = pygame.image.load('Assets/Message/tap.png')
Tap_rect  = Tap_image.get_rect(center=(Screen_width/2, 320))
#_____________________________________________________________________________________#


# FUNCTIONS
def Welcome_Screen(Mode='Normal'):

    '''Welcome! to the $__$ Ocean Bird $__$'''

    global floor_scroll

    if Mode == 'Normal':
        pygame.mixer.music.play()

    x = 70
    y = (Screen_height/2)

    base_x = 0
    base_shift = ground_image.get_width() - Background_Page.get_width()

    Flight_mode = {'val': 0, 'dir': 1}


    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                
                # End Pygame Modules
                pygame.quit()
                # Exit Programm
                sys.exit()
            
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                
                Fluttering = True
                Main_game(Fluttering)
    

            elif event.type == MOUSEBUTTONDOWN and Game_Status == True:
                
                Fluttering = True
                Main_game(Fluttering)
                
                
            # Wining Bird
            if event.type == Create_wing:
                
                if Flappy_bird.index < 2:
                    Flappy_bird.index += 1
                
                else:
                    Flappy_bird.index = 0
                    # Flappy_bird.My_Birds[Flappy_bird.index]

        # Down & Up flap (Movement)
        Energy_Bird(Flight_mode)

        Main_Screen.blit(Background_Page, (0, 0))

        rectangle = Flappy_bird.My_Birds[Flappy_bird.index].get_rect(center=(x, (y + Flight_mode['val'])))
        Main_Screen.blit(Flappy_bird.My_Birds[Flappy_bird.index], rectangle)

        Main_Screen.blit(ground_image, (floor_scroll, floor_height))
        Main_Screen.blit(ground_image, (floor_scroll + Screen_width, floor_height))

        if Mode == 'Normal':
            
            Main_Screen.blit(name_image, name_rect)
            Main_Screen.blit(get_ready_Page, get_ready_rect)
            Main_Screen.blit(Tap_image, Tap_rect)

        floor_scroll -= floor_speed

        if (floor_scroll) <= -Screen_width:

            floor_scroll = 0

        Flappy_bird.rect.center = [x, y]
        Flappy_bird.gravity = 0

        pygame.display.update()
        
        FPSClock.tick(FPS)



def Energy_Bird(Energy):

    '''Up and down the bird on the Home screen'''

    Movment_Low = 15

    if abs(Energy['val']) == Movment_Low:
        Energy['dir'] *= -1

    if Energy['dir'] == 1:
        Energy['val'] += 1
    
    else:
        Energy['val'] -= 1



def Flighting(Click_status, gravity, Fluttering):

    '''If I click, how does the bird fly?'''


    Click_Pressed = pygame.mouse.get_pressed()

    if Click_Pressed[0] == 1 and Click_status == False and Fluttering == True:
        
        Click_status = True
        gravity = -5
        Audio_Flight.play()

    elif pygame.key.get_pressed()[pygame.K_SPACE] and Click_status == False and Fluttering == True:

        Click_status = True
        gravity = -5
        # Audio_Flight.play()
    
    if Click_Pressed[0] == 0:

        Click_status = False

    return Click_status, gravity



def Colision():

    '''What happens if I collide with a pipe?'''

    Main_Screen.blit(gameover_image, gameover_rect)

    Game_Status = False

    return Game_Status


def Reset_Game():

    '''Restoring everything to its original state'''

    PIPELINE.empty()
    
    Flappy_bird.rect.x = 70
    Flappy_bird.rect.y = (Screen_height/2)

    Score = 0
    return Score


def Counting_Score(Score):

    '''Give me points if I go through the pipes'''

    Font_score = pygame.font.Font('Assets/Font/Score.ttf', 30)

    Points = Font_score.render(f'{Score}', False, CornflowerBlue)
    Points_rect = Points.get_rect(center=(x_point, y_point))

    pygame.draw.circle(Main_Screen, Beige, (x_point, y_point), 25)
    Main_Screen.blit(Points, Points_rect)



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



def Main_game(fly):

    '''Everything that happens will be on the Main Screen'''

    global floor_scroll, Fluttering, Game_Status, last_pipe, Score

    Fluttering = fly

    pygame.mixer.music.stop()

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
                
                if event.key == pygame.K_SPACE:
                    
                    if Fluttering == False and Game_Status == True:

                        Fluttering = True

                    if Fluttering == True and Game_Status == True:
                        Audio_Flight.play()
                   
                   
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
        if Flappy_bird.rect.bottom >= (floor_height + 10):

            Game_Status = Colision()
            Fluttering = False
            
            if Restart_button.stat == False:
                Restart_button.stat = True


        if Game_Status == True and Fluttering == True:

            # generate New pipes
            time_now = pygame.time.get_ticks()
            
            if time_now - last_pipe > pipe_frequency:
                
                pipe_height = randint(-110, 90)
                
                bottom_pipe = Pipe(Screen_width, (Screen_height/2) + pipe_height, "bottom")
                top_pipe    = Pipe(Screen_width, (Screen_height/2) + pipe_height, "top")
                
                PIPELINE.add(bottom_pipe)
                PIPELINE.add(top_pipe)
                
                last_pipe = time_now

            PIPELINE.update()

            floor_scroll -= floor_speed

            if (floor_scroll) <= -Screen_width:

                floor_scroll = 0

        # Check to see if the bird has collided with the pipe
        if pygame.sprite.groupcollide(PLAYERS_GROUP, PIPELINE, False, False) or Flappy_bird.rect.top < -20:
            Game_Status = Colision()


        Update_Score()
        Counting_Score(Score)

        if Game_Status == False:

            if Restart_button.draw():

                Game_Status = True
                Score = Reset_Game()
                Welcome_Screen('Restart')

        
        FPSClock.tick(FPS)

        pygame.display.update()


if __name__ == '__main__':

    Welcome_Screen('Normal')

# THE END OF CODE          
