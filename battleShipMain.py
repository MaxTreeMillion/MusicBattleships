################################################################ 
# Battleships the Musical: Main Code (at least now)
#    - Ship generation: {{ DONE }}
#    - Hit dectection: {{ DONE }}
#    - Ship damage and sinking: {{ DONE }} 
#    - Ray casting for sonar: {{ DONE }} 
"""  - Game deign: {{ WORKING }}   """
################################################################

# imports
import pygame
import math
from random import randint

# screen deminsions
screenHeight = 1280
screenWidth = 720
doubleScreenWidth = screenWidth*2
playScreenHeight = int(screenHeight/2)
playScreenWidth = screenWidth
playScreen = int(playScreenHeight*0.9)
topBotMargin = (playScreenHeight - playScreen)/2
sideMargin = (playScreenWidth - playScreen)/2
tile = int(playScreen/10) + 0.75

# initialize
pygame.init()
win = pygame.display.set_mode((doubleScreenWidth, screenHeight))
pygame.display.set_caption("Battleships the Musical")
# clock
clock = pygame.time.Clock()

# x/y vectors
vec = pygame.math.Vector2

# Debugging
DEBUG = False

# globals for blocking multiple inputs on one key press
isPress_UP = 0
isPress_DOWN = 0
isPress_LEFT = 0
isPress_RIGHT = 0
isPress_SPACE = 0
isPress_RETURN = 0
isPress_LSHIFT = 0
isPress_TAB = 0
isPress_BACKQUOTE = 0
isPress_w = 0
isPress_a = 0
isPress_s = 0
isPress_d = 0
coord_1 = 0
coord_2 = 0
coord_3 = 0
coord_4 = 0
coord_5 = 0
coord_6 = 0
coord_7 = 0
coord_8 = 0
coord_9 = 0
coord_0 = 0
coord_A = 0
coord_B = 0
coord_C = 0
coord_D = 0
coord_E = 0
coord_F = 0
coord_G = 0
coord_H = 0
coord_I = 0
coord_J = 0
lock_in = 0
isPress_coord_1 = 0
isPress_coord_2 = 0
isPress_coord_3 = 0
isPress_coord_4 = 0
isPress_coord_5 = 0
isPress_coord_6 = 0
isPress_coord_7 = 0
isPress_coord_8 = 0
isPress_coord_9 = 0
isPress_coord_0 = 0
isPress_coord_A = 0
isPress_coord_B = 0
isPress_coord_C = 0
isPress_coord_D = 0
isPress_coord_E = 0
isPress_coord_F = 0
isPress_coord_G = 0
isPress_coord_H = 0
isPress_coord_I = 0
isPress_coord_J = 0
isPress_displayCoords = 0

####### Classes #######
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
    def __init__(self, health, shipSprite, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)
        self.health = health
        self.damage = 0
        self.sonarHitNum = 0
        self.averageDistance = 0
        self.shipSprite = shipSprite
        self.shipSpritePos = vec(x,y)

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
                    shipSprite = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load('Sprites/ship%s.png' % i), (int(tile), int(tile*(directList[2])))), directList[3])
                    ship = Ship(directList[2], shipSprite, (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + topBotMargin + playScreenHeight, directList[0], directList[1])
                    shipDic["ship%s" %i] = ship
                    # recussively calls
                    # the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                    shipDic["ship%s" %i].cleanUpShip(shipDic)

        # checks if current ship is partially off screen
        for i in range(len(shipDic)):
            if ((shipDic["ship%s" %i].pos.x + shipDic["ship%s" %i].width) > sideMargin + playScreen) or ((shipDic["ship%s" %i].pos.y + shipDic["ship%s" %i].height) > topBotMargin + playScreen + playScreenHeight):
                # generates new ship with random position, direction, and maybe shape
                directList = lengthDirect(i, shipDic)
                shipSprite = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load('Sprites/ship%s.png' % i), (int(tile), int(tile*(directList[2])))), directList[3])
                ship = Ship(directList[2], shipSprite, (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + topBotMargin + playScreenHeight, directList[0], directList[1])
                shipDic["ship%s" %i] = ship
                # recussively calls the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                shipDic["ship%s" %i].cleanUpShip(shipDic)
    def draw(self):
        win.blit(self.shipSprite, (self.pos.x, self.pos.y))

# class for missile target
class Target(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/crosshair.png'), (int(tile), int(tile))), (self.pos.x, self.pos.y))

    def move(self):
        global targetCoords
        global coord_1
        global coord_2
        global coord_3
        global coord_4
        global coord_5
        global coord_6
        global coord_7
        global coord_8
        global coord_9
        global coord_0
        global coord_A
        global coord_B
        global coord_C
        global coord_D
        global coord_E
        global coord_F
        global coord_G
        global coord_H
        global coord_I
        global coord_J
        global lock_in
        global isPress_coord_1
        global isPress_coord_2
        global isPress_coord_3
        global isPress_coord_4
        global isPress_coord_5
        global isPress_coord_6
        global isPress_coord_7
        global isPress_coord_8
        global isPress_coord_9
        global isPress_coord_0
        global isPress_coord_A
        global isPress_coord_B
        global isPress_coord_C
        global isPress_coord_D
        global isPress_coord_E
        global isPress_coord_F
        global isPress_coord_G
        global isPress_coord_H
        global isPress_coord_I
        global isPress_coord_J
        global isPress_displayCoords
        # detecting key presses
        keys = pygame.key.get_pressed()

        # sets trigger var to true
        if keys[pygame.K_1] and isPress_coord_1:
            coord_1 = True
            isPress_coord_1 = 0
            isPress_displayCoords = 1
            targetCoords.append(1)
        if not(keys[pygame.K_1]):
            isPress_coord_1 = 1
        if keys[pygame.K_2] and isPress_coord_2:
            coord_2 = True
            isPress_coord_2 = 0
            isPress_displayCoords = 1
            targetCoords.append(2)
        if not(keys[pygame.K_2]):
            isPress_coord_2 = 1
        if keys[pygame.K_3] and isPress_coord_3:
            coord_3 = True
            isPress_coord_3 = 0
            isPress_displayCoords = 1
            targetCoords.append(3)
        if not(keys[pygame.K_3]):
            isPress_coord_3 = 1
        if keys[pygame.K_4] and isPress_coord_4:
            coord_4 = True
            isPress_coord_4 = 0
            isPress_displayCoords = 1
            targetCoords.append(4)
        if not(keys[pygame.K_4]):
            isPress_coord_4 = 1
        if keys[pygame.K_5] and isPress_coord_5:
            coord_5 = True
            isPress_coord_5 = 0
            isPress_displayCoords = 1
            targetCoords.append(5)
        if not(keys[pygame.K_5]):
            isPress_coord_5 = 1
        if keys[pygame.K_6] and isPress_coord_6:
            coord_6 = True
            isPress_coord_6 = 0
            isPress_displayCoords = 1
            targetCoords.append(6)
        if not(keys[pygame.K_6]):
            isPress_coord_6 = 1
        if keys[pygame.K_7] and isPress_coord_7:
            coord_7 = True
            isPress_coord_7 = 0
            isPress_displayCoords = 1
            targetCoords.append(7)
        if not(keys[pygame.K_7]):
            isPress_coord_7 = 1
        if keys[pygame.K_8] and isPress_coord_8:
            coord_8 = True
            isPress_coord_8 = 0
            isPress_displayCoords = 1
            targetCoords.append(8)
        if not(keys[pygame.K_8]):
            isPress_coord_8 = 1
        if keys[pygame.K_9] and isPress_coord_9:
            coord_9 = True
            isPress_coord_9 = 0
            isPress_displayCoords = 1
            targetCoords.append(9)
        if not(keys[pygame.K_9]):
            isPress_coord_9 = 1
        if keys[pygame.K_0] and isPress_coord_0:
            coord_0 = True
            isPress_coord_0 = 0
            isPress_displayCoords = 1
            targetCoords.append(0)
        if not(keys[pygame.K_0]):
            isPress_coord_0 = 1
        if keys[pygame.K_a] and isPress_coord_A:
            coord_A = True
            isPress_coord_A = 0
            isPress_displayCoords = 1
            targetCoords.append('A')
        if not(keys[pygame.K_a]):
            isPress_coord_A = 1
        if keys[pygame.K_b] and isPress_coord_B:
            coord_B = True
            isPress_coord_B = 0
            isPress_displayCoords = 1
            targetCoords.append('B')
        if not(keys[pygame.K_b]):
            isPress_coord_B = 1
        if keys[pygame.K_c] and isPress_coord_C:
            coord_C = True
            isPress_coord_C = 0
            isPress_displayCoords = 1
            targetCoords.append('C')
        if not(keys[pygame.K_c]):
            isPress_coord_C = 1
        if keys[pygame.K_d] and isPress_coord_D:
            coord_D = True
            isPress_coord_D = 0
            isPress_displayCoords = 1
            targetCoords.append('D')
        if not(keys[pygame.K_d]):
            isPress_coord_D = 1
        if keys[pygame.K_e] and isPress_coord_E:
            coord_E = True
            isPress_coord_E = 0
            isPress_displayCoords = 1
            targetCoords.append('E')
        if not(keys[pygame.K_e]):
            isPress_coord_E = 1
        if keys[pygame.K_f] and isPress_coord_F:
            coord_F = True
            isPress_coord_F = 0
            isPress_displayCoords = 1
            targetCoords.append('F')
        if not(keys[pygame.K_f]):
            isPress_coord_F = 1
        if keys[pygame.K_g] and isPress_coord_G:
            coord_G = True
            isPress_coord_G = 0
            isPress_displayCoords = 1
            targetCoords.append('G')
        if not(keys[pygame.K_g]):
            isPress_coord_G = 1
        if keys[pygame.K_h] and isPress_coord_H:
            coord_H = True
            isPress_coord_H = 0
            isPress_displayCoords = 1
            targetCoords.append('H')
        if not(keys[pygame.K_h]):
            isPress_coord_H = 1
        if keys[pygame.K_i] and isPress_coord_I:
            coord_I = True
            isPress_coord_I = 0
            isPress_displayCoords = 1
            targetCoords.append('I')
        if not(keys[pygame.K_i]):
            isPress_coord_I = 1
        if keys[pygame.K_j] and isPress_coord_J:
            coord_J = True
            isPress_coord_J = 0
            isPress_displayCoords = 1
            targetCoords.append('J')
        if not(keys[pygame.K_j]):
            isPress_coord_J = 1

        targetCoords_cut = targetCoords[0:2]
        # confirmation buttom
        if keys[pygame.K_LSHIFT] and len(targetCoords_cut) == 2:
            if isinstance(targetCoords_cut[0],str) and isinstance(targetCoords_cut[1],str):
                print("You must enter coordinates in form: '(0,A)' or '(A,0)'")
                isPress_displayCoords = 0
            elif isinstance(targetCoords_cut[0],int) and isinstance(targetCoords_cut[1],int):
                print("You must enter coordinates in form: '(0,A)' or '(A,0)'")
                isPress_displayCoords = 0
            else:
                lock_in = True
                isPress_displayCoords = 0
                print("~~~~~~~~")
                print("Ready...")
                print("Aim...")
            targetCoords = []

        if isPress_displayCoords:
            isPress_displayCoords = 0
            print(targetCoords_cut)


        # moves curser to coords
        # row 1
        if coord_1 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*0
            coord_1 = 0
            coord_A = 0
        if coord_1 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*1
            coord_1 = 0
            coord_B = 0
        if coord_1 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*2
            coord_1 = 0
            coord_C = 0
        if coord_1 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*3
            coord_1 = 0
            coord_D = 0
        if coord_1 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*4
            coord_1 = 0
            coord_E = 0
        if coord_1 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*5
            coord_1 = 0
            coord_F = 0
        if coord_1 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*6
            coord_1 = 0
            coord_G = 0
        if coord_1 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*7
            coord_1 = 0
            coord_H = 0
        if coord_1 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*8
            coord_1 = 0
            coord_I = 0
        if coord_1 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*0
            curser.pos.y = topBotMargin + tile*9
            coord_1 = 0
            coord_J = 0
        # row 2
        if coord_2 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*0
            coord_2 = 0
            coord_A = 0
        if coord_2 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*1
            coord_2 = 0
            coord_B = 0
        if coord_2 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*2
            coord_2 = 0
            coord_C = 0
        if coord_2 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*3
            coord_2 = 0
            coord_D = 0
        if coord_2 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*4
            coord_2 = 0
            coord_E = 0
        if coord_2 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*5
            coord_2 = 0
            coord_F = 0
        if coord_2 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*6
            coord_2 = 0
            coord_G = 0
        if coord_2 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*7
            coord_2 = 0
            coord_H = 0
        if coord_2 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*8
            coord_2 = 0
            coord_I = 0
        if coord_2 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*1
            curser.pos.y = topBotMargin + tile*9
            coord_2 = 0
            coord_J = 0
        # row 3
        if coord_3 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*0
            coord_3 = 0
            coord_A = 0
        if coord_3 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*1
            coord_3 = 0
            coord_B = 0
        if coord_3 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*2
            coord_3 = 0
            coord_C = 0
        if coord_3 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*3
            coord_3 = 0
            coord_D = 0
        if coord_3 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*4
            coord_3 = 0
            coord_E = 0
        if coord_3 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*5
            coord_3 = 0
            coord_F = 0
        if coord_3 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*6
            coord_3 = 0
            coord_G = 0
        if coord_3 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*7
            coord_3 = 0
            coord_H = 0
        if coord_3 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*8
            coord_3 = 0
            coord_I = 0
        if coord_3 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*2
            curser.pos.y = topBotMargin + tile*9
            coord_3 = 0
            coord_J = 0
        # row 4
        if coord_4 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*0
            coord_4 = 0
            coord_A = 0
        if coord_4 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*1
            coord_4 = 0
            coord_B = 0
        if coord_4 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*2
            coord_4 = 0
            coord_C = 0
        if coord_4 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*3
            coord_4 = 0
            coord_D = 0
        if coord_4 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*4
            coord_4 = 0
            coord_E = 0
        if coord_4 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*5
            coord_4 = 0
            coord_F = 0
        if coord_4 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*6
            coord_4 = 0
            coord_G = 0
        if coord_4 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*7
            coord_4 = 0
            coord_H = 0
        if coord_4 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*8
            coord_4 = 0
            coord_I = 0
        if coord_4 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*3
            curser.pos.y = topBotMargin + tile*9
            coord_4 = 0
            coord_J = 0
        # row 5
        if coord_5 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*0
            coord_1 = 0
            coord_A = 0
        if coord_5 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*1
            coord_1 = 0
            coord_B = 0
        if coord_5 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*2
            coord_5 = 0
            coord_C = 0
        if coord_5 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*3
            coord_5 = 0
            coord_D = 0
        if coord_5 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*4
            coord_5 = 0
            coord_E = 0
        if coord_5 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*5
            coord_5 = 0
            coord_F = 0
        if coord_5 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*6
            coord_5 = 0
            coord_G = 0
        if coord_5 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*7
            coord_5 = 0
            coord_H = 0
        if coord_5 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*8
            coord_5 = 0
            coord_I = 0
        if coord_5 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*4
            curser.pos.y = topBotMargin + tile*9
            coord_5 = 0
            coord_J = 0
        # row 6
        if coord_6 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*0
            coord_6 = 0
            coord_A = 0
        if coord_6 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*1
            coord_6 = 0
            coord_B = 0
        if coord_6 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*2
            coord_6 = 0
            coord_C = 0
        if coord_6 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*3
            coord_6 = 0
            coord_D = 0
        if coord_6 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*4
            coord_6 = 0
            coord_E = 0
        if coord_6 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*5
            coord_6 = 0
            coord_F = 0
        if coord_6 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*6
            coord_6 = 0
            coord_G = 0
        if coord_6 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*7
            coord_6 = 0
            coord_H = 0
        if coord_6 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*8
            coord_6 = 0
            coord_I = 0
        if coord_6 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*5
            curser.pos.y = topBotMargin + tile*9
            coord_6 = 0
            coord_J = 0
        # row 7
        if coord_7 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*0
            coord_7 = 0
            coord_A = 0
        if coord_7 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*1
            coord_7 = 0
            coord_B = 0
        if coord_7 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*2
            coord_7 = 0
            coord_C = 0
        if coord_7 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*3
            coord_7 = 0
            coord_D = 0
        if coord_7 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*4
            coord_7 = 0
            coord_E = 0
        if coord_7 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*5
            coord_7 = 0
            coord_F = 0
        if coord_7 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*6
            coord_7 = 0
            coord_G = 0
        if coord_7 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*7
            coord_7 = 0
            coord_H = 0
        if coord_7 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*8
            coord_7 = 0
            coord_I = 0
        if coord_7 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*6
            curser.pos.y = topBotMargin + tile*9
            coord_7 = 0
            coord_J = 0
        # row 8
        if coord_8 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*0
            coord_8 = 0
            coord_A = 0
        if coord_8 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*1
            coord_8 = 0
            coord_B = 0
        if coord_8 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*2
            coord_8 = 0
            coord_C = 0
        if coord_8 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*3
            coord_8 = 0
            coord_D = 0
        if coord_8 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*4
            coord_8 = 0
            coord_E = 0
        if coord_8 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*5
            coord_8 = 0
            coord_F = 0
        if coord_8 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*6
            coord_8 = 0
            coord_G = 0
        if coord_8 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*7
            coord_8 = 0
            coord_H = 0
        if coord_8 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*8
            coord_8 = 0
            coord_I = 0
        if coord_8 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*7
            curser.pos.y = topBotMargin + tile*9
            coord_8 = 0
            coord_J = 0
        # row 9
        if coord_9 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*0
            coord_9 = 0
            coord_A = 0
        if coord_9 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*1
            coord_9 = 0
            coord_B = 0
        if coord_9 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*2
            coord_9 = 0
            coord_C = 0
        if coord_9 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*3
            coord_9 = 0
            coord_D = 0
        if coord_9 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*4
            coord_9 = 0
            coord_E = 0
        if coord_9 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*5
            coord_9 = 0
            coord_F = 0
        if coord_9 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*6
            coord_9 = 0
            coord_G = 0
        if coord_9 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*7
            coord_9 = 0
            coord_H = 0
        if coord_9 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*8
            coord_9 = 0
            coord_I = 0
        if coord_9 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*8
            curser.pos.y = topBotMargin + tile*9
            coord_9 = 0
            coord_J = 0
        # row 10
        if coord_0 and coord_A and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*0
            coord_0 = 0
            coord_A = 0
        if coord_0 and coord_B and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*1
            coord_0 = 0
            coord_B = 0
        if coord_0 and coord_C and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*2
            coord_0 = 0
            coord_C = 0
        if coord_0 and coord_D and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*3
            coord_0 = 0
            coord_D = 0
        if coord_0 and coord_E and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*4
            coord_0 = 0
            coord_E = 0
        if coord_0 and coord_F and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*5
            coord_0 = 0
            coord_F = 0
        if coord_0 and coord_G and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*6
            coord_0 = 0
            coord_G = 0
        if coord_0 and coord_H and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*7
            coord_0 = 0
            coord_H = 0
        if coord_0 and coord_I and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*8
            coord_0 = 0
            coord_I = 0
        if coord_0 and coord_J and lock_in:
            curser.pos.x = sideMargin + tile*9
            curser.pos.y = topBotMargin + tile*9
            coord_0 = 0
            coord_J = 0
        lock_in = 0
# class for ship damage
class ShipDamage(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/bulletHole.png'), (int(tile), int(tile))), (self.pos.x, self.pos.y))

class Sprite():
    ocean = pygame.transform.smoothscale(pygame.image.load('Sprites/Ocean.jpg'), (playScreen, playScreen))
    sonarBackground = pygame.transform.smoothscale(pygame.image.load('Sprites/sonarBackground.png'), (playScreen, playScreen))
    grid = pygame.transform.smoothscale(pygame.image.load('Sprites/grid.png'), (playScreen + 2, playScreen + 2))
    gridSonar = pygame.transform.smoothscale(pygame.image.load('Sprites/gridSonar.png'), (playScreen + 2, playScreen + 2))
    backGround = pygame.transform.smoothscale(pygame.image.load('Sprites/subControls.jpg'), (doubleScreenWidth, screenHeight))
    hitSprite = pygame.transform.smoothscale(pygame.image.load('Sprites/hitTile.png'), (int(tile), int(tile)))
    missSprite = pygame.transform.smoothscale(pygame.image.load('Sprites/missTile.png'), (int(tile), int(tile)))
####### Functions ########

# updates image/screen
def update():
    # adds background
    win.blit(Sprite.backGround, (0,0))

    # behind the grids image
    win.blit(Sprite.sonarBackground, (sideMargin, topBotMargin))
    win.blit(Sprite.ocean, (sideMargin, topBotMargin + playScreenHeight))
    win.blit(Sprite.sonarBackground, (sideMargin + playScreenWidth, topBotMargin))
    win.blit(Sprite.ocean, (sideMargin + playScreenWidth, topBotMargin + playScreenHeight))
    # draws grid
    win.blit(Sprite.gridSonar, (sideMargin - 1, topBotMargin - 1))
    win.blit(Sprite.grid, (sideMargin - 1, topBotMargin + playScreenHeight - 1))
    win.blit(Sprite.gridSonar, (sideMargin + playScreenWidth - 1, topBotMargin - 1))
    win.blit(Sprite.grid, (sideMargin + playScreenWidth - 1, topBotMargin + playScreenHeight - 1))
    
    # gets the average distance from sonar orgin to ship
    averageDist()

    # draws all ships
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
    for key, val in shipDic.items():
        shipDic[key].draw()
        #########################################################################################################################
        ###       THIS IS WHERE THE OUTPUTS FOR WHAT SHIP IS BEING HIT BY SONAR AND HOW MANY SONAR BEANS ARE HITTING IT       ###
        #                                                                                                                       #
        #                                                                                                                       #
        #print("{0:5}: {1:3}    Average Distance in Range:". format(key, shipDic[key].sonarHitNum), shipDic[key].averageDistance)#
        #                                                                                                                       #
        ###                                                                                                                   ###
        #########################################################################################################################

        #reset sonar collide counters (how many beams are currently hitting a ship 
        shipDic[key].sonarHitNum = 0

        for key, val in shipDic.items():
            averageLength[key] = []

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

# takes the average length of all beams colliding with a ship
def averageDist():
    for key, val in averageLength.items():
        if len(averageLength[key]) != 0:
            # crashes if i dont do the try/except -/(-.-)\-
            try:
                shipDic[key].averageDistance = sum(averageLength[key])/len(averageLength[key])
            except:
                pass
        else:
            # crashes if i dont do the try/except -/(-.-)\-
            try:
                shipDic[key].averageDistance = 0
            except:
                pass

# aims, widens, and extense the sonar
def sonarAim():
    global sonarRange
    global sonarWidth
    global sonarStartAngle
    global sonarPos
    global isPress_LEFT
    global isPress_RIGHT
    global isPress_UP
    global isPress_DOWN

    keys = pygame.key.get_pressed()

    mouse = pygame.mouse.get_pressed(num_buttons=5)

    # sonar center position

    # right bound detection and left movement
    if sonarPos.x > sideMargin + tile and keys[pygame.K_LEFT] and isPress_LEFT == 0:
        isPress_LEFT = 1
        sonarPos.x -= tile
    # anti repetition
    if not(keys[pygame.K_LEFT]):
        isPress_LEFT = 0

    # left bound detection and right movement
    if sonarPos.x < playScreen + sideMargin - tile and keys[pygame.K_RIGHT] and isPress_RIGHT == 0:
        isPress_RIGHT = 1
        sonarPos.x += tile
    # anti repetition
    if not(keys[pygame.K_RIGHT]):
        isPress_RIGHT = 0

    # bottom bound detection and up movement
    if sonarPos.y > topBotMargin + tile + playScreenHeight and keys[pygame.K_UP] and isPress_UP == 0:
        isPress_UP = 1
        sonarPos.y -= tile
    # anti repetition
    if not(keys[pygame.K_UP]):
        isPress_UP = 0    
        
    # top bound detection and down movement
    if sonarPos.y < playScreen + topBotMargin - tile + playScreenHeight and keys[pygame.K_DOWN] and isPress_DOWN == 0:
        isPress_DOWN = 1
        sonarPos.y += tile
    # anti repetition
    if not(keys[pygame.K_DOWN]):
        isPress_DOWN = 0
    
    # controls
    # rotate counter-clockwise
    if mouse[0] or keys[pygame.K_SEMICOLON]:
        sonarStartAngle += 5
 
    # rotate clockwise
    if mouse[2] or keys[pygame.K_BACKSLASH]:
        sonarStartAngle -= 5

    # increase range

    if (keys[pygame.K_EQUALS] or (mouse[4] and not(mouse[1]))) and sonarRange <= math.sqrt((playScreen/2)**2 + (playScreen/2)**2):
        sonarRange += 5

    # decrease range
    if (keys[pygame.K_MINUS] or (mouse[3] and not(mouse[1]))) and sonarRange >= 50:
        sonarRange -= 5

    # increase width
    if (keys[pygame.K_RIGHTBRACKET] or (mouse[4] and mouse[1])) and sonarWidth <= 358:
        sonarWidth += 1
    # decrease width
    if (keys[pygame.K_LEFTBRACKET] or (mouse[3] and mouse[1])) and sonarWidth >= 1:
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
    global averageDistance
    # temp dictionary for use when beam crosses multiple ships
    tempCollDic = {}
    minCalcDic = {}

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
        collideShip = min(minCalcDic, key = minCalcDic.get)
        newEnd = tempCollDic[collideShip]
        shipDic[collideShip].sonarHitNum += 1

        # crashes if i dont do the try/except -/(-.-)\-
        try:
            averageLength[collideShip].append(math.sqrt((sonarPos.x-newEnd[0])**2 + (sonarPos.y-newEnd[1])**2))
        except:
            pass

        return Sonar((255,0,255), sonarPos.x , sonarPos.y , newEnd[0], newEnd[1])

# decides legnth and direction of ship
def lengthDirect(shipNum, shipDic):
    # calcs the different sized ships
        # there are 5 ships
        # Legths: 5, 4, 3, 3, 2
    isRotate = 0

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
        isRotate = 90
        temp = length
        length = width
        width = temp

    return width, length, health, isRotate

# creates all ships
def createShip(numShip):
    # holds the ship names and class info
    shipDic = {}
    # creates ships as needed
    for i in range(numShip):
        # gets length and orientation
        directList = lengthDirect(i, shipDic)
        # creates ship object
        
        shipSprite = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load('Sprites/ship%s.png' % i), (int(tile), int(tile*(directList[2])))), directList[3])
        ship = Ship(directList[2], shipSprite, (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + topBotMargin*2 + playScreenWidth + 3.5, directList[0], directList[1])
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
        # crashes if i dont do the try/except -/(-.-)\-
        try:
            if (shipDamages["shipDamage%s" %i].pos.x == curser.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser.pos.y):
                damageTest = 0
        except:
            pass

    print("Fire!!!")
    print("~~~~~~~~")
    # set to a variable to extract 2 returns
    isCollides = isCollide()
    # did it hit
    if isCollides[0] and damageTest:
        print("You hit {}!!". format(isCollides[1]))
        print("~~~~~~~~")
        # places yellow square on damaged spot
        shipDamages["shipDamage%s" %len(shipDamages)] = ShipDamage((255,255,0), curser.pos.x, curser.pos.y, curser.width, curser.height)
        # decreases health
        if shipDic[isCollides[1]].health > 0:
            shipDic[isCollides[1]].health -= 1
    else:
        if damageTest:
            print("All you shot was sea!")
            print("~~~~~~~~")
        else:
            print("You already damaged that part!")
            print("~~~~~~~~")

# detects if any sunken ships
def isSunk():
    global shipDic
    deadShip = 0
    # sinks ship if health is zero
    for key, items in shipDic.items():
        if not(shipDic[key].health):
            print("You got one!!")
            print("~~~~~~~~")
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
    global run
    tot = 0
    for key, val in shipDic.items():
        tot += shipDic[key].health

    if tot == 0:
        print("\n\n\n\t\t\t\t**********************")
        print("\t\t\t\t*****  You Win!  *****")
        print("\t\t\t\t**********************")
        run = False

def detectInputs(numShip):
    global isPress_SPACE
    global isPress_RETURN
    global isPress_LSHIFT
    global isPress_TAB
    global isPress_BACKQUOTE
    global shipDic
    global run

    key = pygame.key.get_pressed()
    # detects if user wants to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            run = False

    # for test, generates new boats
    if key[pygame.K_TAB] and isPress_TAB == 0:
        isPress_TAB = 1
        shipDic = createShip(numShip)
        for i in range(len(shipDic)):
            shipDic["ship%s" %i].cleanUpShip(shipDic)
    # anti repetition
    if not(key[pygame.K_TAB]):
        isPress_TAB = 0
    
    # shooting missle
    if key[pygame.K_SPACE] and isPress_SPACE == 0:
        isPress_SPACE = 1
        shootMissile()
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_SPACE]):
        isPress_SPACE = 0

    # curser movement is in it's own class function
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
sonarPos = vec(sideMargin + tile/2, topBotMargin + tile/2 + playScreenHeight)

# for calculating average distance
averageLength = {}

# create target curser
curser = Target((150,150,150), sideMargin + tile, topBotMargin + tile, tile, tile)

# framerate of the game
    # this probably won't matter too much, unless we decide to make animations
    # then we'll have to put in more thought into it
frameRate = 60

targetCoords = []
#########################################################################################
# MAIN GAME LOOP 
#########################################################################################

run = True
while run:
    # controls rate of the game
    clock.tick(frameRate)
    # dectects inputs from all sources
    detectInputs(numShip)
    # sonar iteration
    sonarDic = createSonar()
    # is there a sunken ship
    isSunk()
    # updates screen
    update()
    # did win
    isWin()


# if main loop is broke then close program
pygame.quit()