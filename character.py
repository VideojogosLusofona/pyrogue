import pygame
import pygame.freetype
import math

from utilities import *

class Character:
    def __init__(self, archetype, position, gamedata):
        self.archetype = archetype
        self.position = position
        self.level = 1
        self.health = archetype.get_max_health(self.level)
        self.mp = archetype.get_max_mp(self.level)
        self.stamina = archetype.get_max_stamina(self.level)
        self.xp = 0
        self.render_flipx = False
        self.gamedata = gamedata

    def render(self, map_pos, tile_size, camera_pos, screen):
        px = map_pos[0] + tile_size[0] * (self.position[0] - camera_pos[0])
        py = map_pos[1] + tile_size[1] * (self.position[1] - camera_pos[1])

        image = self.archetype.image
        if (self.render_flipx):
            image = self.archetype.image_flipx
        if (self.health <= 0):
            image = self.gamedata.get_image("Blood")

        screen.blit(image, (px, py))

    def render_stats(self, stats_pos, font, text_color, screen):
        pygame.draw.rect(screen, (255, 255, 255), (stats_pos[0] - 2, stats_pos[1] - 2, 132, 132), 0)
        pygame.draw.rect(screen, (40, 40, 40), (stats_pos[0] - 1, stats_pos[1] - 1, 130, 130), 0)
        screen.blit(self.archetype.stat_image, stats_pos)

        font.render_to(screen, (stats_pos[0] + 140, stats_pos[1]), self.archetype.display_name, text_color, None, pygame.freetype.STYLE_DEFAULT, 0, 36)
        font.render_to(screen, (stats_pos[0] + 140, stats_pos[1] + 36), f"Level {self.level}", text_color, None, pygame.freetype.STYLE_DEFAULT, 0, 20)

        y = stats_pos[1] + 140

        center_text_y(screen, (stats_pos[0], y + 12), font, "HP:", (255, 255, 255), 20)
        render_progress_bar(screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (0, 200, 0), font, (0, 0, 0), 2, self.health, self.archetype.get_max_health(self.level), "")
        y = y + 30

        if (self.archetype.get_max_mp(self.level) > 0):
            center_text_y(screen, (stats_pos[0], y + 12), font, "MP:", (255, 255, 255), 20)
            render_progress_bar(screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (0, 200, 200), font, (0, 0, 0), 2, self.mp, self.archetype.get_max_mp(self.level), "")
            y = y + 30

        if (self.archetype.get_max_stamina(self.level) > 0):
            center_text_y(screen, (stats_pos[0], y + 12), font, "ST:", (255, 255, 255), 20)
            render_progress_bar(screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (200, 200, 0), font, (0, 0, 0), 2, self.stamina, self.archetype.get_max_stamina(self.level), "")
            y = y + 30

        if (self.archetype.has_xp):
            center_text_y(screen, (stats_pos[0], y + 12), font, "XP:", (255, 255, 255), 20)
            render_progress_bar(screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (200, 200, 200), font, (0, 0, 0), 2, self.xp, self.archetype.get_max_xp(self.level), "")
            y = y + 30
            
        return y

    def update(self):
        self.stamina = min(self.stamina + self.archetype.get_stamina_recover(self.level), self.archetype.get_max_stamina(self.level))

    def modify_stamina(self, delta):
        self.stamina = min(self.archetype.get_max_stamina(self.level), max(0, self.stamina + delta))

    def modify_health(self, delta):
        self.health = min(self.archetype.get_max_health(self.level), max(0, self.health + delta))

    def get_xp(self, level):
        # Retrieves how much XP you get from this enemy
        delta = level - self.level
        if (delta < 0):
            # You had more level than the enemy, so just get a measly amount
            return 10
        
        delta = delta + 1

        # Square the delta (plus one) and multiply by 20
        # So, if level difference is 0 , you get 20,
        # if it is 1, you get 80, if it is 2, you get 180, if it is 3, you get 320, etc
        return (delta * delta) * 20

    def modify_xp(self, delta):
        self.xp = self.xp + delta
        while (self.xp >= self.archetype.get_max_xp(self.level)):
            self.xp = self.xp - self.archetype.get_max_xp(self.level)
            self.level = self.level + 1

            self.gamedata.spawn_combat_text(self.position, (255, 255, 0), f"LEVEL UP!", 24, 3, -40)

            # Restore health, just a gift for level up!
            self.health = self.archetype.get_max_health(self.level)
            self.mp = self.archetype.get_max_mp(self.level)
            self.stamina = self.archetype.get_max_stamina(self.level)

    def move(self, map, delta_x, delta_y):
        # Check if it is alive
        if (self.health <= 0):
            return False

        # If the character needs stamina (max_stamina > 0), check if we have enough stamina to move
        tile = map.get_tile(self.position[0], self.position[1])
        if (self.archetype.get_max_stamina(self.level) > 0):
            cost = tile.stamina_cost
            if (self.stamina < cost):
                return False
        else:
            cost = 0

        if (delta_x < 0):
            self.render_flipx = True
        elif (delta_x > 0):
            self.render_flipx = False

        npx = self.position[0] + delta_x
        npy = self.position[1] + delta_y

        # Check if there is an enemy in the new position, if there is
        # do a melee attack, otherwise move
        enemy = self.gamedata.get_enemy_in_position(npx, npy)
        if (enemy != None):
            # Check if we have stamina for an attack
            cost = self.archetype.get_melee_attack_stamina_cost(self.level)
            if (self.stamina < cost):
                # Can't attack, no stamina
                return True

            self.stamina = self.stamina - cost

            # Run melee attack
            attack = self.archetype.get_attack_power(self.level)
            defense = enemy.archetype.get_defense_power(enemy.level)
            total = attack - defense
            if (total <= 0):
                # Missed attack
                self.gamedata.spawn_combat_text(enemy.position, (0, 200, 200), f"MISS!", 16)
                pass
            else:                
                enemy.modify_health(-total)
                if (enemy.health <= 0):
                    # Killed enemy, get XP
                    self.gamedata.spawn_combat_text(enemy.position, (255, 0, 0), f"DEAD!", 16)
                    xp = enemy.get_xp(self.level)
                    self.modify_xp(xp)
                    self.gamedata.spawn_combat_text(self.position, (255, 255, 255), f"+{xp} XP!", 24, 2, 20)
                else:
                    self.gamedata.spawn_combat_text(enemy.position, (255, 255, 0), f"-{total}", 16)
                    self.gamedata.track_enemy(enemy)

            return True

        next_tile = map.get_tile(npx, npy)
        if (not next_tile.solid):
            self.stamina = self.stamina - cost
            self.position = (npx, npy)
            return True

        return False
