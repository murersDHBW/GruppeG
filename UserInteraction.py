from threading import Thread
from time import sleep

class UserInteraction:

    # 1 Argument, der Ev3 Bildschirm
    def __init__(self, ev3):
        self.screen = ev3.screen

        # Die Dimensionen des EV3
        self.width = 178
        self.height = 128

        # Variablen um das Grid zu zeichnen
        self.cell_size = 20
        self.horizontal_padding = 19
        self.upper_padding = 4
        self.lower_padding = 24

        # Position des Cursors
        self.cursor_pos_x = 3
        self.cursor_pos_y = 4

        # Cursor soll unabhängig vom Rest gezeichnet werden
        t_cursor = Thread(target=self.draw_cursor)
        t_cursor.start()

    def draw(self):
        self.screen.clear()
        self.draw_grid()
        self.draw_cursor()

    # Malt ein 7x5 Grid auf das Display, mit einer Zellengröße von 20px
    def draw_grid(self):

        # Vertikale Linien malen
        horizontal_offset = self.horizontal_padding
        for i in range(8):
            self.screen.draw_line(horizontal_offset, self.upper_padding, horizontal_offset, self.height - self.lower_padding)
            horizontal_offset += self.cell_size

        # Horizontale Linien malen
        vertical_offset = self.upper_padding
        for i in range(6):
            print(vertical_offset)
            self.screen.draw_line(self.horizontal_padding, vertical_offset, self.width - self.horizontal_padding, vertical_offset)
            vertical_offset += self.cell_size
    
    def draw_cursor(self):

        while(True):

            # Statusbereich unten clearen


            # Koordinaten
            # 106 = Niedrigste horizontale Linie ist bei 104 + 2 Abstand
            cursor_pos = "(" + str(self.cursor_pos_x) + "," + str(self.cursor_pos_y) + ")"
            self.screen.draw_text(self.horizontal_padding, 106, cursor_pos)

            print("draw cursor")
            sleep(1)

