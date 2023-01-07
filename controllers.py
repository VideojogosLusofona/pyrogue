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
        enemy = self.gamedata.get_closest_enemy(self.character.position, self.character.faction)
        if (enemy != None):
            delta = enemy.position - self.character.position
            dist = delta.magnitude()

            if (dist < 5):
                if (abs(delta.x) > abs(delta.y)):
                    # Move in X
                    delta.y = 0
                else:
                    # Move in Y
                    delta.x = 0

                if (delta.is_null()):
                    return

                delta.normalize()

                self.character.move(delta.x, delta.y)
