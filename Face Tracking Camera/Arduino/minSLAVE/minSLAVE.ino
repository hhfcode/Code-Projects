/*
   PanTiltDRC
   Arduino code to implement control of pan and tilt  using
        Two RC-servos
        One Arduino
        And a modified version of DRC - The Drogon Remote Control.
   Allow another device talking to us over the serial port to control the
  IO pins.
   DRC originally Copyright (c) 2012 Gordon Henderson
   Full details at:
   http://projects.drogon.net/drogon-remote-control/drc-protocol-arduino/
   Commands:
   @: 0x40 Ping          Send back #: 0x23
   0: 0x30 0xNN  Set servo position of servo on pin 2 to NN (degrees)
   0: 0x31 0xNN  Set servo position of servo on pin 3 to NN (degrees)
*************************************************************************
********
   This file is part of drcAduino:
   Drogon Remote Control for Arduino
   http://projects.drogon.net/drogon-remote-control/
   drcAduino is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   drcAduino is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with drcAduino.  If not, see <http://www.gnu.org/licenses/>.
*************************************************************************
********
*/
// Serial commands
#define CMD_PING        '@'
#define CMD_SERVO_PIN_2       '0'
#define CMD_SERVO_PIN_3       '1'
#include <Servo.h>

Servo pan,tilt;  // create servo object to control a servo
// twelve servo objects can be created on most boards

// buttonTest
#define S0 0
#define S1 1
#define S2 2
#define S3 3
#define S4 4
#define S5 5
int myState=S0, panSucces=0, tiltSucces=0, blinkCounter=0,timeCounter=0;
int pos = 0;

void setup ()
{

  Serial.begin (115200) ;
  Serial.println ("DRC Arduino 1.0") ;
  pan.attach(2);  // attaches the servo on pin 2 to the servo object
  tilt.attach(3);  // attaches the servo on pin 3 to the servo object
  pinMode(4, INPUT_PULLUP); //button
  pinMode(5, OUTPUT); //blinking LED
  pinMode(9, OUTPUT); //succes LED
  
}

int myGetchar ()
{
  int x ;
  while ((x = Serial.read ()) == -1)
    ;
  return x ;
}

void loop ()
{
  


  unsigned int pin ;
  unsigned int aVal, dVal ;
  int pos ;
  String panString ;
  String totalPan ;
  String tiltString ;
  String totalTilt ;
  for (;;)
  {
    testButtton();
    Serial.print("myState ");
    Serial.println(myState);
    delay(100); //10Hz
    if (Serial.available () > 0)
    {
      switch (myGetchar ())
      {
        case CMD_PING:
          Serial.write (CMD_PING) ;
          continue ;
        case CMD_SERVO_PIN_2: //pan
          pos  = myGetchar () ;
          if ((pos >= 0) && (pos <= 180))
            pan.write(pos);
            panString = String(pos);
            totalPan = "!P" + panString + "-" ;
            Serial.println(totalPan);
          continue ;
        case CMD_SERVO_PIN_3:  //tilt
          pos  = myGetchar () ;
          if ((pos >= 0) && (pos <= 180))
            tilt.write(pos);
            tiltString = String(pos);
            totalTilt = "!T" + tiltString + "-";
            Serial.println(totalTilt);  // Tilt banditen
          continue;
      }
    }
  }
}

void testButtton(){
  //transition
  switch(myState){
    case S0://standBy, button press to move on
            if(digitalRead(4) == 0){
              myState=S1;
            }
            else{
              myState=S0;
              digitalWrite(5,0);
              digitalWrite(9,0);
              timeCounter=0;
              blinkCounter=0;
                             
            }
            break;
    case S1://LED blinks 3 times, succes move to S2 else go to F1
            if (blinkCounter>=3){
              myState = S3;
            }
            else{
                myState = S2;
            }
            break;
    case S2:
              myState = S1;
              blinkCounter++;
            break;
    case S3://Pan test min/max succes go to S4 else go to F2
            if (panSucces = 1){
              myState = S4;
            }
            break;
    case S4://Tilt test min/max succes go to S5 else go to F3
            if (tiltSucces = 1){
              myState = S5;
            }
            break;
    
    case S5://Turn on succes LED, wait 5 sec and go to standBy
            if(timeCounter>=50){
              myState=S0;
            }
            else{
              timeCounter++;
            }
            break;
    
  }
  //output
  switch(myState){
    case S0:
            break;
    case S1: //blinking LED on
            digitalWrite(5,0);
            break;
    case S2://blinking LED off
            digitalWrite(5,1);
            break;
    case S3:
            for (pos = 15; pos <= 150; pos += 1) { // goes from 0 degrees to 180 degrees
              // in steps of 1 degree
              pan.write(pos);              // tell servo to go to position in variable 'pos'
              delay(15);                       // waits 15ms for the servo to reach the position
                }
            for (pos = 150; pos >= 15; pos -= 1) { // goes from 180 degrees to 0 degrees
              pan.write(pos);              // tell servo to go to position in variable 'pos'
              delay(15);                       // waits 15ms for the servo to reach the position
            }
            panSucces = 1;
            break;
    case S4:
            for (pos = 15; pos <= 150; pos += 1) { // goes from 0 degrees to 180 degrees
              // in steps of 1 degree
              tilt.write(pos);              // tell servo to go to position in variable 'pos'
              delay(15);                       // waits 15ms for the servo to reach the position
                }
            for (pos = 150; pos >= 15; pos -= 1) { // goes from 180 degrees to 0 degrees
              tilt.write(pos);              // tell servo to go to position in variable 'pos'
              delay(15);                       // waits 15ms for the servo to reach the position
            }
            tiltSucces = 1;
            break;
    case S5:
            digitalWrite(9,1);
            pan.write(72);
            tilt.write(72);
            break;
  }
}
