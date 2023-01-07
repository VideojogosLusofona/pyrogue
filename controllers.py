import pygame
import random

from vector2 import *

class Controller:
    def __init__(self, character):
        self.character = character
        self.gamedata = character.gamedata
        self.spawn_position = character.position

    def update(self):
        pass

    def Create(character):
        return None


class KeyboardController(Controller):
    def handle_keypress(self, key):
        if (not self.character.can_take_action()):
            # Can't take an action, so any key will trigger a new turn
            return True

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
        if ((key >= pygame.K_1) and (key <= pygame.K_9)):
            return self.character.run_ability(key - pygame.K_1)

        return False

    @staticmethod
    def Create(character):
        return KeyboardController(character)


class AIController(Controller):
    target_enemy = None

    def chase(self, can_attack):
        if (self.target_enemy != None):
            self.move_to(self.target_enemy.position, can_attack)

    def move_to(self, target_pos, can_attack):
        delta = target_pos - self.character.position

        if (abs(delta.x) > abs(delta.y)):
            # Move in X, if able. If not, try to move in Y
            tmp = Vector2(delta)
            tmp.y = 0
            if (not tmp.is_null()):
                tmp.normalize()
                if (self.character.move(tmp.x, tmp.y, can_attack)):
                    return

        # Move in Y
        tmp = Vector2(delta)
        tmp.x = 0
        if (tmp.is_null()):
            return
        tmp.normalize()
        self.character.move(tmp.x, tmp.y, can_attack)

    def random_wander(self, can_attack):
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dir = random.choice(dirs)

        self.character.move(*dir, can_attack)

    @staticmethod
    def Create(character):
        return AIController(character)

class AIController_WanderAndChase(AIController):
    returning_to_spawn = False

    def __init__(self, character, sight_radius = 5, return_distance = 10):
        super().__init__(character)
        self.sight_radius = sight_radius
        self.return_distance = return_distance

    def update(self):
        # Check if current position is too far from spawn position
        if (Vector2.distance(self.character.position, self.spawn_position) > self.return_distance):
            self.returning_to_spawn = True

        if self.returning_to_spawn:
            self.move_to(self.spawn_position, False)
            if (self.spawn_position == self.character.position):
                self.returning_to_spawn = False
            return

        if (self.target_enemy == None) or (self.target_enemy.is_dead()):
            self.target_enemy = self.gamedata.get_closest_enemy(self.character.position, self.character.faction)
            if (self.target_enemy != None):
                if (Vector2.distance(self.target_enemy.position, self.character.position) > self.sight_radius):
                    self.target_enemy = None

        if (self.target_enemy != None):
            # Check if any ability can be triggered, and trigger it
            for index in range(0, len(self.character.ability_data)):
                if (self.character.run_ability(index)):
                    return

            # Chase enemy otherwise
            self.chase(True)
        else:
            self.random_wander(False)

    @staticmethod
    def Create(character, sight_radius, return_distance):
        return AIController_WanderAndChase(character, sight_radius, return_distance)
