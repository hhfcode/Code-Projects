"""This Is the Module for controlling the Servos, Group 6 - Henrik"""

#Our Servos have a range of 15-165. That gives us around 150 Degrees to play with for the Camera.
# THE MOVEMENTS SHOULD NOT EXCREED OR GO BELOW THESE VALUES!!!!!!!!

import time
import serial
import turtle

wn = turtle.Screen()

pan = 48
tilt = 49
startPos = 72


#delete everything below until class when combinding modules
ser = serial.Serial()

ser.baudrate = 115200
ser.port = 'COM4'
ser.open()

print("send @")
ser.write(bytearray([64]))

print("pos 10")
ser.write(bytearray([pan,10]))
time.sleep(1)

print("pos 10")
ser.write(bytearray([tilt,10]))
time.sleep(1)

time.sleep(1)

#This is a Class that controls the Servos. Allows User to input data to move around the servos
#A Manual Control is also implemented in this class, which won't be part of the fully automatic code.
class servo:
    def __init__(self):
        self = 0
#The Movement, Getters and Setters are the most crucial for this project
    def Panmove(self, PanMove):
        self.PanMove = PanMove #Putting the Value into a self.panmove allows getters to access
        ser.write(bytearray([pan,PanMove])) #This line writes to Pan - The Degrees it will be put at.
        self.setPan(PanMove)

    def Tiltmove(self, TiltMove):
        self.TiltMove = TiltMove
        ser.write(bytearray([tilt, TiltMove]))
        self.setTilt(TiltMove)

#The Return Methods are Getters. Mostly used for Debugging and manual control
    def ReturnPan(self):
        return self.PanMove

    def ReturnTilt(self):
        return self.TiltMove

#The Setters are below, mostly used for debugging and manual control
    def setTilt(self, number):
        self.TiltMove = number

    def setPan(self, number2):
        self.PanMove = number2

#Below is the Manual control methods - Comments for first examply only
    def MovemeUp(self):
        myTilt = self.ReturnTilt()       # Get current position
        newPos = myTilt - 1          # 2 is used as a low degree that gives stability when manual control is active
        self.Tiltmove(newPos)  # Camera movement happens here
        self.setTilt(newPos)               # Set new position

    def MoveMeLeft(self):
        MyPan = self.ReturnPan()
        newPan = MyPan + 2
        ser.write(bytearray([pan, newPan]))
        self.setPan(newPan)


    def MoveMeRight(self):
        myPan = self.ReturnPan()
        NewPan = myPan - 2
        self.Panmove(NewPan)
        self.setTilt(NewPan)

    def MoveMeDown(self):
        mytilt = self.ReturnTilt()
        NewTilt = mytilt + 1
        self.Tiltmove(NewTilt)
        self.setPan(NewTilt)

#Last is the Start Position - Returns Servos to the med position.
    def Startposition(self):
        ser.write(bytearray([pan, startPos]))
        ser.write(bytearray([tilt, startPos]))
        self.setPan(startPos)
        self.setTilt(startPos)

    def Suvalliance(self):
        Surv = 1
        myAccumilator = 0
        while Surv == 1:
            self.Tiltmove(90)

            for pos in range(20, 150, 2):
                Servos.Panmove(pos)
                time.sleep(0.3)

            self.Tiltmove(60)

            for pos in range(20, 150, 2):
                Servos.Panmove(pos)
                time.sleep(0.3)
            myAccumilator += 1
            if myAccumilator == 30:
                Surv = 0


Servos = servo()

#for pos in range( 20, 150, 2):
    #Servos.Panmove(pos)
    #time.sleep(0.1)

Servos.Tiltmove(70)

#for pos in range ( 20, 150, 2):
    #Servos.Panmove(pos)
    #time.sleep(0.1)

#for pos in range( 20, 150, 2):
    #Servos.Tiltmove(pos)
    #time.sleep(0.1)



ser.write(bytearray([49,100]))
Servos.Tiltmove(25)
time.sleep(0.1)

Servos.Startposition()

#Here we read the Serial from the Arduino, this deserves it's class of it's own, but time cut it down
def serialReader():
    while True:
        nowPos = ser.readline()
        decodeNTP = nowPos.decode()
        stringNTP = decodeNTP.rstrip()
        Servos.Tiltmove(50)
        print(stringNTP)
        if ('!P' in stringNTP):
            print('Pan is at ' + (stringNTP[2:len(stringNTP) - 1]))
            #myString = stringNTP.lstrip("!P")
            #Mypan = myString.rstrip("-")
            #print('Pan is at ' + Mypan)
        elif ('!T' in stringNTP):
            print('Tilt is at ' + (stringNTP[2:len(stringNTP) - 1]))
            #mystrtilt = stringNTP.lstrip("!T")
            #mytilt = mystrtilt.rstrip("-")
            #print('Tilt is at ' + mytilt)

        else:
            print('Error, no string received')



