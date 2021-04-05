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
    def __init__(self, color, x1, y1, x2, y2, angle):
        self.color = color
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)
        self.angle = angle
        self.length = 0

    # this fn is call everytime the display is updated for every line
    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 1)

    def drawSonarMap(self):
        if self == sonarDisplay1[0]:
            pygame.draw.line(win, sonarDisplay1[0].color, sonarDisplay1[0].end1, sonarDisplay1[0].end2, width = 5)
            if len(sonarDisplay1) == 2:
                pygame.draw.line(win, sonarDisplay1[1].color, sonarDisplay1[1].end1, sonarDisplay1[1].end2, width = 5)
                pygame.draw.arc(win, sonarDisplay1[0].color, pygame.Rect(sonarPos1.x - sonarRange1 + playScreenWidth, sonarPos1.y - sonarRange1 - playScreenHeight, sonarRange1*2, sonarRange1*2), sonarDisplay1[0].angle, sonarDisplay1[1].angle, width=5)
        if self == sonarDisplay2[0]:
            pygame.draw.line(win, sonarDisplay2[0].color, sonarDisplay2[0].end1, sonarDisplay2[0].end2, width = 5)
            if len(sonarDisplay2) == 2:
                pygame.draw.line(win, sonarDisplay2[1].color, sonarDisplay2[1].end1, sonarDisplay2[1].end2, width = 5)
                pygame.draw.arc(win, sonarDisplay2[0].color, pygame.Rect(sonarPos2.x - sonarRange2 - playScreenWidth, sonarPos2.y - sonarRange2 - playScreenHeight, sonarRange2*2, sonarRange2*2), sonarDisplay2[0].angle, sonarDisplay2[1].angle, width=5)

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
    def cleanUpShip(self, shipDic1, playerNum):
        if playerNum == 1:
            # checks if current ship is overlapping any of the other ships
            for i in range(len(shipDic1)):
                if shipDic1["ship%s" %i] != self:        # neglects the instense of dectecing if a ship collides with itself
                    if pygame.Rect.colliderect(self.rect, shipDic1["ship%s" %i].rect):       # does current ship overlap with another ship
                        # overides overlapping ship with new ship generation
                        # generates new ship with random position, direction, and maybe shape
                        shipDic1["ship%s" %i] = createShip(i, 1)
                        # recussively calls
                        # the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                        shipDic1["ship%s" %i].cleanUpShip(shipDic1, 1)

            # checks if current ship is partially off screen
            for i in range(len(shipDic1)):
                if ((shipDic1["ship%s" %i].pos.x + shipDic1["ship%s" %i].width) > sideMargin + playScreen + tile) or ((shipDic1["ship%s" %i].pos.y + shipDic1["ship%s" %i].height) > topBotMargin + playScreen + playScreenHeight + tile):
                    # generates new ship with random position, direction, and maybe shape
                    shipDic1["ship%s" %i] = createShip(i, 1)
                    # recussively calls the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                    shipDic1["ship%s" %i].cleanUpShip(shipDic1, 1)

        if playerNum == 2:
            # checks if current ship is overlapping any of the other ships
            for i in range(len(shipDic2)):
                if shipDic2["ship%s" %i] != self:        # neglects the instense of dectecing if a ship collides with itself
                    if pygame.Rect.colliderect(self.rect, shipDic2["ship%s" %i].rect):       # does current ship overlap with another ship
                        # overides overlapping ship with new ship generation
                        # generates new ship with random position, direction, and maybe shape
                        shipDic2["ship%s" %i] = createShip(i, 2)
                        # recussively calls
                        # the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                        shipDic2["ship%s" %i].cleanUpShip(shipDic2, 2)

            # checks if current ship is partially off screen
            for i in range(len(shipDic2)):
                if ((shipDic2["ship%s" %i].pos.x + shipDic2["ship%s" %i].width) > sideMargin + playScreen + tile + playScreenWidth) or ((shipDic2["ship%s" %i].pos.y + shipDic2["ship%s" %i].height) > topBotMargin + playScreen + playScreenHeight + tile):
                    # generates new ship with random position, direction, and maybe shape
                    shipDic2["ship%s" %i] = createShip(i, 2)
                    # recussively calls the cleanUpShip fn again until all ships are no longer overlapping or partially off screen
                    shipDic2["ship%s" %i].cleanUpShip(shipDic2, 2)

    def draw(self):
        win.blit(self.shipSprite, (self.pos.x, self.pos.y))

# class for missile target
class Target(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def drawCurser1(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/crosshair.png'), (int(tile), int(tile))), (self.pos.x - playScreenWidth, self.pos.y - playScreenHeight))
    def drawCurser2(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/crosshair.png'), (int(tile), int(tile))), (self.pos.x + playScreenWidth, self.pos.y - playScreenHeight))

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

        if playerTurn == 1:
            # moves curser1 to coords
            # row 1
            if coord_1 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_1 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_1 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_1 = 0
                coord_C = 0
            if coord_1 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_1 = 0
                coord_D = 0
            if coord_1 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_1 = 0
                coord_E = 0
            if coord_1 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_1 = 0
                coord_F = 0
            if coord_1 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_1 = 0
                coord_G = 0
            if coord_1 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_1 = 0
                coord_H = 0
            if coord_1 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_1 = 0
                coord_I = 0
            if coord_1 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*0
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_1 = 0
                coord_J = 0
            # row 2
            if coord_2 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_2 = 0
                coord_A = 0
            if coord_2 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_2 = 0
                coord_B = 0
            if coord_2 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_2 = 0
                coord_C = 0
            if coord_2 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_2 = 0
                coord_D = 0
            if coord_2 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_2 = 0
                coord_E = 0
            if coord_2 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_2 = 0
                coord_F = 0
            if coord_2 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_2 = 0
                coord_G = 0
            if coord_2 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_2 = 0
                coord_H = 0
            if coord_2 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_2 = 0
                coord_I = 0
            if coord_2 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*1 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_2 = 0
                coord_J = 0
            # row 3
            if coord_3 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_3 = 0
                coord_A = 0
            if coord_3 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_3 = 0
                coord_B = 0
            if coord_3 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_3 = 0
                coord_C = 0
            if coord_3 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_3 = 0
                coord_D = 0
            if coord_3 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_3 = 0
                coord_E = 0
            if coord_3 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_3 = 0
                coord_F = 0
            if coord_3 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_3 = 0
                coord_G = 0
            if coord_3 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_3 = 0
                coord_H = 0
            if coord_3 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_3 = 0
                coord_I = 0
            if coord_3 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*2 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_3 = 0
                coord_J = 0
            # row 4
            if coord_4 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_4 = 0
                coord_A = 0
            if coord_4 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_4 = 0
                coord_B = 0
            if coord_4 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_4 = 0
                coord_C = 0
            if coord_4 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_4 = 0
                coord_D = 0
            if coord_4 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_4 = 0
                coord_E = 0
            if coord_4 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_4 = 0
                coord_F = 0
            if coord_4 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_4 = 0
                coord_G = 0
            if coord_4 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_4 = 0
                coord_H = 0
            if coord_4 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_4 = 0
                coord_I = 0
            if coord_4 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*3 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_4 = 0
                coord_J = 0
            # row 5
            if coord_5 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_5 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_5 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_5 = 0
                coord_C = 0
            if coord_5 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_5 = 0
                coord_D = 0
            if coord_5 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_5 = 0
                coord_E = 0
            if coord_5 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_5 = 0
                coord_F = 0
            if coord_5 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_5 = 0
                coord_G = 0
            if coord_5 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_5 = 0
                coord_H = 0
            if coord_5 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_5 = 0
                coord_I = 0
            if coord_5 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*4 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_5 = 0
                coord_J = 0
            # row 6
            if coord_6 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_6 = 0
                coord_A = 0
            if coord_6 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_6 = 0
                coord_B = 0
            if coord_6 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_6 = 0
                coord_C = 0
            if coord_6 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_6 = 0
                coord_D = 0
            if coord_6 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_6 = 0
                coord_E = 0
            if coord_6 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_6 = 0
                coord_F = 0
            if coord_6 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_6 = 0
                coord_G = 0
            if coord_6 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_6 = 0
                coord_H = 0
            if coord_6 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_6 = 0
                coord_I = 0
            if coord_6 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*5 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_6 = 0
                coord_J = 0
            # row 7
            if coord_7 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_7 = 0
                coord_A = 0
            if coord_7 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_7 = 0
                coord_B = 0
            if coord_7 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_7 = 0
                coord_C = 0
            if coord_7 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_7 = 0
                coord_D = 0
            if coord_7 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_7 = 0
                coord_E = 0
            if coord_7 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_7 = 0
                coord_F = 0
            if coord_7 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_7 = 0
                coord_G = 0
            if coord_7 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_7 = 0
                coord_H = 0
            if coord_7 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_7 = 0
                coord_I = 0
            if coord_7 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*6 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_7 = 0
                coord_J = 0
            # row 8
            if coord_8 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_8 = 0
                coord_A = 0
            if coord_8 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_8 = 0
                coord_B = 0
            if coord_8 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_8 = 0
                coord_C = 0
            if coord_8 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_8 = 0
                coord_D = 0
            if coord_8 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_8 = 0
                coord_E = 0
            if coord_8 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_8 = 0
                coord_F = 0
            if coord_8 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_8 = 0
                coord_G = 0
            if coord_8 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_8 = 0
                coord_H = 0
            if coord_8 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_8 = 0
                coord_I = 0
            if coord_8 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*7 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_8 = 0
                coord_J = 0
            # row 9
            if coord_9 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_9 = 0
                coord_A = 0
            if coord_9 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_9 = 0
                coord_B = 0
            if coord_9 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_9 = 0
                coord_C = 0
            if coord_9 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_9 = 0
                coord_D = 0
            if coord_9 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_9 = 0
                coord_E = 0
            if coord_9 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_9 = 0
                coord_F = 0
            if coord_9 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_9 = 0
                coord_G = 0
            if coord_9 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_9 = 0
                coord_H = 0
            if coord_9 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_9 = 0
                coord_I = 0
            if coord_9 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*8 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_9 = 0
                coord_J = 0
            # row 10
            if coord_0 and coord_A and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_0 = 0
                coord_A = 0
            if coord_0 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_0 = 0
                coord_B = 0
            if coord_0 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_0 = 0
                coord_C = 0
            if coord_0 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_0 = 0
                coord_D = 0
            if coord_0 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_0 = 0
                coord_E = 0
            if coord_0 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_0 = 0
                coord_F = 0
            if coord_0 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_0 = 0
                coord_G = 0
            if coord_0 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_0 = 0
                coord_H = 0
            if coord_0 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_0 = 0
                coord_I = 0
            if coord_0 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*9 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_0 = 0
                coord_J = 0

        if playerTurn == 2:
            # moves curser2 to coords
            # row 1
            if coord_1 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_1 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_1 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_1 = 0
                coord_C = 0
            if coord_1 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_1 = 0
                coord_D = 0
            if coord_1 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_1 = 0
                coord_E = 0
            if coord_1 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_1 = 0
                coord_F = 0
            if coord_1 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_1 = 0
                coord_G = 0
            if coord_1 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_1 = 0
                coord_H = 0
            if coord_1 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_1 = 0
                coord_I = 0
            if coord_1 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*0
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_1 = 0
                coord_J = 0
            # row 2
            if coord_2 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_2 = 0
                coord_A = 0
            if coord_2 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_2 = 0
                coord_B = 0
            if coord_2 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_2 = 0
                coord_C = 0
            if coord_2 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_2 = 0
                coord_D = 0
            if coord_2 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_2 = 0
                coord_E = 0
            if coord_2 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_2 = 0
                coord_F = 0
            if coord_2 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_2 = 0
                coord_G = 0
            if coord_2 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_2 = 0
                coord_H = 0
            if coord_2 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_2 = 0
                coord_I = 0
            if coord_2 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*1
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_2 = 0
                coord_J = 0
            # row 3
            if coord_3 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_3 = 0
                coord_A = 0
            if coord_3 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_3 = 0
                coord_B = 0
            if coord_3 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_3 = 0
                coord_C = 0
            if coord_3 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_3 = 0
                coord_D = 0
            if coord_3 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_3 = 0
                coord_E = 0
            if coord_3 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_3 = 0
                coord_F = 0
            if coord_3 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_3 = 0
                coord_G = 0
            if coord_3 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_3 = 0
                coord_H = 0
            if coord_3 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_3 = 0
                coord_I = 0
            if coord_3 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*2
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_3 = 0
                coord_J = 0
            # row 4
            if coord_4 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_4 = 0
                coord_A = 0
            if coord_4 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_4 = 0
                coord_B = 0
            if coord_4 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_4 = 0
                coord_C = 0
            if coord_4 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_4 = 0
                coord_D = 0
            if coord_4 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_4 = 0
                coord_E = 0
            if coord_4 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_4 = 0
                coord_F = 0
            if coord_4 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_4 = 0
                coord_G = 0
            if coord_4 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_4 = 0
                coord_H = 0
            if coord_4 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_4 = 0
                coord_I = 0
            if coord_4 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*3
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_4 = 0
                coord_J = 0
            # row 5
            if coord_5 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_5 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_5 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_5 = 0
                coord_C = 0
            if coord_5 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_5 = 0
                coord_D = 0
            if coord_5 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_5 = 0
                coord_E = 0
            if coord_5 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_5 = 0
                coord_F = 0
            if coord_5 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_5 = 0
                coord_G = 0
            if coord_5 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_5 = 0
                coord_H = 0
            if coord_5 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_5 = 0
                coord_I = 0
            if coord_5 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*4
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_5 = 0
                coord_J = 0
            # row 6
            if coord_6 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_6 = 0
                coord_A = 0
            if coord_6 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_6 = 0
                coord_B = 0
            if coord_6 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_6 = 0
                coord_C = 0
            if coord_6 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_6 = 0
                coord_D = 0
            if coord_6 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_6 = 0
                coord_E = 0
            if coord_6 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_6 = 0
                coord_F = 0
            if coord_6 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_6 = 0
                coord_G = 0
            if coord_6 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_6 = 0
                coord_H = 0
            if coord_6 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_6 = 0
                coord_I = 0
            if coord_6 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*5
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_6 = 0
                coord_J = 0
            # row 7
            if coord_7 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_7 = 0
                coord_A = 0
            if coord_7 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_7 = 0
                coord_B = 0
            if coord_7 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_7 = 0
                coord_C = 0
            if coord_7 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_7 = 0
                coord_D = 0
            if coord_7 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_7 = 0
                coord_E = 0
            if coord_7 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_7 = 0
                coord_F = 0
            if coord_7 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_7 = 0
                coord_G = 0
            if coord_7 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_7 = 0
                coord_H = 0
            if coord_7 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_7 = 0
                coord_I = 0
            if coord_7 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*6
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_7 = 0
                coord_J = 0
            # row 8
            if coord_8 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_8 = 0
                coord_A = 0
            if coord_8 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_8 = 0
                coord_B = 0
            if coord_8 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_8 = 0
                coord_C = 0
            if coord_8 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_8 = 0
                coord_D = 0
            if coord_8 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_8 = 0
                coord_E = 0
            if coord_8 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_8 = 0
                coord_F = 0
            if coord_8 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_8 = 0
                coord_G = 0
            if coord_8 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_8 = 0
                coord_H = 0
            if coord_8 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_8 = 0
                coord_I = 0
            if coord_8 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*7
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_8 = 0
                coord_J = 0
            # row 9
            if coord_9 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_9 = 0
                coord_A = 0
            if coord_9 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_9 = 0
                coord_B = 0
            if coord_9 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_9 = 0
                coord_C = 0
            if coord_9 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_9 = 0
                coord_D = 0
            if coord_9 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_9 = 0
                coord_E = 0
            if coord_9 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_9 = 0
                coord_F = 0
            if coord_9 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_9 = 0
                coord_G = 0
            if coord_9 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_9 = 0
                coord_H = 0
            if coord_9 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_9 = 0
                coord_I = 0
            if coord_9 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*8
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_9 = 0
                coord_J = 0
            # row 10
            if coord_0 and coord_A and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_0 = 0
                coord_A = 0
            if coord_0 and coord_B and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_0 = 0
                coord_B = 0
            if coord_0 and coord_C and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_0 = 0
                coord_C = 0
            if coord_0 and coord_D and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_0 = 0
                coord_D = 0
            if coord_0 and coord_E and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_0 = 0
                coord_E = 0
            if coord_0 and coord_F and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_0 = 0
                coord_F = 0
            if coord_0 and coord_G and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_0 = 0
                coord_G = 0
            if coord_0 and coord_H and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_0 = 0
                coord_H = 0
            if coord_0 and coord_I and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_0 = 0
                coord_I = 0
            if coord_0 and coord_J and lock_in:
                curser2.pos.x = sideMargin + tile*9
                curser2.pos.y = topBotMargin + tile*9 + playScreenHeight
                coord_0 = 0
                coord_J = 0
        lock_in = 0

# class for ship damage
class ShipDamage(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/bulletHole.png'), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class for hit markers
class HitMarker:
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/missTile.png'), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class for miss markers
class MissMarker:
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/hitTile.png'), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class to hold misc sprites
class Sprite():
    ocean = pygame.transform.smoothscale(pygame.image.load('Sprites/Ocean.jpg'), (playScreen, playScreen))
    sonarBackground = pygame.transform.smoothscale(pygame.image.load('Sprites/sonarBackground.png'), (playScreen, playScreen))
    grid = pygame.transform.smoothscale(pygame.image.load('Sprites/grid.png'), (playScreen + 2, playScreen + 2))
    gridSonar = pygame.transform.smoothscale(pygame.image.load('Sprites/gridSonar.png'), (playScreen + 2, playScreen + 2))
    backGround = pygame.transform.smoothscale(pygame.image.load('Sprites/subControls.jpg'), (doubleScreenWidth, screenHeight))
    sub = pygame.transform.smoothscale(pygame.image.load('Sprites/Sub.png'), (int(tile), int(tile)))
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

    # draw submarine
    # sub 1
    win.blit(Sprite.sub, (sonarPos1.x - tile/2 + playScreenWidth, sonarPos1.y - tile/2 - playScreenHeight))
    # sub 2
    win.blit(Sprite.sub, (sonarPos2.x - tile/2 - playScreenWidth, sonarPos2.y - tile/2 - playScreenHeight))

    # draws all ships
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
    for key, val in shipDic1.items():
        shipDic1[key].draw()
        #########################################################################################################################
        ###       THIS IS WHERE THE OUTPUTS FOR WHAT SHIP IS BEING HIT BY SONAR AND HOW MANY SONAR BEANS ARE HITTING IT       ###
        #                                                                                                                       #
        #                                                                                                                       #
        #print("{0:5}: {1:3}    Average Distance in Range:". format(key, shipDic1[key].sonarHitNum), shipDic1[key].averageDistance)#
        #                                                                                                                       #
        ###                                                                                                                   ###
        #########################################################################################################################

        #reset sonar collide counters (how many beams are currently hitting a ship 
        shipDic1[key].sonarHitNum = 0

        for key, val in shipDic1.items():
            averageLength[key] = []

    for key, val in shipDic2.items():
        shipDic2[key].draw()
        #########################################################################################################################
        ###       THIS IS WHERE THE OUTPUTS FOR WHAT SHIP IS BEING HIT BY SONAR AND HOW MANY SONAR BEANS ARE HITTING IT       ###
        #                                                                                                                       #
        #                                                                                                                       #
        #print("{0:5}: {1:3}    Average Distance in Range:". format(key, shipDic1[key].sonarHitNum), shipDic1[key].averageDistance)#
        #                                                                                                                       #
        ###                                                                                                                   ###
        #########################################################################################################################

        #reset sonar collide counters (how many beams are currently hitting a ship 
        shipDic2[key].sonarHitNum = 0

        for key, val in shipDic2.items():
            averageLength[key] = []

    # draws all ship damage sprites
    for key, val in shipDamages.items():
        shipDamages[key].draw()
    # draws all hit sprites
    for key, val in hitMarkers.items():
        hitMarkers[key].draw()
    # draws all miss sprites
    for key, val in missMarkers.items():
        missMarkers[key].draw()

    # draws curser1 in new position
    curser1.drawCurser1()
    curser2.drawCurser2()

    # draws all sonar beams
    for key, value in sonarDic1.items():
        sonarDic1[key].draw()
    for key, value in sonarDic2.items():
        sonarDic2[key].draw()

    sonarDisplay1[0].drawSonarMap()
    sonarDisplay2[0].drawSonarMap()


    # updates screen
    pygame.display.update()

# takes the average length of all beams colliding with a ship
def averageDist():
    for key, val in averageLength.items():
        if len(averageLength[key]) != 0:
            # crashes if i dont do the try/except -/(-.-)\-
            try:
                shipDic1[key].averageDistance = sum(averageLength[key])/len(averageLength[key])
            except:
                pass
        else:
            # crashes if i dont do the try/except -/(-.-)\-
            try:
                shipDic1[key].averageDistance = 0
            except:
                pass

# aims, widens, and extense the sonar
def sonarAim(playerTurn):
    global sonarRange1
    global sonarWidth1
    global sonarStartAngle1
    global sonarRange2
    global sonarWidth2
    global sonarStartAngle2
    global sonarPos1
    global isPress_LEFT
    global isPress_RIGHT
    global isPress_UP
    global isPress_DOWN

    keys = pygame.key.get_pressed()

    mouse = pygame.mouse.get_pressed(num_buttons=5)

    # sonar center position
    if playerTurn == 2:
        # right bound detection and left movement
        if sonarPos1.x > sideMargin + tile and keys[pygame.K_LEFT] and isPress_LEFT == 0:
            isPress_LEFT = 1
            sonarPos1.x -= tile
        # anti repetition
        if not(keys[pygame.K_LEFT]):
            isPress_LEFT = 0

        # left bound detection and right movement
        if sonarPos1.x < playScreen + sideMargin - tile and keys[pygame.K_RIGHT] and isPress_RIGHT == 0:
            isPress_RIGHT = 1
            sonarPos1.x += tile
        # anti repetition
        if not(keys[pygame.K_RIGHT]):
            isPress_RIGHT = 0

        # bottom bound detection and up movement
        if sonarPos1.y > topBotMargin + tile + playScreenHeight and keys[pygame.K_UP] and isPress_UP == 0:
            isPress_UP = 1
            sonarPos1.y -= tile
        # anti repetition
        if not(keys[pygame.K_UP]):
            isPress_UP = 0    
        
        # top bound detection and down movement
        if sonarPos1.y < playScreen + topBotMargin - tile + playScreenHeight and keys[pygame.K_DOWN] and isPress_DOWN == 0:
            isPress_DOWN = 1
            sonarPos1.y += tile
        # anti repetition
        if not(keys[pygame.K_DOWN]):
            isPress_DOWN = 0
    
        # controls
        # rotate counter-clockwise
        if mouse[0] or keys[pygame.K_LEFTBRACKET]:
            sonarStartAngle1 += 5
 
        # rotate clockwise
        if mouse[2] or keys[pygame.K_RIGHTBRACKET]:
            sonarStartAngle1 -= 5

        # increase power level
        if (keys[pygame.K_EQUALS] or (mouse[3] and mouse[1])) and sonarWidth1 >= 1:
            sonarWidth1 -= 1
            sonarRange1 += 5
            # make the sonar power grow and shrink smoother
            if sonarWidth1%2:
                sonarStartAngle1 += 1
        # decrease power level
        if (keys[pygame.K_MINUS] or (mouse[4] and mouse[1])) and sonarWidth1 <= 135:
            sonarWidth1 += 1
            sonarRange1 -= 5
            # make the sonar power grow and shrink smoother
            if sonarWidth1%2:
                sonarStartAngle1 -= 1



    # sonar center position
    if playerTurn == 1:
        # right bound detection and left movement
        if sonarPos2.x > sideMargin + tile + playScreenWidth and keys[pygame.K_LEFT] and isPress_LEFT == 0:
            isPress_LEFT = 1
            sonarPos2.x -= tile
        # anti repetition
        if not(keys[pygame.K_LEFT]):
            isPress_LEFT = 0

        # left bound detection and right movement
        if sonarPos2.x < playScreen + sideMargin - tile + playScreenWidth and keys[pygame.K_RIGHT] and isPress_RIGHT == 0:
            isPress_RIGHT = 1
            sonarPos2.x += tile
        # anti repetition
        if not(keys[pygame.K_RIGHT]):
            isPress_RIGHT = 0

        # bottom bound detection and up movement
        if sonarPos2.y > topBotMargin + tile + playScreenHeight and keys[pygame.K_UP] and isPress_UP == 0:
            isPress_UP = 1
            sonarPos2.y -= tile
        # anti repetition
        if not(keys[pygame.K_UP]):
            isPress_UP = 0    
        
        # top bound detection and down movement
        if sonarPos2.y < playScreen + topBotMargin - tile + playScreenHeight and keys[pygame.K_DOWN] and isPress_DOWN == 0:
            isPress_DOWN = 1
            sonarPos2.y += tile
        # anti repetition
        if not(keys[pygame.K_DOWN]):
            isPress_DOWN = 0
    
        # controls
        # rotate counter-clockwise
        if mouse[0] or keys[pygame.K_LEFTBRACKET]:
            sonarStartAngle2 += 5
 
        # rotate clockwise
        if mouse[2] or keys[pygame.K_RIGHTBRACKET]:
            sonarStartAngle2 -= 5

        # increase power level
        if (keys[pygame.K_EQUALS] or (mouse[3] and mouse[1])) and sonarWidth2 >= 1:
            sonarWidth2 -= 1
            sonarRange2 += 5
            # make the sonar power grow and shrink smoother
            if sonarWidth2%2:
                sonarStartAngle2 += 1
        # decrease power level
        if (keys[pygame.K_MINUS] or (mouse[4] and mouse[1])) and sonarWidth2 <= 135:
            sonarWidth2 += 1
            sonarRange2 -= 5
            # make the sonar power grow and shrink smoother
            if sonarWidth2%2:
                sonarStartAngle2 -= 1

# creates sonar array
def createSonar(playerTurn):
    global sonarPos1
    global sonarPos2
    global sonarDisplay1
    global sonarDisplay2
    # reset sonar dictionary
    sonarDic1 = {}
    sonarDic2 = {}
    sonarDisplay1 = []
    sonarDisplay2 = []

    # get the aim of the sonar
    sonarAim(playerTurn)

    # create each beam of the sonar
    for i in range(sonarStartAngle1, sonarStartAngle1 + sonarWidth1 + 1):
        # gives the beams a radius of influence
        x2 = sonarPos1.x + math.cos(-math.radians(i)) * sonarRange1 
        y2 = sonarPos1.y + math.sin(-math.radians(i)) * sonarRange1 
        # creates first case line for collision function to use
        sonarDic1["beam%s" %i] = Sonar((255,0,255), sonarPos1.x, sonarPos1.y, x2, y2, math.radians(i))
        if i == sonarStartAngle1 or i == sonarStartAngle1 + sonarWidth1:
            sonarDisplay1.append(Sonar((215,25,45), sonarPos1.x + playScreenWidth, sonarPos1.y - playScreenHeight, x2 + playScreenWidth, y2 - playScreenHeight, math.radians(i)))
        # modifies beam to new length depending on if it collided
        sonarDic1["beam%s" %i] = isCollideSonar(i, sonarDic1, sonarDic2, x2, y2, 1)

    for i in range(sonarStartAngle2, sonarStartAngle2 + sonarWidth2 + 1):
        # gives the beams a radius of influence
        x2 = sonarPos2.x + math.cos(-math.radians(i)) * sonarRange2 
        y2 = sonarPos2.y + math.sin(-math.radians(i)) * sonarRange2
        # creates first case line for collision function to use
        sonarDic2["beam%s" %i] = Sonar((255,0,255), sonarPos2.x, sonarPos2.y, x2, y2, math.radians(i))
        if i == sonarStartAngle2 or i == sonarStartAngle2 + sonarWidth2:
            sonarDisplay2.append(Sonar((215,25,45), sonarPos2.x - playScreenWidth, sonarPos2.y - playScreenHeight, x2 - playScreenWidth, y2 - playScreenHeight, math.radians(i)))
        # modifies beam to new length depending on if it collided
        sonarDic2["beam%s" %i] = isCollideSonar(i, sonarDic1, sonarDic2, x2, y2, 2)
    # returns dictionary of all the lines
    return sonarDic1, sonarDic2

# sonar collision
def isCollideSonar(beamnum, sonarDic1, sonarDic2, x2, y2, playerNum):
    global averageDistance
    global shipDic1
    global shipDic2
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
    if playerNum == 1:
        # runs through each ship for player 1
        for key, val in shipDic1.items():
            # checks if beam collides with ship
            newEnd = shipDic1[key].rect.clipline(sonarDic1["beam%s" %beamnum].end1.x, sonarDic1["beam%s" %beamnum].end1.y, sonarDic1["beam%s" %beamnum].end2.x, sonarDic1["beam%s" %beamnum].end2.y)
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
            minCalcDic[key] = math.sqrt((sonarPos1.x-value[0])**2 + (sonarPos1.y-value[1])**2)
        # if the dictionary is empty then there was no collision so return the same line
        if tempCollDic == {}:
            # screen bounds
            return Sonar((255,0,255), sonarPos1.x , sonarPos1.y , x2, y2, sonarDic1["beam%s" %beamnum].angle)
        else:
            # if not, then update line
            collideShip = min(minCalcDic, key = minCalcDic.get)
            newEnd = tempCollDic[collideShip]
            shipDic1[collideShip].sonarHitNum += 1

            # crashes if i dont do the try/except -/(-.-)\-
            try:
                averageLength[collideShip].append(math.sqrt((sonarPos1.x-newEnd[0])**2 + (sonarPos1.y-newEnd[1])**2))
            except:
                pass

            return Sonar((255,0,255), sonarPos1.x , sonarPos1.y , newEnd[0], newEnd[1], sonarDic1["beam%s" %beamnum].angle)

    if playerNum == 2:
        # runs through each ship for player 2
        for key, val in shipDic2.items():
            # checks if beam collides with ship
            newEnd = shipDic2[key].rect.clipline(sonarDic2["beam%s" %beamnum].end1.x, sonarDic2["beam%s" %beamnum].end1.y, sonarDic2["beam%s" %beamnum].end2.x, sonarDic2["beam%s" %beamnum].end2.y)
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
            minCalcDic[key] = math.sqrt((sonarPos2.x-value[0])**2 + (sonarPos2.y-value[1])**2)
        # if the dictionary is empty then there was no collision so return the same line
        if tempCollDic == {}:
            # screen bounds
            return Sonar((255,0,255), sonarPos2.x , sonarPos2.y , x2, y2, sonarDic2["beam%s" %beamnum].angle)
        else:
            # if not, then update line
            collideShip = min(minCalcDic, key = minCalcDic.get)
            newEnd = tempCollDic[collideShip]
            shipDic2[collideShip].sonarHitNum += 1

            # crashes if i dont do the try/except -/(-.-)\-
            try:
                averageLength[collideShip].append(math.sqrt((sonarPos2.x-newEnd[0])**2 + (sonarPos2.y-newEnd[1])**2))
            except:
                pass

            return Sonar((255,0,255), sonarPos2.x , sonarPos2.y , newEnd[0], newEnd[1], sonarDic2["beam%s" %beamnum].angle)

# decides legnth and direction of ship
def lengthDirect(shipNum):
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
        rand = randint(2,5)
        length = rand*tile
        width = tile
        health = rand

    # decides direction at random
    if randint(0,1):
        temp = length
        length = width
        width = temp
        if randint(0,1):
            isRotate = 90
        else:
            isRotate = 270
    else:
        if randint(0,1):
            isRotate = 0
        else:
            isRotate = 180

    return width, length, health, isRotate

# creates all ships
def createShip(i, playerNum):
    # creates ships as needed
    # gets length and orientation
    directList = lengthDirect(i)
    # creates ship object
    shipSprite = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load('Sprites/ship%s.png' % i), (int(tile), int(tile*(directList[2])))), directList[3])
    if playerNum == 1:
        ship = Ship(directList[2], shipSprite, (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin, tile*randint(0,9) + playScreenHeight + topBotMargin, directList[0], directList[1])
    if playerNum == 2:
        ship = Ship(directList[2], shipSprite, (randint(0,255), randint(0,255), randint(0,255)), tile*randint(0,9) + sideMargin + playScreenWidth, tile*randint(0,9) + playScreenHeight + topBotMargin, directList[0], directList[1])
    # returns dictionary
    return ship

# dectects collision of curser1 and ship
def isCollide():
    global playerTurn
    key = "NONE"
    if playerTurn == 1:
        for key, val in shipDic2.items():
            if pygame.Rect.colliderect(pygame.Rect(curser1.pos.x, curser1.pos.y, curser1.width, curser1.height), shipDic2[key].rect):
                return True, key      # returns if collision and if so, the ship that was hit
        return False, key
    if playerTurn == 2:
        for key, val in shipDic1.items():
            if pygame.Rect.colliderect(pygame.Rect(curser2.pos.x, curser2.pos.y, curser2.width, curser2.height), shipDic1[key].rect):
                return True, key      # returns if collision and if so, the ship that was hit
        return False, key

# shoots missile at ship and does damage
def shootMissile():
    global shipDamages
    global playerTurn
    damageTest = 1
    # so the user cant shoot the same spot and do more damage
    for i in range(len(shipDamages)):
        # crashes if i dont do the try/except -/(-.-)\-
        try:
            if (shipDamages["shipDamage%s" %i].pos.x == curser1.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser1.pos.y):
                damageTest = 0
        except:
            pass
        # for player 2
        try:
            if (shipDamages["shipDamage%s" %i].pos.x == curser2.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser2.pos.y):
                damageTest = 0
        except:
            pass

    print("Fire!!!")
    print("~~~~~~~~")
    # set to a variable to extract 2 returns
    isCollides = isCollide()
    # did it hit
    if playerTurn == 1:
        if isCollides[0] and damageTest:
            print("You hit {}!!". format(isCollides[1]))
            print("~~~~~~~~")
            # hit marker for player 1 sonar
            hitMarkers["hit%s" %len(hitMarkers)] = HitMarker((0,255,0), curser1.pos.x - playScreenWidth, curser1.pos.y - playScreenHeight, tile, tile)
            # places bullethole on damaged spot
            shipDamages["shipDamage%s" %len(shipDamages)] = ShipDamage((255,255,0), curser1.pos.x, curser1.pos.y, curser1.width, curser1.height)
            # decreases health
            if shipDic2[isCollides[1]].health > 0:
                shipDic2[isCollides[1]].health -= 1
        else:
            # miss marker for player 1 sonar
            missMarkers["miss%s" %len(missMarkers)] = MissMarker((255,0,0), curser1.pos.x - playScreenWidth, curser1.pos.y - playScreenHeight, tile, tile)
            if damageTest:
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                print("You already damaged that part!")
                print("~~~~~~~~")

    if playerTurn == 2:
        if isCollides[0] and damageTest:
            print("You hit {}!!". format(isCollides[1]))
            print("~~~~~~~~")
            # hit marker for player 2 sonar
            hitMarkers["hit%s" %len(hitMarkers)] = HitMarker((0,255,0), curser2.pos.x + playScreenWidth, curser2.pos.y - playScreenHeight, tile, tile)
            # places yellow square on damaged spot
            shipDamages["shipDamage%s" %len(shipDamages)] = ShipDamage((255,255,0), curser2.pos.x, curser2.pos.y, curser2.width, curser2.height)
            # decreases health
            if shipDic1[isCollides[1]].health > 0:
                shipDic1[isCollides[1]].health -= 1
        else:
            # miss marker for player 2 sonar
            missMarkers["miss%s" %len(missMarkers)] = MissMarker((255,0,0), curser2.pos.x + playScreenWidth, curser2.pos.y - playScreenHeight, tile, tile)
            if damageTest:
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                print("You already damaged that part!")
                print("~~~~~~~~")

# detects if any sunken ships
def isSunk():
    global shipDic1
    global shipDic2
    deadShip1 = 0
    deadShip2 = 0
    # sinks ship if health is zero
    for key, items in shipDic1.items():
        if not(shipDic1[key].health):
            print("You got one!!")
            print("~~~~~~~~")
            sink(key)
            deadShip1 = key

    for key, items in shipDic2.items():
        if not(shipDic2[key].health):
            print("You got one!!")
            print("~~~~~~~~")
            sink(key)
            deadShip2 = key
    # deletes ship thats been sunk
    if deadShip1:
        del shipDic1[deadShip1]
    # deletes ship thats been sunk
    if deadShip2:
        del shipDic2[deadShip2]

# is ship is sunken, then remove it and the shipDamage
def sink(ship):
    global shipDic1
    global shipDic2
    global shipDamages
    delShipDamages = []

    # deletes shipDamage sprites that are on sunken ship
    for key, val in shipDamages.items():
        if pygame.Rect.colliderect(pygame.Rect(shipDamages[key].pos.x, shipDamages[key].pos.y, shipDamages[key].width, shipDamages[key].height), shipDic1[ship].rect):
            delShipDamages.append(key)

    for key, val in shipDamages.items():
        if pygame.Rect.colliderect(pygame.Rect(shipDamages[key].pos.x, shipDamages[key].pos.y, shipDamages[key].width, shipDamages[key].height), shipDic2[ship].rect):
            delShipDamages.append(key)
    # deleting damage sprites of sunken ship
    for ish in delShipDamages:
        del shipDamages[ish]

# detects if game has been won
def isWin():
    global run
    tot = 0
    for key, val in shipDic1.items():
        tot += shipDic1[key].health

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
    global shipDic1
    global shipDic2
    global run
    global playerTurn
    global missMarkers
    global hitMarkers
    global shipDamages

    key = pygame.key.get_pressed()
    # detects if user wants to close the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            run = False

    # for test, generates new boats
    if key[pygame.K_TAB] and isPress_TAB == 0:
        isPress_TAB = 1
        hitMarkers = {}
        missMarkers = {}
        shipDamages = {}
        shipDic1 = {}
        shipDic2 = {}

        for i in range(numShip):
            shipDic1["ship%s" %i] = createShip(i, 1)
        for i in range(len(shipDic1)):
            shipDic1["ship%s" %i].cleanUpShip(shipDic1, 1)

        for i in range(numShip):
            shipDic2["ship%s" %i] = createShip(i, 2)
        for i in range(len(shipDic1)):
            shipDic2["ship%s" %i].cleanUpShip(shipDic2, 2)
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
   
    # shooting missle
    if key[pygame.K_COMMA]:
        playerTurn = 1
    if key[pygame.K_PERIOD]:
        playerTurn = 2
    # curser1 movement is in it's own class function
    curser1.move()
 
# default first player to get to control
playerTurn = 1

# number of ships on the water
numShip = 5
# create all ship's sizes and positions for player 1
shipDic1 = {}
for i in range(numShip):
    shipDic1["ship%s" %i] = createShip(i, 1)        # the 1 is the player number
for i in range(len(shipDic1)):
    shipDic1["ship%s" %i].cleanUpShip(shipDic1, 1)

#create all ship's sizes and positions for player 2
shipDic2 = {}
for i in range(numShip):
    shipDic2["ship%s" %i] = createShip(i, 2)        # the 2 is the player number 
for i in range(len(shipDic1)):
    shipDic2["ship%s" %i].cleanUpShip(shipDic2, 2)

# ship damage sprites
shipDamages = {}
missMarkers = {}
hitMarkers = {}

# Default sonar 
sonarRange1 = tile
sonarWidth1 = 135
sonarStartAngle1 = 0
sonarRange2 = tile
sonarWidth2 = 135
sonarStartAngle2 = 0
sonarPos1 = vec(sideMargin + tile/2, topBotMargin + tile/2 + playScreenHeight)
sonarPos2 = vec(sideMargin + tile/2 + playScreenWidth, topBotMargin + tile/2 + playScreenHeight)

# for calculating average distance
averageLength = {}

# create target curser1
curser1 = Target((150,150,150), sideMargin + tile + playScreenWidth, topBotMargin + tile + playScreenHeight, tile, tile)
curser2 = Target((150,150,150), sideMargin + tile, topBotMargin + tile + playScreenHeight, tile, tile)

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
    sonarDicUnpacker = createSonar(playerTurn)
    sonarDic1 = sonarDicUnpacker[0]
    sonarDic2 = sonarDicUnpacker[1]
    # is there a sunken ship
    isSunk()
    # updates screen
    update()
    # did win
    isWin()


# if main loop is broke then close program
pygame.quit()