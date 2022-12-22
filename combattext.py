from utilities import *

class CombatText:
    def __init__(self, position, color, text, font, size, max_life, total_delta):
        self.position = position
        self.color = color
        self.text = text
        self.size = size
        self.font = font
        self.life = max_life
        self.inc_y = total_delta / self.life

    def render(self, screen):
        center_text_x(screen, self.position, self.font, self.text, self.color, self.size)

    def update(self, time_elapsed):
        self.position = (self.position[0], self.position[1] - time_elapsed * self.inc_y)
        self.life = self.life - time_elapsed
