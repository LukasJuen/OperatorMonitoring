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
        elapsed = time.time()-prev #Verstrichene Zeit, seit dem letzen Gesichtserkennen       
    else:
        elapsed = time.time()-prev #Verstrichene Zeit, seit dem letzen Gesichtserkennen
        
    return prev, elapsed

def set_buzzer(status, pin, last_timer, gap, flag):
    if status == 3:
        GPIO.output(pin,GPIO.HIGH)
    elif status == 2:
        if flag == True:
            if  time.time()  > gap + last_timer:
                GPIO.output(pin,GPIO.LOW)
                flag = False
                last_timer = time.time()
        else:
            if time.time() > gap + last_timer:
                GPIO.output(pin,GPIO.HIGH)
                flag = True
                last_timer = time.time()
    else:
        GPIO.output(pin, GPIO.LOW)
    return flag, last_timer

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

def get_danger(pin): #input als Liste, überprüfen, falls einer error anzeigt, ausgabe als error
    j = 0
    for i in pin:
        if GPIO.input(i) == 1:
            j += 1
    if j > 0:
        return True
    else:
        return False

