class UserInteraction:

    # 1 Argument, der Ev3 Bildschirm
    def __init__(self, screen):
        self.screen = screen

        self.width = 178
        self.height = 128
        self.horizontal_padding = 9
        self.vertical_padding = 4

    def draw_map(self):
        self.draw_grid()
    
    # Malt ein 8x6 Grid auf das Display, mit einer Zellengröße von 20px
    def draw_grid(self):
        horizontal_offset = self.horizontal_padding
        for i in range(9):
            self.screen.screen.draw_line(horizontal_offset, self.vertical_padding, horizontal_offset, self.height - self.vertical_padding)
            horizontal_offset = horizontal_offset + 20

        vertical_offset = self.vertical_padding
        for i in range(7):
            self.screen.screen.draw_line(self.horizontal_padding, vertical_offset, self.width - self.horizontal_padding, vertical_offset)
            vertical_offset = vertical_offset + 20