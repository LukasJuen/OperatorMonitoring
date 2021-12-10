import cv2 as cv
#import RPi.GPIO as GPIO

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
    
    #Falls Gesicht, etwas tun
    if face_flag:
        print('face found')
    else:
        print('no face')

    #Zeige das Bild
    cv.imshow('Detected Faces', frame)

    #face-flag ausgeben
    return face_flag


def setoutput(outputflag, buzzer):
        #Falls Gesicht, etwas tun
    #if outputflag:
        #GPIO.output(buzzer,GPIO.LOW)
    #else:
        #GPIO.output(buzzer,GPIO.HIGH)
    return 0