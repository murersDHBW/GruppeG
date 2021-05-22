from pybricks.ev3devices import GyroSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from threading import Thread
from time import sleep

class Inputs:
    def __init__(self, ev3):
        self.gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)
        # self.ultrasonic_sensor = UltrasonicSensor(Port.S1)
        self.ev3 = ev3

        self.angle = 0
        self.distance = 0
        # self.presence = self.ultrasonic_sensor.presence()

        input_thread = Thread(target=self.read_inputs)
        # Dies ist ein Background-Thread. Wenn der main-Thread beendet wird,
        # soll dieser Thread auch beendet werden
        input_thread.daemon = True
        input_thread.start()
    
    # Alle 10ms die Inputs neu einlesen
    def read_inputs(self):
        while True:
            self.angle = self.gyro_sensor.angle()
            self.ev3.screen.print(self.angle)
            # self.distance = self.ultrasonic_sensor.distance()
            sleep(0.05)
    
    def reset_angle(self):
        self.gyro_sensor.reset_angle(0)

        # Falls der angle vor dem nächsten Poll angefragt wird
        self.angle = 0
        print("Reset angle")
        return self.angle



        