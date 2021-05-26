from MotorController import MotorController
from Inputs import Inputs
from threading import Thread
import math

class Mapping:
    def __init__(self, motorController: MotorController, inputs: Inputs):
        self.motorController = motorController
        self.inputs = inputs

        self.wall = []
        self.positions = [[0,0]]
        self.measureFrequency = 0.008
        self.rawData = []
    
    def scan_360(self) -> None:
        stop_threads = False

        t = Thread(target = getWallPos, args =(lambda : stop_threads, ))
        t.start()

        self.motorController.turn_by_degree(360)
        stop_threads = True

        print('Fred killed')
        with open("rawData.txt", "a+") as f:
            for element in rawData:
                print(element)
                f.write(str(element[0]) + "," + str(element[1]) + "\n")


    def getWallPos(self, stop) -> None:
        while True:
            if stop():
                break

            robotAngle = inputs.angle % 360
            distance = inputs.distance
            rawData.append([robotAngle, distance])

            if distance < 1000:
                robot2wall = self.degToPos(robotAngle, distance)
                wallpoint = self.vectorAddition(positions[-1], robot2wall)
                if wallpoint not in wall:
                    wall.append(robot2wall)
                print(robot2wall)
            time.sleep(self.measureFrequency)
    
    def degToPos(self, angle: float, length: float) -> list[float]:
        y = math.cos(angle * (2 * math.pi / 360)) * length
        x = math.sin(angle * (2 * math.pi / 360)) * length
        return [x,y]

    def vectorAddition(self, v1:list[float], v2:list[float]) -> list[float]:
        x = v1[0] + v2[0]
        y = v1[1] + v2[1]
        return [x,y]

    def buildSVG(self) -> None:
        with open("wallList.svg", "a+") as f:
            f.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
                        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
                        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="-1000 -1000 1000 1000">""")
            for wallPos in self.wall:
                f.write('<circle cx="' + str(wallPos[0]/10) + '" cy="' + str(wallPos[1]/10) + '" r="2" fill="black"/>')
            f.write('</svg>')