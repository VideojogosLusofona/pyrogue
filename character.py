import pygame
import pygame.freetype
import math

from utilities import *
from vector2 import *
from ability import *
from buff import *

class Character:
    def __init__(self, archetype, level, position, faction, gamedata):
        self.archetype = archetype
        self.position = position
        self.level = level
        self.health = archetype.get_max_health(self.level)
        self.mp = archetype.get_max_mp(self.level)
        self.stamina = archetype.get_max_stamina(self.level)
        self.xp = 0
        self.render_flipx = False
        self.gamedata = gamedata
        self.faction = faction
        self.last_movement = Vector2(1, 0)

        if (self.archetype.controller != None):
            if (isinstance(self.archetype.controller, tuple)):
                params = (self,) + self.archetype.controller[1:]
                self.controller = self.archetype.controller[0].Create(*params)
            else:
                self.controller = self.archetype.controller.Create(self)
        else:
            self.controller = None

        self.ability_data = []
        for ability in self.archetype.abilities:
            self.ability_data.append(AbilityData(ability))

        self.buffs = []


    def render(self):
        p = self.gamedata.map_pos + self.gamedata.tile_size * (self.position - self.gamedata.camera_pos)

        image = self.archetype.image
        if (self.render_flipx):
            image = self.archetype.image_flipx
        if (self.health <= 0):
            image = self.gamedata.get_image("Blood")

        self.gamedata.screen.blit(image, p.to_int_tuple())

    def render_stats(self, stats_pos):
        pygame.draw.rect(self.gamedata.screen, (255, 255, 255), (stats_pos.x - 2, stats_pos.y - 2, 132, 132), 0)
        pygame.draw.rect(self.gamedata.screen, (40, 40, 40), (stats_pos.x - 1, stats_pos.y - 1, 130, 130), 0)
        self.gamedata.screen.blit(self.archetype.stat_image, stats_pos.to_int_tuple())

        self.gamedata.font.render_to(self.gamedata.screen, (stats_pos.x + 140, stats_pos.y), self.archetype.display_name, self.archetype.text_color, None, pygame.freetype.STYLE_DEFAULT, 0, 36)
        self.gamedata.font.render_to(self.gamedata.screen, (stats_pos.x + 140, stats_pos.y + 36), f"Level {self.level}", self.archetype.text_color, None, pygame.freetype.STYLE_DEFAULT, 0, 20)

        y = stats_pos.y + 140

        center_text_y(self.gamedata.screen, Vector2(stats_pos.x, y + 12), self.gamedata.font, "HP:", (255, 255, 255), 20)
        render_progress_bar(self.gamedata.screen, Vector2(stats_pos.x + 40, y), Vector2(240, 24), (255, 255, 255), (50, 50, 50), (0, 200, 0), self.gamedata.font, (0, 0, 0), 2, self.health, self.archetype.get_max_health(self.level), "")
        y = y + 30

        if (self.archetype.get_max_mp(self.level) > 0):
            center_text_y(self.gamedata.screen, Vector2(stats_pos.x, y + 12), self.gamedata.font, "MP:", (255, 255, 255), 20)
            render_progress_bar(self.gamedata.screen, Vector2(stats_pos.x + 40, y), Vector2(240, 24), (255, 255, 255), (50, 50, 50), (0, 200, 200), self.gamedata.font, (0, 0, 0), 2, self.mp, self.archetype.get_max_mp(self.level), "")
            y = y + 30

        if (self.archetype.get_max_stamina(self.level) > 0):
            center_text_y(self.gamedata.screen, Vector2(stats_pos.x, y + 12), self.gamedata.font, "ST:", (255, 255, 255), 20)
            render_progress_bar(self.gamedata.screen, Vector2(stats_pos.x + 40, y), Vector2(240, 24), (255, 255, 255), (50, 50, 50), (200, 200, 0), self.gamedata.font, (0, 0, 0), 2, self.stamina, self.archetype.get_max_stamina(self.level), "")
            y = y + 30

        if (self.archetype.has_xp):
            center_text_y(self.gamedata.screen, Vector2(stats_pos.x, y + 12), self.gamedata.font, "XP:", (255, 255, 255), 20)
            render_progress_bar(self.gamedata.screen, Vector2(stats_pos.x + 40, y), Vector2(240, 24), (255, 255, 255), (50, 50, 50), (200, 200, 200), self.gamedata.font, (0, 0, 0), 2, self.xp, self.archetype.get_max_xp(self.level), "")
            y = y + 30

        # Render buffs
        for buff in self.buffs:
            if (buff.buff.has_duration):
              self.gamedata.font.render_to(self.gamedata.screen, (stats_pos.x, y), f"{buff.buff.display_name} ({buff.duration})", buff.buff.color, None, pygame.freetype.STYLE_DEFAULT, 0, 14)
            else:
                self.gamedata.font.render_to(self.gamedata.screen, (stats_pos.x, y), f"{buff.buff.display_name}", buff.buff.color, None, pygame.freetype.STYLE_DEFAULT, 0, 14)
            y = y + 16
            
        return y

    def render_actions(self, action_pos):
        y = action_pos.y
        self.gamedata.font.render_to(self.gamedata.screen, (action_pos.x, y), "(R): Rest", (150, 150, 150), None, pygame.freetype.STYLE_DEFAULT, 0, 20)
        y = y + 25

        i = 1
        for ability_data in self.ability_data:
            if (ability_data.cooldown > 0):
                self.gamedata.font.render_to(self.gamedata.screen, (action_pos.x, y), f'({i}): {ability_data.ability.display_name} ({ability_data.cooldown} turns)', (50, 50, 50), None, pygame.freetype.STYLE_DEFAULT, 0, 20)
            else:
                self.gamedata.font.render_to(self.gamedata.screen, (action_pos.x, y), f'({i}): {ability_data.ability.display_name}', (150, 150, 150), None, pygame.freetype.STYLE_DEFAULT, 0, 20)
            i = i + 1
            y = y + 25

        return y

    def update(self):
        if (self.can_take_action()):
            if (self.controller != None):
                self.controller.update()

    def upkeep(self):
        # Regen
        self.stamina = min(self.stamina + self.archetype.get_stamina_recover(self.level), self.archetype.get_max_stamina(self.level))
        self.mp = min(self.mp + self.archetype.get_mp_recover(self.level), self.archetype.get_max_mp(self.level))

        # Update abilities
        for ability_data in self.ability_data:
            ability_data.cooldown = max(0, ability_data.cooldown - 1)
            
        # Update buffs
        for buff in self.buffs:
            if (buff.buff.has_duration):
                buff.tick()

        self.buffs = [b for b in self.buffs if (not b.buff.has_duration) or (b.duration > 0)]
        

    def modify_stamina(self, delta):
        self.stamina = min(self.archetype.get_max_stamina(self.level), max(0, self.stamina + delta))

        # Check if player runs out of stamina in a place where he needs stamina - like drowning
        if (self.stamina > 0):
            tile = self.gamedata.map_data.get_tile(self.position)
            if (tile.need_stamina):
                # Player takes damage
                self.player.modify_health(-10)

    def modify_health(self, delta):
        self.health = min(self.archetype.get_max_health(self.level), max(0, self.health + delta))

    def modify_mp(self, delta):
        self.mp = min(self.archetype.get_max_mp(self.level), max(0, self.mp + delta))

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

    def move(self, delta_x, delta_y, can_attack = True):
        # Check if it is alive
        if (self.health <= 0):
            return False

        # If the character needs stamina (max_stamina > 0), check if we have enough stamina to move
        tile = self.gamedata.map_data.get_tile(self.position)
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

        np = self.position + Vector2(delta_x, delta_y)

        # Check if there is an enemy in the new position, if there is
        # do a melee attack, otherwise move
        enemy = self.gamedata.get_character_in_position(np)
        if (enemy != None):
            # Check if it is hostile
            if (not self.gamedata.is_hostile(self.faction, enemy.faction)) or (not can_attack):
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
            else:                
                enemy.deal_damage(total, self)

            self.last_movement = Vector2(delta_x, delta_y)
            return True

        next_tile = self.gamedata.map_data.get_tile(np)
        if (not next_tile.solid):
            self.stamina = self.stamina - cost
            self.position = np
            self.last_movement = Vector2(delta_x, delta_y)

            # Check if there is a projectile in this position
            projectile = self.gamedata.get_projectile_at_position(self.position)
            if (projectile != None):
                projectile.execute_damage(self)
            return True

        return False

    def deal_damage(self, damage, damage_src):
        self.modify_health(-damage)
        if (self.health <= 0):
            self.gamedata.spawn_combat_text(self.position, (255, 0, 0), f"DEAD!", 16)
            if (damage_src.archetype.has_xp):
                # Killed enemy, get XP
                xp = self.get_xp(self.level, damage_src.level)
                damage_src.modify_xp(xp)
                self.gamedata.spawn_combat_text(damage_src.position, (255, 255, 255), f"+{xp} XP!", 24, 2, 20)
        else:
            text_color = (255, 255, 0)
            if damage_src.archetype.has_xp:
                text_color = (255, 0, 0)

            self.gamedata.spawn_combat_text(self.position, text_color, f"-{damage}", 16)

            if (damage_src.archetype.has_xp):
                self.gamedata.track_character(self)
        
    def is_alive(self):
        return self.health > 0

    def is_dead(self):
        return self.health <= 0

    def run_ability(self, index):
        # Check if ability exists
        if (index < 0) or (index >= len(self.ability_data)):
            return False

        ability_data = self.ability_data[index]
        
        can_execute = ability_data.ability.can_execute(ability_data, self)
        if (can_execute):
            ability_data.ability.execute(ability_data, self)

        return can_execute

    def get_melee_position(self):
        # Computes the position next to the player in the direction he is moving
        return self.position + self.last_movement

    def get_direction(self):
        return self.last_movement

    def apply_buff(self, buff, src):
        buff_data = BuffData(buff, self, src)
        self.buffs.append(buff_data)

        if (buff_data.buff.status_text != None):
            self.gamedata.spawn_combat_text(self.position, buff_data.buff.color, buff_data.buff.status_text, 30, 2, 40)

    def can_take_action(self):
        for buff in self.buffs:
            if (not buff.buff.can_take_actions):
                return False

        return True