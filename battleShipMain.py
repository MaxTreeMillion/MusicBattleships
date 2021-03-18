################################################################ 
# Battleships the Musical: Main Code (at least now)
#    - Working on ship generation
#    - Working on ray casting for sonar later
#    - Working on game deign evintually
################################################################

# imports
import pygame
import math
from random import randint

# screen deminsions
squareScreen = 600
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

# Classes

# class for the lines that make up the grid
class Line():
    def __init__(self, x1, x2, y1, y2):
        self.color = (255,255,255)
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 2)

##class Student(Person):
##  def __init__(self, fname, lname):
##    Person.__init__(self, fname, lname)

# class for target which has mush of the same elements as the rectangle class
def Target(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        
    def move(self):
        # detecting key presses
        keys = pygame.key.get_pressed()

        # horizontal boundary dectection
        if self.pos.x > margin and self.pos.x < screenWidth - margin + self.width:
            # horizontal movement
            if keys[pygame.K_LEFT]:
                self.pos.x -= 100

            if keys[pygame.K_RIGHT]:
                self.pos.x += 100
        # vertical boundary dectection
        if self.pos.y > margin and self.pos.y < screenHeight - margin + self.height:
            # vertical movement
            if keys[pygame.K_UP]:
                self.pos.y -= 100
                
            if keys[pygame.K_DOWN]:
                self.pos.y += 100
    
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

    #curser.draw()
    
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

    if shipNum == 3:    # Submarine Ship or another Cruiser
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 4:    # Destroyer Ship
        length = 2*(screenHeight/10)
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


# number of ships
numRect = 5

# generate ships
rectDic = createRect(numRect)
for i in range(len(rectDic)):
    rectDic["rect%s" %i].cleanUpRect(rectDic)

# Create Grid
lineDic = createLine()

# Create Target/Curser
#curser = Target((255,255,255), margin, margin, 100, 100)

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
        
    #curser.move()
    
    # updates the screen to different events
    update(rectDic, lineDic)

# if main loop is broke then close program
pygame.quit()



