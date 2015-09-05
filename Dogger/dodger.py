#!/usr/bin/python

#import pygame
import pygame , random , sys , time
from pygame.locals import *

# setup pygame
pygame.init()

# set up clock
mainClock = pygame.time.Clock()

# Setup window
WindowWidth = 600
WINDOWHeight = 600
windowSurface = pygame.display.set_mode((WindowWidth, WINDOWHeight))
pygame.display.set_caption('Dog doger')

# Hide mouse
pygame.mouse.set_visible(False)


# set up fonts
font = pygame.font.SysFont(None, 48)

# Import high score
f = open("Savedata.txt","r+")
HighScore = f.read()
f.close()

# Import and load images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
CatImage = pygame.image.load('Cat.png')
coinimage = pygame.image.load('coin.png')

TEXTCOLOR = (255, 255, 255)
FPS = 40
CatMinSize = 10
CatMaxSize = 40
CatMinSPEED = 1
CatMaxSPEED = 8
AddNewCatRate = 6
PLAYERMOVERATE = 5
coinMinSize = 20
coinMaxSize = 50
coinMinspeed = 6
coinMaxspeed = 6
AddNewCoinRate = 300 #300
CoinPoints = 0
   

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    pygame.quit()
                    exit()
                return

def playerHasHitCat(playerRect, Cats , coin):
    for b in Cats:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def playerHasHitcoin(playerRect, Cats , coin):
    for b in coin:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



# show the start screen
drawText('Dog dodger', font, windowSurface, (WindowWidth / 3), (WINDOWHeight / 3) - 100)
drawText('Press a key to start.', font, windowSurface, (WindowWidth / 3) - 30, (WINDOWHeight / 3) + 50 - 100)
drawText('Made by:', font, windowSurface, (WindowWidth / 3) - 30, (WINDOWHeight / 3) + 150 )
drawText('ZachZ', font, windowSurface, (WindowWidth / 3) - 30, (WINDOWHeight / 3) + 200)
pygame.display.update()
waitForPlayerToPressKey()
while True:
    # set up the start of the game
    lose = 1
    Cats = []
    score = 0
    playerRect.topleft = (WindowWidth / 2, WINDOWHeight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    CatAddCounter = 0
    coin = []
    CoinAddCounter = 0

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == ord('a'): moveLeft = True
                if event.key == ord('d'): moveRight = True
                if event.key == ord('w'): moveUp = True
                if event.key == ord('s'): moveDown = True
                    

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                # Stop key movement
                moveLeft = False
                moveRight = False
                moveUp = False
                moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new Cats at the top of the screen, if needed.
        CatAddCounter += 1
        CoinAddCounter += 1
        if CatAddCounter == AddNewCatRate:
            CatAddCounter = 0
            CatSize = random.randint(CatMinSize, CatMaxSize)
            newCat = {'rect': pygame.Rect(random.randint(0, WindowWidth-CatSize), 0 - CatSize, CatSize, CatSize),
                        'speed': random.randint(CatMinSPEED, CatMaxSPEED),
                        'surface':pygame.transform.scale(CatImage, (CatSize, CatSize)),
                        }

            Cats.append(newCat)
        if CoinAddCounter == AddNewCoinRate:
            CoinAddCounter = 0
            Coinsize = random.randint(coinMinSize, coinMaxSize)
            newcoin = {'rect': pygame.Rect(random.randint(0, WindowWidth-Coinsize), 0 - Coinsize, Coinsize, Coinsize),
                        'speed': random.randint(coinMinspeed, coinMaxspeed),
                        'surface':pygame.transform.scale(coinimage, (Coinsize, Coinsize)),
                        }

            coin.append(newcoin)

        # Move the player around.
        if moveLeft and playerRect.left > 0:  
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WindowWidth:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHeight:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the Cats down.
        for b in Cats:
            b['rect'].move_ip(0, b['speed'])
         
        for b in coin:
            b['rect'].move_ip(0, b['speed'])
         # Delete Cats that have fallen past the bottom.
        for b in Cats[:]:
            if b['rect'].top > WINDOWHeight:
                Cats.remove(b)
        for b in coin[:]:
            if b['rect'].top > WINDOWHeight:
                coin.remove(b)
        
        # Draw the game world on the window.
        windowSurface.fill((0,0,0))

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('High Score: %s' % (HighScore), font, windowSurface, 10, 40)
        drawText('Coins: %s' % (CoinPoints), font, windowSurface, 10, 80)
        
        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each cat
        for b in Cats:
            windowSurface.blit(b['surface'], b['rect'])
            
        # Draw each coin
        for b in coin:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the Cats have hit the player.
        if playerHasHitCat(playerRect, Cats, coin):
            break
         
        # Check if player has hit coin
        if playerHasHitcoin(playerRect, Cats, coin):
            CoinPoints = CoinPoints + 1
            coin.remove(b)
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    CP = 100*CoinPoints
    CoinPoints = 0
    print CP
    get_CP = 1
    endc = 0
    while get_CP==1:
        if int(CP)>0:
            print "trying"
            CP = CP - 1
            score = score + 1
            windowSurface.fill((0,0,200))
             
            drawText('Score: %s /' % (score), pygame.font.SysFont(None, 100), windowSurface, 10, 0)
            drawText('High Score: %s' % (HighScore), font, windowSurface, 10, 60)
            pygame.display.update()
            time.sleep(0.01)
            
        else:
            windowSurface.fill((150,0,0))
            drawText('Score: %s /' % (score), pygame.font.SysFont(None, 100), windowSurface, 10, 0)
            drawText('High Score: %s' % (HighScore), font, windowSurface, 10, 60)
            pygame.display.update()
            get_CP = 0
        
    if int(HighScore) < int(score):
        print "New high score"
        HighScore = score # set new top score
        ##Saves score
        f = open("Savedata.txt","w")
        f.write(str(score))
        f.close()
        windowSurface.fill((255,0,0))
        drawText('Score: %s /' % (score), pygame.font.SysFont(None, 100), windowSurface, 10, 0)
        drawText('High Score: %s' % (HighScore), font, windowSurface, 10, 60)
        drawText('High score', pygame.font.SysFont(None,120), windowSurface, (WindowWidth / 3 - 100), (WINDOWHeight / 3))
        drawText('Press a key to play again.', font, windowSurface, (WindowWidth / 3) - 100, (WINDOWHeight / 3) + 75)
        
        pygame.display.update()
        
        lose = 0
    if lose == 1:
        drawText('GAME OVER', font, windowSurface, (WindowWidth / 3), (WINDOWHeight / 3))
        drawText('Press a key to play again.', font, windowSurface, (WindowWidth / 3) - 90, (WINDOWHeight / 3) + 30)
        pygame.display.update()
    waitForPlayerToPressKey()
