#!/usr/bin/env pybricks-micropython
from UserInterface import UserInterface
from threading import Thread
from Inputs import Inputs
from UserInterface import UserInterface
from Mapping import buildSVG, degToPos, euclidean_distance, get_mid_coord, get_next_pos, posToDeg, vectorAddition
from MotorController import MotorController
import math
from UltraSonicSensor import UltraSonicSensor
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font
from time import sleep
import os

def main():
    ev3 = EV3Brick()

    # Eigener Thread der sensoren einliest
    inputs = Inputs(ev3)
    inputs.calculate_gyro_offset()

    # Eigener Thread der die UI anzeigt
    ui = UserInterface(ev3, inputs)

    # Initialisiert alle angeschlossenen Geräte, welche gesteuert werden können
    motorController = MotorController(inputs)

    # Vorherige Messung entfernern
    try:
        os.remove("rawData1.txt")
    except:
        print("Keine Daten vorhanden")

    #instantiate variables needed for mapping
    wall = []
    positions = [[0,0]]
    measureFrequency = 0.004
    data_version = 1
    drive_time = 5
    drive_dist_per_sec = 80
    angles = []

    def localize_past_pos(go_to, angles):
        rev_angles = angles.reverse()
        if go_to > len(rev_angles):
            go_to == len(rev_angles)
        for i in go_to:
            current_angle = (rev_angles[i]+180)%360
            motorController.turn_by_degree(current_angle)
            motorController.drive(c/, True)
            motorController.turn_by_degree(-current_angle)
    
    def localize_coordinate(x,y, drive_dist_per_sec):
        current_angle = posToDeg(x,y)
        c = math.sqrt(x**2 + y**2)
        motorController.turn_by_degree(current_angle)
        motorController.drive(c / drive_dist_per_sec, True)
        motorController.turn_by_degree(-current_angle)

        next_position = vectorAddition(degToPos(angle_next_pos, drive_time * drive_dist_per_sec),positions[-1])

        positions.append(next_position)
        ui.waypoints.append(next_position)

    def getRawData(stop):
        while True:
            if stop():
                break
            robotAngle = inputs.angle
            robotAngle = robotAngle % 360
            
            distance = inputs.distance
            
            test = [robotAngle, distance]
            if test not in rawData:
                rawData.append(test)
            sleep(measureFrequency)
            
    #instantiate threads
    def random_Fred():
        stop_threads = False
        t = Thread(target = getRawData, args =(lambda : stop_threads, ))
        t.start()
        motorController.turn_by_degree(360)
        stop_threads = True
        print('Fred killed')
        
    for _ in range(3):
        rawData = []
        random_Fred()
        with open("rawData" + str(data_version) + ".txt", "a+") as f:
            f.write(str(positions[-1][0]) + "," + str(positions[-1][1]) + "\n")
            for element in rawData:
                f.write(str(element[0]) + "," + str(element[1]) + "\n")
        data_version += 1

        angle_next_pos, current_surrounding = get_next_pos(rawData, positions[-1])
        wall.append(current_surrounding)
        motorController.turn_by_degree(angle_next_pos)
        angles.append(angle_next_pos)
        motorController.drive(drive_time, True)
        motorController.turn_by_degree(-angle_next_pos)

        next_position = vectorAddition(degToPos(angle_next_pos, drive_time * drive_dist_per_sec),positions[-1])

        positions.append(next_position)
        ui.waypoints.append(next_position)

    


    with open("map.txt", "a+") as f:
        for element in wall[0]:
            print(element)
            f.write(str(element[0]) + "," + str(element[1]) + "\n")
            print(f.read())

    print("ENDE")
    while True:
        sleep(0.05)


main()