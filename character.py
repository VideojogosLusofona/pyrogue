import pygame
import pygame.freetype
import math

from utilities import *

class Character:
    def __init__(self, archetype, level, position, faction, gamedata):
        self.archetype = archetype
        self.controller = None
        self.position = position
        self.level = level
        self.health = archetype.get_max_health(self.level)
        self.mp = archetype.get_max_mp(self.level)
        self.stamina = archetype.get_max_stamina(self.level)
        self.xp = 0
        self.render_flipx = False
        self.gamedata = gamedata
        self.faction = faction

    def render(self):
        px = self.gamedata.map_pos[0] + self.gamedata.tile_size[0] * (self.position[0] - self.gamedata.camera_pos[0])
        py = self.gamedata.map_pos[1] + self.gamedata.tile_size[1] * (self.position[1] - self.gamedata.camera_pos[1])

        image = self.archetype.image
        if (self.render_flipx):
            image = self.archetype.image_flipx
        if (self.health <= 0):
            image = self.gamedata.get_image("Blood")

        self.gamedata.screen.blit(image, (px, py))

    def render_stats(self, stats_pos):
        pygame.draw.rect(self.gamedata.screen, (255, 255, 255), (stats_pos[0] - 2, stats_pos[1] - 2, 132, 132), 0)
        pygame.draw.rect(self.gamedata.screen, (40, 40, 40), (stats_pos[0] - 1, stats_pos[1] - 1, 130, 130), 0)
        self.gamedata.screen.blit(self.archetype.stat_image, stats_pos)

        self.gamedata.font.render_to(self.gamedata.screen, (stats_pos[0] + 140, stats_pos[1]), self.archetype.display_name, self.archetype.text_color, None, pygame.freetype.STYLE_DEFAULT, 0, 36)
        self.gamedata.font.render_to(self.gamedata.screen, (stats_pos[0] + 140, stats_pos[1] + 36), f"Level {self.level}", self.archetype.text_color, None, pygame.freetype.STYLE_DEFAULT, 0, 20)

        y = stats_pos[1] + 140

        center_text_y(self.gamedata.screen, (stats_pos[0], y + 12), self.gamedata.font, "HP:", (255, 255, 255), 20)
        render_progress_bar(self.gamedata.screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (0, 200, 0), self.gamedata.font, (0, 0, 0), 2, self.health, self.archetype.get_max_health(self.level), "")
        y = y + 30

        if (self.archetype.get_max_mp(self.level) > 0):
            center_text_y(self.gamedata.screen, (stats_pos[0], y + 12), self.gamedata.font, "MP:", (255, 255, 255), 20)
            render_progress_bar(self.gamedata.screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (0, 200, 200), self.gamedata.font, (0, 0, 0), 2, self.mp, self.archetype.get_max_mp(self.level), "")
            y = y + 30

        if (self.archetype.get_max_stamina(self.level) > 0):
            center_text_y(self.gamedata.screen, (stats_pos[0], y + 12), self.gamedata.font, "ST:", (255, 255, 255), 20)
            render_progress_bar(self.gamedata.screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (200, 200, 0), self.gamedata.font, (0, 0, 0), 2, self.stamina, self.archetype.get_max_stamina(self.level), "")
            y = y + 30

        if (self.archetype.has_xp):
            center_text_y(self.gamedata.screen, (stats_pos[0], y + 12), self.gamedata.font, "XP:", (255, 255, 255), 20)
            render_progress_bar(self.gamedata.screen, (stats_pos[0] + 40, y), (240, 24), (255, 255, 255), (50, 50, 50), (200, 200, 200), self.gamedata.font, (0, 0, 0), 2, self.xp, self.archetype.get_max_xp(self.level), "")
            y = y + 30
            
        return y

    def update(self):
        if (self.controller != None):
            self.controller.update()

        self.stamina = min(self.stamina + self.archetype.get_stamina_recover(self.level), self.archetype.get_max_stamina(self.level))

    def modify_stamina(self, delta):
        self.stamina = min(self.archetype.get_max_stamina(self.level), max(0, self.stamina + delta))

        # Check if player runs out of stamina in a place where he needs stamina - like drowning
        if (self.stamina > 0):
            tile = self.gamedata.map_data.get_tile(self.player.position[0], self.player.position[1])
            if (tile.need_stamina):
                # Player takes damage
                self.player.modify_health(-10)

    def modify_health(self, delta):
        self.health = min(self.archetype.get_max_health(self.level), max(0, self.health + delta))

    def get_xp(self, level_hostile, level_friend):
        # Retrieves how much XP you get from this enemy
        delta = level_hostile - level_friend

        if (delta < -3):
            # You outlevel by too much, no XP
            return 0

        delta = delta + 4

        # Square the delta (plus three - so you get XP from enemies close to the level, but below) and multiply by 2
        # So, if level difference is 0 , you get 32,
        # if it is 1, you get 50, if it is 2, you get 72, if it is 3, you get 98, etc
        return (delta * delta) * 2

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

    def move(self, delta_x, delta_y):
        # Check if it is alive
        if (self.health <= 0):
            return False

        # If the character needs stamina (max_stamina > 0), check if we have enough stamina to move
        tile = self.gamedata.map_data.get_tile(self.position[0], self.position[1])
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
        enemy = self.gamedata.get_character_in_position(npx, npy)
        if (enemy != None):
            # Check if it is hostile
            if not self.gamedata.is_hostile(self.faction, enemy):
                # Can't move, position is occupied
                return False

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
                    self.gamedata.spawn_combat_text(enemy.position, (255, 0, 0), f"DEAD!", 16)
                    if (self.archetype.has_xp):
                        # Killed enemy, get XP
                        xp = enemy.get_xp(enemy.level, self.level)
                        self.modify_xp(xp)
                        self.gamedata.spawn_combat_text(self.position, (255, 255, 255), f"+{xp} XP!", 24, 2, 20)
                else:
                    if self.archetype.has_xp:
                        self.gamedata.spawn_combat_text(enemy.position, (255, 255, 0), f"-{total}", 16)
                    else:
                        self.gamedata.spawn_combat_text(enemy.position, (255, 0, 0), f"-{total}", 16)
                        
                    if (self.archetype.has_xp):
                        self.gamedata.track_character(enemy)

            return True

        next_tile = self.gamedata.map_data.get_tile(npx, npy)
        if (not next_tile.solid):
            self.stamina = self.stamina - cost
            self.position = (npx, npy)
            return True

        return False
