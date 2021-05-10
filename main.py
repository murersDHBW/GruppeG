#!/usr/bin/env pybricks-micropython
from MotorController import MotorController
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

motorController = MotorController()

# 5 Sekunden gerade aus fahren
motorController.drive(5)

# Umdrehen
motorController.turn_around()

# 5 Sekunden zurück fahren
motorController.drive(5)
