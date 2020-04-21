""" This is the Menu code to help facilitate the functionality of the prototype - Henrik"""

import Servo, time, turtle, Camera
wn = turtle.Screen()
wn.screensize(1073, 606)

class menu:
    def __init__(self):
        self = 0

    def Menulook(self):
        wn.bgpic("bgpicturetrue.png")

    def ManualMenu(self):
        wn.bgpic("bgpicturefalsk.png")


#Yes I know it calls instances of other classes, but this OO... Grrr
def freeMove():
    time.sleep(1)
    wn.listen()
    wn.clearscreen()
    myMenu.Menulook()
    wn.onkey(ManualMove, 'b')
    wn.onkey(Servo.Servos.Startposition, 'o')
    wn.onkey(Servo.Servos.Suvalliance, "p")
    wn.onkey(Camera.myCamera.MotionDetect, 'm')
    wn.onkey(Camera.myCamera.FaceDetect, 'k')

def ManualMove():
    wn.clearscreen()
    myMenu.ManualMenu()
    wn.onkey(Servo.Servos.MoveMeLeft, "a")
    wn.onkey(Servo.Servos.MoveMeDown, "s")
    wn.onkey(Servo.Servos.MoveMeRight, "d")
    wn.onkey(Servo.Servos.MovemeUp, "w")
    wn.onkey(freeMove, 'x')


myMenu = menu()
freeMove()

turtle.done()
