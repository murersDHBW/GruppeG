#!/usr/bin/env pybricks-micropython
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

leftMotor = Motor(Port.D)
rightMotor = Motor(Port.B)
sensor = GyroSensor(Port.S4)

# Create your objects here.
ev3 = EV3Brick()


leftMotor.run(500)
rightMotor.run(400)

# 10 Sekunden fahren
t_end = time.time() + 10

while time.time() < t_end:

    # Speed = angular velocity
    # links = minus
    # rechts = plus

    print("Gyro Speed: " + str(sensor.speed()))
    print("Motor links Winkel :" + str(leftMotor.angle()))
    print("Motor rechts Winkel:" + str(rightMotor.angle()))
    time.sleep(0.1)

leftMotor.stop()
rightMotor.stop()
