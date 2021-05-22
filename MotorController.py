from time import sleep, time

class MotorController:

    def __init__(self, inputs, outputs):
        self.speed = 300
        self.inputs = inputs
        self.outputs = outputs
    
    def drive(self, drive_seconds, reverse=False):
        left_speed = self.speed
        right_speed = self.speed
        drive_until = time() + drive_seconds

        # Negative Werte drehen den Motor in die andere Richtung -> rückwärts
        reverse_multiplier = -1 if reverse else 1

        angle = self.inputs.reset_angle()

        while time() < drive_until:

            self.outputs.run_left_motor(left_speed * reverse_multiplier)
            self.outputs.run_right_motor(right_speed * reverse_multiplier)
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

        self.outputs.stop_motors()
    
    def reverse(self, drive_seconds):
        self.drive(drive_seconds, reverse=True)

    def drive_until_obstacle(self):
        raise NotImplementedError("Dafür müssen wir erst irgend einen Sensor verbauen, der sowas erkennen kann.")

    def turn_by_degree(self, deg):
        angle = self.inputs.reset_angle()
        turning_speed = 200

        if deg > 0:
            # nach rechts drehen
            self.outputs.run_left_motor(turning_speed)
            self.outputs.run_right_motor(turning_speed * -1)

            while(True):
                if(angle >= deg):
                    break
                angle = self.inputs.angle
        else:
            # nach links drehen
            self.outputs.run_left_motor(turning_speed * -1)
            self.outputs.run_right_motor(turning_speed)

            while(True):
                if(angle <= deg):
                    break
                angle = self.inputs.angle
        
        self.outputs.stop_motors()
    
    def turn_left(self):
        self.turn_by_degree(-90)
        
    def turn_right(self):
        self.turn_by_degree(90)

    def turn_around(self):
        self.turn_by_degree(180)
            
