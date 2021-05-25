#!/usr/bin/env pybricks-micropython
from MotorController import MotorController
from UltraSonicSensor import UltraSonicSensor
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread
import mapping
import sys
import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
## Belegung Ports:
## Motor Link = B
## Motor Rechts = D
## UltraSonic = 1
## Gyro = 4

## !!! Beachten: VS Code EOL von CRLF auf LF !!!

# Create your objects here.
ev3 = EV3Brick()

# Controller und Sensoren initialisieren
motorController = MotorController()
ultraSonicSensor = UltraSonicSensor()

#instantiate variables needed for mapping
wall = []
positions = [[0,0]]
robotAngle = 0
measureFrequency = 0.008
rawData = []

def getWallPos(stop):
    while True:
        if stop():
                break
        robotAngle = motorController.gyro_sensor.angle()
        robotAngle = robotAngle % 360
        print(robotAngle)
        distance = ultraSonicSensor.measureDistance()
        rawData.append([robotAngle, distance])
        if distance < 1000:
            robot2wall = mapping.degToPos(robotAngle, distance)
            #print(distance, robotAngle)
            wallpoint = mapping.vectorAddition(positions[-1], robot2wall)
            if wallpoint not in wall:
                wall.append(robot2wall)
            print(robot2wall)
        time.sleep(measureFrequency)
        
#instantiate threads
def main_thread():
    stop_threads = False
    t = Thread(target = getWallPos, args =(lambda : stop_threads, ))
    t.start()
    motorController.turn_360()
    stop_threads = True
    print('Fred killed')
    with open("rawData.txt", "a+") as f:
        for element in rawData:
            print(element)
            f.write(str(element[0]) + "," + str(element[1]) + "\n")

main_thread()
mapping.buildSVG(wall)


# Ultraschallpräsenz erkennen
presence = ultraSonicSensor.scanForUltrasonicPresence()
print("Ultrasonic Presence: " + str(presence))
ev3.screen.print("Ultrasonic Presence: " + str(presence))

# Distanz via Ultraschall messen
"""while True:
    distance = ultraSonicSensor.measureDistance()
    robotAngle = motorController.gyro_sensor.angle()
    #ev3.screen.print(distance)
    ev3.screen.print(robotAngle)"""


# 5 Sekunden gerade aus fahren
#motorController.drive(3)

# Umdrehen
#motorController.turn_around()

# 5 Sekunden zurück fahren
#motorController.reverse(3)

# Wieder zum Start zurück fahren
#motorController.drive(6)

