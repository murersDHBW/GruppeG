#!/usr/bin/env pybricks-micropython
from UserInterface import UserInterface
from threading import Thread
from Outputs import Outputs
from Inputs import Inputs
from UserInterface import UserInterface
from MotorController import MotorController
from UltraSonicSensor import UltraSonicSensor
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

# This program requires LEGO EV3 MicroPython v2.0 or higher.
## Belegung Ports:
## Motor Link = B
## Motor Rechts = D
## UltraSonic = 1
## Gyro = 4

## !!! Beachten: VS Code EOL von CRLF auf LF !!!

def setup():
    ev3 = EV3Brick()

    # Eigener Thread der sensoren einliest
    inputs = Inputs(ev3)
    inputs.calculate_gyro_offset()

    # Eigener Thread der die UI anzeigt
    ui = UserInterface(ev3)

    # Initialisiert alle angeschlossenen Geräte, welche gesteuert werden können
    outputs = Outputs()

    motorController = MotorController(inputs, outputs)

    while True:
        loop(ev3, inputs, outputs, ui, motorController)

def loop(ev3, inputs, outputs, ui, motorController):

    do_in_bg(motorController.drive, (10, ))

    while len(ev3.buttons.pressed()) == 0:
        sleep(0.05)

def do_in_bg(method, arg_tuple):
    t = Thread(name= str(method.__name__) ,target=method, args=arg_tuple)
    t.start()

setup()