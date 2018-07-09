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


#Init generaux
GPIO.setwarnings(False)
GPIO.cleanup()


decoded = 0

PinSensors = (31,32,33,35,36,37,38,40)
Seuil = 12

GPIO.setmode(GPIO.BOARD)

#Capteur Ultra son
PinTrig = 7
PinEcho = 11
GPIO.setup(PinTrig,GPIO.OUT)
GPIO.setup(PinEcho,GPIO.IN)
GPIO.output(PinTrig,False)

#Capteur de ligne
timeout=200

GPIO.setup(29,GPIO.OUT)
GPIO.output(29,GPIO.HIGH)

#Moteur
ZB = ZeroBorg.ZeroBorg()
ZB.Init()

#Bouton Start Stop
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ip = "10.4.0.5"

#speed = 0.90
#speedReduct = 0.10

#Definition des methodes
def maxiDroite():
    ZB.SetMotor1(-0.90)
    ZB.SetMotor2(-0.90)
    ZB.SetMotor3(1)
    ZB.SetMotor4(1)
    return
def droite():
    ZB.SetMotor1(0)
    ZB.SetMotor2(0)
    ZB.SetMotor3(0.90)
    ZB.SetMotor4(0.90)
    return
def miDroite():
    ZB.SetMotor1(0)
    ZB.SetMotor2(0)
    ZB.SetMotor3(0.85)
    ZB.SetMotor4(0.85)
    return
def millieu():
    ZB.SetMotor1(0.80)
    ZB.SetMotor2(0.80)
    ZB.SetMotor3(0.80)
    ZB.SetMotor4(0.80)
    return
def miGauche():
    ZB.SetMotor1(0.85)
    ZB.SetMotor2(0.85)
    ZB.SetMotor3(0)
    ZB.SetMotor4(0)
    return
def gauche():
    ZB.SetMotor1(0.90)
    ZB.SetMotor2(0.90)
    ZB.SetMotor3(0)
    ZB.SetMotor4(0)
    return
def maxiGauche():
    ZB.SetMotor1(1)
    ZB.SetMotor2(1)
    ZB.SetMotor3(-0.90)
    ZB.SetMotor4(-0.90)
    return

def Stop():
    ZB.SetMotor1(0)
    ZB.SetMotor2(0)
    ZB.SetMotor3(0)
    ZB.SetMotor4(0)
    return

def CroisementGauche():
    MilieuTiming(0.5);
    time.sleep(0.5)
    ZB.SetMotor1(1)
    ZB.SetMotor2(1)
    ZB.SetMotor3(-1)
    ZB.SetMotor4(-1)
    time.sleep(0.64)
    Stop();
    time.sleep(0.5)
    MilieuTiming(0.5);
    time.sleep(0.5)
                
    

def CroisementDroite():
    MilieuTiming(0.5);
    time.sleep(0.5)
    ZB.SetMotor1(-1)
    ZB.SetMotor2(-1)
    ZB.SetMotor3(1)
    ZB.SetMotor4(1)
    time.sleep(0.64)
    Stop();
    time.sleep(0.5)
    MilieuTiming(0.5);
    time.sleep(0.5)

def CroisementMilieu():
    MilieuTiming(0.5);
    time.sleep(0.5)
    MilieuTiming(0.5);
    time.sleep(0.5)

    
    
def MilieuTiming(timing):
    ZB.SetMotor1(0.95)
    ZB.SetMotor2(0.95)
    ZB.SetMotor3(0.95)
    ZB.SetMotor4(0.95)
    time.sleep(timing)
    Stop();

def Demitour():
    ZB.SetMotor1(-1)
    ZB.SetMotor2(-1)
    ZB.SetMotor3(1)
    ZB.SetMotor4(1)
    time.sleep(1)
    

#Methode pour camera
def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  
 
  # Print results
  for obj in decodedObjects:

    print(obj.data)
    print("DECODE")
    decoded = 1
    
    requests.post("http://10.4.0.49:1337/receiveData/", data={"type":"QRCODE","value":obj.data,"ip":ip})
    
    print("coucou")
    sys.exit()
    
    if r.status_code == 200:
        print('Success')
    else :
       print('Fail')

    
    #print('On va kill le process')
    #os.system("sh killAll.sh")
    #print('Killed')
    
    #raise SystemExit

    #if this == that:
        #quit()

        
    #Prevenir le serveur du Qr code qu'on vient de rencontrer
     
  return decodedObjects



  


#0 pour droite 1 pour gauche
LastLine = 2
StackRight = 0
StackLeft = 0
        
while 1:

    #Si bouton de marche active
    if GPIO.input(13) == 1:
        #print("Bouton one")
        
        #Verification obstacle
        GPIO.output(PinTrig,True)
        time.sleep(0.00001)
        GPIO.output(PinTrig,False)

        while GPIO.input(PinEcho) == 0:
            debutImpulsion = time.time()

        while GPIO.input(PinEcho) == 1:
            finImpulsion = time.time()

        distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2,1)

        #Si obstacle alors stop
        if distance < 25 :
            #print("obstacle")
            Stop();
            

            
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

                
        print(Seuil)
        print('SEUIL')
        print(delay[0])
        print(delay[1])
        print(delay[2])
        print(delay[3])
        print(delay[4])
        print(delay[5])
        print(delay[6])
        print(delay[7])

        
        if  delay[1] > Seuil and delay[2] > Seuil and delay[3] > Seuil and delay[4] > Seuil:
            bigger = 0

        #print (bigger)
            
        if bigger > Seuil:
            #print("ligne")
            if delay[0] == bigger:
                #print("MaxiDroite")
                LastLine = 0
                StackRight = 10

                #print("LINE = 0")
                maxiDroite();
            elif delay[1] == bigger:
                #print("Droite")
                LastLine = 0
                StackRight = 10
                droite();
            elif delay[2] == bigger:
                #print("Midroite")
                LastLine = 0
                StackRight = 10
                miDroite();
            elif delay[3] == bigger:
                #print("Millieu")
                millieu();
            elif delay[4] == bigger:
                #print("Millieu")
                millieu();
            elif delay[5] == bigger:
                #print("Migauche")
                LastLine = 1
                StackLeft = 10
                miGauche();
            elif delay[6] == bigger:
                #print("Gauche")
                LastLine = 1
                StackLeft = 10
                gauche();
            elif delay[7] == bigger:
                #print("MaxiGauche")
                #print("LINE = 1")
                LastLine = 1
                StackLeft = 10
                maxiGauche();
        else :
            if bigger == 0 :
                Stop();
                #Commencer a lire
                
                MilieuTiming(0.1);

                LastLine = 2
        
                camera = PiCamera()
                camera.start_preview()
                
                
                while decoded == 0:
    
                    #print("pas ligne")
                
                    camera.capture('frame.jpg')
                    print ('Creating... frame.jpg')
                    im = cv2.imread('frame.jpg')
                    decodedObjects = decode(im);
       
                  
                    #simulation virage gauche
                
                    #CroisementGauche()
                if decoded == 1:
                    
                    camera.stop_preview()
                    camera.close()
                    sys.exit()
                 
            else :
                if LastLine == 0:
                    StackRight = StackRight - 1
                    if(StackRight == 0):
                        LastLine = 2
                        maxiDroite();
                    
                elif LastLine == 1 :
                    StackLeft = StackLeft - 1
                    if(StackLeft == 0):
                        LastLine = 2
                        maxiGauche();
                
                
                
                

                else :
                    #print("bouton off")
                    Stop();
            
        



