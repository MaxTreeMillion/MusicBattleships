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
screenHeight = 1280
screenWidth = 720
#screenHeight = 896
#screenWidth = 504
doubleScreenWidth = screenWidth*2
playScreenHeight = int(screenHeight/2)
playScreenWidth = screenWidth
playScreen = int(playScreenHeight*0.9)
topBotMargin = (playScreenHeight - playScreen)/2
sideMargin = (playScreenWidth - playScreen)/2 
tile = int(playScreen/10) + 0.75
# for scaling certain things to different sizes
scalingFactor = screenHeight/1280
powerMeterScalingFactor = 0.875

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
isTargetSub1 = 0
isTargetSub2 = 0
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
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','crosshair.png')), (int(tile), int(tile))), (self.pos.x - playScreenWidth, self.pos.y - playScreenHeight))
    def drawCurser2(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','crosshair.png')), (int(tile), int(tile))), (self.pos.x + playScreenWidth, self.pos.y - playScreenHeight))

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
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','bulletHole.png')), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class for distress calls
class distressCall(Rectangle):
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','distressSignal.png')), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class for hit markers
class HitMarker:
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','missTile.png')), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class for miss markers
class MissMarker:
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','hitTile.png')), (int(tile), int(tile))), (self.pos.x, self.pos.y))

# class for miss markers
class HighLight:
    def __init__(self, color, x, y, width, height):
        Rectangle.__init__(self, color, x, y, width, height)

    def draw(self):
        win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','highlightTile.png')), (int(tile), int(tile))), (self.pos.x, self.pos.y))

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
    highLightSprite = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','highlightTile.png')), (int(tile), int(tile)))
    warningSub = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','SubWarning.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    hitMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','YouHitAShip.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    missMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','YouMissedAShip.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    alreadyHitMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','AlreadyHitThat.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    subDestroyedMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','SubWasDestroyed.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    subUnderShip = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','SubUnderShip.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    luckyUsMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','justEnoughCharge.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    notEnoughMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','notEnoughCharge.png')), (int(tile*8 + 12), int(tile*4 + 12)))

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

    warningCounter1 = 0
    warningCounter2 = 0

    hitMessage1 = False
    hitMessage2 = False

    missMessage1 = False
    missMessage2 = False

    alreadyHitMessage1 = False
    alreadyHitMessage2 = False

    subDestroyedMessage1 = False
    subDestroyedMessage2 = False

    subUnderShip1 = False
    subUnderShip2 = False
    subUnderShipCounter1 = 0
    subUnderShipCounter2 = 0

    luckyUsMessage1 = False
    luckyUsMessage2 = False
    luckyUsMessageCounter1 = 0
    luckyUsMessageCounter2 = 0

    notEnoughMessage1 = False
    notEnoughMessage2 = False
    notEnoughMessageCounter1 = 0
    notEnoughMessageCounter2 = 0


####### Functions ########

# updates image/screen
def update():
    win.fill((0,0,0))

    # draws sonar background
    win.blit(Sprite.sonarBackground, (sideMargin, topBotMargin))
    win.blit(Sprite.sonarBackground, (sideMargin + playScreenWidth, topBotMargin))
    # draws distress calls
    if (myClock//5)% 5:
        for key, val in distressCalls.items():
            distressCalls[key].draw()

    #if pinPointPulse1:
    #    win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','distressSignal.png')), (int(tile), int(tile))), (shipDic1[pinPointPulse1].pos.x, shipDic1[pinPointPulse1].pos.y))
    #if pinPointPulse2:
    #    win.blit(pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','distressSignal.png')), (int(tile), int(tile))), (shipDic1[pinPointPulse2].pos.x, shipDic1[pinPointPulse2].pos.y))

    win.blit(Sprite.gridSonar, (sideMargin - 1, topBotMargin - 1))
    win.blit(Sprite.gridSonar, (sideMargin + playScreenWidth - 1, topBotMargin - 1))

    # draws all ship damage sprites
    for key, val in highLightMarkers.items():
        highLightMarkers[key].draw()

    # draws red sonar before the ocean map, so you can't see it one the ocean
    if not(playerTurn == 1) and not(subSink2):
        sonarDisplay1[0].drawSonarMap()
    if not(playerTurn == 2) and not(subSink1):
        sonarDisplay2[0].drawSonarMap()

    # draws ocean background
    oceanAnimation()
    win.blit(Sprite.grid, (sideMargin - 1, topBotMargin + playScreenHeight - 1))
    win.blit(Sprite.grid, (sideMargin + playScreenWidth - 1, topBotMargin + playScreenHeight - 1))

    # gets the average distance from sonar orgin to ship
    averageDist()

    # draw submarine
    # sub 1
    if subSink2 == False:
        win.blit(Sprite.sub, (sonarPos1.x - tile/2 + playScreenWidth, sonarPos1.y - tile/2 - playScreenHeight))
    # sub 2
    if subSink1 == False:
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

    # draws warning message for sonar targeting
    if isTargetSub1 and (myClock//5)%5:
        Sprite.warningCounter1 += 1
        if Sprite.warningCounter1 < 50:
            win.blit(Sprite.warningSub, (sideMargin + tile - 6, topBotMargin + tile - 6))
    if isTargetSub2 and (myClock//5)%5:
        Sprite.warningCounter2 += 1
        if Sprite.warningCounter2 < 50:
            win.blit(Sprite.warningSub, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
    
    # draws ship hit message
    if Sprite.hitMessage1 and not(playerTurn):
        win.blit(Sprite.hitMessage, (sideMargin + tile - 6, topBotMargin + tile - 6))
    if whatOtherPlayer() == 1:
        Sprite.hitMessage1 = False
    if Sprite.hitMessage2 and not(playerTurn):
        win.blit(Sprite.hitMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
    if whatOtherPlayer() == 2:
        Sprite.hitMessage2 = False

    # draws ship miss message
    if Sprite.missMessage1 and not(playerTurn):
        win.blit(Sprite.missMessage, (sideMargin + tile - 6, topBotMargin + tile - 6))
    if whatOtherPlayer() == 1:
        Sprite.missMessage1 = False
    if Sprite.missMessage2 and not(playerTurn):
        win.blit(Sprite.missMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
    if whatOtherPlayer() == 2:
        Sprite.missMessage2 = False

    # draws ship already hit message
    if Sprite.alreadyHitMessage1 and not(playerTurn):
        win.blit(Sprite.alreadyHitMessage, (sideMargin + tile - 6, topBotMargin + tile - 6))
    if whatOtherPlayer() == 1:
        Sprite.alreadyHitMessage1 = False
    if Sprite.alreadyHitMessage2 and not(playerTurn):
        win.blit(Sprite.alreadyHitMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
    if whatOtherPlayer() == 2:
        Sprite.alreadyHitMessage2 = False

    # draws ship already hit message
    if Sprite.subDestroyedMessage1 and not(playerTurn):
        win.blit(Sprite.subDestroyedMessage, (sideMargin + tile - 6, topBotMargin + tile - 6))
    if whatOtherPlayer() == 2:
        Sprite.subDestroyedMessage1 = False
    if Sprite.subDestroyedMessage2 and not(playerTurn):
        win.blit(Sprite.subDestroyedMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
    if whatOtherPlayer() == 1:
        Sprite.subDestroyedMessage2 = False

    # draws warning message for sub under ship targeting
    if Sprite.subUnderShip1:
        win.blit(Sprite.highLightSprite, (sonarPos2.x - tile/2 - playScreenWidth, sonarPos2.y - tile/2 - playScreenHeight))
        Sprite.subUnderShipCounter1 += 1
        if Sprite.subUnderShipCounter1 < 50:
            win.blit(Sprite.subUnderShip, (sideMargin + tile - 6, topBotMargin + tile - 6))
    if Sprite.subUnderShip2:
        win.blit(Sprite.highLightSprite, (sonarPos1.x - tile/2 + playScreenWidth, sonarPos1.y - tile/2 - playScreenHeight))
        Sprite.subUnderShipCounter2 += 1
        if Sprite.subUnderShipCounter2 < 50:
            win.blit(Sprite.subUnderShip, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))

    # draws 'lucky us' message
    if Sprite.luckyUsMessage1:
        win.blit(Sprite.luckyUsMessage, (sideMargin + tile - 6, topBotMargin + tile - 6))
        Sprite.luckyUsMessageCounter1 += 1
        if Sprite.luckyUsMessageCounter1 > 50:
            Sprite.luckyUsMessageCounter1 = 0
            Sprite.luckyUsMessage1 = False
    if Sprite.luckyUsMessage2:
        win.blit(Sprite.luckyUsMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
        Sprite.luckyUsMessageCounter2 += 1
        if Sprite.luckyUsMessageCounter2 > 50:
            Sprite.luckyUsMessageCounter2 = 0
            Sprite.luckyUsMessage2 = False
    
    # draws 'not enough sonar charge' message
    if Sprite.notEnoughMessage1:
        win.blit(Sprite.notEnoughMessage, (sideMargin + tile - 6, topBotMargin + tile - 6))
        Sprite.notEnoughMessageCounter1 += 1
        if Sprite.notEnoughMessageCounter1 > 50:
            Sprite.notEnoughMessageCounter1 = 0
            Sprite.notEnoughMessage1 = False
    if Sprite.notEnoughMessage2:
        win.blit(Sprite.notEnoughMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin + tile - 6))
        Sprite.notEnoughMessageCounter2 += 1
        if Sprite.notEnoughMessageCounter2 > 50:
            Sprite.notEnoughMessageCounter2 = 0
            Sprite.notEnoughMessage2 = False

    # draws all sonar beams
    for key, value in sonarDic1.items():
        sonarDic1[key].draw()
    for key, value in sonarDic2.items():
        sonarDic2[key].draw()

    # draws the sonar power meter
    # background of meter
    win.blit(Sprite.sonarPowerMeter, (playScreen + 1.1*sideMargin, topBotMargin*1.5))
    win.blit(Sprite.sonarPowerMeter, (playScreen + 1.1*sideMargin + playScreenWidth, topBotMargin*1.5))
    # black bar that covers up background of meter
    sonarMeter1.draw()
    sonarMeter2.draw()

    # draws the sonar charge/battery bar
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
    global gamePhase
    global sonarDic1
    global sonarDic2

    # reset sonar dictionary
    sonarDic1 = {}
    sonarDic2 = {}
    sonarDisplay1 = []
    sonarDisplay2 = []
    # get the aim of the sonar
    if gamePhase == "sonar":
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

    createSonarPowerMeter(sonarRange1, sonarRange2)
    # returns dictionary of all the lines
    return sonarDic1, sonarDic2

# creates sonar power level meter
def createSonarPowerMeter(sonarRange1, sonarRange2):
    global sonarMeter1
    global sonarMeter2
    sonarMeter1 = Rectangle((0,0,0), playScreen + 1.1*sideMargin, topBotMargin*2, 0.8*sideMargin, playScreen*0.9 - sonarRange2*powerMeterScalingFactor)
    sonarMeter2 = Rectangle((0,0,0), playScreen + 1.1*sideMargin + playScreenWidth, topBotMargin*2, 0.8*sideMargin, playScreen*0.9 - sonarRange1*powerMeterScalingFactor)

# pulse sonar to give game sense of ships around
def pulseSonar():
    global sonarRange1
    global sonarRange2
    global sonarCharge1
    global sonarCharge2
    global gamePhase
    global pinPointPulse1
    global pinPointPulse2

    # check it under ship
    isSubUnderShip()
    # i guess put sounds here or maybe in a seperate function
    # implement sonar charge
    if playerTurn == 1:
        tempSonarCharge1 = sonarCharge1
        tempSonarCharge1 -= sonarRange2     # sonarRange# are switch to fixed some previous swap
        if tempSonarCharge1 >= 0:
            sonarCharge1 = tempSonarCharge1
        elif sonarRange2 < tile and tempSonarCharge1 < 0:
            Sprite.luckyUsMessage1 = True
            print("Low on charge, but I'll give you this one!")
            sonarCharge1 = 0
        elif tempSonarCharge1 < 0:
            Sprite.notEnoughMessage1 = True
            Sprite.subUnderShip1 = False
            print("Not Enough Sonar Charge")
            gamePhase = "sonar"


    if playerTurn == 2:
        tempSonarCharge2 = sonarCharge2
        tempSonarCharge2 -= sonarRange1     # sonarRange# are switch to fixed some previous swap
        if tempSonarCharge2 >= 0:
            sonarCharge2 = tempSonarCharge2
        elif sonarRange1 < tile and tempSonarCharge2 < 0:
            Sprite.luckyUsMessage2 = True
            print("Low on charge, but I'll give you this one!")
            sonarCharge2 = 0
        elif tempSonarCharge2 < 0:
            Sprite.notEnoughMessage2 = True
            Sprite.subUnderShip2 = False
            print("Not Enough Sonar Charge")
            gamePhase = "sonar"

    # update sonar charge meter
    createSonarChargeMeter()

    #if len(sonarDic1) == 1:                          #######################################################
    #    for key, item in shipDic1.items():
    #        print(shipDic1[key].sonarHitNum)
    #        if shipDic1[key].sonarHitNum:
    #            print("frog")
    #            pinPointPulse1 = key
    #if len(sonarDic2) == 1:
    #    for key, item in shipDic2.items():
    #        if shipDic2[key].sonarHitNum:
    #            print("frog")
    #            pinPointPulse2 = key

# creates and updates sonar charge meter
def createSonarChargeMeter():
    global sonarCharge1
    global sonarCharge2
    global sonarChargeMeter1
    global sonarChargeMeter2
    # doesn't let sonarCharge get above the max sonar charge
    if sonarCharge1 > MAXSONARCHARGE:
        sonarCharge1 = MAXSONARCHARGE
    if sonarCharge2 > MAXSONARCHARGE:
        sonarCharge1 = MAXSONARCHARGE
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
    global subSink1
    global subSink2
    global sonarCharge1
    global sonarCharge2

    shoooted = True
    player1End = False
    player2End = False
    Sprite.subUnderShip1 = False
    Sprite.subUnderShip2 = False
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
            Sprite.hitMessage1 = True
            sonarCharge1 += MAXSONARCHARGE/rechargePercent
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
                Sprite.missMessage1 = True
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                Sprite.alreadyHitMessage1 = True
                print("Player 1, you already damaged that part!")
                print("~~~~~~~~")

    if playerTurn == 2:
        # for explosion animation
        playerShot2 = True
        # end turn
        player2End = True
        if isCollides[0] and damageTest2:
            sonarCharge2 += MAXSONARCHARGE/rechargePercent
            Sprite.hitMessage2 = True
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
            if damageTest2:
                Sprite.missMessage2 = True
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                Sprite.alreadyHitMessage2 = True
                print("Player 2, you already damaged that part!")
                print("~~~~~~~~")

    # is a sub sunk
    isSubSunk()
    # sub hit causation
    if isTargetSub1:
        print("frog1")
        subSink1 = True
    if isTargetSub2:
        print("frog2")
        subSink2 = True

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
            sink(key , 1)
            deadShip1 = key

    for key, items in shipDic2.items():
        if not(shipDic2[key].health):
            print("You got one!!")
            print("~~~~~~~~")
            sink(key , 2)
            deadShip2 = key
    # deletes ship thats been sunk
    if deadShip1:
        del shipDic1[deadShip1]
    # deletes ship thats been sunk
    if deadShip2:
        del shipDic2[deadShip2]

# is ship is sunken, then remove it and the shipDamage
def sink(ship, shipsPlayer):
    global shipDic1
    global shipDic2
    global shipDamages
    global highLightMarkers

    delShipDamages = []

    # deletes shipDamage sprites that are on sunken ship
    if shipsPlayer == 1:
        for key, val in shipDamages.items():
            if pygame.Rect.colliderect(pygame.Rect(shipDamages[key].pos.x, shipDamages[key].pos.y, shipDamages[key].width, shipDamages[key].height), shipDic1[ship].rect):
                highLightMarkers["highLight%s" %len(highLightMarkers)] = HighLight((0,255,0), shipDamages[key].pos.x + playScreenWidth, shipDamages[key].pos.y - playScreenHeight, tile, tile)
                delShipDamages.append(key)
    
    if shipsPlayer == 2:
        for key, val in shipDamages.items():
            if pygame.Rect.colliderect(pygame.Rect(shipDamages[key].pos.x, shipDamages[key].pos.y, shipDamages[key].width, shipDamages[key].height), shipDic2[ship].rect):
                highLightMarkers["highLight%s" %len(highLightMarkers)] = HighLight((0,255,0), shipDamages[key].pos.x - playScreenWidth, shipDamages[key].pos.y - playScreenHeight, tile, tile)
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

# gives other player
def whatOtherPlayer():
    if playerTurn == 1:
        return 2
    elif playerTurn == 2:
        return 1
    else:
        return 0

# detects if ship is in distress
def isDistressed():
    global isDisplayingDistress
    global sonarCharge1
    global sonarCharge2
    global distressCalls
    global tempPlayerTurn
    global shoooted

    otherPlayer = whatOtherPlayer()

    if not(sonarCharge1) and isDisplayingDistress == 0 and tempPlayerTurn != playerTurn and playerTurn != 0:
        isDisplayingDistress = 1
        shipDistress(1)
    if not(sonarCharge2) and isDisplayingDistress == 0 and tempPlayerTurn != playerTurn and playerTurn != 0:
        isDisplayingDistress = 1
        shipDistress(2)

    #print("OtherPLayer: {}\tShoooted: {}" .format(otherPlayer, shoooted))
    if otherPlayer == 1 and shoooted and sonarCharge1 == 0:
        sonarCharge1 = MAXSONARCHARGE
        distressCalls = {}
        isDisplayingDistress = 0
    if otherPlayer == 2 and shoooted and sonarCharge2 == 0:#####################################
        sonarCharge2 = MAXSONARCHARGE
        distressCalls = {}
        isDisplayingDistress = 0

    shoooted = False
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
    global shipDic1
    global shipDic2
    global run
    global playerTurn
    global missMarkers
    global hitMarkers
    global shipDamages
    global shoooted
    global gamePhase

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
    if key[pygame.K_SPACE] and isPress_SPACE == 0 and playerTurn and gamePhase == "shoot":
        gamePhase = "sonar"
        isPress_SPACE = 1
        shootMissile()
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_SPACE]):
        isPress_SPACE = 0

    # shoot sonar
    if key[pygame.K_p] and isPress_p == 0 and gamePhase == "sonar":
        gamePhase = "shoot"
        pulseSonar()
        isPress_p = 1
    if not(key[pygame.K_p]):
        isPress_p = 0

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

    # curser1 movement is in it's own class function
    if gamePhase == "shoot":
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

# detects if sub is being targeted by curser and showing player that it's bad
def isSubTargeted():
    global isTargetSub1
    global isTargetSub2
    global gamePhase

    if pygame.Rect.colliderect(pygame.Rect(curser1.pos.x, curser1.pos.y, curser1.width, curser1.height), pygame.Rect((sonarPos2.x - tile/2), (sonarPos2.y - tile/2), curser1.width, curser1.height)) and isTargetSub1 == 0:
        isTargetSub1 = 1
    if not(pygame.Rect.colliderect(pygame.Rect(curser1.pos.x, curser1.pos.y, curser1.width, curser1.height), pygame.Rect((sonarPos2.x - tile/2), (sonarPos2.y - tile/2), curser1.width, curser1.height))):
        Sprite.warningCounter1 = 0
        isTargetSub1 = 0

    if pygame.Rect.colliderect(pygame.Rect(curser2.pos.x, curser2.pos.y, curser2.width, curser2.height), pygame.Rect((sonarPos1.x - tile/2), (sonarPos1.y - tile/2), curser2.width, curser2.height)) and isTargetSub2 == 0:
        isTargetSub2 = 1
    if not(pygame.Rect.colliderect(pygame.Rect(curser2.pos.x, curser2.pos.y, curser2.width, curser2.height), pygame.Rect((sonarPos1.x - tile/2), (sonarPos1.y - tile/2), curser2.width, curser2.height))):
        Sprite.warningCounter2 = 0
        isTargetSub2 = 0

    if subSink1 and whatOtherPlayer() == 2 and playerTurn != tempPlayerTurn:
        print("frogger1")
        gamePhase = "shoot"
    if subSink2 and whatOtherPlayer() == 1 and playerTurn != tempPlayerTurn:
        print("frogger2")
        gamePhase = "shoot"

# detects if sub should be sunk and then punishes for it
def isSubSunk():
    global subSinkPunish1
    global subSinkPunish2
    global subSink1
    global subSink2

    if subSink1:
        Sprite.subDestroyedMessage1 = True
        subSinkPunish1 += 1
    if subSink2:
        Sprite.subDestroyedMessage2 = True
        subSinkPunish2 += 1

    if subSinkPunish1 >= subPunishLevel*2 and whatOtherPlayer() == 1:
        Sprite.subDestroyedMessage1 = False
        subSinkPunish1 = 0
        subSink1 = False
    if subSinkPunish2 >= subPunishLevel*2 and whatOtherPlayer() == 2:
        Sprite.subDestroyedMessage2 = False
        subSinkPunish2 = 0
        subSink2 = False

# checks if sub is under ship
def isSubUnderShip():
    if playerTurn == 1:
        for key, val in shipDic2.items():
            if pygame.Rect.colliderect(pygame.Rect((sonarPos2.x - tile/2), (sonarPos2.y - tile/2), curser1.width, curser1.height), shipDic2[key].rect):
                Sprite.subUnderShip1 = True
            else:
                Sprite.subUnderShip1 = False
                Sprite.subUnderShipCounter1 = 0

    if playerTurn == 2:
        for key, val in shipDic1.items():
            if pygame.Rect.colliderect(pygame.Rect((sonarPos1.x - tile/2), (sonarPos1.y - tile/2), curser1.width, curser1.height), shipDic1[key].rect):
                Sprite.subUnderShip2 = True
            else:
                Sprite.subUnderShip2 = False
                Sprite.subUnderShipCounter2 = 0

# plays background water sounds
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

      
# default player stuff
playerTurn = 1
player1End = False
player2End = True
playerCount = 0
playerTrigger = 0
playerShot1 = False
playerShot2 = False
tempPlayerTurn = 0
shoooted = False
pinPointPulse1 = 0
pinPointPulse2 = 0
gamePhase = "sonar"

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
highLightMarkers = {}

# Default sonar 
sonarDic1 = {}
sonarDic2 = {}
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
subSink1 = False
subSink2 = False
subSinkPunish1 = 0
subSinkPunish2 = 0
subPunishLevel = 1
warningCounter1 = 0
warningCounter2 = 0
# default sonar charge amount
MAXSONARCHARGE = 700
sonarCharge1 = MAXSONARCHARGE
sonarCharge2 = MAXSONARCHARGE
rechargePercent = 0.25   # how much the sonar battery recharges when a ship is hit
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
    # controls rate of the game
    clock.tick(frameRate)
    #calls water sound playback and maintains fade loop
    waterSound(run, waterClock, waterS_array, ch_water, ch_waterBuffer)
    # dectects inputs from all sources
    detectInputs(numShip)
    # sonar targeted?
    isSubTargeted()
    # sonar iteration
    createSonarChargeMeter()
    sonarDicUnpacker = createSonar(playerTurn)
    sonarDic1 = sonarDicUnpacker[0]
    sonarDic2 = sonarDicUnpacker[1]
    #ship distress detection
    isDistressed()
    # is there a sunken ship
    isSunk()
    # updates screen
    update()
    # desides player turn
    if playerTrigger:
        isPlayerTurn()
    # did win
    isWin()


# if main loop is broke then close program
pygame.quit()


