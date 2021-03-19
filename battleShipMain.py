################################################################ 
# Battleships the Musical: Main Code (at least now)
#    - Ship generation: {{ DONE }}
#    - Hit dectection: {{ DONE }}
"""  - Ship damage and sinking: {{ WORKING }}   """
#    - Ray casting for sonar: {{ NOT STARTED }} 
#    - Game deign: {{ NOT STARTED }}
################################################################

# imports
import pygame
import math
from random import randint

# screen deminsions
squareScreen = 1000
screenHeight = squareScreen
screenWidth = squareScreen

margin = 0 + int(squareScreen/10)

# initialize
pygame.init()
win = pygame.display.set_mode((screenWidth + margin, screenHeight + margin))

# clock
clock = pygame.time.Clock()

# x/y vectors
vec = pygame.math.Vector2

# Debugging
DEBUG = False


####### Classes #######

# class for the lines that make up the grid
class Line():
    def __init__(self, x1, x2, y1, y2):
        self.color = (255,255,255)
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 2)


# class for rectangles that make the hitboxes for the ships
class Rectangle():
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.pos = vec(x,y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)        # hitbox of ship

    # this fn is call everytime the display is updated for every rect
    def draw(self):
        pygame.draw.rect(win, self.color, (self.pos.x, self.pos.y, self.width, self.height))

    # cleans the ship generation by insuring no ship is overlapping another or partially off screen
    # this fn is called for all 5 ships
    def cleanUpRect(self, rectDic):
        # checks if current ship is overlapping any of the other ships
        for i in range(len(rectDic)):
            if rectDic["rect%s" %i] != self:        # neglects the instense of dectecing if a ship collides with itself
                if pygame.Rect.colliderect(self.rect, rectDic["rect%s" %i].rect):       # does current ship overlap with another ship
                    if DEBUG:
                        print("Overlapping: %s" %i)

                    del rectDic["rect%s" %i]        # deletes the key of the ship that is overlapping current ship

                    # generates new ship with random position, direction, and maybe shape
                    directList = lengthDirect(i)
                    rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,10) + margin, (screenHeight/10)*randint(0,10) + margin, directList[0], directList[1])
                    rectDic["rect%s" %i] = rect
                    # recussively calls the cleanUpRect fn again until all ships are no longer overlapping or partially off screen
                    rectDic["rect%s" %i].cleanUpRect(rectDic)

        # checks if current ship is partially off screen
        for i in range(len(rectDic)):
            if ((rectDic["rect%s" %i].pos.x + rectDic["rect%s" %i].width) > screenWidth) or ((rectDic["rect%s" %i].pos.y + rectDic["rect%s" %i].height) > screenHeight):
                if DEBUG:
                    print("Off Screen: %s" %i)

                del rectDic["rect%s" %i]        # deletes the key of the ship that is overlapping current ship
               
                # generates new ship with random position, direction, and maybe shape
                directList = lengthDirect(i)
                rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,10) + margin, (screenHeight/10)*randint(0,10) + margin, directList[0], directList[1])
                rectDic["rect%s" %i] = rect
                # recussively calls the cleanUpRect fn again until all ships are no longer overlapping or partially off screen
                rectDic["rect%s" %i].cleanUpRect(rectDic)


# class for target which has mush of the same elements as the rectangle class
class Target(Rectangle):
    antiRep1 = 0
    antiRep2 = 0
    antiRep3 = 0
    antiRep4 = 0
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)
      
    def move(self):
        # detecting key presses
        keys = pygame.key.get_pressed()
        # right bound detection and left movement
        if self.pos.x > margin and keys[pygame.K_LEFT] and Target.antiRep1 == 0:
            Target.antiRep1 = 1
            self.pos.x -= int(squareScreen/10)
        # anti repetition
        if not(keys[pygame.K_LEFT]):
            Target.antiRep1 = 0

        # left bound detection and right movement
        if self.pos.x < screenWidth - margin and keys[pygame.K_RIGHT] and Target.antiRep2 == 0:
            Target.antiRep2 = 1
            self.pos.x += int(squareScreen/10)
        # anti repetition
        if not(keys[pygame.K_RIGHT]):
            Target.antiRep2 = 0

        # bottom bound detection and up movement
        if self.pos.y > margin and keys[pygame.K_UP] and Target.antiRep3 == 0:
            Target.antiRep3 = 1
            self.pos.y -= int(squareScreen/10)
        # anti repetition
        if not(keys[pygame.K_UP]):
            Target.antiRep3 = 0    
            
        # top bound detection and down movement
        if self.pos.y < screenHeight - margin and keys[pygame.K_DOWN] and Target.antiRep4 == 0:
            Target.antiRep4 = 1
            self.pos.y += int(squareScreen/10)
        # anti repetition
        if not(keys[pygame.K_DOWN]):
            Target.antiRep4 = 0



####### Functions #######

# updates screen every frame
def update(rectDic, lineDic):
    win.fill((0,0,0))       # makes background black
    
    # draw grit with lines
    for i in range(1,len(lineDic)):
        lineDic["line%s" %i].draw()

    # drawing rectangles
    #for rect in rectList:
    for i in range(len(rectDic)):
        rectDic["rect%s" %i].draw()

    # moves and draws curser in new position
    curser.move()
    curser.draw()
    
    pygame.display.update()     # displays updated screen


# decides legnth and direction of ship
def lengthDirect(shipNum):
    global screenHeight
    global screenWidt

    # calcs the different sized ships
        # there are 5 ships
        # Legths: 5, 4, 3, 3, 2

    if shipNum == 0:    # Carrier Ship
        length = 2*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 1:    # Battleship Ship
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 2:    # Cruiser Ship
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 3:    # Submarine Ship or another Cruiser
        length = 4*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 4:    # Destroyer Ship
        length = 5*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum > 4:     # Overflow protection
        length = randint(2,5)*(screenHeight/10)
        width = (screenWidth/10)

    # decides direction at random
    if randint(0,1):
        temp = length
        length = width
        width = temp
    return width, length


# creates ships of random shapes and position
def createRect(numRect):
    # dictionary to store ship data
    rectDic = {}
    # creates as many ships needed
    for i in range(numRect):
        # gets length and orientation
        directList = lengthDirect(i)
        # creates rectangle object
        rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,9) + margin, (screenHeight/10)*randint(0,9) + margin, directList[0], directList[1])
        # creates and assigns key for rectangle dictionary
        # the syntax below is just to make keys in the style: rect0, rect1, rect2, ...
        rectDic["rect%s" %i] = rect
    # returns dictionary
    return rectDic

# creates lines for grit

#### this is most likely temporary, until we get a background for the game
def createLine():
    # dictionary for lines
    lineDic = {}
    # creates horizontal lines
    for i in range(0,11):
        line = Line((screenWidth/10)*(i-1)-1 + margin,(screenWidth/10)*(i-1)-1 + margin, margin, screenHeight)
        lineDic["line%s" %i] = line
    # creates vertical lines
    for i in range(11,21):
        line = Line(margin, screenWidth, (screenHeight/10)*(i-11)-1 + margin,(screenHeight/10)*(i-11)-1 + margin)
        lineDic["line%s" %i] = line
    # returns dictionary
    return lineDic

# dectects collision of curser and ship
def isCollide():
    for i in range(len(rectDic)):
        if pygame.Rect.colliderect(pygame.Rect(curser.pos.x, curser.pos.y, curser.width, curser.height), rectDic["rect%s" %i].rect):
            return True
    return False

def shootMissile():
    if isCollide():
        print("That's a hit!!")
    else:
        print("All you shot was sea!")


# number of ships
numRect = 5

# generate ships
rectDic = createRect(numRect)
for i in range(len(rectDic)):
    rectDic["rect%s" %i].cleanUpRect(rectDic)

# Create Grid
lineDic = createLine()

# Create Target/Curser
curser = Target((255,255,255), margin, margin, int(squareScreen/10), int(squareScreen/10))

# boolean to allow the breaking of the main loop
run = True

# framerate of the game
    # this probably won't matter too much, unless we decide to make animations
    # then we'll have to put in more thought into it
frameRate = 60



#########################################################################################
# MAIN GAME LOOP 
#########################################################################################
# for rep detection
antiRep = 0
antiRep1 = 1

while run:
    # controls rate of the game
    clock.tick(frameRate)

    # detects if user wants to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # for test, generates new boats
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and antiRep == 0:
        antiRep = 1     # blocks multiple interations in one click
        rectDic = createRect(numRect)
        for i in range(len(rectDic)):
            rectDic["rect%s" %i].cleanUpRect(rectDic)
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_SPACE]):
        antiRep = 0
        
    # shooting missle
    if key[pygame.K_RETURN] and antiRep1 == 0:
        antiRep1 = 1
        shootMissile()
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_RETURN]):
        antiRep1 = 0

    #print("x: {} y: {}". format(curser.pos.x, curser.pos.y))
    
    # updates the screen to different events
    update(rectDic, lineDic)

# if main loop is broke then close program
pygame.quit()

