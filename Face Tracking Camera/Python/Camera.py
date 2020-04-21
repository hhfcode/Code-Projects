""" This is the Class for the Camera -- Henrik"""

import cv2, Servo, time
import numpy as np
from datetime import datetime


#Frame Setup is X, Y - WE CAN USE THIS DATA TO GET TO KNOW CENTRER AND CREATE A CENTRE SQUARE THAT we AIM TO ACHIEVE

FrameX = 1080 # 200 + and - should make a centrer box from half
FrameY = 640 # 100 + and - should make a centrer box from half

#This is the Class for Camera
class Camera:

    def __init__(self, frameWidth, frameHeight):
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

    def setupFrame(self):
        self.video = cv2.VideoCapture(1)
        Height = self.frameHeight, Width = self.frameWidth
        video = cv2.resize(Height, Width)
        self.check, self.frame = video.read()

#The next Class allows our camera to follow the action
#Yes I know this calls an instance of another class, Yes I know I suck, but it works and that matters more right now :(
    def actionFollower(self,horizon, verizon):
        if horizon <= 200:
            Servo.Servos.MoveMeLeft()
            time.sleep(0.1)

        if horizon >= 300:
            Servo.Servos.MoveMeRight()
            time.sleep(0.1)

        if verizon >= 140:
            Servo.Servos.MoveMeDown()
            time.sleep(0.1)

        if verizon <= 80:
            Servo.Servos.MovemeUp()
            time.sleep(0.1)

#This Method calls another module that is motion detection. It returns X and Y Coordinates that we then use to move around
#don't get me wrong, this is absolutely terrible OO code, but it works :(
    def MotionDetect(self):
        count = 0
        cv2.namedWindow('frame')
        cv2.namedWindow('dist')

        # capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
        cap = cv2.VideoCapture(1)

        _, frame1 = cap.read()
        _, frame2 = cap.read()

        facecount = 0
        while (True):

            sdThresh = 15
            font = cv2.FONT_HERSHEY_SIMPLEX
            # TODO: Face Detection 1



            _, frame3 = cap.read()
            rows, cols, _ = np.shape(frame3)
            cv2.imshow('dist', frame3)
            dist = distMap(frame1, frame3)

            frame1 = frame2
            frame2 = frame3

            # apply Gaussian smoothing
            mod = cv2.GaussianBlur(dist, (9, 9), 0)

            # apply thresholding
            _, thresh = cv2.threshold(mod, 100, 255, 0)

            # calculate st dev test
            _, stDev = cv2.meanStdDev(mod)

            cv2.imshow('dist', mod)
            cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0], 0)), (70, 70), font, 1,
                        (255, 0, 255), 1, cv2.LINE_AA)
            if stDev > sdThresh:
                print("Motion detected.. Do something!!!")
                name = "file-" + str(count)
                cv2.imwrite( 'C:\\private\\'+str(name)+'.jpg' , frame2 )
                print('took a picture' + str(datetime.now()))
                count += 1 # Accumilator
                time.sleep(2)
                # TODO: Face Detection 2

            cv2.imshow('frame', frame2)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    # don't get me wrong, this is absolutely terrible OO code, but it works :(
    def FaceDetect(self):
        import cv2
        import numpy as np

        cv2.namedWindow('frame')
        cv2.namedWindow('dist')

        # the classifier that will be used in the cascade
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

        # capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
        cap = cv2.VideoCapture(1)

        triggered = False
        sdThresh = 10
        font = cv2.FONT_HERSHEY_SIMPLEX

        _, frame1 = cap.read()
        _, frame2 = cap.read()
        facecount = 0
        while (True):
            _, frame3 = cap.read()
            rows, cols, _ = np.shape(frame3)
            cv2.imshow('dist', frame3)
            dist = distMap(frame1, frame3)

            frame1 = frame2
            frame2 = frame3

            # apply Gaussian smoothing
            mod = cv2.GaussianBlur(dist, (9, 9), 0)

            # apply thresholding
            _, thresh = cv2.threshold(mod, 100, 255, 0)

            # calculate st dev test
            _, stDev = cv2.meanStdDev(mod)

            cv2.imshow('dist', mod)
            cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0], 0)), (70, 70), font, 1,
                        (255, 0, 255), 1, cv2.LINE_AA)

            if stDev > sdThresh:
                # the cascade is implemented in grayscale mode
                gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

                # begin face cascade
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=2, minSize=(20, 20))
                facecount = 0
                # draw a rectangle over detected faces
                for (x, y, w, h) in faces:
                    print(x,y)
                    self.actionFollower(x,y)
                    facecount = facecount + 1
                    cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    cv2.putText(frame2, "No of faces {}".format(facecount), (50, 50), font, 1, (0, 0, 255), 1,
                                cv2.LINE_AA)
                else:
                    if facecount > 0:
                        #print("Face count:")
                        #print(facecount)
                        facecount = 0
                cv2.imshow('frame', frame2)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist


myCamera = Camera(640,480)



















