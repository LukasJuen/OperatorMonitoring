#pylint:disable=no-member
#Bibliotheken laden
import cv2 as cv
import time
import functions
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

#Definierung von Zeitvariablen
previous_time = time.time()
warning_gap = 20
emergency_gap = 60



#Schleife die permanent ausgeführt wird, evtl auslagerbar in Funktion?
while True:
    # Gesicht erkennen
    face_flag = functions.getface(capture, haar_cascade)

    #Zeitvariablen befüllen
    if face_flag:
        previous_time = time.time() #Zeit, seit dem letzten Erkennen eines Gesichtes
    else:
        elapsed_time = time.time()-previous_time

    #Buzzer einschalten, falls erforderlich
    if elapsed_time > emergency_gap:
        break

    # Buzzer 
    if elapsed_time > warning_gap:
        functions.setoutput(True, buzzer)
    else:
        functions.setoutput(False, buzzer)

    #Abbruchbedingung um aus While auszubrechen, für Testzwecke
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

# Nach While, Kamerazugriff lösen und alle Fenster schließen.
capture.release()
cv.destroyAllWindows()

# Stop Buzzer
GPIO.cleanup()
