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



#Schleife die permanent ausgeführt wird, evtl auslagerbar in Funktion?
while True:

    face_flag = functions.getface(capture, haar_cascade)
    functions.setoutput(face_flag, buzzer)

    #Abbruchbedingung um aus While auszubrechen
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

# Nach While, Kamerazugriff lösen und alle Fenster schließen.
capture.release()
cv.destroyAllWindows()

# Stop Buzzer
GPIO.cleanup()
