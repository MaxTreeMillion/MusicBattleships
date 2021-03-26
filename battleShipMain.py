################################################################ 
# Battleships the Musical: Main Code (at least now)
#    - Ship generation: {{ DONE }}
#    - Hit dectection: {{ DONE }}
#    - Ship damage and sinking: {{ DONE }} 
"""  - Ray casting for sonar: {{ WORKING }}  """
#    - Game deign: {{ NOT STARTED }}
################################################################

# imports
import pygame
import math
from random import randint

# screen deminsions
squareScreen = 1200
screenHeight = randint(1000, 1400)
screenWidth = randint(1000, 1400)
playScreen = randint(800, 1000)
topBotMargin = (screenHeight - playScreen)/2
sideMargin = (screenWidth - playScreen)/2
tile = int(playScreen/10)

# initialize
pygame.init()
win = pygame.display.set_mode((screenWidth, screenHeight))

# clock
clock = pygame.time.Clock()

# x/y vectors
vec = pygame.math.Vector2

# Debugging
DEBUG = False

####### Classes #######
# class that holds globals
class Global():
    isPress_UP = 0
    isPress_DOWN = 0
    isPress_LEFT = 0
    isPress_RIGHT = 0
    isPress_SPACE = 0
    isPress_RETURN = 0
    isPress_LSHIFT = 0
    isPress_w = 0
    isPress_a = 0
    isPress_s = 0
    isPress_d = 0
    run = True

# class for the lines that make up the grid (temp class)
class Line():
    def __init__(self, x1, y1, x2, y2):
        self.color = (255,255,255)
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 2)

# class for each sonar beam
class Sonar():
    def __init__(self, color, x1, y1, x2, y2):
        self.color = color
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)
        self.length = 0

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 1)

# class for rectangles that mainly create the hitbox
class Rectangle():
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.pos = vec(x,y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(win, self.color, pygame.Rect(self.pos.x, self.pos.y, self.width, self.height))

# class for ships in the game
class Ship(Rectangle):
    def __init__(self, health, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)
        self.health = health
        self.damage = 0
        self.sonarHitNum = 0
        self.averageDistance = 0

    # cleans the ship generation by insuring no ship is overlapping another or partially off screen
        # this fn is called for all 5 ships
    def cleanUpShip(self, shipDic):
        # checks if current ship is overlapping any of the other ships
        for i in range(len(shipDic)):
            if shipDic["ship%s" %i] != self:        # neglects the instense of dectecing if a ship collides with itself
                if pygame.Rect.colliderect(self.rect, shipDic["ship%s" %i].rect):       # does current ship overlap with another ship
                    # overides overlapping ship with new ship generation
                    # generates new ship with random position, direction, and maybe shape
                    directList = lengthDirect(i, shipDic)
                    ship = Ship(directList[2], (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + topBotMargin, directList[0], directList[1])
                    shipDic["ship%s" %i] = ship
                    # recussively calls the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                    shipDic["ship%s" %i].cleanUpShip(shipDic)

        # checks if current ship is partially off screen
        for i in range(len(shipDic)):
            if ((shipDic["ship%s" %i].pos.x + shipDic["ship%s" %i].width) > sideMargin + playScreen) or ((shipDic["ship%s" %i].pos.y + shipDic["ship%s" %i].height) > topBotMargin + playScreen):
                # generates new ship with random position, direction, and maybe shape
                directList = lengthDirect(i, shipDic)
                ship = Ship(directList[2], (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + topBotMargin, directList[0], directList[1])
                shipDic["ship%s" %i] = ship
                # recussively calls the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                shipDic["ship%s" %i].cleanUpShip(shipDic)

# class for missile target
class Target(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def move(self):
        # detecting key presses
        keys = pygame.key.get_pressed()
        # right bound detection and left movement
        if self.pos.x > sideMargin and keys[pygame.K_LEFT] and Global.isPress_LEFT == 0:
            Global.isPress_LEFT = 1
            self.pos.x -= tile
        # anti repetition
        if not(keys[pygame.K_LEFT]):
            Global.isPress_LEFT = 0

        # left bound detection and right movement
        if self.pos.x < playScreen + sideMargin - tile and keys[pygame.K_RIGHT] and Global.isPress_RIGHT == 0:
            Global.isPress_RIGHT = 1
            self.pos.x += tile
        # anti repetition
        if not(keys[pygame.K_RIGHT]):
            Global.isPress_RIGHT = 0

        # bottom bound detection and up movement
        if self.pos.y > topBotMargin and keys[pygame.K_UP] and Global.isPress_UP == 0:
            Global.isPress_UP = 1
            self.pos.y -= tile
        # anti repetition
        if not(keys[pygame.K_UP]):
            Global.isPress_UP = 0    
            
        # top bound detection and down movement
        if self.pos.y < playScreen + topBotMargin - tile and keys[pygame.K_DOWN] and Global.isPress_DOWN == 0:
            Global.isPress_DOWN = 1
            self.pos.y += tile
        # anti repetition
        if not(keys[pygame.K_DOWN]):
            Global.isPress_DOWN = 0

# class for ship damage
class ShipDamage(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)


#### Functions ####

# updates image/screen
def update(gridDic):
    # blacks out background
    win.fill((0,0,0))

    # draws grid with lines
    for key, val in gridDic.items():
        gridDic[key].draw()

    # draws all ships
    for key, val in shipDic.items():
        shipDic[key].draw()
        ###################################################################################################################
        ###    THIS IS WHERE THE OUTPUTS FOR WHAT SHIP IS BEING HIT BY SONAR AND HOW MANY SONAR BEANS ARE HITTING IT    ###
        #                                                                                                                 #
        #                                                                                                                 #
        #                                                                                                                 #
        print("{}: {}". format(key, shipDic[key].sonarHitNum))                                                            #
        #                                                                                                                 #
        #                                                                                                                 #
        #                                                                                                                 #
        ###################################################################################################################

        #reset sonar collide counters (how many beams are currently hitting a ship 
        shipDic[key].sonarHitNum = 0
    
    # draws all ship damage sprites
    for key, val in shipDamages.items():
        shipDamages[key].draw()

    # draws curser in new position
    curser.draw()

    # draws all sonar beams
    for key, value in sonarDic.items():
        sonarDic[key].draw()

    # updates screen
    pygame.display.update()

# creates grid for game board
def createGrid():
    # dictionary for lines making up the grid
    gridDic = {}
    # creates horizontal lines
    for i in range(0,11):
        x = sideMargin + tile*i -1
        y = topBotMargin
        new_y = topBotMargin + playScreen
        gridDic["line%s" %i] = Line(x, y, x, new_y)
    # creates vertical lines
    for i in range(11,22):
        x = sideMargin
        new_x = sideMargin + playScreen
        y = topBotMargin + tile*(i-11)-1
        gridDic["line%s" %i] = Line(x, y, new_x, y)

    # returns dictionary
    return gridDic

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
    if sonarPos.x > sideMargin + tile/2 and keys[pygame.K_a] and Global.isPress_a == 0:
        Global.isPress_a = 1
        sonarPos.x -= tile
    # anti repetition
    if not(keys[pygame.K_a]):
        Global.isPress_a = 0

    # left bound detection and right movement
    if sonarPos.x < playScreen + sideMargin - tile/2 and keys[pygame.K_d] and Global.isPress_d == 0:
        Global.isPress_d = 1
        sonarPos.x += tile
    # anti repetition
    if not(keys[pygame.K_d]):
        Global.isPress_d = 0

    # bottom bound detection and up movement
    if sonarPos.y > topBotMargin + tile/2 and keys[pygame.K_w] and Global.isPress_w == 0:
        Global.isPress_w = 1
        sonarPos.y -= tile
    # anti repetition
    if not(keys[pygame.K_w]):
        Global.isPress_w = 0    
        
    # top bound detection and down movement
    if sonarPos.y < playScreen + topBotMargin - tile/2 and keys[pygame.K_s] and Global.isPress_s == 0:
        Global.isPress_s = 1
        sonarPos.y += tile
    # anti repetition
    if not(keys[pygame.K_s]):
        Global.isPress_s = 0
    
    # controls
    # rotate counter-clockwise
    if mouse[0] or keys[pygame.K_9]:
        sonarStartAngle += 5
 
    # rotate clockwise
    if mouse[2] or keys[pygame.K_0]:
        sonarStartAngle -= 5

    # increase range

    if (keys[pygame.K_RIGHTBRACKET] or (mouse[4] and not(mouse[1]))) and sonarRange <= math.sqrt((playScreen/2)**2 + (playScreen/2)**2):
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

# creates sonar array
def createSonar():
    global sonarPos
    # reset sonar dictionary
    sonarDic = {}

    # get the aim of the sonar
    sonarAim()

    # create each beam of the sonar
    for i in range(sonarStartAngle, sonarStartAngle + sonarWidth + 1):
        # gives the beams a radius of influence
        x2 = sonarPos.x + math.cos(-math.radians(i)) * sonarRange 
        y2 = sonarPos.y + math.sin(-math.radians(i)) * sonarRange 
        # creates first case line for collision function to use
        sonarDic["beam%s" %i] = Sonar((255,0,255), sonarPos.x , sonarPos.y , x2, y2)
        # modifies beam to new length depending on if it collided
        sonarDic["beam%s" %i] = isCollideSonar(i, sonarDic, x2, y2)
    # returns dictionary of all the lines
    return sonarDic

# sonar collision
def isCollideSonar(beamnum, sonarDic, x2, y2):
    # temp dictionary for use when beam crosses multiple ships
    tempCollDic = {}
    minCalcDic = {}
    averageLength = {}

    """per beam, it runs through and checks if that beam is caolliding with ANY ships
    this means that the beam could possibly pass through multiple ships
    to midigate this I put of the ships that the beam collided with into a temporary dictionary "tempCollDic"
    I then find the distance between the origin of the sonar and the collision points of each ship
    I find the smallest of those distances and make that the new end point of that beam
    though, you must keep in mind that this function is called once per beam
    if 80 beams are shot out, then the function runs 80 times per frame"""
    # runs through each ship
    for key, val in shipDic.items():
        # checks if beam collides with ship
        newEnd = shipDic[key].rect.clipline(sonarDic["beam%s" %beamnum].end1.x, sonarDic["beam%s" %beamnum].end1.y, sonarDic["beam%s" %beamnum].end2.x, sonarDic["beam%s" %beamnum].end2.y)
        # weird syntax that more complex than it should be
            # but for whateer reason I wasnt able to unpack the tuple that the 'clipline' fn gave
            # this was the only way a got it working
        for item in newEnd:
            if item == newEnd[0] and item != ():
                # saves the coords of the entrance point to the dictionary
                tempCollDic[key] = item
                collideShip = key
    # calcs the distances of each entrance coord and the sonars origin
        # then saves in another dictionary
    for key, value in tempCollDic.items():
        minCalcDic[key] = math.sqrt((sonarPos.x-value[0])**2 + (sonarPos.y-value[1])**2)
    # if the dictionary is empty then there was no collision so return the same line
    if tempCollDic == {}:
        # screen bounds
        return Sonar((255,0,255), sonarPos.x , sonarPos.y , x2, y2)
    else:
        # if not, then update line
        newEnd = tempCollDic[min(minCalcDic, key = minCalcDic.get)]

        shipDic[collideShip].sonarHitNum += 1

        ######                                                                                              ######
        ###       The idea is create dictionary of list where the keys are ship names and the list are full    ###
        #      of the lengths of all the beams colliding with the ship. After that we just need to take the      #
        ###    average of the lengthes of those beams and then return it !!!!!                                 ###
        #####                                                                                               ######

        #averageLength[collideShip].append(math.sqrt((sonarPos.x-value[0])**2 + (sonarPos.y-value[1])**2))
        #print(averageLength)
        # return updated line
        return Sonar((255,0,255), sonarPos.x , sonarPos.y , newEnd[0], newEnd[1])

# decides legnth and direction of ship
def lengthDirect(shipNum, shipDic):
    # calcs the different sized ships
        # there are 5 ships
        # Legths: 5, 4, 3, 3, 2

    if shipNum == 0:    # Carrier Ship
        length = 2*tile
        width = tile
        health = 2

    if shipNum == 1:    # Battleship Ship
        length = 3*tile
        width = tile
        health = 3

    if shipNum == 2:    # Cruiser Ship
        length = 3*tile
        width = tile
        health = 3

    if shipNum == 3:    # Submarine Ship or another Cruiser
        length = 4*tile
        width = tile
        health = 4

    if shipNum == 4:    # Destroyer Ship
        length = 5*tile
        width = tile
        health = 5

    if shipNum > 4:     # Overflow protection
        j = len(shipDic)
        rand = randint(2,5)
        length = rand*tile
        width = tile
        health = rand

    # decides direction at random
    if randint(0,1):
        temp = length
        length = width
        width = temp
    return width, length, health

# creates all ships
def createShip(numShip):
    # holds the ship names and class info
    shipDic = {}
    # creates ships as needed
    for i in range(numShip):
        # gets length and orientation
        directList = lengthDirect(i, shipDic)
        # creates ship object
        ship = Ship(directList[2], (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + topBotMargin, directList[0], directList[1])
        # creates and assigns key for ship dictionary
        # the syntax below is just to make keys in the style: ship0, ship1, ship2, ...
        shipDic["ship%s" %i] = ship
    # returns dictionary
    return shipDic

# dectects collision of curser and ship
def isCollide():
    key = "NONE"
    for key, val in shipDic.items():
        if pygame.Rect.colliderect(pygame.Rect(curser.pos.x, curser.pos.y, curser.width, curser.height), shipDic[key].rect):
            return True, key      # returns if collision and if so, the ship that was hit
    return False, key

# shoots missile at ship and does damage
def shootMissile():
    global shipDamages
    damageTest = 1
    # so the user cant shoot the same spot and do more damage
    for i in range(len(shipDamages)):
        if (shipDamages["shipDamage%s" %i].pos.x == curser.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser.pos.y):
            damageTest = 0
    
    # set to a variable to extract 2 returns
    isCollides = isCollide()
    # did it hit
    if isCollides[0] and damageTest:
        print("You hit {}!!". format(isCollides[1]))
        # places yellow square on damaged spot
        shipDamages["shipDamage%s" %len(shipDamages)] = ShipDamage((255,255,0), curser.pos.x, curser.pos.y, curser.width, curser.height)
        # decreases health
        if shipDic[isCollides[1]].health > 0:
            shipDic[isCollides[1]].health -= 1
    else:
        if damageTest:
            print("All you shot was sea!")
        else:
            print("You already damaged that part!")

# detects if any sunken ships
def isSunk():
    global shipDic
    deadShip = 0
    # sinks ship if health is zero
    for key, items in shipDic.items():
        if not(shipDic[key].health):
            print("You got one!!")
            sink(key)
            deadShip = key
    # deletes ship thats been sunk
    if deadShip:
        del shipDic[deadShip]

# is ship is sunken, then remove it and the shipDamage
def sink(ship):
    global shipDic
    global shipDamages
    delShipDamages = []

    # deletes shipDamage sprites that are on sunken ship
    for key, val in shipDamages.items():
        if pygame.Rect.colliderect(pygame.Rect(shipDamages[key].pos.x, shipDamages[key].pos.y, shipDamages[key].width, shipDamages[key].height), shipDic[ship].rect):
            delShipDamages.append(key)
    # deleting damage sprites of sunken ship
    for ish in delShipDamages:
        del shipDamages[ish]

# detects if game has been won
def isWin():
    tot = 0
    for key, val in shipDic.items():
        tot += shipDic[key].health

    if tot == 0:
        print("\n\n\n\t\t\t\t**********************")
        print("\t\t\t\t*****  You Win!  *****")
        print("\t\t\t\t**********************")
        Global.run = False

def detectInputs(numShip):
    global shipDic
    # detects if user wants to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Global.run = False
       
    key = pygame.key.get_pressed()

    # for test, generates new boats
    if key[pygame.K_SPACE] and Global.isPress_SPACE == 0:
        Global.isPress_SPACE = 1
        shipDic = createShip(numShip)
        for i in range(len(shipDic)):
            shipDic["ship%s" %i].cleanUpShip(shipDic)
    # anti repetition
    if not(key[pygame.K_SPACE]):
        Global.isPress_SPACE = 0
    
    # shooting missle
    if key[pygame.K_LSHIFT] and Global.isPressed_LSHIFT == 0:
        Global.isPressed_LSHIFT = 1
        shootMissile()
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_LSHIFT]):
        Global.isPressed_LSHIFT = 0

    # checking random stuff (changes a lot)
    if key[pygame.K_RETURN] and Global.isPress_RETURN == 0:
        Global.isPress_RETURN = 1
        for key, val in shipDic.items():
            print(shipDic[key].health)
    # anti repetition
    if not(key[pygame.K_RETURN]):
        Global.isPress_RETURN = 0

    curser.move()
 
# number of ships on the water
numShip = 5
# create all ship's sizes and positions
shipDic = createShip(numShip)
for i in range(len(shipDic)):
    shipDic["ship%s" %i].cleanUpShip(shipDic)
# ship damage sprites
shipDamages = {}

# Default sonar 
sonarRange = 200
sonarWidth = 45
sonarStartAngle = 0
sonarPos = vec(sideMargin + tile/2, topBotMargin + tile/2)

# creating game grid
gridDic = createGrid()

# create target curser
curser = Target((150,150,150), sideMargin + tile, topBotMargin + tile, tile, tile)

# framerate of the game
    # this probably won't matter too much, unless we decide to make animations
    # then we'll have to put in more thought into it
frameRate = 60


#########################################################################################
# MAIN GAME LOOP 
#########################################################################################

while Global.run:
    # controls rate of the game
    clock.tick(frameRate)
    # dectects inputs from all sources
    detectInputs(numShip)
    # sonar iteration
    sonarDic = createSonar()
    # is there a sunken ship
    isSunk()
    # updates screen
    update(gridDic)
    # did win
    isWin()


# if main loop is broke then close program
pygame.quit()