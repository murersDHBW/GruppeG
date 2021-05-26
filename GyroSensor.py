from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port

class UltraSonicSensor:
    def __init__(self):
        # Sensor verbinden
        self.gyro_sensor = GyroSensor(Port.S4)
        self.angle = 0

    def scanForGyroPresence(self):
        # Prüfen ob weitere Ultraschallpräsenz vorhanden und ermittelten Wert zurückgeben
        if (self.ultraSonic.presence() == True):
            return True
        return False

    def reset_angle(angle):
      GyroSensor.reset_angle(angle)

    def angle():
      return GyroSensor.angle()