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
import os

# screen deminsions stuff
screenHeight = 600
screenWidth = 600
doubleScreenWidth = screenWidth*2
playScreenHeight = int(screenHeight/2)
playScreenWidth = screenWidth
playScreen = int(playScreenHeight*0.9)
topBotMargin = (playScreenHeight - playScreen)/2
sideMargin = (playScreenWidth - playScreen)/2
tile = int(playScreen/10) + 0.75
# for scaling certain things to different sizes
scalingFactor = screenHeight/1280

# initialize
pygame.init()
win = pygame.display.set_mode((doubleScreenWidth, screenHeight))
pygame.display.set_caption("Battleships the Musical")
# clock
clock = pygame.time.Clock()

# # sounds
pygame.mixer.init()
# ##############################
# #   -Channels
ch_water = pygame.mixer.Channel(0)
ch_shipTheme0 = pygame.mixer.Channel(1)
ch_shipTheme1 = pygame.mixer.Channel(2)
ch_shipTheme2 = pygame.mixer.Channel(3)
ch_shipTheme3 = pygame.mixer.Channel(4)
ch_shipTheme4 = pygame.mixer.Channel(5)
ch_waterBuffer = pygame.mixer.Channel(6)
#   -Water Sounds
#all water sounds are 5400 frames long (at 60FPS)

#boost below sounds volume in logic
water1 = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'water1.wav'))
water2 = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'water2.wav'))
water3 = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'water3.wav'))
waterS_array = [water1, water2, water3]
#   -Ship Themes
carrier_close = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy','Carrier - Close Range.wav'))
carrier_mid = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy','Carrier - Mid Range.wav'))
carrier_far = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy','Carrier - Long Range.wav'))

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
isPress_COMMA = 0
isPress_PERIOD = 0
isPress_w = 0
isPress_a = 0
isPress_s = 0
isPress_d = 0
isPress_p = 0
isPress_z = 0
isDisplayingDistress = 0
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
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_1 and coord_B and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_1 and coord_C and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*2 + playScreenHeight
                coord_1 = 0
                coord_C = 0
            if coord_1 and coord_D and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*3 + playScreenHeight
                coord_1 = 0
                coord_D = 0
            if coord_1 and coord_E and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*4 + playScreenHeight
                coord_1 = 0
                coord_E = 0
            if coord_1 and coord_F and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*5 + playScreenHeight
                coord_1 = 0
                coord_F = 0
            if coord_1 and coord_G and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*6 + playScreenHeight
                coord_1 = 0
                coord_G = 0
            if coord_1 and coord_H and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*7 + playScreenHeight
                coord_1 = 0
                coord_H = 0
            if coord_1 and coord_I and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
                curser1.pos.y = topBotMargin + tile*8 + playScreenHeight
                coord_1 = 0
                coord_I = 0
            if coord_1 and coord_J and lock_in:
                curser1.pos.x = sideMargin + tile*0 + playScreenWidth
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

# class for distress calls
class distressCall(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load('Sprites/distressSignal.png'), (int(tile), int(tile))), (self.pos.x, self.pos.y))

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
    sonarBackground = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','sonarBackground.png')), (playScreen, playScreen))
    waitingScreen = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','waitingScreen.png')), (screenWidth, screenHeight))
    grid = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','grid.png')), (playScreen + 2, playScreen + 2))
    gridSonar = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','gridSonar.png')), (playScreen + 2, playScreen + 2))
    backGround = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','mainbackground.png')), (doubleScreenWidth, screenHeight))
    sub = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Sub.png')), (int(tile), int(tile)))
    sonarPowerMeter = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','SonarPowerMeter.png')), (int(0.8*sideMargin), int(0.95*playScreen)))
    hitSprite = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','hitTile.png')), (int(tile), int(tile)))
    missSprite = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','missTile.png')), (int(tile), int(tile)))

    # animation sprites
    oceanAniCount = 0
    oceanAni = [pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 01.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 02.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 03.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 04.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 05.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 06.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 07.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 08.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 09.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 10.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 11.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 12.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 13.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 14.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 15.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 16.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 17.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 18.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 19.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 20.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 21.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 22.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 23.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 24.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 25.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 26.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 27.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 28.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 29.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 30.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 31.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 32.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 33.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 34.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 35.png')), (playScreen, playScreen)),
                pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','Ocean','WaterCaustics 36.png')), (playScreen, playScreen))]

    explosionAniCount = 0
    isExplode = 0
    explosionAni = [pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','explosion','exp1.png')), (int(tile), int(tile))),
                    pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','explosion','exp2.png')), (int(tile), int(tile))),
                    pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','explosion','exp3.png')), (int(tile), int(tile))),
                    pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','explosion','exp4.png')), (int(tile), int(tile))),
                    pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','explosion','exp5.png')), (int(tile), int(tile)))]
####### Functions ########

# updates image/screen
def update():
    global isPress_p

    if isPress_p == 0:
        win.fill((0,0,0))

        # draws sonar background
        win.blit(Sprite.sonarBackground, (sideMargin, topBotMargin))
        win.blit(Sprite.sonarBackground, (sideMargin + playScreenWidth, topBotMargin))
        # draws distress calls
        if (myClock//5)% 5:
            for key, val in distressCalls.items():
                distressCalls[key].draw()

        win.blit(Sprite.gridSonar, (sideMargin - 1, topBotMargin - 1))
        win.blit(Sprite.gridSonar, (sideMargin + playScreenWidth - 1, topBotMargin - 1))

        # draws red sonar before the ocean map, so you can't see it one the ocean
        if not(playerTurn == 1):
            sonarDisplay1[0].drawSonarMap()
        if not(playerTurn == 2):
            sonarDisplay2[0].drawSonarMap()

        # draws ocean background
        oceanAnimation()
        win.blit(Sprite.grid, (sideMargin - 1, topBotMargin + playScreenHeight - 1))
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

        # draw explosion animation if needed
        if Sprite.isExplode == 1:
            explosionAnimation()

        # draws curser1 in new position
        curser1.drawCurser1()
        curser2.drawCurser2()

        # draws all sonar beams
        for key, value in sonarDic1.items():
            sonarDic1[key].draw()
        for key, value in sonarDic2.items():
            sonarDic2[key].draw()

        win.blit(Sprite.sonarPowerMeter, (playScreen + 1.1*sideMargin, topBotMargin*1.5))
        win.blit(Sprite.sonarPowerMeter, (playScreen + 1.1*sideMargin + playScreenWidth, topBotMargin*1.5))


        sonarMeter1.draw()
        sonarMeter2.draw()

        sonarChargeMeter1.draw()
        sonarChargeMeter2.draw()


        # adds background
        win.blit(Sprite.backGround, (0,0))

        # draws waiting screen
        #if player2End and not(Sprite.explosionAniCount):
        #    win.blit(Sprite.waitingScreen, (screenWidth, 0))
        #if player1End and not(Sprite.explosionAniCount):
        #    win.blit(Sprite.waitingScreen, (0, 0))

        # updates screen
        pygame.display.update()
        
    elif isPress_p == 1:
        pass

# animates ocean
def oceanAnimation():
    if Sprite.oceanAniCount + 1 >= 138:
        Sprite.oceanAniCount = 0

    if Sprite.oceanAniCount + 1 <= 72:
        win.blit(Sprite.oceanAni[Sprite.oceanAniCount // 2], (sideMargin, topBotMargin + playScreenHeight))
        win.blit(Sprite.oceanAni[Sprite.oceanAniCount // 2], (sideMargin + playScreenWidth, topBotMargin + playScreenHeight))

    if Sprite.oceanAniCount + 1 > 72:
        win.blit(Sprite.oceanAni[(143 - Sprite.oceanAniCount) // 2], (sideMargin, topBotMargin + playScreenHeight))
        win.blit(Sprite.oceanAni[(143 - Sprite.oceanAniCount)  // 2], (sideMargin + playScreenWidth, topBotMargin + playScreenHeight))

    Sprite.oceanAniCount += 1

# animates explosions
def explosionAnimation():
    global playerShot1
    global playerShot2

    Sprite.explosionAniCount += 1

    if playerShot1 and Sprite.explosionAniCount + 1 <= 10:
        win.blit(Sprite.explosionAni[(Sprite.explosionAniCount - 10) // 2], (curser1.pos.x, curser1.pos.y))
    if playerShot2 and Sprite.explosionAniCount + 1 <= 10:
        win.blit(Sprite.explosionAni[(Sprite.explosionAniCount - 10) // 2], (curser2.pos.x, curser2.pos.y))

    if Sprite.explosionAniCount + 1 >= afterShotTime:
        playerShot1 = False
        playerShot2 = False
        Sprite.explosionAniCount = 0
        Sprite.isExplode = 0

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
        if keys[pygame.K_EQUALS] and sonarWidth1 >= 2:
            sonarWidth1 -= 2
            sonarRange1 += int(8 * scalingFactor)
            # make the sonar power grow and shrink smoother
            if sonarWidth1%2:
                sonarStartAngle1 += 1
        # decrease power level
        if keys[pygame.K_MINUS] and sonarWidth1 <= 135:
            sonarWidth1 += 2
            sonarRange1 -= int(8 * scalingFactor)
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
        if keys[pygame.K_EQUALS] and sonarWidth2 >= 2:
            sonarWidth2 -= 2
            sonarRange2 += int(8 * scalingFactor)
            # make the sonar power grow and shrink smoother
            if sonarWidth2%2:
                sonarStartAngle2 += 1
        # decrease power level
        if keys[pygame.K_MINUS] and sonarWidth2 <= 135:
            sonarWidth2 += 2
            sonarRange2 -= int(8 * scalingFactor)
            # make the sonar power grow and shrink smoother
            if sonarWidth2%2:
                sonarStartAngle2 -= 1

# creates sonar array
def createSonar(playerTurn):
    global sonarPos1
    global sonarPos2
    global sonarDisplay1
    global sonarDisplay2
    global sonarRange1
    global sonarRange2
    global isPress_p
    global shipDic1
    global shipDic2

    # reset sonar dictionary
    sonarDic1 = {}
    sonarDic2 = {}
    sonarDisplay1 = []
    sonarDisplay2 = []
    # get the aim of the sonar
    sonarAim(playerTurn)
    # create each beam of the sonar
    for i in range(sonarStartAngle1, sonarStartAngle1 + sonarWidth1 + 1, sonarDensity):
        # gives the beams a radius of influence
        x2 = sonarPos1.x + math.cos(-math.radians(i)) * sonarRange1 
        y2 = sonarPos1.y + math.sin(-math.radians(i)) * sonarRange1 
        # creates first case line for collision function to use
        sonarDic1["beam%s" %i] = Sonar((255,0,255), sonarPos1.x, sonarPos1.y, x2, y2, math.radians(i))
        if i == sonarStartAngle1 or i == sonarStartAngle1 + sonarWidth1 - 1:
            sonarDisplay1.append(Sonar((215,25,45), sonarPos1.x + playScreenWidth, sonarPos1.y - playScreenHeight, x2 + playScreenWidth, y2 - playScreenHeight, math.radians(i)))
        # modifies beam to new length depending on if it collided
        sonarDic1["beam%s" %i] = isCollideSonar(i, sonarDic1, sonarDic2, x2, y2, 1)

    for i in range(sonarStartAngle2, sonarStartAngle2 + sonarWidth2 + 1, sonarDensity):
        # gives the beams a radius of influence
        x2 = sonarPos2.x + math.cos(-math.radians(i)) * sonarRange2 
        y2 = sonarPos2.y + math.sin(-math.radians(i)) * sonarRange2
        # creates first case line for collision function to use
        sonarDic2["beam%s" %i] = Sonar((255,0,255), sonarPos2.x, sonarPos2.y, x2, y2, math.radians(i))
        if i == sonarStartAngle2 or i == sonarStartAngle2 + sonarWidth2 - 1:
            sonarDisplay2.append(Sonar((215,25,45), sonarPos2.x - playScreenWidth, sonarPos2.y - playScreenHeight, x2 - playScreenWidth, y2 - playScreenHeight, math.radians(i)))
        # modifies beam to new length depending on if it collided
        sonarDic2["beam%s" %i] = isCollideSonar(i, sonarDic1, sonarDic2, x2, y2, 2)

    #createSonarPowerMeter(sonarRange1, sonarRange2)

    #coupling good times
    #making a list of ships hit by sonar if in sonar stage
    #player 1 and player 2
    
    if isPress_p == 1:
        sonar_hitShips = {}
        #beamHitNumList = {}
        #print(shipDic1)
        if playerTurn == 1:
            for key, val in shipDic1.items():
                ship = val
                if ship.sonarHitNum > 0:
                    sonar_hitShips[key] = val
                    print('ship added')
                    #beamHitNumList.append(ship.sonarHitNum)
                    #1st item in beamHitNum list will be the first item in sonar_hitShi[s]
    
            #print('beamHitNumList: {}'.format(beamHitNumList))
            print('(1)sonar_hitShips: {}'.format(sonar_hitShips))
        elif playerTurn == 2:
            for key, val in shipDic2.items():
                ship = val
                if ship.sonarHitNum > 0:
                    sonar_hitShips[key] = val
                    print('ship added')
                    #beamHitNumList.append(ship.sonarHitNum)
            print('(2)sonar_hitShips: {}'.format(sonar_hitShips))
        # calls ship sounds,
        shipTheme_playback(sonar_hitShips)
        
        #TO BREAK THE LOOP
        isPress_p = 0


    # returns dictionary of all the lines
    return sonarDic1, sonarDic2

# creates sonar power level meter
def createSonarPowerMeter(sonarRange1, sonarRange2):
    global sonarMeter1
    global sonarMeter2
    sonarMeter1 = Rectangle((0,0,0), playScreen + 1.1*sideMargin, topBotMargin*2, 0.8*sideMargin, playScreen*0.9 - sonarRange2*scalingFactor*0.875)
    sonarMeter2 = Rectangle((0,0,0), playScreen + 1.1*sideMargin + playScreenWidth, topBotMargin*2, 0.8*sideMargin, playScreen*0.9 - sonarRange1*scalingFactor*0.875)

# pulse sonar to give game sense of ships around
def pulseSonar():
    global sonarRange1
    global sonarRange2
    global sonarCharge1
    global sonarCharge2
    # i guess put sounds here or maybe in a seperate function
    # implement sonar charge
    if playerTurn == 1:
        sonarCharge1 -= sonarRange2     # sonarRange# are switch to fixed some previous swap
        if sonarCharge1 < 0:
            sonarCharge1 = 0
    if playerTurn == 2:
        sonarCharge2 -= sonarRange1
        if sonarCharge2 < 0:
            sonarCharge2 = 0
    # update sonar charge meter
    createSonarChargeMeter()

# creates and updates sonar charge meter
def createSonarChargeMeter():
    global sonarCharge1
    global sonarCharge2
    global sonarChargeMeter1
    global sonarChargeMeter2
    sonarCharge1_scaled = (sonarCharge1/MAXSONARCHARGE)
    sonarCharge2_scaled = (sonarCharge2/MAXSONARCHARGE)
    sonarChargeMeter1 = Rectangle((0,155,0), playScreen + 1.05*sideMargin, topBotMargin*2 + playScreenHeight + playScreen*0.235, 0.7*sideMargin, playScreen*0.66*sonarCharge1_scaled)  
    sonarChargeMeter2 = Rectangle((0,155,0), playScreen + 1.05*sideMargin + playScreenWidth, topBotMargin*2 + playScreenHeight + playScreen*0.235, 0.7*sideMargin, playScreen*0.66*sonarCharge2_scaled)

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
    global player1End
    global player2End    
    global isExplode
    global playerTrigger
    global playerShot1
    global playerShot2
    global shoooted

    shoooted = True
    player1End = False
    player2End = False
    Sprite.isExplode = 1
    damageTest1 = 1
    damageTest2 = 1
    playerTrigger = 1
    # so the user cant shoot the same spot and do more damage
    for i in range(len(shipDamages)):
        # crashes if i dont do the try/except -/(-.-)\-
        try:
            if (shipDamages["shipDamage%s" %i].pos.x == curser1.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser1.pos.y):
                damageTest1 = 0
        except:
            pass
        # for player 2
        try:
            if (shipDamages["shipDamage%s" %i].pos.x == curser2.pos.x) and (shipDamages["shipDamage%s" %i].pos.y == curser2.pos.y):
                damageTest2 = 0
        except:
            pass

    print("Fire!!!")
    print("~~~~~~~~")
    # set to a variable to extract 2 returns
    isCollides = isCollide()
    # did it hit
    if playerTurn == 1:
        # for explosion animation
        playerShot1 = True
        # end turn
        player1End = True
        if isCollides[0] and damageTest1:
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
            if damageTest1:
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                print("Player 1, you already damaged that part!")
                print("~~~~~~~~")

    if playerTurn == 2:
        # for explosion animation
        playerShot2 = True
        # end turn
        player2End = True
        if isCollides[0] and damageTest2:
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
            if damageTest2:
                # miss marker for player 2 sonar
                missMarkers["miss%s" %len(missMarkers)] = MissMarker((255,0,0), curser2.pos.x + playScreenWidth, curser2.pos.y - playScreenHeight, tile, tile)
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                print("Player 2, you already damaged that part!")
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
    tot1 = 0
    tot2 = 0
    for key, val in shipDic1.items():
        tot1 += shipDic1[key].health

    if tot1 == 0:
        print("\n\n\n\t\t\t\t      **********************")
        print("\t\t\t\t*****  Player 2 Wins!  *****")
        print("\t\t\t\t      **********************")
        run = False

    for key, val in shipDic2.items():
        tot2 += shipDic2[key].health

    if tot2 == 0:
        print("\n\n\n\t\t\t\t      **********************")
        print("\t\t\t\t*****  Player 1 Wins!  *****")
        print("\t\t\t\t      **********************")
        run = False

# detects if ship is in distress
def isDistressed():
    global isDisplayingDistress
    global sonarCharge1
    global sonarCharge2
    global distressCalls
    global tempPlayerTurn
    global shoooted

    #print(shoooted)
    #print(sonarCharge1)
    if not(sonarCharge1) and isDisplayingDistress == 0 and tempPlayerTurn != playerTurn and playerTurn != 0:
        #print('frog')
        isDisplayingDistress = 1
        shipDistress(1)
    if not(sonarCharge2) and isDisplayingDistress == 0 and tempPlayerTurn != playerTurn and playerTurn != 0:
        #print('frog')
        isDisplayingDistress = 1
        shipDistress(2)

    if tempPlayerTurn != playerTurn and shoooted:
        shoooted = False
        distressCalls = {}
        isDisplayingDistress = 0
        if not(sonarCharge1):
            sonarCharge1 = MAXSONARCHARGE
        if not(sonarCharge2):
            sonarCharge2 = MAXSONARCHARGE

    tempPlayerTurn = playerTurn

# distress mode for certain ship
def shipDistress(playerInDistress):
    global playerTurn
    global shipDic1
    global shipDic2
    global tile
    global distressCalls

    shipName = "ship%s" %randint(0,4)

    # need to make random cloud so other player can guess where ship is
    distressDensity = 2
    distressRange = 1
    distressOffset = randint(-1,1)

    shipLength = shipDic1[shipName].health + shipDic1[shipName].damage

    distressCalls = {}

    if playerInDistress == 1:
        # guarantees that atleast one part of the ship will be lit
        if shipDic1[shipName].width < shipDic1[shipName].height:
            distressCalls["ontarget"] = distressCall((255,255,0), shipDic1[shipName].pos.x + playScreenWidth, shipDic1[shipName].pos.y + randint(0, shipLength - 1)*tile - playScreenHeight, tile, tile)
        else:
            distressCalls["ontarget"] = distressCall((255,255,0), shipDic1[shipName].pos.x + randint(0, shipLength - 1)*tile + playScreenWidth, shipDic1[shipName].pos.y - playScreenHeight, tile, tile)

        # need to make random cloud so other player can guess where ship is
        for k in range(randint(distressDensity, distressDensity + 3)):
            for i in range(0, randint(distressRange, distressRange + 2)):
                if shipDic1[shipName].width < shipDic1[shipName].height:
                    distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic1[shipName].pos.x + tile*randint(-i,i) + distressOffset*tile + playScreenWidth, shipDic1[shipName].pos.y + tile*randint(-i,i) + int(0.5 * shipLength)*tile + distressOffset*tile - playScreenHeight, tile, tile)
                else:
                    distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic1[shipName].pos.x + tile*randint(-i,i) + distressOffset*tile + int(0.5 * shipLength)*tile + playScreenWidth, shipDic1[shipName].pos.y + tile*randint(-i,i) + distressOffset*tile - playScreenHeight, tile, tile)

    if playerInDistress == 2:
        # guarantees that atleast one part of the ship will be lit
        if shipDic2[shipName].width < shipDic2[shipName].height:
            distressCalls["ontarget"] = distressCall((255,255,0), shipDic2[shipName].pos.x + playScreenWidth, shipDic2[shipName].pos.y + randint(0, shipLength - 1)*tile - playScreenHeight, tile, tile)
        else:
            distressCalls["ontarget"] = distressCall((255,255,0), shipDic2[shipName].pos.x + randint(0, shipLength - 1)*tile + playScreenWidth, shipDic2[shipName].pos.y - playScreenHeight, tile, tile)

        # need to make random cloud so other player can guess where ship is
        for k in range(randint(distressDensity, distressDensity + 3)):
            for i in range(0, randint(distressRange, distressRange + 2)):
                if shipDic2[shipName].width < shipDic2[shipName].height:
                    distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic2[shipName].pos.x + tile*randint(-i,i) + distressOffset*tile - playScreenWidth, shipDic2[shipName].pos.y + tile*randint(-i,i) + int(0.5 * shipLength)*tile + distressOffset*tile - playScreenHeight, tile, tile)
                else:
                    distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic2[shipName].pos.x + tile*randint(-i,i) + distressOffset*tile + int(0.5 * shipLength)*tile - playScreenWidth, shipDic2[shipName].pos.y + tile*randint(-i,i) + distressOffset*tile - playScreenHeight, tile, tile)

# detects if key is pressed
def detectInputs(numShip):

    global isPress_SPACE
    global isPress_RETURN
    global isPress_LSHIFT
    global isPress_TAB
    global isPress_BACKQUOTE
    global isPress_COMMA
    global isPress_PERIOD
    global isPress_p
    global isPress_z
    global shipDic1
    global shipDic2
    global run
    global playerTurn
    global missMarkers
    global hitMarkers
    global shipDamages
    global shoooted

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
    if key[pygame.K_SPACE] and isPress_SPACE == 0 and playerTurn:
        isPress_SPACE = 1
        shootMissile()
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_SPACE]):
        isPress_SPACE = 0

    # shoot sonar
    if key[pygame.K_p] and isPress_p == 0:
        isPress_p = 1
        pulseSonar()
        
        
    #if not(key[pygame.K_p]):
        #isPress_p = 0

    # shooting missle
    if key[pygame.K_COMMA] and isPress_COMMA == 0:
        isPress_COMMA = 1
        shipDistress(1)
        #playerTurn = 1
    if not(key[pygame.K_COMMA]):
        isPress_COMMA = 0
    if key[pygame.K_PERIOD] and isPress_PERIOD == 0:
        isPress_PERIOD = 1
        shipDistress(2)
        #playerTurn = 2
    if not(key[pygame.K_PERIOD]):
        isPress_PERIOD = 0

    if key[pygame.K_z] and isPress_z == 0:
        isPress_z = 1

    # curser1 movement is in it's own class function
    curser1.move()
 
# desided when players turns are
def isPlayerTurn():
    global playerTurn
    global player1End
    global player2End
    global playerCount
    global playerTrigger

    # not inputs allowed from either player when this is 0
    playerTurn = 0

    if playerCount + 1 >= 30:
        playerTrigger = 0
        playerCount = 0 
        if player1End:
            playerTurn = 2
    
        if player2End:
            playerTurn = 1

    playerCount += 1

#function for playback of ship themes
#set up for 2 players pulling from their respective collections
def shipTheme_playback(sonar_hitShips):
    global shipDic1
    global shipDic2
    global playerTurn
    #3 volume settings based on amt of beams hitting ship
    ##TO BE REWORKED
        
    for val in sonar_hitShips.values(): 
        #print(sonar_hitShips)
        
        
        #for i in beamHitNumList
        if ch_shipTheme0.get_busy() == False:
            if val.sonarHitNum < 10:
                ch_shipTheme0.set_volume(0.3, 0.3)
            elif val.sonarHitNum > 10 and val.sonarHitNum < 20:
                ch_shipTheme0.set_volume(0.6,0.6)
            else:
                ch_shipTheme0.set_volume(0.9,0.9)

        elif ch_shipTheme1.get_busy() == False:
            if val.sonarHitNum < 10:
                ch_shipTheme1.set_volume(0.3, 0.3)
            elif val.sonarHitNum > 10 and val.sonarHitNum < 20:
                ch_shipTheme1.set_volume(0.6,0.6)
            else:
                ch_shipTheme1.set_volume(0.9,0.9)
        
        elif ch_shipTheme2.get_busy() == False:
            if val.sonarHitNum < 10:
                ch_shipTheme2.set_volume(0.3, 0.3)
            elif val.sonarHitNum > 10 and val.sonarHitNum < 20:
                ch_shipTheme2.set_volume(0.6,0.6)
            else:
                ch_shipTheme2.set_volume(0.9,0.9)
        
        elif ch_shipTheme3.get_busy() == False:
            if val.sonarHitNum < 10:
                ch_shipTheme3.set_volume(0.3, 0.3)
            elif val.sonarHitNum > 10 and val.sonarHitNum < 20:
                ch_shipTheme3.set_volume(0.6,0.6)
            else:
                ch_shipTheme3.set_volume(0.9,0.9)
        
        elif ch_shipTheme4.get_busy() == False:
            if val.sonarHitNum < 10:
                ch_shipTheme4.set_volume(0.3, 0.3)
            elif val.sonarHitNum > 10 and val.sonarHitNum < 20:
                ch_shipTheme4.set_volume(0.6,0.6)
            else:
                ch_shipTheme4.set_volume(0.9,0.9)
        
        
        #playback options based on distance the beam is from sub and what ship is being hit
        if playerTurn == 1:
            if val == shipDic1['ship0']:
                if ch_shipTheme0.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme0.play(carrier_close)
                    print('ship0 channel busy: {} '.format(ch_shipTheme0.get_busy()))
            elif val == shipDic1['ship1']:
                if ch_shipTheme1.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme1.play(carrier_far)
                    print('ship1 channel busy: {} '.format(ch_shipTheme1.get_busy()))
            elif val == shipDic1['ship2']:
                if ch_shipTheme2.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme2.play(carrier_mid)
                    print('ship2 channel busy: {} '.format(ch_shipTheme2.get_busy()))
            elif val == shipDic1['ship3']:
                if ch_shipTheme3.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme3.play(carrier_close)
                    print('ship3 channel busy: {} '.format(ch_shipTheme3.get_busy()))
            elif val == shipDic1['ship4']:
                if ch_shipTheme4.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme4.play(carrier_far)
                    print('ship4 channel busy: {} '.format(ch_shipTheme4.get_busy()))
                    #elif ship.averageDistance > 80 and ship.averageDistance < 130:
                        #ch_shipTheme.play(carrier_mid)
                    #else:
                        #ch_shipTheme.play(carrier_far)

        if playerTurn == 2:
            if val == shipDic2['ship0']:
                if ch_shipTheme0.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme0.play(carrier_close)
                    print('ship0 channel busy: {} '.format(ch_shipTheme0.get_busy()))
            elif val == shipDic2['ship1']:
                if ch_shipTheme1.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme1.play(carrier_far)
                    print('ship1 channel busy: {} '.format(ch_shipTheme1.get_busy()))
            elif val == shipDic2['ship2']:
                if ch_shipTheme2.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme2.play(carrier_mid)
                    print('ship2 channel busy: {} '.format(ch_shipTheme2.get_busy()))
            elif val == shipDic2['ship3']:
                if ch_shipTheme3.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme3.play(carrier_close)
                    print('ship3 channel busy: {} '.format(ch_shipTheme3.get_busy()))
            elif val == shipDic2['ship4']:
                if ch_shipTheme4.get_busy() == False:
                    #if ship.averageDistance < 80:
                    ch_shipTheme4.play(carrier_far)
                    print('ship4 channel busy: {} '.format(ch_shipTheme4.get_busy()))
                    #elif ship.averageDistance > 80 and ship.averageDistance < 130:
                        #ch_shipTheme.play(carrier_mid)
                    #else:
                        #ch_shipTheme.play(carrier_far)
            
    
    return



def waterSound(run, waterClock, waterSound, waterChannel, waterChannelBuffer):
 #water sounds controlled by 2 channels. primary playback channel = waterChannel, secondary playback channel = waterChannelBuffer
 #the buffer provides audio to sustain the water noises while the primary playback channel fades out and back in
 #water clock tracks game ticks, these are used to represent time

    waterSound = waterSound[randint(0,2)]

 #begin playback on main water channel if the game is running and the channel is not currently being used
    if run == True and waterChannel.get_busy() == False:
        
       #play the sound for the length of the duration (will not use the whole duration - could potentially use smaller sound files)
       waterChannel.play(waterSound, maxtime=90000)
       #setting volume (in stereo) to 1/2 of full volume 
       waterChannel.set_volume(0.5,0.5)

 #fade conditional - tracks duration of play length and fades accordingly
 #if water clock number is a number near any number where % 650 = 0:
 #fadeout the primary playback channel, and fade in the secondary playback channel
    if waterChannel.get_busy() == True and waterClock % 3000 == 0:
        waterChannel.fadeout(9000)
        waterChannelBuffer.play(waterSound, maxtime=80000, fade_ms=9000)

 #fades out the buffer channel once enough time has passed for the primary playback channel to fade back in
    if waterChannelBuffer.get_busy() == True and waterChannel.get_busy() == True and waterClock % 3500 == 0:#615+35=685 (5 seconds after a fade occurs)
        waterChannelBuffer.fadeout(5000)

     #below measurements differ according to runtime, but fade works nonetheless (lol (optimize for pi))
     #650 is the cutoff point for a fade
     #~7 increments a second (5 seconds = 35 increments)
     #fadeout should be % == 0 by (650-35= 615)
     # default first player to get to control

         
playerTurn = 1
player1End = False
player2End = True
playerCount = 0
playerTrigger = 0
playerShot1 = False
playerShot2 = False
tempPlayerTurn = 0
shoooted = False

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
sonarDensity = 2
sonarPos1 = vec(sideMargin + tile/2, topBotMargin + tile/2 + playScreenHeight)
sonarPos2 = vec(sideMargin + tile/2 + playScreenWidth, topBotMargin + tile/2 + playScreenHeight)
sonarMeter1 = 0
sonarMeter2 = 0
sonarChargeMeter1 = 0
sonarChargeMeter2 = 0
# default sonar charge amount
MAXSONARCHARGE = 500
sonarCharge1 = MAXSONARCHARGE
sonarCharge2 = MAXSONARCHARGE
# create default sonar charge mater
createSonarChargeMeter()

# for calculating average distance
averageLength = {}

# for distress location
distressCalls = {}

# create target curser1
curser1 = Target((150,150,150), sideMargin + tile + playScreenWidth, topBotMargin + tile + playScreenHeight, tile, tile)
curser2 = Target((150,150,150), sideMargin + tile, topBotMargin + tile + playScreenHeight, tile, tile)


# framerate of the game
frameRate = 60

# to keep time and for blinking animations
myClock = 0
#separate clock for water sound playback
waterClock = 0

# gameplay timing (the pacing of the game)
afterShotTime = 60  # time after shot




targetCoords = []
#########################################################################################
# MAIN GAME LOOP 
#########################################################################################

run = True
while run:
    if myClock == 1000:
        myClock = 0
    if waterClock == 4000:
        waterClock = 0
    myClock += 1
    waterClock += 1
    #calls water sound playback and maintains fade loop
    waterSound(run, waterClock, waterS_array, ch_water, ch_waterBuffer)
    # controls rate of the game
    clock.tick(frameRate)
    # dectects inputs from all sources
    detectInputs(numShip)
    # sonar iteration
    sonarDicUnpacker = createSonar(playerTurn)
    sonarDic1 = sonarDicUnpacker[0]
    sonarDic2 = sonarDicUnpacker[1]
    #ship distress detection
    isDistressed()
    # is there a sunken ship
    isSunk()
    #
    createSonarPowerMeter(sonarRange1, sonarRange2)
    # updates screen
    update()
    # desides player turn
    if playerTrigger:
        isPlayerTurn()
    # did win
    isWin()


# if main loop is broke then close program
pygame.quit()
