from threading import Thread
from time import sleep
from pybricks.media.ev3dev import Font
from pybricks.parameters import Color, Button

class UserInterface:

    # 1 Argument, der Ev3 Bildschirm
    def __init__(self, ev3, inputs):
        self.screen = ev3.screen
        self.ev3 = ev3

        self.title_font = Font(family="Lucida", size=20)
        self.title_height = 0
        self.title = "Wegpunkte"

        self.text_font = Font(family="Lucida", size=12, monospace=True)
        self.status_text_font = Font(family="Lucida", size=8)

        # Bestimmte Pixelwerte, um die UI zu malen
        self.width = 178
        self.height = 128
        self.padding = 4
        self.indicator_width = 20
        self.list_text_height = self.text_font.text_height("Punkt - X")

        # Position jedes Listenelements in einem Tupel (x, y) speichern
        self.list_coordinates = []

        # Position des Cursors
        self.cursor_index = 0
        self.cursor_blink = False
        self.waypoints = ["1 - Punkt", "2 - Punkt", "3 - Punkt", "4 - Punkt"]
        self.status_msg = "Warte..."

        # Der Wegpunkt, zu welchem gefahren werden soll. Der Webpunkt wird erst bei einer Auswahl
        # mit der mittleren Taste ausgewählt. 
        self.selected_waypoint = -1

        # Cursor soll unabhängig vom Rest gezeichnet werden
        t = Thread(name="UI", target=self.draw)
        t.start()

    def draw(self):
        while True:

            # Um zu vermeiden, dass ein Klick als mehrere Klicks interpretiert werden
            # warten wir eine längere Zeit nach einem Klick, nachdem wir die UI 
            # refreshed haben.
            button_pressed = False

            # Wir reagieren nur auf Inputs wenn wir noch kein Element ausgewählt haben
            if self.selected_waypoint == -1:
                for button in self.ev3.buttons.pressed():
                    if button == Button.DOWN:
                        if self.cursor_index == len(self.waypoints) -1:
                            self.cursor_index = 0
                        else:
                            self.cursor_index = self.cursor_index + 1 

                        button_pressed = True
                        break
                    if button == Button.UP:
                        if self.cursor_index == 0:
                            self.cursor_index = len(self.waypoints) - 1
                        else:
                            self.cursor_index = self.cursor_index - 1 

                        button_pressed = True
                        break
                    if button == Button.CENTER:
                        self.selected_waypoint = self.cursor_index
                        button_pressed = True
                        break

            self.screen.clear()
            self.draw_title()
            self.draw_list()
            self.draw_cursor()
            self.draw_status_bar()

            if not button_pressed:
                sleep(0.01)
            else:
                sleep(0.5)
    
    # Title schreiben, und die Größe zurückgeben, damit der restliche Text entsprechend
    # geschrieben werden kann
    def draw_title(self):
        self.screen.set_font(self.title_font)
        self.screen.draw_text(self.padding, self.padding, self.title)
        self.title_height = self.title_font.text_height(self.title)


    # Malt ein 7x5 Grid auf das Display, mit einer Zellengröße von 20px
    def draw_list(self):
        self.list_coordinates = []
        initial_height = self.padding + self.title_height + self.padding
        x1 = self.padding + self.indicator_width + self.padding

        for i in range(0, len(self.waypoints)):
            waypoint_text = "Punkt " + str(i + 1)
            y1 = initial_height + (i * (self.list_text_height + self.padding * 2))

            if self.selected_waypoint != -1 and self.selected_waypoint == i:
                # Ausgewählter Punkt mit schwarzem Hintergrund malen
                self.screen.draw_text(x1, y1, waypoint_text, text_color=Color.WHITE, background_color = Color.BLACK)
            else:
                self.screen.draw_text(x1, y1, waypoint_text, text_color=Color.BLACK)
            
            self.list_coordinates.append((x1, y1)) 
    

    # Malt den Cursor als einen Kreis links neben dem ausgewählten Item
    def draw_cursor(self):
        (_, y) = self.list_coordinates[self.cursor_index]
        height = y + self.list_text_height / 2 + self.padding
        x = self.padding + self.indicator_width / 2
        self.screen.draw_circle(x, height, 2, fill=True, color=Color.BLACK)


    # Malt einen Strich, und ein Wort in die untere Linke Ecke
    # Soll den Status anzeigen, wie 
    def draw_status_bar(self):
        (_, lowest_list_item_y) = self.list_coordinates[-1]
        list_item_bottom = lowest_list_item_y + self.list_text_height + (self.padding * 2)
        self.screen.draw_line(self.padding, list_item_bottom, self.width - self.padding, list_item_bottom)

        text_width = self.status_text_font.text_width(self.status_msg)

        y1 = list_item_bottom + self.padding / 2
        x1 = self.width - text_width - self.padding

        self.screen.set_font(self.status_text_font)
        self.screen.draw_text(x1, y1, self.status_msg)

