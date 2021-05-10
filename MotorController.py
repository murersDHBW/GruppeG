from pybricks.ev3devices import (Motor, GyroSensor)
from pybricks.parameters import Port, Direction
from time import sleep, time

class MotorController:

    def __init__(self):
        self.speed = 300

        # Motoren und Sensoren verbinden
        self.leftMotor = Motor(Port.B, positive_direction = Direction.COUNTERCLOCKWISE)
        self.rightMotor = Motor(Port.D, positive_direction = Direction.COUNTERCLOCKWISE)
        self.gyro_sensor = GyroSensor(Port.S4)
    
    def drive(self, drive_seconds):
        left_speed = self.speed
        right_speed = self.speed
        drive_until = time() + drive_seconds

        angle = 0
        self.gyro_sensor.reset_angle(0)

        while time() < drive_until:
            self.leftMotor.run(left_speed)
            self.rightMotor.run(right_speed)

            sleep(0.1)
            angle = self.gyro_sensor.angle()

            if abs(angle) <= 1:
                # Wenn wir gerade aus fahren, setzen wir die Motoren wieder auf die gleiche Geschwindigkeit
                # um den Kurs beizubehalten
                right_speed = self.speed
                left_speed = self.speed
                continue

            if(angle > 0):
                right_speed = right_speed + 15
                print("MOTORSTEUERUNG: Drift nach rechts. (" + str(angle) +") Motor: L=" + str(left_speed) + " R=" + str(right_speed))
                sleep(0.1)
            else:
                left_speed = left_speed + 15
                print("MOTORSTEUERUNG: Drift nach links. (" + str(angle) +") Motor: L=" + str(left_speed) + " R=" + str(right_speed))
                sleep(0.1)

        self.leftMotor.stop()
        self.rightMotor.stop()
    
    def drive_until_obstacle(self):
        raise NotImplementedError("Dafür müssen wir erst irgend einen Sensor verbauen, der sowas erkennen kann.")

    def turn_by_degree(self, deg):
        self.gyro_sensor.reset_angle(0)
        angle = self.gyro_sensor.angle()

        turning_speed = 200

        if deg > 0:
            # nach rechts drehen
            self.leftMotor.run(turning_speed)
            self.rightMotor.run(-turning_speed)

            while(True):
                if(angle >= deg):
                    break
                angle = self.gyro_sensor.angle()
        else:
            # nach links drehen
            self.leftMotor.run(-turning_speed)
            self.rightMotor.run(turning_speed)

            while(True):
                if(angle <= deg):
                    break
                angle = self.gyro_sensor.angle()
        
        self.leftMotor.stop()
        self.rightMotor.stop()
    
    def turn_left(self):
        self.turn_by_degree(-90)
        
    def turn_right(self):
        self.turn_by_degree(90)

    def turn_around(self):
        self.turn_by_degree(180)
            
