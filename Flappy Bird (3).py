# MohammadReza.D

import pygame
import sys
import random
import time


# Start Pygame Modules
pygame.init()

# All Variable
FPS = 90

Display_Width  = 410
Display_Height = 710

# Floor
ground_game    = pygame.transform.scale(pygame.image.load('Assets/Background/ground.png'),(410, 135))
Floor_height   = 620
Floor_Bad      = 630
floor_x        = 0

# Force of gravity
gravity       = 0.25
Bird_movement = 0
Movment_Low   = 15
Bird_index    = 0
playerIndex   = 0

# Time of Creation pipes & bird
Sleep_Pipe = 1350
Sleep_Flap = 100
Sleep_wing = 150

# Distances
Distance_Between = 150

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

# icon game
Icon = pygame.image.load('Assets/Logo/Pipe_Bird_Logo.png')
pygame.display.set_icon(Icon)

# Timer & Clock
Clock = pygame.time.Clock()



# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = [
    # Red bird
    (
        'Assets/Bird/red-bird-upflap.png',
        'Assets/Bird/red-bird-midflap.png',
        'Assets/Bird/red-bird-downflap.png',
    ),
    # blue bird
    (
        'Assets/Bird/blue-bird-upflap.png',
        'Assets/Bird/blue-bird-midflap.png',
        'Assets/Bird/blue-bird-downflap.png',
    ),
    # yellow bird
    (
        'Assets/Bird/yellow-bird-upflap.png',
        'Assets/Bird/yellow-bird-midflap.png',
        'Assets/Bird/yellow-bird-downflap.png', 
    ),
]


# list of backgrounds
BACKGROUNDS_LIST = [
    'Assets/Background/background-day2.png',
    'Assets/Background/background-night1.png',   
]

# list of pipes
PIPES_LIST = [
    'Assets/Pipe/pipe-green.png',
    'Assets/Pipe/pipe-red.png',
]


# Audio
Audio_Count     = pygame.mixer.Sound('Assets/Audio/Count.ogg')
Audio_Collision = pygame.mixer.Sound('Assets/Audio/Collision.ogg')
Audio_Fall      = pygame.mixer.Sound('Assets/Audio/Fall.ogg')
Audio_Flight    = pygame.mixer.Sound('Assets/Audio/Flight.ogg')
Audio_Wind      = pygame.mixer.Sound('Assets/Audio/Wind.ogg')
Audio_gameover  = pygame.mixer.Sound('Assets/Audio/gameover.wav')
Audio_jump      = pygame.mixer.Sound('Assets/Audio/jump.wav')


# Wecome Page
Welcome_Page = pygame.transform.scale(pygame.image.load('Assets/Write/message.png'),(257, 373))
Welcome_Page_rect = Welcome_Page.get_rect(center=(205, 300))

# Game Over Screen
Game_Over_Page = pygame.transform.scale(pygame.image.load('Assets/Write/gameover.png'),(268, 59))
Game_Over_rect = Game_Over_Page.get_rect(center=(205, 300))


# Select random background
Random_Page = random.randint(0, len(BACKGROUNDS_LIST) - 1)
Page_Background = pygame.transform.scale(pygame.image.load(BACKGROUNDS_LIST[Random_Page]),(410, 710))

# Select random player
Random_Player = random.randint(0, len(PLAYERS_LIST) - 1)
My_Bird = [
    pygame.transform.scale(pygame.image.load(PLAYERS_LIST[Random_Player][0]),(48, 34)),
    pygame.transform.scale(pygame.image.load(PLAYERS_LIST[Random_Player][1]),(48, 34)),
    pygame.transform.scale(pygame.image.load(PLAYERS_LIST[Random_Player][2]),(48, 34)),
]

# Select random pipe
Random_Pipe = random.randint(0, len(PIPES_LIST) -1)
New_Pipe = pygame.transform.scale(pygame.image.load(PIPES_LIST[Random_Pipe]),(72, 448)) 


# Rectangle Bird
rect_bird = My_Bird[0].get_rect(center=(60, 340))


# Bird List
Bird_List = [My_Bird[0], My_Bird[1], My_Bird[2]]
My_Birds  = Bird_List[Bird_index]

# Time to create pipes & Bird (USEREVENTS)
Create_pipe = pygame.USEREVENT
Create_Flap = pygame.USEREVENT + 1
Create_wing  = pygame.USEREVENT + 2

pygame.time.set_timer(Create_Flap, Sleep_Flap)
pygame.time.set_timer(Create_pipe, Sleep_Pipe)
pygame.time.set_timer(Create_wing, Sleep_wing)

# Address of Pipes
List_Pipes = []



# Functions

def Welcome():
    '''Welcome to Flappy Bird!'''

    Main_Screen.blit(Welcome_Page, Welcome_Page_rect)



def Flight():
    '''i want my bird flying'''
    global Bird_movement
    
    # Play Flight Sound
    Audio_Flight.play()

    Bird_movement = 0
    Bird_movement -= 6.5
    return Bird_movement
    


def Generat_Pipe():
    '''How do i bring pipes on the Screen?'''

    Random_Location_Pipe = random.randrange(270, 560)
    
    rect_Pipe_top = New_Pipe.get_rect(midbottom=(700, Random_Location_Pipe - Distance_Between))
    rect_Pipe_bottom = New_Pipe.get_rect(midtop=(700, Random_Location_Pipe))
    return rect_Pipe_top, rect_Pipe_bottom



def Movment_Pipe(pipes):
    '''How the pipes move?'''
    for pipe in pipes:    
        pipe.centerx -= 2

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



def Reset_Game():
    '''What happens after Collision'''
    
    global Game_Status, Score

    if Game_Status == False:
        
        Audio_gameover.stop()
        Game_Status = True
        Score = 0 
        List_Pipes.clear()
        rect_bird.center = (200, 340)
        Bird_movement = 0
        Welcome_Display()
        


def Collision(pipes):
    '''Check Colisions or Crashed'''
    global Active_Score

    for pipe in pipes:
        
        if rect_bird.colliderect(pipe):
            
            Active_Score = True
            
            Audio_Collision.play()
                        
            Audio_gameover.play()
            
            time.sleep(3)

            return False

        if rect_bird.top <= -100 or rect_bird.bottom >= Floor_Bad:
            
            Active_Score = True

            Audio_Collision.play() 
            #Audio_Fall.play()
            
            time.sleep(3)

            return False
    return True



def Game_Over(pipes):
    '''What happens when I lose?'''

    for pipe in pipes:
        
        if rect_bird.colliderect(pipe):
            
            Main_Screen.blit(Game_Over_Page, Game_Over_rect)

        elif rect_bird.top <= -100 or rect_bird.bottom >= Floor_Bad:
        
            Main_Screen.blit(Game_Over_Page, Game_Over_rect)


 
def Animation_Flap():
    '''Create the illusion of flying bird'''
    
    Last_Bird = Bird_List[Bird_index]
    New_bird_rect = Last_Bird.get_rect(center=(100, rect_bird.centery))
    return Last_Bird, New_bird_rect



def Counting_points(Status):
    '''Display and count the points you earn'''

    # Font for show your scoure
    Font_Points     = pygame.font.Font('Assets/Font/Score.ttf', 60)
    Font_Score      = pygame.font.Font('Assets/Font/Score.ttf', 35)
    Font_High_Score = pygame.font.Font('Assets/Font/Score.ttf', 35)

    if Status == 'Active': 
        Points = Font_Points.render(str(Score), False, White)
        Points_rect = Points.get_rect(center=(205, 80))
        Main_Screen.blit(Points, Points_rect)

    if Status == 'Game_Over':
        # SCORE
        Points = Font_Score.render(f'Score : {Score}', False, Beige)
        Points_rect = Points.get_rect(center=(205, 120))
        Main_Screen.blit(Points, Points_rect)
        
        # HIGH SCORE
        High_Points = Font_High_Score.render(f'HighScore : {High_Score}', False, Beige)
        High_Points_rect = Points.get_rect(center=(170, 350))
        Main_Screen.blit(High_Points, High_Points_rect)



def Update_Score():
    '''Update Points by passing any obstacle'''

    global Score, High_Score, Active_Score
    
    if List_Pipes:

        for pipe in List_Pipes:
            
            if 50 < pipe.centerx < 60 and Active_Score:
                
                Score += 1
                Audio_jump.play()
                
                Active_Score = False

            if pipe.centerx < 0:
                Active_Score = True

    if Score > High_Score:
        High_Score = Score

    return High_Score



def Energy_Bird(Energy):
    '''My bird has a lot of energy to start with'''
    
    if abs(Energy['val']) == Movment_Low:
        Energy['dir'] *= -1

    if Energy['dir'] == 1:
        Energy['val'] += 1
    
    else:
        Energy['val'] -= 1



def Welcome_Display():
    '''Show Welcome page to start the game'''
    
    global floor_x, Bird_List, Bird_index
    
    # iterator used to change playerIndex after every 5th iteration
    loop = 0

    playerx = 60
    playery = 340

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = ground_game.get_width() - Page_Background.get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                
                # End Pygame Modules
                pygame.quit()
                # Exit Programm
                sys.exit()
            
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                # make first flap sound and return values for mainGame
                Flight()
    
                return {
                    'playery': playery + playerShmVals['val'],
                }


            # Wining Bird
            if event.type == Create_wing:
                if Bird_index < 2:
                    Bird_index += 1
                
                else:
                    Bird_index = 0
                    Last_Bird = Bird_List[Bird_index]
                    
            
        # Down & Up flap (Movement)
        Energy_Bird(playerShmVals)

        # Display & Mein Screen (background)   
        Main_Screen.blit(Page_Background, (0, 0))
        
        Main_Screen.blit(Bird_List[Bird_index],
                    (playerx, playery + playerShmVals['val']))
        
        Welcome()
        
        Main_Screen.blit(ground_game   , (floor_x, Floor_height))
        Main_Screen.blit(ground_game   , (floor_x + Display_Width, Floor_height))


        floor_x -= 2.1
    
        if floor_x <= - Display_Width:
            floor_x = 0

        pygame.display.update()
        
        Clock.tick(FPS)


Welcome_Display()



# Game Logic
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            
            # End Pygame Modules
            pygame.quit()
            # Exit Programm
            sys.exit()

        # Flighting
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            Flight()

            Reset_Game()

                
        
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

    # Display & Mein Screen (ground,Floor)
    Main_Screen.blit(ground_game   , (floor_x, Floor_height))
    Main_Screen.blit(ground_game   , (floor_x + Display_Width, Floor_height))
    

    # Game Status
    if Game_Status:


        # Blit Pipes
        List_Pipes = Movment_Pipe(List_Pipes)
        Display_Pipe(List_Pipes)

        # Display & Mein Screen (ground,Floor)
        Main_Screen.blit(ground_game   , (floor_x, Floor_height))
        Main_Screen.blit(ground_game   , (floor_x + Display_Width, Floor_height))

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
        
        Game_Over(List_Pipes)

    else:

        Counting_points('Game_Over')

    
    floor_x -= 2
    
    if floor_x <= - Display_Width:
        floor_x = 0
    
    
    pygame.display.update()       
    
    Clock.tick(FPS) # Set Game Speed

# Thanks for reading my code. How was it?