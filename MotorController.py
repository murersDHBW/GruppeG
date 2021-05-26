from time import sleep, time
from threading import Thread
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction

class MotorController:

    def __init__(self, inputs):
        self.speed = 300
        self.inputs = inputs
        self.left_motor = Motor(Port.B, positive_direction = Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.D, positive_direction = Direction.COUNTERCLOCKWISE)

    def drive(self, drive_seconds, reverse=False):
        left_speed = self.speed
        right_speed = self.speed
        drive_until = time() + drive_seconds

        # Negative Werte drehen den Motor in die andere Richtung -> rückwärts
        reverse_multiplier = -1 if reverse else 1

        angle = self.inputs.reset_angle()

        while time() < drive_until:

            self.left_motor.run(left_speed * reverse_multiplier)
            self.left_motor.run(right_speed * reverse_multiplier)
            sleep(0.1)

            # Wenn wir rückwärts fahren sind die Seiten vertauscht
            angle = self.inputs.angle * reverse_multiplier

            if abs(angle) <= 1:
                # Wenn wir gerade aus fahren, setzen wir die Motoren wieder auf die gleiche Geschwindigkeit
                # um den Kurs beizubehalten
                right_speed = self.speed
                left_speed = self.speed
                continue
                
            if angle > 0:
                right_speed = right_speed + 15
                print("MOTORSTEUERUNG: Drift nach rechts. (" + str(angle) +") Motor: L=" + str(left_speed) + " R=" + str(right_speed))
            else:
                left_speed = left_speed + 15
                print("MOTORSTEUERUNG: Drift nach links. (" + str(angle) +") Motor: L=" + str(left_speed) + " R=" + str(right_speed))

            sleep(0.1)

        self.left_motor.stop()
        self.right_motor.stop()
    
    def reverse(self, drive_seconds):
        self.drive(drive_seconds, reverse=True)

    def turn_by_degree(self, deg):
        angle = self.inputs.reset_angle()
        turning_speed = 200

        if deg > 0:
            # nach rechts drehen
            self.left_motor.run(turning_speed)
            self.right_motor.run(turning_speed * -1)

            while(True):
                if(angle >= deg):
                    break
                angle = self.inputs.angle
        else:
            # nach links drehen
            self.left_motor.run(turning_speed * -1)
            self.right_motor.run(turning_speed)

            while(True):
                if(angle <= deg):
                    break
                angle = self.inputs.angle
        
        self.left_motor.stop()
        self.right_motor.stop()
    
    def turn_left(self):
        self.turn_by_degree(-90)
        
    def turn_right(self):
        self.turn_by_degree(90)

    def turn_around(self):
        self.turn_by_degree(180)
            
