import board
import busio
import digitalio

import RPi.GPIO as GPIO
from time import sleep
from math import floor, ceil

from adafruit_mcp230xx.mcp23017 import MCP23017
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

GPIO.setmode(GPIO.BCM)

# setup LED pins for letters P1 and P2
letLedP1 = [18, 23, 24, 25, 12, 16, 20]
letLedP2 = [4, 17, 27, 22, 6, 13, 19]
GPIO.setup(letLedP1, GPIO.OUT)
GPIO.setup(letLedP2, GPIO.OUT)

#######################
# GPIO INITIALIZATION
#######################

# setup "fire" button P1
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# setup "fire" button P2
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# declare i2c connection
i2c = busio.I2C(board.SCL, board.SDA)

# setting up SPI connection for analog inputs
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)

#will use as input for channel variables for P1/P2
analogChip = MCP.MCP3008(spi, cs)

# create P1 and P2 instance of MCP23017 chip controls
mcpP1 = MCP23017(i2c, address=0x20)
mcpP2 = MCP23017(i2c, address=0x21)

################################
# PLAYER 1 GPIO SETUP
################################

# P1 fire button
confirmP1 = GPIO.input(21)

# P1 mcp letter/number I/O setup
# getting pins
pin0p1 = mcpP1.get_pin(0)
pin1p1 = mcpP1.get_pin(1)
pin2p1 = mcpP1.get_pin(2)
pin3p1 = mcpP1.get_pin(3)
pin4p1 = mcpP1.get_pin(4)
pin5p1 = mcpP1.get_pin(5)
pin6p1 = mcpP1.get_pin(6)
pin7p1 = mcpP1.get_pin(7)
pin8p1 = mcpP1.get_pin(8)
pin9p1 = mcpP1.get_pin(9)

# setting pins as input with pull up resistors enabled
pin0p1.direction = digitalio.Direction.INPUT
pin0p1.pull = digitalio.Pull.UP
pin1p1.direction = digitalio.Direction.INPUT
pin1p1.pull = digitalio.Pull.UP
pin2p1.direction = digitalio.Direction.INPUT
pin2p1.pull = digitalio.Pull.UP
pin3p1.direction = digitalio.Direction.INPUT
pin3p1.pull = digitalio.Pull.UP
pin4p1.direction = digitalio.Direction.INPUT
pin4p1.pull = digitalio.Pull.UP
pin5p1.direction = digitalio.Direction.INPUT
pin5p1.pull = digitalio.Pull.UP
pin6p1.direction = digitalio.Direction.INPUT
pin6p1.pull = digitalio.Pull.UP
pin7p1.direction = digitalio.Direction.INPUT
pin7p1.pull = digitalio.Pull.UP
pin8p1.direction = digitalio.Direction.INPUT
pin8p1.pull = digitalio.Pull.UP
pin9p1.direction = digitalio.Direction.INPUT
pin9p1.pull = digitalio.Pull.UP

# P1 ON-ON toggle for switching between letter/number
pin10p1 = mcpP1.get_pin(10)
pin11p1 = mcpP1.get_pin(11)

# setting toggle switch pins for input with pull up resistors enabled
pin10p1.direction = digitalio.Direction.INPUT
pin10p1.pull = digitalio.Pull.UP
pin11p1.direction = digitalio.Direction.INPUT
pin11p1.pull = digitalio.Pull.UP

# P1 analog inputs for slide and pot 
slideP1 = AnalogIn(analogChip, MCP.P0)
potP1 = AnalogIn(analogChip, MCP.P1)

########################
# PLAYER 2 GPIO SETUP
########################

# P2 fire button
confirmP2 = GPIO.input(26)

# P2 mcp letter/number I/O setup
# getting pins
pin0p2 = mcpP2.get_pin(0)
pin1p2 = mcpP2.get_pin(1)
pin2p2 = mcpP2.get_pin(2)
pin3p2 = mcpP2.get_pin(3)
pin4p2 = mcpP2.get_pin(4)
pin5p2 = mcpP2.get_pin(5)
pin6p2 = mcpP2.get_pin(6)
pin7p2 = mcpP2.get_pin(7)
pin8p2 = mcpP2.get_pin(8)
pin9p2 = mcpP2.get_pin(9)

# setting pins as input with pull up resistors enabled
pin0p2.direction = digitalio.Direction.INPUT
pin0p2.pull = digitalio.Pull.UP
pin1p2.direction = digitalio.Direction.INPUT
pin1p2.pull = digitalio.Pull.UP
pin2p2.direction = digitalio.Direction.INPUT
pin2p2.pull = digitalio.Pull.UP
pin3p2.direction = digitalio.Direction.INPUT
pin3p2.pull = digitalio.Pull.UP
pin4p2.direction = digitalio.Direction.INPUT
pin4p2.pull = digitalio.Pull.UP
pin5p2.direction = digitalio.Direction.INPUT
pin5p2.pull = digitalio.Pull.UP
pin6p2.direction = digitalio.Direction.INPUT
pin6p2.pull = digitalio.Pull.UP
pin7p2.direction = digitalio.Direction.INPUT
pin7p2.pull = digitalio.Pull.UP
pin8p2.direction = digitalio.Direction.INPUT
pin8p2.pull = digitalio.Pull.UP
pin9p2.direction = digitalio.Direction.INPUT
pin9p2.pull = digitalio.Pull.UP

# P2 ON-ON toggle for switching between letter/number
pin10p2 = mcpP2.get_pin(10)
pin11p2 = mcpP2.get_pin(11)

# setting toggle switch pins for input with pull up resistors enabled
pin10p2.direction = digitalio.Direction.INPUT
pin10p2.pull = digitalio.Pull.UP
pin11p2.direction = digitalio.Direction.INPUT
pin11p2.pull = digitalio.Pull.UP

# P2 analog inputs for slide and pot 
slideP2 = AnalogIn(analogChip, MCP.P2)
potP2 = AnalogIn(analogChip, MCP.P3)

# control class
class Control:
    
    # CLASS VARIABLES
    # Case lists for letter LEDs
    letA = [1, 1, 1, 0, 1, 1, 1]
    letB = [0, 0, 1, 1, 1, 1, 1]
    letC = [1, 0, 0, 1, 1, 1, 0]
    letD = [0, 1, 1, 1, 1, 0, 1]
    letE = [1, 0, 0, 1, 1, 1, 1]
    letF = [1, 0, 0, 0, 1, 1, 1]
    letG = [1, 1, 1, 1, 0, 1, 1]
    letH = [0, 1, 1, 0, 1, 1, 1]
    letI = [0, 1, 1, 0, 0, 0, 0]
    letJ = [0, 1, 1, 1, 1, 0, 0]
    let0 = [1, 1, 1, 1, 1, 0, 1]
    letOff = [0, 0, 0, 0, 0, 0, 0]
    let0 = [1, 1, 1, 1, 1, 1, 0]
    
    # Case lists for number LEDs
    num0 = [1, 1, 1, 1, 1, 1, 0]
    num1 = [0, 1, 1, 0, 0, 0, 0]
    num2 = [1, 1, 0, 1, 1, 0, 1]
    num3 = [1, 1, 1, 1, 0, 0, 1]
    num4 = [0, 1, 1, 0, 0, 1, 1]
    num5 = [1, 0, 1, 1, 0, 1, 1]
    num6 = [1, 0, 1, 1, 1, 1, 1]
    num7 = [1, 1, 1, 0, 0, 0, 0]
    num8 = [1, 1, 1, 1, 1, 1, 1]
    num9 = [1, 1, 1, 0, 0, 1, 1]
    numOff = [0, 0, 0, 0, 0, 0, 0]
    
    # CLASS INSTANTIATION
    def __init(self, player, playerPhase = 1):
        
        self.player =  player
        self.playerTurn = playerPhase
        
    
    # GETTERS/SETTERS
    @property
    def player(self):
        return self._player
    @player.setter
    def player(self, value):
        self._player = value
    
    @property
    def playerPhase(self):
        return self._playerPhase
    @playerPhase.setter
    def playerPhase(self, value):
        self._playerPhase = value
    
    # CLASS METHODS
    
    # method to display letter LEDS
    def letDisp(self, let):
        
        # player 1 letter LED controls
        GPIO.output(18, let[0])
        GPIO.output(23, let[1])
        GPIO.output(24, let[2])
        GPIO.output(25, let[3])
        GPIO.output(12, let[4])
        GPIO.output(16, let[5])
        GPIO.output(20, let[6])
        
        # player 2 letter LED
        GPIO.output(4, let[0])
        GPIO.output(17, let[1])
        GPIO.output(27, let[2])
        GPIO.output(22, let[3])
        GPIO.output(6, let[4])
        GPIO.output(13, let[5])
        GPIO.output(19, let[6])
    
    # method to display number LEDS
    def numDisp(self, num):
        
        # player 1 number LED controls
        # PLACEHOLDER
        GPIO.output(18, num[0])
        GPIO.output(23, num[1])
        GPIO.output(24, num[2])
        GPIO.output(25, num[3])
        GPIO.output(12, num[4])
        GPIO.output(16, num[5])
        GPIO.output(20, num[6])
        
        # player 2 number LED controls
        # PLACEHOLDER
        GPIO.output(4, num[0])
        GPIO.output(17, num[1])
        GPIO.output(27, num[2])
        GPIO.output(22, num[3])
        GPIO.output(6, num[4])
        GPIO.output(13, num[5])
        GPIO.output(19, num[6])
    
    # method to put LEDS in inital 0,0 state
    def setupLED(self, self.let0, self.num0):
        I1 = letDisp(self, self.let0)
        I1 = numDisp(self, self.num0)
        I2 = letDisp(self, self.let0)
        I2 = numDisp(self, self.num0)
    
    # method to turn off LEDS
    def turnOffLED(self.self.letOff, self.numOff):
        I1 = letDisp(self, self.letOff)
        I1 = numDisp(self, self.numOff)
        I2 = letDisp(self, self.letOff)
        I2 = numDisp(self, self.numOff)
        
    # method to control turns
    def turn(self):
        if (self.player == 1):
            I1.moveFire()
            I1.aimSonar()
            I1.moveFire()
        
        elif (self.player == 2):
            I2.moveFire()
            I2. aimSonar()
            I2.moveFire()

# input class
class Inputs(Control):
   
   # CLASS INSTANTIATION
    def __init__(self, let, num, coordinate, sonarStrength, sonarDirection):
        Control.__init__(self, player, playerPhase)
    
        self.let = []
        self.num = []
        self.coordinate = [0, 0]
        self.sonarStrength = 0
        self.sonarDirection = 0
    
    # GETTERS/SETTERS
    @property
    def let(self):
        return self._let
    @let.setter
    def let(self, value):
        self.let = value
        
    @property
    def num(self):
        return self._num
    @num.setter
    def num(self, value):
        self.num = value
    
    @property
    def sonarStrength(self):
        return self._sonarStrength
    @sonarStrength.setter
    def sonarStrength(self, value):
        self.sonarStrength = value
        
    @property
    def sonarDirection(self):
        return self._sonarDirection
    @sonarDirection.setter
    def sonarDirection(self, value):
        self.sonarDirection = value
    
    # method to control moving submarine and firing missile        
    def moveFire(self):
        # player 1 inputs
        if (self.player == 1):
            while True:
                
                # A/1 button
                if (pin0p1 == 0 and pin10p1 == 0):
                    self.let = self.letA
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "A"
                elif (pin0p1 == 0 and pin11p1 == 0):
                    self.num = self.num1
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 1
                
                # B/2 button
                if (pin1p1 == 0 and pin10p1 == 0):
                    self.let = self.letB
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "B"
                elif (pin1p1 == 0 and pin11p1 == 0):
                    self.num = self.num2
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 2
                
                # C/3 button    
                if (pin2p1 == 0 and pin10p1 == 0):
                    self.let = self.letC
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "C"
                elif (pin2p1 == 0 and pin11p1 == 0):
                    self.num = self.num3
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 3
                
                # D/4 button    
                if (pin3p1 == 0 and pin10p1 == 0):
                    self.let = self.letD
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "D"
                elif (pin3p1 == 0 and pin11p1 == 0):
                    self.num = self.num4
                    self.numDisp(self, self.let)
                    self.coordinate[1] = 4
                
                # E/5 button    
                if (pin4p1 == 0 and pin10p1 == 0):
                    self.let = self.letE
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "E"
                elif (pin4p1 == 0 and pin11p1 ==0):
                    self.num = self.num5
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 5
                
                # F/6 button    
                if (pin5p1 == 0 and pin10p1 == 0):
                    self.let = self.letF
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "F"
                elif (pin5p1 == 0 and pin11p1 ==0):
                    self.num = self.num6
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 6
                
                # G/7 button
                if (pin6p1 == 0 and pin10p1 == 0):
                    self.let = self.letG
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "G"
                elif (pin6p1 == 0 and pin11p1 ==0):
                    self.num = self.num7
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 7
                
                # H/8 button
                if (pin7p1 == 0 and pin10p1 == 0):
                    self.let = self.letH
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "H"
                elif (pin7p1 == 0 and pin11p1 ==0):
                    self.num = self.num8
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 8
                
                # I/9 button
                if (pin8p1 == 0 and pin10p1 == 0):
                    self.let = self.letI
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "I"
                elif (pin8p1 == 0 and pin11p1 ==0):
                    self.num = self.num9
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 9
                
                # J/0 (10) button
                if (pin9p1 == 0 and pin10p1 == 0):
                    self.let = self.letJ
                    self.letDisp(self, self.let)
                    self.coordinate[0] = "J"
                elif (pin6p1 == 0 and pin11p1 ==0):
                    self.num = self.num0
                    self.numDisp(self, self.num)
                    self.coordinate[1] = 0
                
                # player 1 confirmation
                if (confirmP1 == 1):
                    return I1.confirm(self.coordinate, self.playerPhase)
        
        # player 2 inputs
        elif (self.player == 2):
            while True:
            
            # A/1 button
            if (pin0p2 == 0 and pin10p2 == 0):
                self.let = self.letA
                self.letDisp(self, self.let)
                self.coordinate[0] = "A"
            elif (pin0p2 == 0 and pin11p2 == 0):
                self.num = self.num1
                self.numDisp(self, self.num)
                self.coordinate[1] = 1
            
            # B/2 button    
            if (pin1p2 == 0 and pin10p2 == 0):
                self.let = self.letB
                self.letDisp(self, self.let)
                self.coordinate[0] = "B"
            elif (pin1p2 == 0 and pin11p2 == 0):
                self.num = self.num2
                self.numDisp(self, self.num)
                self.coordinate[1] = 2
            
            # C/3 button    
            if (pin2p2 == 0 and pin10p2 == 0):
                self.let = self.letC
                self.letDisp(self, self.let)
                self.coordinate[0] = "C"
            elif (pin2p2 == 0 and pin11p2 == 0):
                self.num = self.num3
                self.numDisp(self, self.num)
                self.coordinate[1] = 3
            
            # D/4 button    
            if (pin3p2 == 0 and pin10p2 == 0):
                self.let = self.letD
                self.letDisp(self, self.let)
                self.coordinate[0] = "D"
            elif (pin3p2 == 0 and pin11p2 == 0):
                self.num = self.num4
                self.numDisp(self, self.let)
                self.coordinate[1] = 4
            
            # E/5 button    
            if (pin4p2 == 0 and pin10p2 == 0):
                self.let = self.letE
                self.letDisp(self, self.let)
                self.coordinate[0] = "E"
            elif (pin4p2 == 0 and pin11p2 ==0):
                self.num = self.num5
                self.numDisp(self, self.num)
                self.coordinate[1] = 5
            
            # F/6 button    
            if (pin5p2 == 0 and pin10p2 == 0):
                self.let = self.letF
                self.letDisp(self, self.let)
                self.coordinate[0] = "F"
            elif (pin5p2 == 0 and pin11p2 ==0):
                self.num = self.num6
                self.numDisp(self, self.num)
                self.coordinate[1] = 6
            
            # G/7 button
            if (pin6p2 == 0 and pin10p2 == 0):
                self.let = self.letG
                self.letDisp(self, self.let)
                self.coordinate[0] = "G"
            elif (pin6p2 == 0 and pin11p2 ==0):
                self.num = self.num7
                self.numDisp(self, self.num)
                self.coordinate[1] = 7
            
            # H/8 button
            if (pin7p2 == 0 and pin10p2 == 0):
                self.let = self.letH
                self.letDisp(self, self.let)
                self.coordinate[0] = "H"
            elif (pin7p2 == 0 and pin11p2 ==0):
                self.num = self.num8
                self.numDisp(self, self.num)
                self.coordinate[1] = 8
            
            # I/9 button
            if (pin8p2 == 0 and pin10p2 == 0):
                self.let = self.letI
                self.letDisp(self, self.let)
                self.coordinate[0] = "I"
            elif (pin8p2 == 0 and pin11p2 ==0):
                self.num = self.num9
                self.numDisp(self, self.num)
                self.coordinate[1] = 9
            
            # J/0 (10) button
            if (pin9p2 == 0 and pin10p2 == 0):
                self.let = self.letJ
                self.letDisp(self, self.let)
                self.coordinate[0] = "J"
            elif (pin6p2 == 0 and pin11p2 ==0):
                self.num = self.num0
                self.numDisp(self, self.num)
                self.coordinate[1] = 0
            
            # player 2 confirmation    
            if (confirmP2 == 1):
                return I2.confirm(self.coordinate, self.playerPhase)

    def aimSonar(self):
        
        # player 1 sonar
        if (self.player == 1):
            while True:
                self.sonarStrength = slideP1.voltage
                self.sonarDirection = potP1.voltage
                sleep(.5)
        
                if (confirmP1 == 1):
                    return I1.confirmSonar(self.sonarDirection, self.sonarStrength)
        
        #player 2 sonar
        if (self.player == 2):
            while True:
                self.sonarStrength = slideP2.voltage
                self.sonarDirection = potP2.voltage
                sleep(.5)
                
                if (confirmP2 == 1):
                    return I2.confirmSonar(self.sonarDirection, self.sonarStrength)
                    
    def confirm(self, self.coordinate, self.sonarDirection):
        
        # return for moving submarine
        if (self.playerPhase == 1):
            self.playerPhase += 1
            print("You moved your submarine to coordinates ({},{})!"\
                    .format(self.coordinate[0], self.coordinate[1]))
        
        # return for firing a missile
        elif (self.playerPhase == 3):
            self.playerPhase = 1
            print("You fired a missle at coordinates ({},{})!"\
                    .format(self.coordinate[0], self.coordinate[1]))
    
    def confirmSonar(self, self.sonarDirection, self.sonarStrength):
        
        # return for aiming and choosing intensity of sonar
        if (self.playerPhase == 2):
            self.playerPhase += 1
            print("You aimed the sonar at {} degrees with {} intensity" \
                .format(self.sonarDirection, self.sonarStrength))
