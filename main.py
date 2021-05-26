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
import os

#if os.path.isfile("rawData1.txt"):
os.remove("rawData1.txt")
#os.remove("rawData2.txt")
#if os.path.isfile("map.txt"):
#os.remove("map.txt")

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
measureFrequency = 0.004
data_version = 1
navigation = 5

def getRawData(stop):
    while True:
        if stop():
            break
        robotAngle = motorController.gyro_sensor.angle()
        robotAngle = robotAngle % 360
        
        distance = ultraSonicSensor.measureDistance()
        
        test = [robotAngle, distance]
        if test not in rawData:
            rawData.append(test)
        time.sleep(measureFrequency)
        
#instantiate threads
def random_Fred():
    stop_threads = False
    t = Thread(target = getRawData, args =(lambda : stop_threads, ))
    t.start()
    motorController.turn_360()
    stop_threads = True
    print('Fred killed')
    
for x in range(3):
    rawData = []
    random_Fred()
    with open("rawData" + str(data_version) + ".txt", "a+") as f:
        f.write(str(positions[-1][0]) + "," + str(positions[-1][1]) + "\n")
        for element in rawData:
            f.write(str(element[0]) + "," + str(element[1]) + "\n")
    data_version += 1

    angle_next_pos, current_surrounding = mapping.get_next_pos(rawData, positions[-1])
    wall.append(current_surrounding)
    motorController.turn_by_degree(angle_next_pos)
    motorController.drive(navigation, True)
    motorController.turn_by_degree(-angle_next_pos)
    positions.append(mapping.vectorAddition(mapping.degToPos(angle_next_pos, navigation * 80),positions[-1]))

with open("map.txt", "a+") as f:
    for element in wall[0]:
        print(element)
        f.write(str(element[0]) + "," + str(element[1]) + "\n")
        print(f.read())

#mapping.buildSVG(wall)


"""differences = []
times = 3
for i in range(10):
    first = ultraSonicSensor.measureDistance()
    motorController.drive(times)
    second = ultraSonicSensor.measureDistance()
    differences.append((second - first)/times)

    first = ultraSonicSensor.measureDistance()
    motorController.drive(times, reverse=True)
    second = ultraSonicSensor.measureDistance()
    differences.append((first - second)/times)

with open("distanceVariation.txt", "a+") as f:
        for element in rawData:
            print(element)
            f.write(str(element) + "\n")"""




# Ultraschallpräsenz erkennen
presence = ultraSonicSensor.scanForUltrasonicPresence()
print("Ultrasonic Presence: " + str(presence))
ev3.screen.print("Ultrasonic Presence: " + str(presence))

# Distanz via Ultraschall messen
distance = ultraSonicSensor.measureDistance()
print(distance)
ev3.screen.print(distance)

# 5 Sekunden gerade aus fahren
motorController.drive(3)

# Umdrehen
motorController.turn_around()

# 5 Sekunden zurück fahren
motorController.reverse(3)

# Wieder zum Start zurück fahren
motorController.drive(6)
