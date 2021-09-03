# *__* Flappy Birds *__* :( Careless Series!
# Release v10.1-alpha (first Update)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Python Version : 3.9.0
# Pygame Version : 2.0.0
# - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Programmer : Mohammadreza.D
# Developer name : *_* Every Developer *_*
# Github >>> https://github.com/Every-Developer/Flappy_Birds
# ____________________________________________________________#

import pygame
import sys
from random import randrange

# Start Pygame Modules
pygame.init()

# All Variable
FPS = 90

Display_Width  = 576
Display_Height = 1024

# Floor
ground_game    = pygame.transform.scale2x(pygame.image.load('Background/ground.png'))
Floor_height   = 900
floor_x        = 0

# Force of gravity
gravity       = 0.25
Bird_movement = 0
Bird_index    = 0

# Time of Creation pipes & bird
Sleep_Pipe = 1200
Sleep_Flap = 250

# Distances
Distance_Between = 250

# Game is active or disable (GAME STATUS)
Game_Status = True

# Colors
Beige = (245, 245, 220)
White = (255, 255, 255)

# Firs Score
Score = 0
High_Score = 0
Active_Score = True

# Game Display
Main_Screen = pygame.display.set_mode((Display_Width, Display_Height))
pygame.display.set_caption('Flappy Bird')


# Timer & Clock
Clock = pygame.time.Clock()

# Audio
Audio_Count     = pygame.mixer.Sound('Audio/sfx_point.wav')
Audio_Collision = pygame.mixer.Sound('Audio/sfx_hit.wav')
Audio_Fall      = pygame.mixer.Sound('Audio/sfx_hit.wav')
Audio_Flight    = pygame.mixer.Sound('Audio/sfx_swooshing.wav')
Audio_gameover  = pygame.mixer.Sound('Audio/sfx_die.wav')
Audio_jump      = pygame.mixer.Sound('Audio/sfx_point.wav')

# Wecome Page
Welcome_Page = pygame.transform.scale2x(pygame.image.load('Write/message.png'))
Welcome_Page_rect = Welcome_Page.get_rect(center=(288, 512))

Page_Background = pygame.transform.scale(pygame.image.load('Background/background-day.png'), (576, 1024))

My_Bird = [
    pygame.transform.scale2x(pygame.image.load('Bird/yellow-bird-upflap.png')),
    pygame.transform.scale2x(pygame.image.load('Bird/yellow-bird-midflap.png')),
    pygame.transform.scale2x(pygame.image.load('Bird/yellow-bird-downflap.png')),
]

New_Pipe = pygame.transform.scale2x(pygame.image.load('Pipe/pipe-green.png'))
    
# Rectangle Bird
rect_bird = My_Bird[0].get_rect(center=(100, 500))
# Bird List
Bird_List = [My_Bird[0], My_Bird[1], My_Bird[2]]
My_Birds  = Bird_List[Bird_index]

# Time to create pipes & Bird (USEREVENTS)
Create_pipe = pygame.USEREVENT
Create_Flap = pygame.USEREVENT + 1

pygame.time.set_timer(Create_Flap, Sleep_Flap)
pygame.time.set_timer(Create_pipe, Sleep_Pipe)

# Address of Pipes
List_Pipes = []


# Functions
def Flight():
    '''i want my bird flying'''
    global Bird_movement
    
    # Play Flight Sound
    Audio_Flight.play()

    Bird_movement = 0
    Bird_movement -= 8
    return Bird_movement
    

def Generat_Pipe():
    '''How do i bring pipes on the Screen?'''

    Random_Location_Pipe = randrange(400, 800)
    
    rect_Pipe_top = New_Pipe.get_rect(midbottom=(700, Random_Location_Pipe -Distance_Between))
    rect_Pipe_bottom = New_Pipe.get_rect(midtop=(700, Random_Location_Pipe))
    return rect_Pipe_top, rect_Pipe_bottom


def Movment_Pipe(pipes):
    '''How the pipes move?'''
    for pipe in pipes:    
        pipe.centerx -= 4

    inside_pipe = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipe



def Display_Pipe(pipes):
    '''Show Created pipe'''

    for pipe in pipes:
        
        if pipe.bottom >= Display_Height:
            Main_Screen.blit(New_Pipe, pipe)
        else:
            Reversed_pipe = pygame.transform.flip(New_Pipe, False, True)
            Main_Screen.blit(Reversed_pipe, pipe)


def Collision(pipes):
    '''Check Colisions'''
    global Active_Score

    for pipe in pipes:
        if rect_bird.colliderect(pipe):
            
            Active_Score = True
            
            Audio_Collision.play()
            #Audio_Fall.play()
            Audio_gameover.play()
            
            return False

        if rect_bird.top <= -50 or rect_bird.bottom >= Floor_height:
            
            Active_Score = True

            Audio_Collision.play() 
            #Audio_Fall.play()
            Audio_gameover.play()

            return False
    return True

def Game_Over():
    '''What happens after Collision'''
    global Game_Status, Score

    if Game_Status == False:
        
        Audio_gameover.stop()
        Game_Status = True
        Score = 0 
        List_Pipes.clear()
        rect_bird.center = (100, 500)
        Bird_movement = 0
        

def Animation_Flap():
    '''Create the illusion of flying bird'''
    
    Last_Bird = Bird_List[Bird_index]
    New_bird_rect = Last_Bird.get_rect(center=(100, rect_bird.centery))
    return Last_Bird, New_bird_rect


def Counting_points(Status):
    '''Display and count the points you earn'''

    # Font for show your scoure
    Font_Points     = pygame.font.Font('Font/Score.ttf', 60)
    Font_Score      = pygame.font.Font('Font/Score.ttf', 40)
    Font_High_Score = pygame.font.Font('Font/Score.ttf', 40)

    if Status == 'Active': 
        Points = Font_Points.render(str(Score), False, Beige)
        Points_rect = Points.get_rect(center=(288, 100))
        Main_Screen.blit(Points, Points_rect)

    if Status == 'Game_Over':
        # SCORE
        Points = Font_Score.render(f'Score : {Score}', False, Beige)
        Points_rect = Points.get_rect(center=(288, 100))
        Main_Screen.blit(Points, Points_rect)
        
        # HIGH SCORE
        High_Points = Font_High_Score.render(f'HighScore : {High_Score}', False, Beige)
        High_Points_rect = Points.get_rect(center=(250, 850))
        Main_Screen.blit(High_Points, High_Points_rect)


def Update_Score():

    global Score, High_Score, Active_Score
    
    if List_Pipes:

        for pipe in List_Pipes:
            if 95 < pipe.centerx < 105 and Active_Score:
                
                Score += 1
                Audio_jump.play()
                
                Active_Score = False

            if pipe.centerx < 0:
                Active_Score = True

    if Score > High_Score:
        High_Score = Score

    return High_Score


# Game Logic
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            # End Pygame Modules
            pygame.quit()
            # Exit Programm
            sys.exit()

        # Flighting
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                
                Flight()
                # Reset Game
                Game_Over()
                
        # Create pipes
        if event.type == Create_pipe:
            List_Pipes.extend(Generat_Pipe())

        # Create flap
        if event.type == Create_Flap:
            if Bird_index < 2:
                
                Bird_index += 1
            else:
                Bird_index = 0
                
            My_Birds, rect_bird = Animation_Flap()

    # Display & Mein Screen (background)   
    Main_Screen.blit(Page_Background, (0, 0))
    
    # Game Status
    if Game_Status:

        # Blit Pipes
        List_Pipes = Movment_Pipe(List_Pipes)
        Display_Pipe(List_Pipes)

        # Display Bird image
        Main_Screen.blit(My_Birds, rect_bird)

        # Check for Collision
        Game_Status = Collision(List_Pipes)

        # Force of gravity & Movment
        Bird_movement += gravity
        rect_bird.centery += Bird_movement

        # Display Score
        Update_Score()
        Counting_points('Active')

    else:
        
        Main_Screen.blit(Welcome_Page, Welcome_Page_rect)
        Counting_points('Game_Over')

    # Display & Mein Screen (ground,Floor)
    Main_Screen.blit(ground_game   , (floor_x, Floor_height))
    Main_Screen.blit(ground_game   , (floor_x + Display_Width, Floor_height))


    floor_x -= 1
    
    if floor_x <= - Display_Width:
        floor_x = 0
    
    
    pygame.display.update()       
    
    Clock.tick(FPS) # Set Game Speed

# THE END OF CODE