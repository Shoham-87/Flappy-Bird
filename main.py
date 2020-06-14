import pygame
import sys
import random
from pygame.locals import *
pygame.init()
screen_width=400
screen_height=550
ground=int(screen_height*0.78)
FPS=40
clock=pygame.time.Clock()
Game_images={}
Game_sounds={}
player='Images/Bird.png'
background='Images/background.png'
pipe='Images/pipe.png'
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird By Shoham Dey Sarkar")
gameIcon = pygame.image.load('Images/Bird.png')
pygame.display.set_icon(gameIcon)
pygame.display.update()

def Welcome():
    """
    To Produce the Welcome Screen
    """
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(Game_images['Intro'],(0,0))
                screen.blit(Game_images['Hover_Title'],(basex,ground))
                pygame.display.update()
                clock.tick(FPS)
def MainGame():
    score = 0
    playerx = int(screen_width/6)
    playery = int(screen_width/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': screen_width+200, 'y':newPipe1[0]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': screen_width+200, 'y':newPipe1[1]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    Game_sounds['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            Welcome()
            return     

        #Score
        playerMidPos = playerx + Game_images['Player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + Game_images['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                Game_sounds['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = Game_images['Player'].get_height()
        playery = playery + min(playerVelY, ground - playery - playerHeight)

        # Pipes towards  left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < - Game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        screen.blit(Game_images['Background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(Game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(Game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(Game_images['Base'], (basex, ground))
        screen.blit(Game_images['Player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += Game_images['Number'][digit].get_width()
        Xoffset = (screen_width - width)/2

        for digit in myDigits:
            screen.blit(Game_images['Number'][digit], (Xoffset, screen_height*0.12))
            Xoffset += Game_images['Number'][digit].get_width()
        pygame.display.update()
        clock.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> ground - 25  or playery<0:
        Game_sounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = Game_images['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < Game_images['pipe'][0].get_width()):
            Game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + Game_images['Player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < Game_images['pipe'][0].get_width():
            Game_sounds['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = Game_images['pipe'][0].get_height()
    offset = screen_height/3 
    y2 = offset + random.randrange(0, int(screen_height - Game_images['Base'].get_height()  - 1.2 *offset))
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe
if __name__ == "__main__":
    #loading the Images
    Game_images['Number']=(
    pygame.image.load('Images/0.png').convert_alpha(),
    pygame.image.load('Images/1.png').convert_alpha(),
    pygame.image.load('Images/2.png').convert_alpha(),
    pygame.image.load('Images/3.png').convert_alpha(),
    pygame.image.load('Images/4.png').convert_alpha(),
    pygame.image.load('Images/5.png').convert_alpha(),
    pygame.image.load('Images/6.png').convert_alpha(),
    pygame.image.load('Images/7.png').convert_alpha(),
    pygame.image.load('Images/8.png').convert_alpha(),
    pygame.image.load('Images/9.png').convert_alpha()
    )
    Game_images['Intro']=pygame.image.load('Images/Intro.jpg').convert_alpha()
    Game_images['Player']=pygame.image.load(player).convert_alpha() 
    Game_images['Hover_Title']=pygame.image.load('Images/Hover_Title.jpg').convert_alpha() 
    Game_images['Base']=pygame.image.load('Images/Ground.png').convert_alpha()  
    Game_images['Background']=pygame.image.load(background).convert()   
    Game_images['pipe']=(pygame.transform.rotate(pygame.image.load(pipe), 180).convert_alpha(),
    pygame.image.load(pipe).convert_alpha())

    #Loading the Sound Effect

    Game_sounds['die'] = pygame.mixer.Sound('Sounds/die.wav')
    Game_sounds['hit'] = pygame.mixer.Sound('Sounds/hit.wav')
    Game_sounds['point'] = pygame.mixer.Sound('Sounds/point.wav')
    Game_sounds['swoosh'] = pygame.mixer.Sound('Sounds/swoosh.wav')
    Game_sounds['wing'] = pygame.mixer.Sound('Sounds/wing.wav')
    while True:
        Welcome()
        MainGame()
