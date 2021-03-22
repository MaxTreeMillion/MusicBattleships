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
squareScreen = 500
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

class Sonar():
    antiRep1 = 0
    antiRep2 = 0
    antiRep3 = 0
    antiRep4 = 0
    def __init__(self, color, x1, y1, x2, y2):
        self.color = color
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 1)



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
                    directList = lengthDirect(i, rectDic)
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
                directList = lengthDirect(i, rectDic)
                rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,10) + margin, (screenHeight/10)*randint(0,10) + margin, directList[0], directList[1])
                rectDic["rect%s" %i] = rect
                # recussively calls the cleanUpRect fn again until all ships are no longer overlapping or partially off screen
                rectDic["rect%s" %i].cleanUpRect(rectDic)


# class for target which has mush of the same elements as the rectangle class
class Target(Rectangle):
    # hacky way of elemenating multiple calling when holding down mouse
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
    global shipHealths
    win.fill((0,0,0))       # makes background black
    
    # draw grit with lines
    for i in range(1,len(lineDic)):
        lineDic["line%s" %i].draw()

    # drawing rectangles
    for i in range(len(rectDic)):
        if not(isSunk(shipHealths, i)):
            rectDic["rect%s" %i].draw()

    # draws ship damage
    for key, value in shipDamages.items():
        shipDamages[key].draw()


    # moves and draws curser in new position
    curser.move()
    curser.draw()

    # draw grit with lines
    #for i in range(1,len(sonarDic)):
    #    sonarDic["beam%s" %i].draw()
    for key, value in sonarDic.items():
        sonarDic[key].draw()

    pygame.display.update()     # displays updated screen

# decides legnth and direction of ship
def lengthDirect(shipNum, rectDic):
    global screenHeight
    global screenWidth
    global shipHealths
    
    # calcs the different sized ships
        # there are 5 ships
        # Legths: 5, 4, 3, 3, 2

    if shipNum == 0:    # Carrier Ship
        shipHealths["shipHealth%s" %0] = 2          #[1,1]
        length = 2*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 1:    # Battleship Ship
        shipHealths["shipHealth%s" %1] = 3          #[1,1,1]
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 2:    # Cruiser Ship
        shipHealths["shipHealth%s" %2] = 3          #[1,1,1]
        length = 3*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 3:    # Submarine Ship or another Cruiser
        shipHealths["shipHealth%s" %3] = 4          #[1,1,1,1]
        length = 4*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum == 4:    # Destroyer Ship
        shipHealths["shipHealth%s" %4] = 5          #[1,1,1,1,1]
        length = 5*(screenHeight/10)
        width = (screenWidth/10)

    if shipNum > 4:     # Overflow protection
        j = len(rectDic)
        shipHealths["shipHealth%s" %j] = []
        rand = randint(2,5)
        for i in range(rand):
            shipHealths["shipHealth%s" %j].append(1)
        length = rand*(screenHeight/10)
        width = (screenWidth/10)
    # decides direction at random
    if randint(0,1):
        temp = length
        length = width
        width = temp
    return width, length #, shipHealth

# creates ships of random shapes and position
def createRect(numRect):
    # dictionary to store ship data
    rectDic = {}
    # creates as many ships needed
    for i in range(numRect):
        # gets length and orientation
        directList = lengthDirect(i, rectDic)
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

# aims, widens, and extense the sonar
def sonarAim():
    global sonarRange
    global sonarWidth
    global sonarStartAngle
    global sonarPos
    

    keys = pygame.key.get_pressed()

    mouse = pygame.mouse.get_pressed(num_buttons=5)

    # sonar center position

    # right bound detection and left movement
    if sonarPos.x > margin + int(squareScreen/10)/2 and keys[pygame.K_a] and Sonar.antiRep1 == 0:
        Sonar.antiRep1 = 1
        sonarPos.x -= int(squareScreen/10)
    # anti repetition
    if not(keys[pygame.K_a]):
        Sonar.antiRep1 = 0

    # left bound detection and right movement
    if sonarPos.x < screenWidth - margin and keys[pygame.K_d] and Sonar.antiRep2 == 0:
        Sonar.antiRep2 = 1
        sonarPos.x += int(squareScreen/10)
    # anti repetition
    if not(keys[pygame.K_d]):
        Sonar.antiRep2 = 0

    # bottom bound detection and up movement
    if sonarPos.y > margin + int(squareScreen/10)/2 and keys[pygame.K_w] and Sonar.antiRep3 == 0:
        Sonar.antiRep3 = 1
        sonarPos.y -= int(squareScreen/10)
    # anti repetition
    if not(keys[pygame.K_w]):
        Sonar.antiRep3 = 0    
        
    # top bound detection and down movement
    if sonarPos.y < screenHeight - margin and keys[pygame.K_s] and Sonar.antiRep4 == 0:
        Sonar.antiRep4 = 1
        sonarPos.y += int(squareScreen/10)
    # anti repetition
    if not(keys[pygame.K_s]):
        Sonar.antiRep4 = 0

    
    # controls
    # rotate counter-clockwise
    if mouse[0] or keys[pygame.K_9]:
        sonarStartAngle += 5
 
    # rotate clockwise
    if mouse[2] or keys[pygame.K_0]:
        sonarStartAngle -= 5

    # increase range

    if (keys[pygame.K_RIGHTBRACKET] or (mouse[4] and not(mouse[1]))) and sonarRange <= math.sqrt(((screenHeight - margin)/2)**2 + ((screenWidth - margin)/2)**2):
        sonarRange += 5

    # decrease range
    if (keys[pygame.K_LEFTBRACKET] or (mouse[3] and not(mouse[1]))) and sonarRange >= 50:
        sonarRange -= 5

    # increase width
    if (keys[pygame.K_EQUALS] or (mouse[4] and mouse[1])) and sonarWidth <= 358:
        sonarWidth += 1
    # decrease width
    if (keys[pygame.K_MINUS] or (mouse[3] and mouse[1])) and sonarWidth >= 1:
        sonarWidth -= 1

# sonar creation
def createSonar():
    global sonarPos
    # reset sonar dictionary
    sonarDic ={}

    # get the aim of the sonar
    sonarAim()

    # create each beam of the sonar
    for i in range(sonarStartAngle, sonarStartAngle + sonarWidth + 1):
        x2 = sonarPos.x + math.cos(-math.radians(i)) * sonarRange 
        y2 = sonarPos.y + math.sin(-math.radians(i)) * sonarRange 
        sonarDic["beam%s" %i] = Sonar((255,0,255), sonarPos.x , sonarPos.y , x2, y2)
        #sonarDic["beam%s" %i] = isCollideSonar(i)
    return sonarDic

# sonar collision
##def isCollideSonar(beamNum):
##    for i in range(len(rectDic)):
##    rectDic["rect%s" %i].rect.clipline(sonarDic["beam%s" %beamNum])
    

# dectects collision of curser and ship
def isCollide():
    for i in range(len(rectDic)):
        if pygame.Rect.colliderect(pygame.Rect(curser.pos.x, curser.pos.y, curser.width, curser.height), rectDic["rect%s" %i].rect):
            return True, i      # returns if collision and if so, the ship that was hit
    return False, i

# shoots a missle where the curser is 
def shootMissile():
    global shipDamages
    global shipHealths
    damageTest = 1

    # so the user cant shoot the same spot and do more damage
    for i in range(len(shipDamages)):
        if (shipDamages["shipDamage%s" %i].pos.x == curser.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser.pos.y):
            damageTest = 0

    # set to a variable to extract 2 returns
    isCollides = isCollide()
    # did it hit
    if isCollides[0] and damageTest:
        print("You hit boat {}!!". format(isCollides[1]+1))
        # places yellow square on damaged spot
        shipDamages["shipDamage%s" %len(shipDamages)] = Rectangle((255,255,0), curser.pos.x, curser.pos.y, curser.width, curser.height)
        # decreases health
        #print(shipDamages)
        if shipHealths["shipHealth%s" % isCollides[1]] > 0:
            shipHealths["shipHealth%s" % isCollides[1]] -= 1

    else:
        if damageTest:
            print("All you shot was sea!")
        else:
            print("You already damaged that part!")

# detects if ship is sunk
def isSunk(shipHealths, i):
    #for i in range(len(shipHealths)):
    if not(shipHealths["shipHealth%s" %i]):
        sink(i)
        return True
    else:
        return False

# sinks the ship and tells draw function to not draw ship
def sink(i):
     for j in range(len(shipDamages)):
        if pygame.Rect.colliderect(pygame.Rect(shipDamages["shipDamage%s" %j].pos.x, shipDamages["shipDamage%s" %j].pos.y, shipDamages["shipDamage%s" %j].width, shipDamages["shipDamage%s" %j].height), rectDic["rect%s" %i].rect):
            del shipDamages["shipDamage%s" %j]

# detects if game has been won
def isWin():
    global shipHealths
    tot = 0
    for i in range(len(shipHealths)):
        tot += shipHealths["shipHealth%s" %i]

    if tot != 0:
        return False
    else:
        return True


# number of ships
numRect = 5
# ship health in order
shipHealths = {}
# damage dictionary
shipDamages = {}

# generate ships
rectDic = createRect(numRect)
for i in range(len(rectDic)):
    rectDic["rect%s" %i].cleanUpRect(rectDic)

# Default sonar 
sonarRange = 200
sonarWidth = 45
sonarStartAngle = 0
sonarPos = vec((screenHeight + margin)/2,(screenWidth + margin)/2)

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
        shipDamages = {}
        shipHealths = {}
        antiRep = 1     # blocks multiple interations in one click
        rectDic = createRect(numRect)
        for i in range(len(rectDic)):
            rectDic["rect%s" %i].cleanUpRect(rectDic)
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_SPACE]):
        antiRep = 0
    
    # Generate first Sonar
    sonarDic = createSonar()

    # shooting missle
    if key[pygame.K_RETURN] and antiRep1 == 0:
        antiRep1 = 1
        shootMissile()
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_RETURN]):
        antiRep1 = 0

    # detects winning condition met
    if isWin():
        print("\n\n\n\t\t\t\t**********************")
        print("\t\t\t\t*****  You Win!  *****")
        print("\t\t\t\t**********************")
        run = False
    
    # updates the screen to different events
    update(rectDic, lineDic)

# if main loop is broke then close program
pygame.quit()

