#       COPYRIGHT® 2020
#       ——————————————
#       PyFlappy Bird
#       Made by "Charitra Agarwal"
#       "www.youtube.com/c/EverythingComputerized"



      ############               ###
     #############              #####
    ###                        ### ###
   ###                        ###   ###
  ###                        ###     ###
  ###                       ###       ###
  ###                      ###############
  ###                     #################
   ###                    ###           ###
    ###                   ###           ###
     #############        ###           ###
      ############        ###           ###



# Instructions:- 
# 1. Install pygame library first to run the program
# 2. Assets should be correctly placed in the path


import sys, pygame, math
from pygame.locals import *
from time import sleep
from random import randint
pygame.init()

############ SCREEN SETUP ############

# Screen info
displayInfo = pygame.display.Info()
SCREENWIDTH, SCREENHEIGHT = displayInfo.current_w, displayInfo.current_h

# Screen dimensions
if SCREENWIDTH >= SCREENHEIGHT: # best resolution = 1920x1080, ratio = 1.7777777778
    SCREENRATIO = 1.7777777778
    SCREENWIDTH = int(SCREENHEIGHT/SCREENRATIO)

# Set up the screen
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Flappy Bird")


########## CONSTANTS ##########
GROUNDY = int(SCREENHEIGHT*0.9)   # for baseline
FPSCLOCK = pygame.time.Clock()    # FPS counter
FPS = 60                          # FPS
GAME_SPRITES, GAME_SOUNDS = {}, {}  # dictionary for resources
SPRITEPATH = 'gallery/sprites/{0}.png'    # path for image files
AUDIOPATH = 'gallery/audio/{0}.wav'       # path for sound files
LIFT = math.ceil(SCREENHEIGHT / 240)          # speed of upward movement
GRAVITY = SCREENHEIGHT / 2742.857142857143    # speed of downward movement
SPEED = SCREENWIDTH / 135              # speed of pipes
HIGHSCORE = 0                          # keep the record of live high score
PREVIOUSHIGHSCORE = 0                  # keep tge record of previous high score


def updateHighscore(score):
    """Helper Functiont to Write the highscore value to the database"""
    highscorefile = open('highscore.dat', 'w')
    highscorefile.write(str(score))
    highscorefile.close()
# Load highscore from database
try:
    with open('highscore.dat', 'r') as highscorefile: HIGHSCORE = int(highscorefile.read())
except Exception as e:
    HIGHSCORE = 0
    updateHighscore(HIGHSCORE)
PREVIOUSHIGHSCORE = HIGHSCORE

############  GAME ELEMENTS ############

## Audio files ##
sound_files = ['die', 'hit', 'point', 'swoosh', 'wing']    # Filenames
for file in sound_files: GAME_SOUNDS[file] = pygame.mixer.Sound(AUDIOPATH.format(file))

## Image files ##
# Score-digit
GAME_SPRITES['numbers'] = [pygame.image.load(SPRITEPATH.format(str(num))).convert_alpha() for num in range(0, 10)]
# Bird
birdNames = ['bluebird-upflap', 'redbird-upflap', 'yellowbird-upflap']
GAME_SPRITES['player'] = [pygame.image.load(SPRITEPATH.format(name)).convert_alpha() for name in birdNames]
# Base
GAME_SPRITES['base'] = pygame.image.load(SPRITEPATH.format('base')).convert_alpha()
# Scoreboard
GAME_SPRITES['scoreboard'] = pygame.image.load(SPRITEPATH.format('scoreboard')).convert_alpha()
# Pipe
GAME_SPRITES['pipe'] = [
    pygame.transform.rotate(pygame.image.load(SPRITEPATH.format('pipe')), 180).convert_alpha(),
    pygame.image.load(SPRITEPATH.format('pipe')).convert_alpha()]
# Background
backgroundNames = ['background-day', 'background-night']
GAME_SPRITES['background'] = [pygame.image.load(SPRITEPATH.format(name)).convert() for name in backgroundNames]
# Banner
GAME_SPRITES['message'] = pygame.image.load(SPRITEPATH.format('message')).convert_alpha()   
# Medals
medalNames = ['bronze', 'silver', 'gold', 'platinum']
GAME_SPRITES['medal'] = [pygame.image.load(SPRITEPATH.format(name)).convert_alpha() for name in medalNames]
# Tap-tap
GAME_SPRITES['taptap'] = pygame.image.load(SPRITEPATH.format('tap-tap')).convert_alpha()
# New Highscore sticker
GAME_SPRITES['new'] = pygame.image.load(SPRITEPATH.format('new-highscore')).convert_alpha()


#### SIZE ALTERATION ####
# Pipe size
GAME_SPRITES['pipe'][0] = pygame.transform.scale(GAME_SPRITES['pipe'][0], (SCREENWIDTH//5, SCREENWIDTH//5*6))
GAME_SPRITES['pipe'][1] = pygame.transform.scale(GAME_SPRITES['pipe'][1], (SCREENWIDTH//5, SCREENWIDTH//5*6))
# Bird size (size set for homescreen only)
for _ in range(0, len(GAME_SPRITES['player'])): GAME_SPRITES['player'][_] = pygame.transform.scale(GAME_SPRITES['player'][_] , ( int(SCREENWIDTH*0.17), int(SCREENHEIGHT*0.08)) )
# Base size
GAME_SPRITES['base'] = pygame.transform.scale(GAME_SPRITES['base'], (SCREENWIDTH, SCREENHEIGHT//5))    
# Background size
GAME_SPRITES['background'][0] = pygame.transform.scale(GAME_SPRITES['background'][0], (SCREENWIDTH, SCREENHEIGHT))
GAME_SPRITES['background'][1] = pygame.transform.scale(GAME_SPRITES['background'][1], (SCREENWIDTH, SCREENHEIGHT))
# Banner size
messageRatio = GAME_SPRITES['message'].get_height()/GAME_SPRITES['message'].get_width()
GAME_SPRITES['message']= pygame.transform.scale(GAME_SPRITES['message'], (int(SCREENWIDTH*0.55), int(SCREENWIDTH*0.55*messageRatio))).convert_alpha()    
# Tap tap size
GAME_SPRITES['taptap']= pygame.transform.scale(GAME_SPRITES['taptap'], (int(SCREENWIDTH*0.4), int(SCREENWIDTH*0.4))).convert_alpha()    
# New highscore sticker size
newRatio = GAME_SPRITES['new'].get_height()/GAME_SPRITES['new'].get_width()
GAME_SPRITES['new'] = pygame.transform.scale(GAME_SPRITES['new'], (int(SCREENWIDTH//11), int(newRatio*SCREENWIDTH/11)))


########## GAME LOGIC ##########

def welcomeScreen(backgroundImage, playerImage):
    """Shows the HomeSCreen of Game"""
    # Bird co-ordinates
    playerx, playery = (SCREENWIDTH-playerImage.get_width())//2, (SCREENHEIGHT//2 + SCREENHEIGHT*0.07)
    y = playery
    up, down, movement = True, False, 40
    # Banner co-ordinates 
    messagex, messagey = (SCREENWIDTH-GAME_SPRITES['message'].get_width())//2, (SCREENHEIGHT-GAME_SPRITES['message'].get_height()*1.9)//2
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()                
            elif event.type == MOUSEBUTTONDOWN or event.type == FINGERDOWN or (event.type==KEYDOWN and event.key == K_SPACE) or (event.type==KEYDOWN and event.key == K_UP):
                GAME_SOUNDS['wing'].play()
                return
            else: pass
        
        SCREEN.blit(backgroundImage, (0, 0))
        SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        SCREEN.blit(playerImage, (playerx, y))
        SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
        pygame.display.update()
        
        # For slow up-down movement of bird
        if up:
            y -= 1
            movement -= 1
            if movement<=0: movement,up,down = 80,False,True
        if down:
            y += 1
            movement -= 1
            if movement<=0: movement,up,down = 80,True,False
        
        FPSCLOCK.tick(FPS)

# generate co-ordinates of random pipes
def randomPipe(w, h):    
    """Helper function which generates coordinate points for random pipes"""
    #pipe = 216 x 1296
    offset = int(SCREENHEIGHT*0.11)    # distance from screen edges
    distance = int(SCREENHEIGHT*0.21)    # vertical distance between pipes    
    x = SCREENWIDTH    # generate pipe at the end of screen
    y1 = randint(offset-h, GROUNDY-distance-offset-h)
    y2 = y1+h+distance
    points = {'x1': x, 'y1': y1, 'x2': x, 'y2': y2}
    return points


# get a list of digits from scoreNunbers
def getDigits(num):
    """Helper function for returning list of digits from a number"""
    digits = []
    if num==0:
        return [0]
    while num>0:
        digits.append(num%10)    # add digits to the list
        num //= 10
    digits.reverse()    # reverse the order list  
    return digits

# score display during game play and on scoreboard during gameover
def scoreDisplay(score, isGameover = False, scoreboardxy = 0, scoreboardwh = 0):
    """Display live score in gameplay, final score on scorboard, highscore on scoreboard"""
    global HIGHSCORE
    if score > HIGHSCORE: HIGHSCORE = score    # continuously update highscore
    # (height : width) ratio of digit images
    numRatio = 1.5 # GAME_SPRITES['numbers'][0].get_height()/GAME_SPRITES['numbers'][0].get_width()
    # CONSTANTS
    if not isGameover: numWidth = SCREENWIDTH//12    # width of digit on gameplay
    else: numWidth = SCREENWIDTH//25    # width of digit at gameover
    numHeight = int(numWidth * numRatio)    # height of digit
    digitCount = 0    # keep track of which digit is getting printed
    digits = getDigits(score)         # store digits of the score
    
    # display score
    for digit in digits:
        digitCount += 1
        if not isGameover:
            # points of digit at gameplay
            numx = (SCREENWIDTH-numWidth*len(digits)+(digitCount-1)*2*numWidth)//2
            numy = SCREENHEIGHT//10
        else:
            # points of score digit at gameover
            numx = scoreboardxy[0]+scoreboardwh[0]+numWidth*(digitCount-3-len(digits))
            numy = scoreboardxy[1]+numHeight*2.1
        # resize image
        digitImage = pygame.transform.scale(GAME_SPRITES['numbers'][digit], (numWidth, numHeight))
        # display score image
        SCREEN.blit(digitImage, (numx, numy))
 
   # display highscore image
    if isGameover:
        digitCount = 0    # keep track of which digit is getting printed
        digits = getDigits(HIGHSCORE)         # store digits of the highscore
        for digit in digits:
            digitCount += 1    
            # points of highscore digit at gameover
            numx = scoreboardxy[0]+scoreboardwh[0]+numWidth*(digitCount-3-len(digits))
            numy = scoreboardxy[1]+numHeight*4.6        
            # resize image
            digitImage = pygame.transform.scale(GAME_SPRITES['numbers'][digit], (numWidth, numHeight))
            # display highscore image
            SCREEN.blit(digitImage, (numx, numy))

# Display falling bird after it collides and dies                
def fallOver(backgroundImage, birdxy, birdImage, pipePoint1, pipeImage, isPipe2, pipePoint2):
        x, y = birdxy    # current position of bird
        jumpCount, dieSound = LIFT, False
        GAME_SOUNDS['hit'].play()
        while True:
            # display all the assets
            SCREEN.blit(backgroundImage, (0, 0))
            SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
            SCREEN.blit(pipeImage[0], (pipePoint1['x1'], pipePoint1['y1']))
            SCREEN.blit(pipeImage[1], (pipePoint1['x2'], pipePoint1['y2']))
            if isPipe2:
                SCREEN.blit(pipeImage[0], (pipePoint2['x1'], pipePoint2['y1']))
                SCREEN.blit(pipeImage[1], (pipePoint2['x2'], pipePoint2['y2']))
            # display accelerating bird image
            SCREEN.blit(birdImage, (x, y))            
            if y < GROUNDY:
                y -= (jumpCount*abs(jumpCount))*0.5
                jumpCount -= GRAVITY
                if not dieSound:
                    GAME_SOUNDS['die'].play()
                    dieSound = True
            
            if y >= GROUNDY: return    # exit after bird reaches the ground
            pygame.display.update()
            FPSCLOCK.tick(FPS)

######## MAIN GAME FUNCTION #########
def gamePlay(backgroundImage, playerImage):
    """It is the actual game function. It contains the actual user-game interaction"""
    # position of bird on screen
    
    x, y = (SCREENWIDTH-playerImage.get_width()*3)//2, (SCREENHEIGHT//2 - SCREENHEIGHT*0.03)
    ######## CONSTANTS ########
    # get pipe dimensions
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()     
    pipeWidth = GAME_SPRITES['pipe'][0].get_width()
    # game variables
    isJump, newPipe = True, True
    jumpCount = LIFT
    pipeCount, pipePoint1, pipePoint2 = 1, {}, {}
    score, scoreCounter = 0, True    # add score only once per pipe
    
    # bird size adjust
    playerImage = pygame.transform.scale(playerImage, (int(SCREENWIDTH*0.14), int(SCREENHEIGHT*0.06))).convert_alpha()        
    birdWidth = playerImage.get_width()
    birdHeight = playerImage.get_height()
    
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE): return score
            if event.type == FINGERDOWN or event.type == MOUSEBUTTONDOWN or (event.type==KEYDOWN and (event.key == K_SPACE or event.key==pygame.K_UP)):
                isJump, jumpCount = True, LIFT
                GAME_SOUNDS['wing'].play()
                
        # bird acceleration
        if isJump:
            # stop at the baseline
            if y < GROUNDY:
                y -= (jumpCount*abs(jumpCount))*0.5
                jumpCount -= GRAVITY                      
            # GAMEOVER        
            else:
                y = GROUNDY-playerImage.get_height()
                isPipe2 = False
                if pipeCount == 2: isPipe2 = True
                fallOver(backgroundImage,(x, y),playerImage,pipePoint1,GAME_SPRITES['pipe'] ,isPipe2,pipePoint2)
                return score   
        # display the assets
        SCREEN.blit(backgroundImage, (0, 0))
        SCREEN.blit(playerImage,(x, y))    
        SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
        
        # 1st pipe generation
        if newPipe:
            pipePoint1 = randomPipe(pipeWidth, pipeHeight)
            newPipe = False    # stop after generating one pipe
            
        # 2nd second generation
        if pipePoint1['x1'] < (SCREENWIDTH-pipeWidth)//2:
            if pipeCount < 2:
                pipePoint2 = randomPipe(pipeWidth, pipeHeight)
                pipeCount += 1
        
        # remove 1st pipe after it crosses the screen    
        if pipePoint1['x1'] <= 10-pipeWidth:
            pipePoint1 = pipePoint2
            pipeCount, pipePoint2, scoreCounter = 1, {}, True
            
        # display 2nd pipe
        if pipeCount == 2:
            SCREEN.blit(GAME_SPRITES['pipe'][0], (pipePoint2['x1'], pipePoint2['y1']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (pipePoint2['x2'], pipePoint2['y2']))
        
            # move 2nd pipe
            pipePoint2['x1'] -= SPEED
            pipePoint2['x2'] -= SPEED               
         
        # move 1st pipe
        if pipePoint1['x1'] > -pipeWidth:
            pipePoint1['x1'] -= SPEED
            pipePoint1['x2'] -= SPEED          
        
        #collision checker
        if pipePoint1['x1'] <= x+birdWidth <= pipePoint1['x1']+pipeWidth+birdWidth:
            if pipePoint1['y1']+pipeHeight-birdHeight//10 < y < pipePoint1['y2']-birdHeight+birdHeight//4: pass
            # GAMEOVER
            else:
                isPipe2 = False
                if pipeCount == 2: isPipe2 = True
                fallOver(backgroundImage, (x, y), playerImage, pipePoint1, GAME_SPRITES['pipe'] , isPipe2 , pipePoint2 )
                return score
                    
        # score calculator
        if x > pipePoint1['x1']-birdWidth//2:
            if scoreCounter == True:
                score += 1
                GAME_SOUNDS['point'].play()
                scoreCounter = False
                
        SCREEN.blit(GAME_SPRITES['pipe'][0], (pipePoint1['x1'], pipePoint1['y1']))
        SCREEN.blit(GAME_SPRITES['pipe'][1], (pipePoint1['x2'], pipePoint1['y2']))
        scoreDisplay(score) 
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    

# display the scoreboard screen at GAMEOVER
def gameover(score, backgroundImage, playerImage):
    GAME_SOUNDS['swoosh'].play()
    # scoreboard dimensions
    scoreboardRatio = GAME_SPRITES['scoreboard'].get_height()/GAME_SPRITES['scoreboard'].get_width()
    scoreboardWidth = SCREENWIDTH-SCREENWIDTH//5
    scoreboardHeight = int(scoreboardWidth*scoreboardRatio)
    scoreboardx, scoreboardy = (SCREENWIDTH-scoreboardWidth)//2 , SCREENHEIGHT//5
    #scoreboard size set
    GAME_SPRITES['scoreboard'] = pygame.transform.scale(GAME_SPRITES['scoreboard'], (scoreboardWidth, scoreboardHeight))
    
    up,down,movement = True,False,30
    playery = scoreboardHeight+scoreboardy*1.3
    while True:
        SCREEN.blit(backgroundImage, (0, 0))
        SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
        # scoreboard display
        SCREEN.blit(GAME_SPRITES['scoreboard'], (scoreboardx, scoreboardy))
        # Medal selection
        if score < 20: medalImage = GAME_SPRITES['medal'][0]
        elif score < 30: medalImage = GAME_SPRITES['medal'][1]
        elif score < 40: medalImage = GAME_SPRITES['medal'][2]
        else: medalImage = GAME_SPRITES['medal'][3]
        # Medal position
        medalx = scoreboardWidth//8.5 + scoreboardx
        # Medal dimension and display
        medalWidthHeight = SCREENWIDTH//6
        medalImage = pygame.transform.scale(medalImage, (medalWidthHeight, medalWidthHeight))
        SCREEN.blit(medalImage, (medalx, SCREENWIDTH/2.0377358491))
        # Tap tap display
        taptapx = (SCREENWIDTH - GAME_SPRITES['taptap'].get_width())//2
        SCREEN.blit(GAME_SPRITES['taptap'], (taptapx, scoreboardHeight+scoreboardy))
        # Bird image display
        SCREEN.blit(playerImage, ((SCREENWIDTH-playerImage.get_width())//2, playery))
        # Score and Highscore display
        scoreDisplay(score, True, (scoreboardx, scoreboardy), (scoreboardWidth, scoreboardHeight))
        
        global HIGHSCORE, PREVIOUSHIGHSCORE
        if HIGHSCORE > PREVIOUSHIGHSCORE:
            #New Highscore sticker display
            SCREEN.blit(GAME_SPRITES['new'], (scoreboardx+scoreboardWidth/1.6, SCREENHEIGHT//3.1))
            PREVIOUSHIGHSCORE = HIGHSCORE
       
        # update highscore database
        updateHighscore(HIGHSCORE)
        
        pygame.display.update()   
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)

            elif event.type==pygame.FINGERDOWN or event.type==pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and (event.key==pygame.K_UP or event.key==pygame.K_SPACE)): return
            else: pass
            
        # For slow up-down movement of bird
        if up:
            playery -= 1
            movement -= 1
            if movement<=0: movement,up,down = 60,False,True
        if down:
            playery += 1
            movement -= 1
            if movement<=0: movement,up,down = 60,True,False
            
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    counts = 0    # to display different image in each game
    while True:
        counts += 1
        backgroundImage = GAME_SPRITES['background'][counts%2]
        playerImage = GAME_SPRITES['player'][counts%3]
        # play sound always when NewGame begins
        GAME_SOUNDS['swoosh'].play()
        # Render the Welcom Screen
        welcomeScreen(backgroundImage, playerImage)
        # Render the Main GameLoop and Scoreboard
        gameover(gamePlay(backgroundImage, playerImage), backgroundImage, playerImage)
        FPSCLOCK.tick(FPS)
            