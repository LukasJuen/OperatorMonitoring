#pylint:disable=no-member
#Bibliotheken laden
import cv2 as cv
import time
import functions
import RPi.GPIO as GPIO
from main.functions import set_timers

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
elapsed_time = 0
warning_gap = 10
emergency_gap = 15

#statusflags definieren, 0=keine Überprüfung, 1= Gefahrenquelle erkannt, Gesicht checken, 2= Gesicht zu lange nicht da, Warnung, 3=Ausschalten
danger_status = 0


#Schleife die permanent ausgeführt wird, evtl auslagerbar in Funktion?
while True:
    #HIER CODE EINSETZEN FÜR GPIO UND STATUS von 0 auf 1
    #
    #if gefahrengpio == False and danger_status!=3:
        #danger_status = 0

    #if gefahrengpio == True and danger_status = 0:
        #danger_status = 1
    ##


    if danger_status == 1:
        # Gesicht erkennen
        face_flag = functions.getface(capture, haar_cascade)
        #Zeitvariablen befüllen
        previous_time, elapsed_time = set_timers(face_flag, previous_time, elapsed_time)

        if elapsed_time > warning_gap: #Falls zu lange Zeit verstrichen, Status ändern
            danger_status = 2

    if danger_status == 2:
        # Buzzer hier evtl?
        # Gesicht erkennenung trotzdem fortsetzen
        face_flag = functions.getface(capture, haar_cascade)
        #Zeitvariablen befüllen
        previous_time, elapsed_time = set_timers(face_flag, previous_time, elapsed_time)

        #Status wechseln gegebenenfalls
        if elapsed_time > emergency_gap:
            danger_status = 3 #Abschaltung, falls zu lange gedauert
        elif elapsed_time < warning_gap: #Falls gesicht erkannt, wieder zurück auf status 1
            danger_status = 1

    if danger_status == 3:
        #HIER IRGENDWAS AUSSCHALTEN
        #HIER ALLE LED BLINKEN LASSEN 
        print('gagge')

    print(danger_status)

    #Abbruchbedingung um aus While auszubrechen, für Testzwecke
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

# Nach While, Kamerazugriff lösen und alle Fenster schließen.
capture.release()
cv.destroyAllWindows()

# Stop Buzzer
GPIO.cleanup()
