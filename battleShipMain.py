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
#screenHeight = 1280
#screenWidth = 720
screenHeight = 640
screenWidth = 360
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
ch_buttonSounds = pygame.mixer.Channel(7)

#   -Water Sounds
#all water sounds are 5400 frames long (at 60FPS)

#boost below sounds volume in logic
water1 = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'water1.wav'))
water2 = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'water2.wav'))
water3 = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'water3.wav'))
waterS_array = [water1, water2, water3]
#   -Ship Themes
th_destroyerSimple = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_destroyerSimple.wav'))
th_carrierSimple = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_carrierSimple.wav'))
th_cruiser1Simple = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_cruiser1Simple.wav'))
th_cruiser2Simple = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_cruiser2Simple.wav'))
th_battleshipSimple = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_battleshipSimple.wav'))
th_destroyerIntense = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_destroyerIntense.wav'))
th_carrierIntense = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_carrierIntense.wav'))
th_cruiser1Intense = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_cruiser1Intense.wav'))
th_cruiser2Intense = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_cruiser2Intense.wav'))
th_battleshipIntense = pygame.mixer.Sound(os.path.join('Ship Themes (wav) copy', 'th_battleshipIntense1.wav'))
#   -UI Sounds
num_letter_button1 = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'num_letter_button1.wav'))
num_letter_button2 = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'num_letter_button2.wav'))
num_letter_button3 = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'num_letter_button3.wav'))
buttonS_array = [num_letter_button1, num_letter_button2, num_letter_button3]
NOSHIPSDETECTED = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'NOSHIPS.wav'))
missile_hit = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'missile_hit.wav'))
missile_miss = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'missile_miss.wav'))
distressBeaconLight = pygame.mixer.Sound(os.path.join('UI Sounds (wav)', 'distressBeaconLight.wav'))


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
        self.length = health
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
        global buttonS_array


        # detecting key presses
        keys = pygame.key.get_pressed()

        # sets trigger var to true
        if keys[pygame.K_1] and isPress_coord_1:
            num_letter_buttonSound()
            isPress_coord_1 = 0
            isPress_displayCoords = 1
            targetCoords.append(1)
        if not(keys[pygame.K_1]):
            isPress_coord_1 = 1
        if keys[pygame.K_2] and isPress_coord_2:
            num_letter_buttonSound()
            isPress_coord_2 = 0
            isPress_displayCoords = 1
            targetCoords.append(2)
        if not(keys[pygame.K_2]):
            isPress_coord_2 = 1
        if keys[pygame.K_3] and isPress_coord_3:
            num_letter_buttonSound()
            isPress_coord_3 = 0
            isPress_displayCoords = 1
            targetCoords.append(3)
        if not(keys[pygame.K_3]):
            isPress_coord_3 = 1
        if keys[pygame.K_4] and isPress_coord_4:
            num_letter_buttonSound()
            isPress_coord_4 = 0
            isPress_displayCoords = 1
            targetCoords.append(4)
        if not(keys[pygame.K_4]):
            isPress_coord_4 = 1
        if keys[pygame.K_5] and isPress_coord_5:
            num_letter_buttonSound()
            isPress_coord_5 = 0
            isPress_displayCoords = 1
            targetCoords.append(5)
        if not(keys[pygame.K_5]):
            isPress_coord_5 = 1
        if keys[pygame.K_6] and isPress_coord_6:
            num_letter_buttonSound()
            isPress_coord_6 = 0
            isPress_displayCoords = 1
            targetCoords.append(6)
        if not(keys[pygame.K_6]):
            isPress_coord_6 = 1
        if keys[pygame.K_7] and isPress_coord_7:
            num_letter_buttonSound()
            isPress_coord_7 = 0
            isPress_displayCoords = 1
            targetCoords.append(7)
        if not(keys[pygame.K_7]):
            isPress_coord_7 = 1
        if keys[pygame.K_8] and isPress_coord_8:
            num_letter_buttonSound()
            isPress_coord_8 = 0
            isPress_displayCoords = 1
            targetCoords.append(8)
        if not(keys[pygame.K_8]):
            isPress_coord_8 = 1
        if keys[pygame.K_9] and isPress_coord_9:
            num_letter_buttonSound()
            isPress_coord_9 = 0
            isPress_displayCoords = 1
            targetCoords.append(9)
        if not(keys[pygame.K_9]):
            isPress_coord_9 = 1
        if keys[pygame.K_0] and isPress_coord_0:
            num_letter_buttonSound()
            isPress_coord_0 = 0
            isPress_displayCoords = 1
            targetCoords.append(0)
        if not(keys[pygame.K_0]):
            isPress_coord_0 = 1
        if keys[pygame.K_a] and isPress_coord_A:
            num_letter_buttonSound()
            isPress_coord_A = 0
            isPress_displayCoords = 1
            targetCoords.append('A')
        if not(keys[pygame.K_a]):
            isPress_coord_A = 1
        if keys[pygame.K_b] and isPress_coord_B:
            num_letter_buttonSound()
            isPress_coord_B = 0
            isPress_displayCoords = 1
            targetCoords.append('B')
        if not(keys[pygame.K_b]):
            isPress_coord_B = 1
        if keys[pygame.K_c] and isPress_coord_C:
            num_letter_buttonSound()
            isPress_coord_C = 0
            isPress_displayCoords = 1
            targetCoords.append('C')
        if not(keys[pygame.K_c]):
            isPress_coord_C = 1
        if keys[pygame.K_d] and isPress_coord_D:
            num_letter_buttonSound()
            isPress_coord_D = 0
            isPress_displayCoords = 1
            targetCoords.append('D')
        if not(keys[pygame.K_d]):
            isPress_coord_D = 1
        if keys[pygame.K_e] and isPress_coord_E:
            num_letter_buttonSound()
            isPress_coord_E = 0
            isPress_displayCoords = 1
            targetCoords.append('E')
        if not(keys[pygame.K_e]):
            isPress_coord_E = 1
        if keys[pygame.K_f] and isPress_coord_F:
            num_letter_buttonSound()
            isPress_coord_F = 0
            isPress_displayCoords = 1
            targetCoords.append('F')
        if not(keys[pygame.K_f]):
            isPress_coord_F = 1
        if keys[pygame.K_g] and isPress_coord_G:
            num_letter_buttonSound()
            isPress_coord_G = 0
            isPress_displayCoords = 1
            targetCoords.append('G')
        if not(keys[pygame.K_g]):
            isPress_coord_G = 1
        if keys[pygame.K_h] and isPress_coord_H:
            num_letter_buttonSound()
            isPress_coord_H = 0
            isPress_displayCoords = 1
            targetCoords.append('H')
        if not(keys[pygame.K_h]):
            isPress_coord_H = 1
        if keys[pygame.K_i] and isPress_coord_I:
            num_letter_buttonSound()
            isPress_coord_I = 0
            isPress_displayCoords = 1
            targetCoords.append('I')
        if not(keys[pygame.K_i]):
            isPress_coord_I = 1
        if keys[pygame.K_j] and isPress_coord_J:
            num_letter_buttonSound()
            isPress_coord_J = 0
            isPress_displayCoords = 1
            targetCoords.append('J')
        if not(keys[pygame.K_j]):
            isPress_coord_J = 1

        targetCoords_cut = targetCoords[0:2]

        if isPress_displayCoords:
            isPress_displayCoords = 0
            print(targetCoords_cut)

        coordPass = False
        # confirmation buttom
        if len(targetCoords_cut) == 2:
            if isinstance(targetCoords_cut[0],str) and isinstance(targetCoords_cut[1],str):
                print("You must enter coordinates in form: '(0,A)' or '(A,0)'")
                coord_1 = False
                coord_2 = False
                coord_3 = False
                coord_4 = False
                coord_5 = False
                coord_6 = False
                coord_7 = False
                coord_8 = False
                coord_9 = False
                coord_0 = False
                coord_A = False
                coord_B = False
                coord_C = False
                coord_D = False
                coord_E = False
                coord_F = False
                coord_G = False
                coord_H = False
                coord_I = False
                coord_J = False
                coordPass = False
            elif isinstance(targetCoords_cut[0],int) and isinstance(targetCoords_cut[1],int):
                print("You must enter coordinates in form: '(0,A)' or '(A,0)'")
                coord_1 = False
                coord_2 = False
                coord_3 = False
                coord_4 = False
                coord_5 = False
                coord_6 = False
                coord_7 = False
                coord_8 = False
                coord_9 = False
                coord_0 = False
                coord_A = False
                coord_B = False
                coord_C = False
                coord_D = False
                coord_E = False
                coord_F = False
                coord_G = False
                coord_H = False
                coord_I = False
                coord_J = False
                coordPass = False
            else:
                print("Curser in position")
                if 1 in targetCoords_cut:
                    coord_1 = True
                if 2 in targetCoords_cut:
                    coord_2 = True
                if 3 in targetCoords_cut:
                    coord_3 = True
                if 4 in targetCoords_cut:
                    coord_4 = True
                if 5 in targetCoords_cut:
                    coord_5 = True
                if 6 in targetCoords_cut:
                    coord_6 = True
                if 7 in targetCoords_cut:
                    coord_7 = True
                if 8 in targetCoords_cut:
                    coord_8 = True
                if 9 in targetCoords_cut:
                    coord_9 = True
                if 0 in targetCoords_cut:
                    coord_0 = True
                if 'A' in targetCoords_cut:
                    coord_A = True
                if 'B' in targetCoords_cut:
                    coord_B = True
                if 'C' in targetCoords_cut:
                    coord_C = True
                if 'D' in targetCoords_cut:
                    coord_D = True
                if 'E' in targetCoords_cut:
                    coord_E = True
                if 'F' in targetCoords_cut:
                    coord_F = True
                if 'G' in targetCoords_cut:
                    coord_G = True
                if 'H' in targetCoords_cut:
                    coord_H = True
                if 'I' in targetCoords_cut:
                    coord_I = True
                if 'J' in targetCoords_cut:
                    coord_J = True
                if 'K' in targetCoords_cut:
                    coord_K = True
                coordPass = True
            targetCoords = []

        if playerTurn == 1:
            # moves curser1 to coords
            # row 1
            if coord_1 and coord_A:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_1 and coord_B:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_1 and coord_C:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_1 = 0
                coord_C = 0
            if coord_1 and coord_D:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_1 = 0
                coord_D = 0
            if coord_1 and coord_E:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_1 = 0
                coord_E = 0
            if coord_1 and coord_F:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_1 = 0
                coord_F = 0
            if coord_1 and coord_G:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_1 = 0
                coord_G = 0
            if coord_1 and coord_H:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_1 = 0
                coord_H = 0
            if coord_1 and coord_I:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_1 = 0
                coord_I = 0
            if coord_1 and coord_J:
                mapPosx = sideMargin + tile*0 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_1 = 0
                coord_J = 0
            # row 2
            if coord_2 and coord_A:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_2 = 0
                coord_A = 0
            if coord_2 and coord_B:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_2 = 0
                coord_B = 0
            if coord_2 and coord_C:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_2 = 0
                coord_C = 0
            if coord_2 and coord_D:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_2 = 0
                coord_D = 0
            if coord_2 and coord_E:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_2 = 0
                coord_E = 0
            if coord_2 and coord_F:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_2 = 0
                coord_F = 0
            if coord_2 and coord_G:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_2 = 0
                coord_G = 0
            if coord_2 and coord_H:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_2 = 0
                coord_H = 0
            if coord_2 and coord_I:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_2 = 0
                coord_I = 0
            if coord_2 and coord_J:
                mapPosx = sideMargin + tile*1 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_2 = 0
                coord_J = 0
            # row 3
            if coord_3 and coord_A:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_3 = 0
                coord_A = 0
            if coord_3 and coord_B:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_3 = 0
                coord_B = 0
            if coord_3 and coord_C:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_3 = 0
                coord_C = 0
            if coord_3 and coord_D:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_3 = 0
                coord_D = 0
            if coord_3 and coord_E:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_3 = 0
                coord_E = 0
            if coord_3 and coord_F:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_3 = 0
                coord_F = 0
            if coord_3 and coord_G:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_3 = 0
                coord_G = 0
            if coord_3 and coord_H:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_3 = 0
                coord_H = 0
            if coord_3 and coord_I:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_3 = 0
                coord_I = 0
            if coord_3 and coord_J:
                mapPosx = sideMargin + tile*2 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_3 = 0
                coord_J = 0
            # row 4
            if coord_4 and coord_A:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_4 = 0
                coord_A = 0
            if coord_4 and coord_B:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_4 = 0
                coord_B = 0
            if coord_4 and coord_C:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_4 = 0
                coord_C = 0
            if coord_4 and coord_D:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_4 = 0
                coord_D = 0
            if coord_4 and coord_E:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_4 = 0
                coord_E = 0
            if coord_4 and coord_F:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_4 = 0
                coord_F = 0
            if coord_4 and coord_G:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_4 = 0
                coord_G = 0
            if coord_4 and coord_H:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_4 = 0
                coord_H = 0
            if coord_4 and coord_I:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_4 = 0
                coord_I = 0
            if coord_4 and coord_J:
                mapPosx = sideMargin + tile*3 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_4 = 0
                coord_J = 0
            # row 5
            if coord_5 and coord_A:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_5 = 0
                coord_A = 0
            if coord_5 and coord_B:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_5 = 0
                coord_B = 0
            if coord_5 and coord_C:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_5 = 0
                coord_C = 0
            if coord_5 and coord_D:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_5 = 0
                coord_D = 0
            if coord_5 and coord_E:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_5 = 0
                coord_E = 0
            if coord_5 and coord_F:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_5 = 0
                coord_F = 0
            if coord_5 and coord_G:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_5 = 0
                coord_G = 0
            if coord_5 and coord_H:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_5 = 0
                coord_H = 0
            if coord_5 and coord_I:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_5 = 0
                coord_I = 0
            if coord_5 and coord_J:
                mapPosx = sideMargin + tile*4 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_5 = 0
                coord_J = 0
            # row 6
            if coord_6 and coord_A:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_6 = 0
                coord_A = 0
            if coord_6 and coord_B:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_6 = 0
                coord_B = 0
            if coord_6 and coord_C:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_6 = 0
                coord_C = 0
            if coord_6 and coord_D:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_6 = 0
                coord_D = 0
            if coord_6 and coord_E:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_6 = 0
                coord_E = 0
            if coord_6 and coord_F:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_6 = 0
                coord_F = 0
            if coord_6 and coord_G:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_6 = 0
                coord_G = 0
            if coord_6 and coord_H:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_6 = 0
                coord_H = 0
            if coord_6 and coord_I:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_6 = 0
                coord_I = 0
            if coord_6 and coord_J:
                mapPosx = sideMargin + tile*5 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_6 = 0
                coord_J = 0
            # row 7
            if coord_7 and coord_A:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_7 = 0
                coord_A = 0
            if coord_7 and coord_B:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_7 = 0
                coord_B = 0
            if coord_7 and coord_C:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_7 = 0
                coord_C = 0
            if coord_7 and coord_D:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_7 = 0
                coord_D = 0
            if coord_7 and coord_E:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_7 = 0
                coord_E = 0
            if coord_7 and coord_F:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_7 = 0
                coord_F = 0
            if coord_7 and coord_G:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_7 = 0
                coord_G = 0
            if coord_7 and coord_H:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_7 = 0
                coord_H = 0
            if coord_7 and coord_I:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_7 = 0
                coord_I = 0
            if coord_7 and coord_J:
                mapPosx = sideMargin + tile*6 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_7 = 0
                coord_J = 0
            # row 8
            if coord_8 and coord_A:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_8 = 0
                coord_A = 0
            if coord_8 and coord_B:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_8 = 0
                coord_B = 0
            if coord_8 and coord_C:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_8 = 0
                coord_C = 0
            if coord_8 and coord_D:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_8 = 0
                coord_D = 0
            if coord_8 and coord_E:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_8 = 0
                coord_E = 0
            if coord_8 and coord_F:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_8 = 0
                coord_F = 0
            if coord_8 and coord_G:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_8 = 0
                coord_G = 0
            if coord_8 and coord_H:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_8 = 0
                coord_H = 0
            if coord_8 and coord_I:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_8 = 0
                coord_I = 0
            if coord_8 and coord_J:
                mapPosx = sideMargin + tile*7 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_8 = 0
                coord_J = 0
            # row 9
            if coord_9 and coord_A:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_9 = 0
                coord_A = 0
            if coord_9 and coord_B:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_9 = 0
                coord_B = 0
            if coord_9 and coord_C:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_9 = 0
                coord_C = 0
            if coord_9 and coord_D:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_9 = 0
                coord_D = 0
            if coord_9 and coord_E:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_9 = 0
                coord_E = 0
            if coord_9 and coord_F:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_9 = 0
                coord_F = 0
            if coord_9 and coord_G:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_9 = 0
                coord_G = 0
            if coord_9 and coord_H:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_9 = 0
                coord_H = 0
            if coord_9 and coord_I:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_9 = 0
                coord_I = 0
            if coord_9 and coord_J:
                mapPosx = sideMargin + tile*8 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_9 = 0
                coord_J = 0
            # row 10
            if coord_0 and coord_A:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_0 = 0
                coord_A = 0
            if coord_0 and coord_B:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_0 = 0
                coord_B = 0
            if coord_0 and coord_C:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_0 = 0
                coord_C = 0
            if coord_0 and coord_D:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_0 = 0
                coord_D = 0
            if coord_0 and coord_E:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_0 = 0
                coord_E = 0
            if coord_0 and coord_F:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_0 = 0
                coord_F = 0
            if coord_0 and coord_G:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_0 = 0
                coord_G = 0
            if coord_0 and coord_H:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_0 = 0
                coord_H = 0
            if coord_0 and coord_I:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_0 = 0
                coord_I = 0
            if coord_0 and coord_J:
                mapPosx = sideMargin + tile*9 + playScreenWidth
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_0 = 0
                coord_J = 0

            # sets positions of sonar and target for player 1
            if gamePhase == "shoot" and coordPass:
                curser1.pos.x = mapPosx
                curser1.pos.y = mapPosy
            if gamePhase == "sonar" and coordPass:
                sonarPos2.x = mapPosx + tile/2
                sonarPos2.y = mapPosy + tile/2

        if playerTurn == 2:
            # moves curser2 to coords
            # row 1
            if coord_1 and coord_A:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_1 = 0
                coord_A = 0
            if coord_1 and coord_B:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_1 = 0
                coord_B = 0
            if coord_1 and coord_C:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_1 = 0
                coord_C = 0
            if coord_1 and coord_D:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_1 = 0
                coord_D = 0
            if coord_1 and coord_E:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_1 = 0
                coord_E = 0
            if coord_1 and coord_F:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_1 = 0
                coord_F = 0
            if coord_1 and coord_G:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_1 = 0
                coord_G = 0
            if coord_1 and coord_H:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_1 = 0
                coord_H = 0
            if coord_1 and coord_I:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_1 = 0
                coord_I = 0
            if coord_1 and coord_J:
                mapPosx = sideMargin + tile*0
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_1 = 0
                coord_J = 0
            # row 2
            if coord_2 and coord_A:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_2 = 0
                coord_A = 0
            if coord_2 and coord_B:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_2 = 0
                coord_B = 0
            if coord_2 and coord_C:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_2 = 0
                coord_C = 0
            if coord_2 and coord_D:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_2 = 0
                coord_D = 0
            if coord_2 and coord_E:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_2 = 0
                coord_E = 0
            if coord_2 and coord_F:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_2 = 0
                coord_F = 0
            if coord_2 and coord_G:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_2 = 0
                coord_G = 0
            if coord_2 and coord_H:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_2 = 0
                coord_H = 0
            if coord_2 and coord_I:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_2 = 0
                coord_I = 0
            if coord_2 and coord_J:
                mapPosx = sideMargin + tile*1
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_2 = 0
                coord_J = 0
            # row 3
            if coord_3 and coord_A:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_3 = 0
                coord_A = 0
            if coord_3 and coord_B:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_3 = 0
                coord_B = 0
            if coord_3 and coord_C:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_3 = 0
                coord_C = 0
            if coord_3 and coord_D:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_3 = 0
                coord_D = 0
            if coord_3 and coord_E:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_3 = 0
                coord_E = 0
            if coord_3 and coord_F:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_3 = 0
                coord_F = 0
            if coord_3 and coord_G:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_3 = 0
                coord_G = 0
            if coord_3 and coord_H:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_3 = 0
                coord_H = 0
            if coord_3 and coord_I:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_3 = 0
                coord_I = 0
            if coord_3 and coord_J:
                mapPosx = sideMargin + tile*2
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_3 = 0
                coord_J = 0
            # row 4
            if coord_4 and coord_A:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_4 = 0
                coord_A = 0
            if coord_4 and coord_B:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_4 = 0
                coord_B = 0
            if coord_4 and coord_C:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_4 = 0
                coord_C = 0
            if coord_4 and coord_D:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_4 = 0
                coord_D = 0
            if coord_4 and coord_E:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_4 = 0
                coord_E = 0
            if coord_4 and coord_F:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_4 = 0
                coord_F = 0
            if coord_4 and coord_G:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_4 = 0
                coord_G = 0
            if coord_4 and coord_H:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_4 = 0
                coord_H = 0
            if coord_4 and coord_I:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_4 = 0
                coord_I = 0
            if coord_4 and coord_J:
                mapPosx = sideMargin + tile*3
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_4 = 0
                coord_J = 0
            # row 5
            if coord_5 and coord_A:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_5 = 0
                coord_A = 0
            if coord_5 and coord_B:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_5 = 0
                coord_B = 0
            if coord_5 and coord_C:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_5 = 0
                coord_C = 0
            if coord_5 and coord_D:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_5 = 0
                coord_D = 0
            if coord_5 and coord_E:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_5 = 0
                coord_E = 0
            if coord_5 and coord_F:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_5 = 0
                coord_F = 0
            if coord_5 and coord_G:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_5 = 0
                coord_G = 0
            if coord_5 and coord_H:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_5 = 0
                coord_H = 0
            if coord_5 and coord_I:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_5 = 0
                coord_I = 0
            if coord_5 and coord_J:
                mapPosx = sideMargin + tile*4
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_5 = 0
                coord_J = 0
            # row 6
            if coord_6 and coord_A:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_6 = 0
                coord_A = 0
            if coord_6 and coord_B:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_6 = 0
                coord_B = 0
            if coord_6 and coord_C:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_6 = 0
                coord_C = 0
            if coord_6 and coord_D:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_6 = 0
                coord_D = 0
            if coord_6 and coord_E:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_6 = 0
                coord_E = 0
            if coord_6 and coord_F:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_6 = 0
                coord_F = 0
            if coord_6 and coord_G:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_6 = 0
                coord_G = 0
            if coord_6 and coord_H:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_6 = 0
                coord_H = 0
            if coord_6 and coord_I:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_6 = 0
                coord_I = 0
            if coord_6 and coord_J:
                mapPosx = sideMargin + tile*5
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_6 = 0
                coord_J = 0
            # row 7
            if coord_7 and coord_A:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_7 = 0
                coord_A = 0
            if coord_7 and coord_B:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_7 = 0
                coord_B = 0
            if coord_7 and coord_C:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_7 = 0
                coord_C = 0
            if coord_7 and coord_D:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_7 = 0
                coord_D = 0
            if coord_7 and coord_E:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_7 = 0
                coord_E = 0
            if coord_7 and coord_F:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_7 = 0
                coord_F = 0
            if coord_7 and coord_G:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_7 = 0
                coord_G = 0
            if coord_7 and coord_H:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_7 = 0
                coord_H = 0
            if coord_7 and coord_I:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_7 = 0
                coord_I = 0
            if coord_7 and coord_J:
                mapPosx = sideMargin + tile*6
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_7 = 0
                coord_J = 0
            # row 8
            if coord_8 and coord_A:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_8 = 0
                coord_A = 0
            if coord_8 and coord_B:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_8 = 0
                coord_B = 0
            if coord_8 and coord_C:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_8 = 0
                coord_C = 0
            if coord_8 and coord_D:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_8 = 0
                coord_D = 0
            if coord_8 and coord_E:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_8 = 0
                coord_E = 0
            if coord_8 and coord_F:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_8 = 0
                coord_F = 0
            if coord_8 and coord_G:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_8 = 0
                coord_G = 0
            if coord_8 and coord_H:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_8 = 0
                coord_H = 0
            if coord_8 and coord_I:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_8 = 0
                coord_I = 0
            if coord_8 and coord_J:
                mapPosx = sideMargin + tile*7
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_8 = 0
                coord_J = 0
            # row 9
            if coord_9 and coord_A:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_9 = 0
                coord_A = 0
            if coord_9 and coord_B:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_9 = 0
                coord_B = 0
            if coord_9 and coord_C:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_9 = 0
                coord_C = 0
            if coord_9 and coord_D:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_9 = 0
                coord_D = 0
            if coord_9 and coord_E:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_9 = 0
                coord_E = 0
            if coord_9 and coord_F:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_9 = 0
                coord_F = 0
            if coord_9 and coord_G:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_9 = 0
                coord_G = 0
            if coord_9 and coord_H:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_9 = 0
                coord_H = 0
            if coord_9 and coord_I:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_9 = 0
                coord_I = 0
            if coord_9 and coord_J:
                mapPosx = sideMargin + tile*8
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_9 = 0
                coord_J = 0
            # row 10
            if coord_0 and coord_A:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*0 + playScreenHeight
                coord_0 = 0
                coord_A = 0
            if coord_0 and coord_B:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*1 + playScreenHeight
                coord_0 = 0
                coord_B = 0
            if coord_0 and coord_C:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*2 + playScreenHeight
                coord_0 = 0
                coord_C = 0
            if coord_0 and coord_D:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*3 + playScreenHeight
                coord_0 = 0
                coord_D = 0
            if coord_0 and coord_E:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*4 + playScreenHeight
                coord_0 = 0
                coord_E = 0
            if coord_0 and coord_F:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*5 + playScreenHeight
                coord_0 = 0
                coord_F = 0
            if coord_0 and coord_G:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*6 + playScreenHeight
                coord_0 = 0
                coord_G = 0
            if coord_0 and coord_H:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*7 + playScreenHeight
                coord_0 = 0
                coord_H = 0
            if coord_0 and coord_I:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*8 + playScreenHeight
                coord_0 = 0
                coord_I = 0
            if coord_0 and coord_J:
                mapPosx = sideMargin + tile*9
                mapPosy = topBotMargin + tile*9 + playScreenHeight
                coord_0 = 0
                coord_J = 0
            # sets positions of sonar and target for player 1
            if gamePhase == "shoot" and coordPass and playerTurn == 2:
                curser2.pos.x = mapPosx
                curser2.pos.y = mapPosy
            if gamePhase == "sonar" and coordPass and playerTurn == 2:
                sonarPos1.x = mapPosx + tile/2
                sonarPos1.y = mapPosy + tile/2

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
    destroyedShipMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','destroyedShip.png')), (int(tile*8 + 12), int(tile*4 + 12)))
    missilePhaseMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','missilePhase.png')), (int(tile*8 + 12), int(tile + 12)))
    subPhaseMessage = pygame.transform.smoothscale(pygame.image.load(os.path.join('Sprites','subPhase.png')), (int(tile*8 + 12), int(tile + 12)))

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

    missilePhaseMessage1 = False
    missilePhaseMessage2 = False
    missilePhaseMessageCounter1 = 0
    missilePhaseMessageCounter2 = 0

    subPhaseMessage1 = True
    subPhaseMessage2 = False
    subPhaseMessageCounter1 = 0
    subPhaseMessageCounter2 = 0


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

    if pinPointPulse1 and playerTurn == 2:
        pinPointDistress.draw()
    if pinPointPulse2 and playerTurn == 1:
        pinPointDistress.draw()

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
        #print("{0:5}: {1:3}    Average Distance in Range:". format(key, shipDic2[key].sonarHitNum), shipDic2[key].averageDistance)#
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

    # draws 'subPhase' message
    if Sprite.subPhaseMessage1:
        win.blit(Sprite.subPhaseMessage, (sideMargin + tile - 6, topBotMargin))
        Sprite.subPhaseMessageCounter1 += 1
        if Sprite.subPhaseMessageCounter1 > 30:
            Sprite.subPhaseMessageCounter1 = 0
            Sprite.subPhaseMessage1 = False
    if Sprite.subPhaseMessage2:
        win.blit(Sprite.subPhaseMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin))
        Sprite.subPhaseMessageCounter2 += 1
        if Sprite.subPhaseMessageCounter2 > 30:
            Sprite.subPhaseMessageCounter2 = 0
            Sprite.subPhaseMessage2 = False

    # draws 'missilePhase' message
    if Sprite.missilePhaseMessage1:
        win.blit(Sprite.missilePhaseMessage, (sideMargin + tile - 6, topBotMargin - 6))
        Sprite.missilePhaseMessageCounter1 += 1
        if Sprite.missilePhaseMessageCounter1 > 30:
            Sprite.missilePhaseMessageCounter1 = 0
            Sprite.missilePhaseMessage1 = False
    if Sprite.missilePhaseMessage2:
        win.blit(Sprite.missilePhaseMessage, (sideMargin + tile - 6 + playScreenWidth, topBotMargin - 6))
        Sprite.missilePhaseMessageCounter2 += 1
        if Sprite.missilePhaseMessageCounter2 > 30:
            Sprite.missilePhaseMessageCounter2 = 0
            Sprite.missilePhaseMessage2 = False

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

    for key, val in averageLength.items():
        if len(averageLength[key]) != 0:
            # crashes if i dont do the try/except -/(-.-)\-
            try:
                shipDic2[key].averageDistance = sum(averageLength[key])/len(averageLength[key])
            except:
                pass
        else:
            # crashes if i dont do the try/except -/(-.-)\-
            try:
                shipDic2[key].averageDistance = 0
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
        # calling for sonar position
        curser1.move()
    
        # controls
        # rotate counter-clockwise
        if keys[pygame.K_LEFTBRACKET]:
            sonarStartAngle1 += 5
 
        # rotate clockwise
        if keys[pygame.K_RIGHTBRACKET]:
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
        # calling for sonar position
        curser1.move()

        # controls
        # rotate counter-clockwise
        if keys[pygame.K_LEFTBRACKET]:
            sonarStartAngle2 += 5
 
        # rotate clockwise
        if keys[pygame.K_RIGHTBRACKET]:
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
    global sonarController

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



    #coupling good times
    #for ship theme playback
    #makes a list of ships hit by sonar if in sonar stage
    #player 1 and player 2

    #valve anti-cheat
    if playerTurn == 1 and Sprite.notEnoughMessage1:
        sonarController = 0

    if playerTurn == 2 and Sprite.notEnoughMessage2:
        sonarController = 0

    if sonarController == 1:
        sonar_hitShips = {}
        #beamHitNumList = {}
        #print(shipDic1)
        if playerTurn == 1:
            for key, val in shipDic2.items():
                ship = val
                if ship.sonarHitNum > 0:
                    sonar_hitShips[key] = val

                    #beamHitNumList.append(ship.sonarHitNum)
                    #1st item in beamHitNum list will be the first item in sonar_hitShi[s]
    
            #print('beamHitNumList: {}'.format(beamHitNumList))
            #print('(shipDic2)sonar_hitShips: {}'.format(sonar_hitShips))
        elif playerTurn == 2:
            for key, val in shipDic1.items():
                ship = val
                if ship.sonarHitNum > 0:
                    sonar_hitShips[key] = val
                    #beamHitNumList.append(ship.sonarHitNum)
            #print('(shipDic1)sonar_hitShips: {}'.format(sonar_hitShips))
        # calls ship sounds,
        shipTheme_playback(sonar_hitShips)
        
        #TO BREAK THE LOOP
        sonarController = 0
        
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
        Sprite.missilePhaseMessage1 = True
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

        if len(sonarDic2) == 1 and tempSonarCharge1 > 0:
            for key, item in shipDic2.items():
                if shipDic2[key].sonarHitNum:
                    pinPointPulse2 = key
                    whereSonarHit(1, key)

    if playerTurn == 2:
        Sprite.missilePhaseMessage2 = True
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

        if len(sonarDic1) == 1 and tempSonarCharge2 > 0:
            for key, item in shipDic1.items():
                if shipDic1[key].sonarHitNum:
                    pinPointPulse1 = key
                    whereSonarHit(2, key)

    # update sonar charge meter
    createSonarChargeMeter()

# what tile the beam hit ship
def whereSonarHit(playerNum, ship):
    global pinPointDistress
    if playerNum == 1:
        for key, item in sonarDic2.items():
            sonarHitPosx = sonarDic2[key].end2.x
            sonarHitPosy = sonarDic2[key].end2.y
        if shipDic2[ship].width > shipDic2[ship].height:
            for i in range(shipDic2[ship].length):
                if (shipDic2[ship].pos.x + tile*(i + 1)) > sonarHitPosx and sonarHitPosx < (shipDic2[ship].pos.x + tile*(i + 2)):
                    pinPointDistress = distressCall((255,255,0), shipDic2[ship].pos.x + tile*i - playScreenWidth, shipDic2[ship].pos.y - playScreenHeight, tile, tile)
                    return
        if shipDic2[ship].width < shipDic2[ship].height:
            for i in range(shipDic2[ship].length):
                if (shipDic2[ship].pos.y + tile*(i + 1)) > sonarHitPosy and sonarHitPosy < (shipDic2[ship].pos.y + tile*(i + 2)):
                    pinPointDistress = distressCall((255,255,0), shipDic2[ship].pos.x - playScreenWidth, shipDic2[ship].pos.y + tile*i - playScreenHeight, tile, tile)
                    return

    if playerNum == 2:
        for key, item in sonarDic1.items():
            sonarHitPosx = sonarDic1[key].end2.x
            sonarHitPosy = sonarDic1[key].end2.y
        if shipDic1[ship].width > shipDic1[ship].height:
            for i in range(shipDic1[ship].length):
                if (shipDic1[ship].pos.x + tile*(i + 1)) > sonarHitPosx and sonarHitPosx < (shipDic1[ship].pos.x + tile*(i + 2)):
                    pinPointDistress = distressCall((255,255,0), shipDic1[ship].pos.x + tile*i + playScreenWidth, shipDic1[ship].pos.y - playScreenHeight, tile, tile)
                    return
        if shipDic1[ship].width < shipDic1[ship].height:
            for i in range(shipDic1[ship].length):
                if (shipDic1[ship].pos.y + tile*(i + 1)) > sonarHitPosy and sonarHitPosy < (shipDic1[ship].pos.y + tile*(i + 2)):
                    pinPointDistress = distressCall((255,255,0), shipDic1[ship].pos.x + playScreenWidth, shipDic1[ship].pos.y + tile*i - playScreenHeight, tile, tile)
                    return

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
        # for phase message
        Sprite.subPhaseMessage2 = True
        if isCollides[0] and damageTest1:
            #plays explosion sound if missile lands
            ch_buttonSounds.play(missile_hit)
            ch_buttonSounds.set_volume(0.5,0.0)
            
            Sprite.hitMessage1 = True
            sonarCharge1 += MAXSONARCHARGE*rechargePercent
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
                #plays miss sound if missile misses
                ch_buttonSounds.play(missile_miss)
                ch_buttonSounds.set_volume(1.0,0.0)
                
                Sprite.missMessage1 = True
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                #plays explosion sound if missile lands
                ch_buttonSounds.play(missile_hit)
                ch_buttonSounds.set_volume(0.5,0.0)
                Sprite.alreadyHitMessage1 = True
                print("Player 1, you already damaged that part!")
                print("~~~~~~~~")

    if playerTurn == 2:
        # for explosion animation
        playerShot2 = True
        # end turn
        player2End = True
        # for phase message
        Sprite.subPhaseMessage1 = True
        if isCollides[0] and damageTest2:
            #plays explosion sound if missile lands
            ch_buttonSounds.play(missile_hit)
            ch_buttonSounds.set_volume(0.5,0.0)
            
            sonarCharge2 += MAXSONARCHARGE*rechargePercent
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
                #plays miss sound if missile misses
                ch_buttonSounds.play(missile_miss)
                ch_buttonSounds.set_volume(1.0,0.0)
                
                Sprite.missMessage2 = True
                print("All you shot was sea!")
                print("~~~~~~~~")
            else:
                #plays explosion sound if missile lands
                ch_buttonSounds.play(missile_hit)
                ch_buttonSounds.set_volume(1.0,0.0)
                
                Sprite.alreadyHitMessage2 = True
                print("Player 2, you already damaged that part!")
                print("~~~~~~~~")

    # is a sub sunk
    isSubSunk()
    # sub hit causation
    if isTargetSub1:
        subSink1 = True
    if isTargetSub2:
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
        if not(allDistressTest):
            shipDistress(1)
    if not(sonarCharge2) and isDisplayingDistress == 0 and tempPlayerTurn != playerTurn and playerTurn != 0:
        isDisplayingDistress = 1
        if not(allDistressTest):
            shipDistress(2)

    if otherPlayer == 1 and shoooted and sonarCharge1 == 0:
        sonarCharge1 = MAXSONARCHARGE
        distressCalls = {}
        isDisplayingDistress = 0
    if otherPlayer == 2 and shoooted and sonarCharge2 == 0:
        sonarCharge2 = MAXSONARCHARGE
        distressCalls = {}
        isDisplayingDistress = 0

    shoooted = False
    tempPlayerTurn = playerTurn

# distress mode for certain ship
def shipDistress(playerInDistress):
    global distressCalls

    shipName = "ship%s" %randint(0,4)

    # need to make random cloud so other player can guess where ship is
    distressDensity = 2
    distressRange = 1
    distressOffset = randint(-1,1)

    shipLength = shipDic1[shipName].health + shipDic1[shipName].damage

    distressCalls = {}

    if playerInDistress == 1:
        ch_buttonSounds.play(distressBeaconLight)
        ch_buttonSounds.set_volume(1.0,0.0)
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
        ch_buttonSounds.play(distressBeaconLight)
        ch_buttonSounds.set_volume(1.0,0.0)
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

# when called this function distroys enemy sub while putting all your ships in distress
def destroyEnemySub():
    global subSink1
    global subSink2
    global player1End
    global player2End
    global playerTurn
    global playerTrigger
    global gamePhase
    global sonarCharge1
    global sonarCharge2
    global allDistressTest

    # triggers the changing of players
    if gamePhase == "sonar":
        playerTrigger = 1
        if playerTurn == 1:
            if sonarCharge1 == MAXSONARCHARGE:
                allDistressTest = True
                sonarCharge1 = 0
                allShipDistress(1)
                isSubSunk()
                player1End = True
                subSink2 = True
        if playerTurn == 2:
            if sonarCharge2 == MAXSONARCHARGE:
                allDistressTest = True
                sonarCharge2 = 0
                allShipDistress(2)
                isSubSunk()
                player2End = True
                subSink1 = True
        gamePhase = "shoot"
    else:
        print("It's too late for that!")

# puts all ships into distress
def allShipDistress(playerInDistress):
    global distressCalls

    # need to make random cloud so other player can guess where ship is
    distressDensity = 2
    distressRange = 1
    distressCalls = {}

    if playerInDistress == 1:
        for key, item in shipDic1.items():
            distressOffset = randint(-1,1)

            shipLength = shipDic1[key].health + shipDic1[key].damage

            # guarantees that atleast one part of the ship will be lit
            if shipDic1[key].width < shipDic1[key].height:
                distressCalls["ontarget%s" %len(distressCalls)] = distressCall((255,255,0), shipDic1[key].pos.x + playScreenWidth, shipDic1[key].pos.y + randint(0, shipLength - 1)*tile - playScreenHeight, tile, tile)
            else:
                distressCalls["ontarget%s" %len(distressCalls)] = distressCall((255,255,0), shipDic1[key].pos.x + randint(0, shipLength - 1)*tile + playScreenWidth, shipDic1[key].pos.y - playScreenHeight, tile, tile)

            # need to make random cloud so other player can guess where ship is
            for k in range(randint(distressDensity, distressDensity + 3)):
                for i in range(0, randint(distressRange, distressRange + 2)):
                    if shipDic1[key].width < shipDic1[key].height:
                        distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic1[key].pos.x + tile*randint(-i,i) + distressOffset*tile + playScreenWidth, shipDic1[key].pos.y + tile*randint(-i,i) + int(0.5 * shipLength)*tile + distressOffset*tile - playScreenHeight, tile, tile)
                    else:
                        distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic1[key].pos.x + tile*randint(-i,i) + distressOffset*tile + int(0.5 * shipLength)*tile + playScreenWidth, shipDic1[key].pos.y + tile*randint(-i,i) + distressOffset*tile - playScreenHeight, tile, tile)

    if playerInDistress == 2:
        for key, item in shipDic2.items():
            distressOffset = randint(-1,1)

            shipLength = shipDic1[key].health + shipDic1[key].damage

            # guarantees that atleast one part of the ship will be lit
            if shipDic2[key].width < shipDic2[key].height:
                distressCalls["ontarget%s" %len(distressCalls)] = distressCall((255,255,0), shipDic2[key].pos.x + playScreenWidth, shipDic2[key].pos.y + randint(0, shipLength - 1)*tile - playScreenHeight, tile, tile)
            else:
                distressCalls["ontarget%s" %len(distressCalls)] = distressCall((255,255,0), shipDic2[key].pos.x + randint(0, shipLength - 1)*tile + playScreenWidth, shipDic2[key].pos.y - playScreenHeight, tile, tile)

            # need to make random cloud so other player can guess where ship is
            for k in range(randint(distressDensity, distressDensity + 3)):
                for i in range(0, randint(distressRange, distressRange + 2)):
                    if shipDic2[key].width < shipDic2[key].height:
                        distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic2[key].pos.x + tile*randint(-i,i) + distressOffset*tile - playScreenWidth, shipDic2[key].pos.y + tile*randint(-i,i) + int(0.5 * shipLength)*tile + distressOffset*tile - playScreenHeight, tile, tile)
                    else:
                        distressCalls["distress%s" %len(distressCalls)] = distressCall((255,255,0), shipDic2[key].pos.x + tile*randint(-i,i) + distressOffset*tile + int(0.5 * shipLength)*tile - playScreenWidth, shipDic2[key].pos.y + tile*randint(-i,i) + distressOffset*tile - playScreenHeight, tile, tile)

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
    global sonarController

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
    
    # shooting missle and sonar
    # works the smae way that the space bar and p key worked seperately
    # just put whatever you need the the correct if statement
    toggleShoot = 0     # just so they dont both trigger
    if key[pygame.K_SPACE] and isPress_SPACE == 0 and playerTurn:
        # for missile shooting and explosion sound logic
        if gamePhase == "shoot" and toggleShoot == 0:
            gamePhase = "sonar"
            toggleShoot = 1
            shootMissile()
            #explosion sound!
        # for sonar pulse
        if gamePhase == "sonar" and toggleShoot == 0:
            gamePhase = "shoot"
            toggleShoot = 1
            pulseSonar()
            sonarController = 1
        isPress_SPACE = 1
        
    # this just makes sure when space is pressed, it only inputs once
    if not(key[pygame.K_SPACE]):
        isPress_SPACE = 0

    # destroy enemy submarine
    if key[pygame.K_LSHIFT] and isPress_LSHIFT == 0:
        isPress_LSHIFT = 1
        destroyEnemySub()
    if not(key[pygame.K_LSHIFT]):
        isPress_LSHIFT = 0

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
        gamePhase = "shoot"
    if subSink2 and whatOtherPlayer() == 1 and playerTurn != tempPlayerTurn:
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
                return
            else:
                Sprite.subUnderShip1 = False
                Sprite.subUnderShipCounter1 = 0

    if playerTurn == 2:
        for key, val in shipDic1.items():
            if pygame.Rect.colliderect(pygame.Rect((sonarPos1.x - tile/2), (sonarPos1.y - tile/2), curser1.width, curser1.height), shipDic1[key].rect):
                Sprite.subUnderShip2 = True
                return
            else:
                Sprite.subUnderShip2 = False
                Sprite.subUnderShipCounter2 = 0

#function for playback of ship themes
#set up for 2 players pulling from their respective collections
def shipTheme_playback(sonar_hitShips):
    #'importing' necessary globals
    global shipDic1
    global shipDic2
    global playerTurn

    
    #list with all relevent ship objects
    shipList = list(sonar_hitShips.values())

    if shipList == [] and playerTurn == 1:
        ch_buttonSounds.play(NOSHIPSDETECTED)
        ch_buttonSounds.set_volume(0.6,0.0)
        
    if shipList == [] and playerTurn == 2:
        ch_buttonSounds.play(NOSHIPSDETECTED)
        ch_buttonSounds.set_volume(0.0,0.6)
        
    
    #playback - player turn decides what ship dictionaries to pull from for ship values
    if playerTurn == 1:
        #checks for ship object in shipList - plays simple or complex theme, and adjusts volume/pans audio accordingly
        #does this for each ship
        #audio pan done by setting each channels volume w two parameters (0.0,0.0) or (L,R) where L and R are float representations of volume in the stereo field (<=1)
        
        try:
            if shipDic2['ship0'] in shipList:
                #volume_distanceRatio = current avg sonar distance / max sonar distance
                #280 is what im working with for max sonar distance
                volume_distanceRatio = shipDic2['ship0'].averageDistance/280

                
                #using vol dist ratioto select which theme plays (decided to pair the parameters - volume_distanceRatio isn't an accurate name for the variable but whateva)
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme0.play(th_carrierIntense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme0.play(th_carrierSimple)
                

                ch_shipTheme0.set_volume(volume_distanceRatio,0.0)
                #print("ship 0 hit, ship beam avg dist: {}, ship beam hit num: {}, volume_distanceRatio {}".format(shipDic2['ship0'].averageDistance,shipDic2['ship0'].sonarHitNum, volume_distanceRatio))
                
        except:
            pass

               
        try:
            if shipDic2['ship1'] in shipList:
                volume_distanceRatio = shipDic2['ship1'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme1.play(th_battleshipIntense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme1.play(th_battleshipSimple)

                
                ch_shipTheme1.set_volume(volume_distanceRatio,0.0)

                #print("ship 1 hit, ship beam avg dist: {}, ship beam hit num: {} volume_distanceRatio {}".format(shipDic2['ship1'].averageDistance,shipDic2['ship1'].sonarHitNum,volume_distanceRatio))
        except:
            pass

        try:
            if shipDic2['ship2'] in shipList:
                volume_distanceRatio = shipDic2['ship2'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme2.play(th_cruiser1Intense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme2.play(th_cruiser1Simple)

                
                ch_shipTheme2.set_volume(volume_distanceRatio,0.0)

                #print("ship 2 hit, ship beam avg dist: {}, ship beam hit num: {} volume_distanceRatio {}".format(shipDic2['ship2'].averageDistance,shipDic2['ship2'].sonarHitNum, volume_distanceRatio))
        except:
            pass

        try:
            if shipDic2['ship3'] in shipList:
                volume_distanceRatio = shipDic2['ship3'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme3.play(th_cruiser2Intense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme3.play(th_cruiser2Simple)

                
                ch_shipTheme3.set_volume(volume_distanceRatio,0.0)

                #print("ship 3 hit, ship beam avg dist: {}, ship beam hit num: {}, volume_distanceRatio {}".format(shipDic2['ship3'].averageDistance,shipDic2['ship3'].sonarHitNum,volume_distanceRatio))
        except:
            pass

        try:
            
            if shipDic2['ship4'] in shipList:
                volume_distanceRatio = shipDic2['ship4'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme4.play(th_destroyerIntense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme4.play(th_destroyerSimple)

                
                ch_shipTheme4.set_volume(volume_distanceRatio,0.0)

                #print("ship 4 hit, ship beam avg dist: {}, ship beam hit num: {} volume_distanceRatio {}".format(shipDic2['ship4'].averageDistance,shipDic2['ship4'].sonarHitNum, volume_distanceRatio))

        except:
            pass
        
    if playerTurn == 2:

        try:
            if shipDic1['ship0'] in shipList:
                #280 is what im working with for max distance
                volume_distanceRatio = shipDic1['ship0'].averageDistance/280
                print('ship0')

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme0.play(th_carrierIntense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme0.play(th_carrierSimple)
                
                ch_shipTheme0.set_volume(0.0,volume_distanceRatio)
                    
                #print("ship 0 hit, ship beam avg dist: {}, ship beam hit num: {}, volume_distanceRatio {}".format(shipDic1['ship0'].averageDistance,shipDic1['ship0'].sonarHitNum, volume_distanceRatio))
        except:
            pass
            
            
        try:
            
            if shipDic1['ship1'] in shipList:
                #280 is what im working with for max distance
                volume_distanceRatio = shipDic1['ship1'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme1.play(th_battleshipIntense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme1.play(th_battleshipSimple)

                
                ch_shipTheme1.set_volume(0.0,volume_distanceRatio)

                #print("ship 1 hit, ship beam avg dist: {}, ship beam hit num: {} volume_distanceRatio {}".format(shipDic1['ship1'].averageDistance,shipDic1['ship1'].sonarHitNum,volume_distanceRatio))
        except:
            pass

        try:
            if shipDic1['ship2'] in shipList:
                #280 is what im working with for max distance
                volume_distanceRatio = shipDic1['ship2'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme2.play(th_cruiser1Intense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme2.play(th_cruiser1Simple)

                
                ch_shipTheme2.set_volume(0.0,volume_distanceRatio)

                #print("ship 2 hit, ship beam avg dist: {}, ship beam hit num: {} volume_distanceRatio {}".format(shipDic1['ship2'].averageDistance,shipDic1['ship2'].sonarHitNum, volume_distanceRatio))
        except:
            pass

        try:
            if shipDic1['ship3'] in shipList:
                #280 is what im working with for max distance
                volume_distanceRatio = shipDic1['ship3'].averageDistance/280

                
                if volume_distanceRatio <= 0.4:
                    ch_shipTheme3.play(th_cruiser2Intense)
                elif volume_distanceRatio > 0.4:
                    ch_shipTheme3.play(th_cruiser2Simple)

                
                ch_shipTheme3.set_volume(0.0,volume_distanceRatio)

                #print("ship 3 hit, ship beam avg dist: {}, ship beam hit num: {}, volume_distanceRatio {}".format(shipDic1['ship3'].averageDistance,shipDic1['ship3'].sonarHitNum,volume_distanceRatio))
        except:
            pass

        try:
            if shipDic1['ship4'] in shipList:
                    #280 is what im working with for max distance
                    volume_distanceRatio = shipDic1['ship4'].averageDistance/280
                    print('ship4')

                    
                    if volume_distanceRatio <= 0.4:
                        ch_shipTheme4.play(th_destroyerIntense)
                    elif volume_distanceRatio > 0.4:
                        ch_shipTheme4.play(th_destroyerSimple)

                    
                    ch_shipTheme4.set_volume(0.0,volume_distanceRatio)

                    #print("ship 4 hit, ship beam avg dist: {}, ship beam hit num: {} volume_distanceRatio {}".format(shipDic1['ship4'].averageDistance,shipDic1['ship4'].sonarHitNum, volume_distanceRatio))
        except:
            pass
        
    return

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

def num_letter_buttonSound():
    global buttonS_array
    
    ch_buttonSounds.play(buttonS_array[randint(0,2)])

    if playerTurn == 1:
        ch_buttonSounds.set_volume(0.5,0.0)
        
    if playerTurn == 2:
        ch_buttonSounds.set_volume(0.0,0.5)
      
# default player stuff
playerTurn = 1
player1End = False
player2End = False
playerCount = 0
playerTrigger = 0
playerShot1 = False
playerShot2 = False
tempPlayerTurn = 0
shoooted = False
pinPointPulse1 = 0
pinPointPulse2 = 0
gamePhase = "sonar"
allDistressTest = False

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
sonarController = 0
subSink1 = False
subSink2 = False
subSinkPunish1 = 0
subSinkPunish2 = 0
subPunishLevel = 2
warningCounter1 = 0
warningCounter2 = 0
pinPointDistress = 0
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
    # sonar targeted?
    isSubTargeted()
    # sonar iteration
    createSonarChargeMeter()
    sonarDicUnpacker = createSonar(playerTurn)
    sonarDic1 = sonarDicUnpacker[0]
    sonarDic2 = sonarDicUnpacker[1]
    # dectects inputs from all sources
    detectInputs(numShip)
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

##TO DO
#FIND MAGIC NUMBERS FOR WATERCLOCK ON PI
#NOSHIPS playback bug hotfix before expo kek
