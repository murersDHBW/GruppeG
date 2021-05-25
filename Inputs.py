from pybricks.ev3devices import GyroSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait 
from threading import Thread
from time import sleep

class Inputs:
    def __init__(self, ev3):
        self.gyro_sensor = GyroSensor(Port.S4)
        self.GYRO_CALIBRATION_LOOP_COUNT = 200

        # Dieser Offset wird durch die Methode calibrate_gyro_offset() berechnet
        self.gyro_offset = 0

        # self.ultrasonic_sensor = UltrasonicSensor(Port.S1)
        self.ev3 = ev3

        self.angle = 0
        self.distance = 0
        # self.presence = self.ultrasonic_sensor.presence()

        input_thread = Thread(name="Thread-Inputs",target=self.read_inputs)
        # Dies ist ein Background-Thread. Wenn der main-Thread beendet wird,
        # soll dieser Thread auch beendet werden
        input_thread.daemon = True
        input_thread.start()
    
    def read_inputs(self):
        while True:
            self.angle = self.gyro_sensor.angle() + self.gyro_offset
            # self.distance = self.ultrasonic_sensor.distance()

            sleep(0.05)
    
    def reset_angle(self):
        self.gyro_sensor.reset_angle(0)

        # Falls der angle vor dem nächsten Poll angefragt wird
        self.angle = 0
        return self.angle

    # Den Offset des Gyrosensors berechnen. Dieser Offset wird gesetzt, falls der Gyro sich nicht 
    # um mehr als 2 Grad / Sekunde verändert.
    def calculate_gyro_offset(self):
        self.print("Kalibriere Gyro")

        while True:
            gyro_minimum_rate, gyro_maximum_rate = 440, -440
            gyro_sum = 0
            for i in range(self.GYRO_CALIBRATION_LOOP_COUNT):
                gyro_sensor_value = self.gyro_sensor.angle()
                gyro_sum += gyro_sensor_value

                if gyro_sensor_value > gyro_maximum_rate:
                    gyro_maximum_rate = gyro_sensor_value
                if gyro_sensor_value < gyro_minimum_rate:
                    gyro_minimum_rate = gyro_sensor_value
                sleep(0.05)

                if i != 0:
                    self.print(str((i / self.GYRO_CALIBRATION_LOOP_COUNT) * 100)[:2] + "%")
                if i == self.GYRO_CALIBRATION_LOOP_COUNT:
                    self.print("100%. DONE")

            if gyro_maximum_rate - gyro_minimum_rate < 2:
                break
        self.gyro_offset = gyro_sum / self.GYRO_CALIBRATION_LOOP_COUNT

        self.print("Offset [" + str(self.gyro_offset) + "] ---")
    
    def print(self, msg):
        self.ev3.screen.print(msg)


        