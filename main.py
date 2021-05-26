#!/usr/bin/env pybricks-micropython
from MotorController import MotorController
from UltraSonicSensor import UltraSonicSensor
from GyroSensor import GyroSensor
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
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
gyroSensor = GyroSensor()

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
