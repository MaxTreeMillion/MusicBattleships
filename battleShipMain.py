################################################################ 
# Battleships the Musical: Main Code (at least now)
#    - Working on ship generation
#    - Working on ray casting for sonar later
#    - Working on game deign evintually
################################################################
# test
# imports
import pygame
import math
from random import randint

# screen deminsions
screenHeight = 1000
screenWidth = 1000

# initialize
pygame.init()
win = pygame.display.set_mode((screenWidth, screenHeight))

# clock
clock = pygame.time.Clock()

# x/y vectors
vec = pygame.math.Vector2

# Classes

# class for the lines that make up the grid
class Line():
    def __init__(self, x1, x2, y1, y2):
        self.color = (255,255,255)
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 3)

# class for rectangles that make the hitboxes for the ships
class Rectangle():
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.pos = vec(x,y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)        # hitbox of ship

    # this fn is call everytime the display is updated for every rect
    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)

    # cleans the ship generation by insuring no ship is overlapping another or partially off screen
    # this fn is called for all 5 ships
    def cleanUpRect(self, rectDic):
        # checks if current ship is overlapping any of the other ships
        for i in range(len(rectDic)):
            if rectDic["rect%s" %i] != self:        # neglects the instense of dectecing if a ship collides with itself
                if pygame.Rect.colliderect(self.rect, rectDic["rect%s" %i].rect):       # does current ship overlap with another ship
                    del rectDic["rect%s" %i]        # deletes the key of the ship that is overlapping current ship

                    # generates new ship with random position, direction, and maybe shape
                    directList = lengthDirect()
                    rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,10), (screenHeight/10)*randint(0,10), directList[0], directList[1])
                    rectDic["rect%s" %i] = rect
                    # recussively calls the cleanUpRect fn again until all ships are no longer overlapping or partially off screen
                    rectDic["rect%s" %i].cleanUpRect(rectDic)

        # checks if current ship is partially off screen
        for i in range(len(rectDic)):
            if ((rectDic["rect%s" %i].pos.x + rectDic["rect%s" %i].width) > screenWidth) or ((rectDic["rect%s" %i].pos.y + rectDic["rect%s" %i].height) > screenHeight):
                del rectDic["rect%s" %i]        # deletes the key of the ship that is overlapping current ship

                # generates new ship with random position, direction, and maybe shape
                directList = lengthDirect()
                rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,10), (screenHeight/10)*randint(0,10), directList[0], directList[1])
                rectDic["rect%s" %i] = rect
                # recussively calls the cleanUpRect fn again until all ships are no longer overlapping or partially off screen
                rectDic["rect%s" %i].cleanUpRect(rectDic)

# updates screen every frame
def update(rectDic, lineDic):
    win.fill((0,0,0))       # makes background black

    # draw grit with lines
    for i in range(1,len(lineDic)+1):
        lineDic["line%s" %i].draw()

    # drawing rectangles
    #for rect in rectList:
    for i in range(len(rectDic)):
        rectDic["rect%s" %i].draw()

    pygame.display.update()     # displays updated screen


# decides legnth and direction of ship
def lengthDirect(shipNum):
    global screenHeight
    global screenWidt

    # calcs the different sized ships
        # there are 5 ships
        # Legths: 5, 4, 3, 3, 2

    if shipNum == 0:    # Carrier Ship
        length = 5*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 1:    # Battleship Ship
        length = 4*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 2:    # Cruiser Ship
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 3:    # Submarine Ship
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 4:    # Destroyer Ship
        length = 2*(screenHeight/10)
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
        directList = lengthDirect()
        # creates rectangle object
        rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,9), (screenHeight/10)*randint(0,9), directList(i)[0], directList(i)[1])
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
    for i in range(1,10):
        line = Line((screenWidth/10)*i,(screenWidth/10)*i, 0, screenHeight)
        lineDic["line%s" %i] = line
    # creates vertical lines
    for i in range(10,19):
        line = Line(0, screenWidth, (screenHeight/10)*(i-9),(screenHeight/10)*(i-9))
        lineDic["line%s" %i] = line
    # returns dictionary
    return lineDic

# Create Grid
lineDic = createLine()

# boolean to allow the breaking of the main loop
run = True
# framerate of the game
    # this probably won't matter too much, unless we decide to make animations
    # then we'll have to put in more thought into it
frameRate = 1

#########################################################################################
# MAIN GAME LOOP #
##################
while run:
    # controls rate of the game
    clock.tick(frameRate)

    # detects if user wants to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # creat random rectangles
    # this will be before the main loop in the real game
    # it is inside now for deminstation purposes
    numRect = 5
    rectDic = createRect(numRect)
    for i in range(len(rectDic)):
        rectDic["rect%s" %i].cleanUpRect(rectDic)
    
    # updates the screen to different events
    update(rectDic, lineDic)

# if main loop is broke then close program
pygame.quit()



