import pygame
import math

class Controller:
    def __init__(self, character):
        self.character = character
        self.gamedata = character.gamedata
        self.spawn_position = character.position

    def update(self):
        pass


class KeyboardController(Controller):
    def handle_keypress(self, key):
        if (key == pygame.K_r):
            return True
        if (key == pygame.K_RIGHT):
            return self.character.move(1, 0)
        if (key == pygame.K_LEFT):
            return self.character.move(-1, 0)
        if (key == pygame.K_UP):
            return self.character.move(0, -1)
        if (key == pygame.K_DOWN):
            return self.character.move(0, 1)

        return False


class AIController(Controller):
    def update(self):
        enemy = self.gamedata.get_closest_enemy(self.character.position[0], self.character.position[1], self.character.faction)
        if (enemy != None):
            delta_x = enemy.position[0] - self.character.position[0]
            delta_y = enemy.position[1] - self.character.position[1]
            dist = math.sqrt(delta_x**2 + delta_y**2)

            if (dist < 5):
                if (abs(delta_x) > abs(delta_y)):
                    # Move in X
                    delta_y = 0
                else:
                    # Move in Y
                    delta_x = 0

                # Only move one step at a time
                delta_x = min(1, max(-1, delta_x))
                delta_y = min(1, max(-1, delta_y))

                self.character.move(delta_x, delta_y)
