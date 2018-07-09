from __future__ import print_function
import requests

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import qrcode
from picamera import PiCamera

import os
import time
import sys
import RPi.GPIO as GPIO

#IMPORT MOTOR
sys.path.insert(0, '/home/pi/ZeroBorg')
import ZeroBorg
import socket

#Init generaux
GPIO.setwarnings(False)
GPIO.cleanup()


PinSensors = (31,32,33,35,36,37,38,40)
Seuil = 12

GPIO.setmode(GPIO.BOARD)

#Capteur de ligne
timeout=200

GPIO.setup(29,GPIO.OUT)
GPIO.output(29,GPIO.HIGH)

#Bouton Start Stop
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



ZB = ZeroBorg.ZeroBorg()
ZB.Init()





#ip = socket.gethostbyname(socket.gethostname())
ip = "10.4.0.5"
while 1:
    if GPIO.input(13) == 1:
        

        delay = [0,0,0,0,0,0,0,0]
        
        bigger = 0
        
        
        GPIO.setup(PinSensors,GPIO.OUT)
        
        GPIO.output(PinSensors,GPIO.HIGH)
        

        time.sleep(0.00006)

        GPIO.setup(PinSensors,GPIO.IN)

       
        
        for x in range(timeout):
            for pin in range(0,8):
                if delay[pin] == 0:
                    value = GPIO.input(PinSensors[pin])
                    if value == 0:
                        delay[pin] = x
                        if bigger < x:
                            bigger = x
         
        
            time.sleep(0.00001)

      
        print(delay[0])
        print(delay[1])
        print(delay[2])
        print(delay[3])
        print(delay[4])
        print(delay[5])
        print(delay[6])
        print(delay[7])
        
        
        if delay[0] > Seuil and delay[2] > Seuil and delay[4] > Seuil and delay[5] > Seuil and delay[7] > Seuil:
            bigger = 0

        if bigger > Seuil:
            
            if delay[7] == bigger or delay[6] == bigger or delay[5] == bigger or delay[4] == bigger or delay[3] == bigger or delay[2] == bigger or delay[1] == bigger or delay[0] == bigger  :
                
                ZB.MotorsOff()

                r = requests.post("http://10.4.0.49:1337/receiveData/", json={"type":"demitour","status":"OK","ip":ip})
    
                if r.status_code == 200:
                    print('Success')
                    exit()
                else :
                    print('Fail Send')
        else:
            
            ZB.SetMotor1(1)
            ZB.SetMotor2(1)
            ZB.SetMotor3(-0.8)
            ZB.SetMotor4(-0.8)


