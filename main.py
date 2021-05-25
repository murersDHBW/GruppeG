#!/usr/bin/env pybricks-micropython
from Outputs import Outputs
from Inputs import Inputs
from UserInteraction import UserInteraction
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
## Belegung Ports:
## Motor Link = B
## Motor Rechts = D
## UltraSonic = 1
## Gyro = 4

## !!! Beachten: VS Code EOL von CRLF auf LF !!!

# Create your objects here.
ev3 = EV3Brick()

inputs = Inputs(ev3)

# gyro offset kalibrieren
inputs.calculate_gyro_offset()

outputs = Outputs()

# Controller und Sensoren initialisieren
motorController = MotorController(inputs, outputs)

# time.sleep(20)
motorController.drive(10)