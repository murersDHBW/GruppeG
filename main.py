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
import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()

# Controller und Sensoren initialisieren
motorController = MotorController()
ultraSonicSensor = UltraSonicSensor()

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
