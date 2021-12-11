#pylint:disable=no-member
#Bibliotheken laden
import cv2 as cv
import time
import functions
import RPi.GPIO as GPIO

# Definierungen fuer GPIO ##################################################################
# (Buzzer)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzerpin=4
GPIO.setup(buzzerpin,GPIO.OUT)

# GPIO LED
led_rot = 17
GPIO.setup(led_rot,GPIO.OUT)
led_gelb = 27
GPIO.setup(led_gelb,GPIO.OUT)
led_grün = 22
GPIO.setup(led_grün,GPIO.OUT)

#GPIO danger
danger_gpio = True #hier noch input definieren für arduino oder sensoren
external_pins = (23, 24)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
hauptschalter_pin = 18 #gpio des Hauptschalters lesen
GPIO.setup(hauptschalter_pin,GPIO.IN)

#GPIO RELAIS
relaispin = 26
GPIO.setup(relaispin,GPIO.OUT)
###########################################################################################



#Definieren der haar-cascade zur Gesichtserkennung
haar_cascade = cv.CascadeClassifier('haar_face.xml')
#Laden des Kamerastreams an Stelle 0, in unserem Fall Kamera ueber Breitbandkabel, Legacy Modus erforderlich!
capture = cv.VideoCapture(0)

#Definierung von Zeitvariablen
previous_time = time.time()
elapsed_time = 0
warning_gap = 10
emergency_gap = 15

#blinken variablen für buzzer
buzz_timer = 0
buzzgap = 0.25
buzzflag = False

#statusflags definieren, 0=keine Überprüfung, 1= Gefahrenquelle erkannt, Gesicht checken, 2= Gesicht zu lange nicht da, Warnung, 3=Ausschalten
danger_status = 0


#Schleife die permanent ausgeführt wird, evtl auslagerbar in Funktion?
while True:
    if GPIO.input(hauptschalter_pin) == 1:
        danger_gpio = functions.get_danger(external_pins) #externe Gefahrenquelle finden
        if danger_gpio == False and danger_status!=3:
            danger_status = 0
            previous_time = time.time()
            elapsed_time = 0


        if danger_gpio == True and danger_status == 0:
            danger_status = 1


        if danger_status == 1:
            # Gesicht erkennen
            face_flag = functions.getface(capture, haar_cascade)
            #Zeitvariablen befüllen
            previous_time, elapsed_time = functions.set_timers(face_flag, previous_time, elapsed_time)

            if elapsed_time > warning_gap: #Falls zu lange Zeit verstrichen, Status ändern
                danger_status = 2

        if danger_status == 2:
            # Gesicht erkennenung trotzdem fortsetzen
            face_flag = functions.getface(capture, haar_cascade)
            #Zeitvariablen befüllen
            previous_time, elapsed_time = functions.set_timers(face_flag, previous_time, elapsed_time)

            #Status wechseln gegebenenfalls
            if elapsed_time > emergency_gap:
                danger_status = 3 #Abschaltung, falls zu lange gedauert
            elif elapsed_time < warning_gap: #Falls gesicht erkannt, wieder zurück auf status 1
                danger_status = 1

        if danger_status == 3:
            GPIO.output(relaispin, GPIO.HIGH) #relais zum Trennen
    else:
        danger_status = 0
        #Zeiten zurücksetzen, damit der Hauptschalter als reste verwendet werden kann
        previous_time = time.time()
        elapsed_time = 0
        GPIO.output(relaispin, GPIO.LOW) #Relais Kreis geschlossen

    #Set GPIOs
    buzzflag, buzz_timer = functions.set_buzzer(danger_status, buzzerpin, buzz_timer, buzzgap, buzzflag)
    functions.set_led(danger_status, led_rot, led_gelb, led_grün)

    #Abbruchbedingung um aus While auszubrechen, für Testzwecke
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

# Nach While, Kamerazugriff lösen und alle Fenster schließen.
capture.release()
cv.destroyAllWindows()

# Stop Buzzer
GPIO.cleanup()
