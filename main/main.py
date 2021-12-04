#pylint:disable=no-member
#Bibliotheken laden
import cv2 as cv
import time
import RPi.GPIO as GPIO

# Definierungen fuer GPIO (Buzzer)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=4
GPIO.setup(buzzer,GPIO.OUT)

#Definieren der haar-cascade zur Gesichtserkennung
haar_cascade = cv.CascadeClassifier('haar_face.xml')
#Laden des Kamerastreams an Stelle 0, in unserem Fall Kamera ueber Breitbandkabel, Legacy Modus erforderlich!
capture = cv.VideoCapture(0)



#Schleife die permanent ausgeführt wird, evtl auslagerbar in Funktion?
while True:
    #Ein Bild aus dem Stream laden
    isTrue, frame = capture.read()
    
    #Bild in graues Bild wandeln
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    #Gesichter suchen, diese Gegebenenfalls in Variable faces_rect speichern
    faces_rect = haar_cascade.detectMultiScale(gray,1.1,8)
    
    
    face_erkannt = False
    #für jedes gefundene Gesicht ein Rechteck zeichnen
    for (x,y,w,h) in faces_rect:
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=2)
        face_erkannt = True
    
    #Falls Gesicht, etwas tun
    if face_erkannt:
        print('face found')
        GPIO.output(buzzer,GPIO.LOW)
    else:
        print('no face')
        GPIO.output(buzzer,GPIO.HIGH)


    #Zeige das Bild
    cv.imshow('Detected Faces', frame)
    
    #Abbruchbedingung um aus While auszubrechen
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

# Nach While, Kamerazugriff lösen und alle Fenster schließen.
capture.release()
cv.destroyAllWindows()

cv.waitKey(0)

# Stop Buzzer
GPIO.cleanup()
