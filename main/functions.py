import cv2 as cv
import time
import RPi.GPIO as GPIO

def getface(capture, haar_cascade) :
     #Ein Bild aus dem Stream laden
    isTrue, frame = capture.read()
    
    #Bild in graues Bild wandeln
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    #Gesichter suchen, diese Gegebenenfalls in Variable faces_rect speichern
    faces_rect = haar_cascade.detectMultiScale(gray,1.1,8)

    face_flag = False
    #für jedes gefundene Gesicht ein Rechteck zeichnen
    for (x,y,w,h) in faces_rect:
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=2)
        face_flag = True

    #Zeige das Bild
    cv.imshow('Detected Faces', frame)

    #face-flag ausgeben
    return face_flag

def set_timers(flag, prev, elapsed):
    if flag:
        prev = time.time() #Zeit, seit dem letzten Erkennen eines Gesichtes       
    else:
        elapsed = time.time()-prev #Verstrichene Zeit, seit dem letzen Gesichtserkennen
        
    return prev, elapsed

def set_buzzer(status, buzzer):
    if status == 2:
        GPIO.output(buzzer,GPIO.HIGH)
    else:
        GPIO.output(buzzer,GPIO.LOW)
    return 0

def set_led(status, red, yellow, green):
    if status == 1:
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)
    elif status == 2:
        GPIO.output(yellow, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)
    elif status == 3:
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(yellow, GPIO.LOW)
    elif status == 0:
        GPIO.output(green, GPIO.LOW)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)

    return 0