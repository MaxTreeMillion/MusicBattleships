# program to take a jab at ray casting in 2D
# first I will try and draw two intersecting lines and sovle for the intersection
# will work towards a general solution

import pygame
import math
from random import randint

# screen deminsions
screenHeight = 700
screenWidth = 700

# initialize
pygame.init()
win = pygame.display.set_mode((screenWidth, screenHeight))

# clock
clock = pygame.time.Clock()

# x/y vectors
vec = pygame.math.Vector2

# Classes
class Line():
    def __init__(self, x1, x2, y1, y2):
        self.color = (255,255,255)
        self.end1 = vec(x1,y1)
        self.end2 = vec(x2,y2)

    def draw(self):
        pygame.draw.line(win, self.color, self.end1, self.end2, width = 3)

class Rectangle():
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.pos = vec(x,y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)

    def cleanUpRect(self, rectDic):
        for i in range(len(rectDic)):
            if rectDic["rect%s" %i] != self:
                #print(rectDic["rect%s" %i])
                if pygame.Rect.colliderect(self.rect, rectDic["rect%s" %i].rect):
                    del rectDic["rect%s" %i]
                    directList = lengthDirect()
                    rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,10), (screenHeight/10)*randint(0,10), directList[0], directList[1])
                    rectDic["rect%s" %i] = rect
                    rectDic["rect%s" %i].cleanUpRect(rectDic)


def update(rectDic, lineDic):
    win.fill((0,0,0))

    # draw grit with lines
    for i in range(1,len(lineDic)+1):
        lineDic["line%s" %i].draw()

    # drawing rectangles
    #for rect in rectList:
    for i in range(len(rectDic)):
        rectDic["rect%s" %i].draw()

    pygame.display.update()


# decides legnth and direction of ship
def lengthDirect():
    global screenHeight
    global screenWidth

    if randint(0,1):
        length = randint(2,6)*(screenHeight/10)
        width = (screenWidth/10)
    else:
        length = (screenHeight/10)
        width = randint(2,6)*(screenWidth/10)
    return width, length

def createRect(numRect):
    rectDic = {}
    for i in range(numRect):
        directList = lengthDirect()
        rect = Rectangle((randint(0,255), randint(0,255), randint(0,255)), (screenWidth/10)*randint(0,9), (screenHeight/10)*randint(0,9), directList[0], directList[1])
        rectDic["rect%s" %i] = rect
    return rectDic

def createLine():
    lineDic = {}
    for i in range(1,10):
        line = Line((screenWidth/10)*i,(screenWidth/10)*i, 0, screenHeight)
        lineDic["line%s" %i] = line
    for i in range(10,19):
        line = Line(0, screenWidth, (screenHeight/10)*(i-9),(screenHeight/10)*(i-9))
        lineDic["line%s" %i] = line
    return lineDic

# Create Grid
lineDic = createLine()

run = True
frameRate = 1
while run:
    clock.tick(frameRate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run == False

    # creat random rectangles
    numRect = 8
    rectDic = createRect(numRect)
    for i in range(len(rectDic)):
        rectDic["rect%s" %i].cleanUpRect(rectDic)

    update(rectDic, lineDic)
pygame.quit()

