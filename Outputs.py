from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction

class Outputs:
    def __init__(self):
        self.left_motor = Motor(Port.B, positive_direction = Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.D, positive_direction = Direction.COUNTERCLOCKWISE)
    
    def run_left_motor(self, speed):
        self.left_motor.run(speed)
    
    def run_right_motor(self, speed):
        self.right_motor.run(speed)

    def stop_motors(self):
        self.left_motor.stop()
        self.right_motor.stop()