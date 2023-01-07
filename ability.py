import pygame
from projectile import *
from vector2 import *

class Ability:
    def __init__(self, display_name, cooldown = 1, 
                 stamina_cost_base = 0, stamina_cost_per_level = 0,
                 mana_cost_base = 0, mana_cost_per_level = 0,
                 damage_base = 0, damage_per_level = 0,
                 buffs = []):
        self.display_name = display_name
        self.cooldown = cooldown
        self.stamina_cost_base = stamina_cost_base
        self.stamina_cost_per_level = stamina_cost_per_level
        self.mana_cost_base = mana_cost_base
        self.mana_cost_per_level = mana_cost_per_level
        self.damage_base = damage_base
        self.damage_per_level = damage_per_level
        self.buffs = buffs

    def can_execute(self, data, src):
        # Check if ability is on cooldown
        if (data.cooldown > 0):
            return False

        # Check costs
        if (src.stamina < self.get_stamina_cost(src.level)):
            return False
        if (src.mp < self.get_mana_cost(src.level)):
            return False

        return True

    def execute(self, data, src):
        # Handle cooldown and costs
        data.cooldown = self.cooldown
        src.modify_stamina(-self.get_stamina_cost(src.level))
        src.modify_mp(-self.get_mana_cost(src.level))

    def get_damage(self, level):
        return self.damage_base + self.damage_per_level * (level - 1)

    def get_stamina_cost(self, level):
        return self.stamina_cost_base + self.stamina_cost_per_level * (level - 1)

    def get_mana_cost(self, level):
        return self.mana_cost_base + self.mana_cost_per_level * (level - 1)

    def apply_buffs(self, target, src):
        for buff in self.buffs:
            target.apply_buff(buff, src)


########################################################################################################################################################
class Ability_Melee(Ability):
    
    def can_execute(self, data, src):
        if (not super().can_execute(data, src)):
            return False

        # Check if there is an enemy in the direction we've last moved
        enemy = src.gamedata.get_enemy_in_position(src.get_melee_position(), src.faction)
        if (enemy == None):
            return False

        return True

    def execute(self, data, src):
        # Handle cooldown and costs
        super().execute(data, src)

        # Check if there is an enemy in the direction we've last moved
        enemy = src.gamedata.get_enemy_in_position(src.get_melee_position(), src.faction)
        if (enemy != None):
            enemy.deal_damage(self.get_damage(src.level), src)
            self.apply_buffs(enemy, src)

########################################################################################################################################################
class Ability_Projectile(Ability):
    def __init__(self, display_name, cooldown = 1, 
                 stamina_cost_base = 0, stamina_cost_per_level = 0,
                 mana_cost_base = 0, mana_cost_per_level = 0,
                 damage_base = 0, damage_per_level = 0,
                 buffs = [],
                 filename = None,
                 duration = 5):
        super().__init__(display_name, cooldown, stamina_cost_base, stamina_cost_per_level, mana_cost_base, mana_cost_per_level, damage_base, damage_per_level, buffs)

        self.projectile_duration = duration

        if (filename != None):
            self.image = pygame.image.load(filename)
            if (self.image == None):
                print(f"Can't load image {filename}!")
            else:
                self.image_flipx = pygame.transform.flip(self.image, True, False) 
                self.image_up = pygame.transform.rotate(self.image, 90) 
                self.image_down = pygame.transform.rotate(self.image, -90) 
        else:
            self.image = None

    def can_execute(self, data, src):
        if (not super().can_execute(data, src)):
            return False

        return True

    def execute(self, data, src):
        # Handle cooldown and costs
        super().execute(data, src)

        # Create a projectile
        projectile = Projectile(src.position, src.get_direction(), data, src)
        src.gamedata.add_projectile(projectile)


########################################################################################################################################################
class AbilityData:
    def __init__(self, ability):
        self.ability = ability
        self.cooldown = 0
        self.position = Vector2(0, 0)
