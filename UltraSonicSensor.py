from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port

class UltraSonicSensor:
    def __init__(self):
        # Sensor verbinden
        self.ultraSonic = UltrasonicSensor(Port.S1)
        self.distance = 0

    def scanForUltrasonicPresence(self):
        # Prüfen ob weitere Ultraschallpräsenz vorhanden und ermittelten Wert zurückgeben
        if (self.ultraSonic.presence() == True):
            return True
        return False

    def measureDistance(self):
        # Distanz messen und ermittelten Wert zurückgeben
        return int(self.ultraSonic.distance())
