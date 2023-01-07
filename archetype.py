import pygame

class Archetype:
    def __init__(self, display_name, filename = "None", text_color = (240, 0, 0), max_health_base = 100, max_health_per_level = 0, max_mp_base = 0, max_mp_per_level = 0, max_stamina_base = 100, max_stamina_per_level = 0,
                 stamina_recover_base = 0, stamina_recover_per_level = 0, attack_power_base = 10, attack_power_per_level = 0, defense_power_base = 0, defense_power_per_level = 0,
                 melee_stamina_cost_base = 0, melee_stamina_cost_per_level = 0, has_xp = False):
        if (filename != None):
            self.image = pygame.image.load(filename)
            if (self.image == None):
                print(f"Can't load image {filename}!")
            else:
                self.stat_image = pygame.transform.scale(self.image, (128, 128))
                self.image_flipx = pygame.transform.flip(self.image, True, False) 
        else:
            self.image = None

        self.display_name = display_name
        self.text_color = text_color
        self.max_health_base = max_health_base
        self.max_health_per_level = max_health_per_level
        self.max_mp_base = max_mp_base
        self.max_mp_per_level = max_mp_per_level
        self.max_stamina_base = max_stamina_base
        self.max_stamina_per_level = max_stamina_per_level
        self.stamina_recover_base = stamina_recover_base
        self.stamina_recover_per_level = stamina_recover_per_level
        self.attack_power_base = attack_power_base
        self.attack_power_per_level = attack_power_per_level
        self.defense_power_base = defense_power_base
        self.defense_power_per_level = defense_power_per_level
        self.melee_stamina_cost_base = melee_stamina_cost_base
        self.melee_stamina_cost_per_level = melee_stamina_cost_per_level
        self.has_xp = has_xp

    def get_max_health(self, level):
        return self.max_health_base + self.max_health_per_level * (level - 1)

    def get_max_mp(self, level):
        return self.max_mp_base + self.max_mp_per_level * (level - 1)

    def get_max_stamina(self, level):
        return self.max_stamina_base + self.max_stamina_per_level * (level - 1)

    def get_max_xp(self, level):
        return level * 100

    def get_stamina_recover(self, level):
        return self.stamina_recover_base + self.stamina_recover_per_level * (level - 1)

    def get_attack_power(self, level):
        return self.attack_power_base + self.attack_power_per_level * (level - 1)

    def get_defense_power(self, level):
        return self.defense_power_base + self.defense_power_per_level * (level - 1)

    def get_melee_attack_stamina_cost(self, level):
        return self.melee_stamina_cost_base + self.melee_stamina_cost_per_level * (level - 1)