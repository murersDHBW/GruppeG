from pybricks.ev3devices import GyroSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait 
from threading import Thread
from time import sleep

class Inputs:
    def __init__(self, ev3):
        self.gyro_sensor = GyroSensor(Port.S4)
        self.GYRO_CALIBRATION_LOOP_COUNT = 200

        # Dieser Offset wird durch die Methode calibrate_gyro_offset() berechnent
        self.gyro_offset = 0

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
    
    def read_inputs(self):
        while True:
            self.angle = self.gyro_sensor.angle() + self.gyro_offset
            # self.ev3.screen.print(self.angle)
            # self.distance = self.ultrasonic_sensor.distance()
            sleep(0.05)
    
    def reset_angle(self):
        self.gyro_sensor.reset_angle(0)

        # Falls der angle vor dem nächsten Poll angefragt wird
        self.angle = 0
        print("Reset angle")
        return self.angle

    # Calibrate the gyro offset. This makes sure that the robot is perfectly
    # still by making sure that the measured rate does not fluctuate more than
    # 2 deg/s. Gyro drift can cause the rate to be non-zero even when the robot
    # is not moving, so we save that value for use later.
    # Berechne Gyro Offset
    def calculate_gyro_offset(self):
        while True:
            gyro_minimum_rate, gyro_maximum_rate = 440, -440
            gyro_sum = 0
            for _ in range(self.GYRO_CALIBRATION_LOOP_COUNT):
                gyro_sensor_value = self.gyro_sensor.angle()
                gyro_sum += gyro_sensor_value
                if gyro_sensor_value > gyro_maximum_rate:
                    gyro_maximum_rate = gyro_sensor_value
                if gyro_sensor_value < gyro_minimum_rate:
                    gyro_minimum_rate = gyro_sensor_value
                sleep(0.05)
            if gyro_maximum_rate - gyro_minimum_rate < 2:
                break
        self.gyro_offset = gyro_sum / self.GYRO_CALIBRATION_LOOP_COUNT



        