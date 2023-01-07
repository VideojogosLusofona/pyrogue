from archetype import *
from controllers import * 

ARCHETYPES = {
    "PlayerWarrior": Archetype(
        display_name = "Warrior", 
        filename = "images/player.png",
        controller = (KeyboardController),
        text_color = (0, 240, 240),
        max_health_base = 100,
        max_health_per_level = 5,
        max_mp_base = 0,
        max_mp_per_level = 0,
        max_stamina_base = 100,
        max_stamina_per_level = 10,
        stamina_recover_base = 1,
        stamina_recover_per_level = 0.25,
        attack_power_base = 10,
        attack_power_per_level = 5,
        defense_power_base = 0,
        defense_power_per_level = 0,
        melee_stamina_cost_base = 2,
        melee_stamina_cost_per_level = 0,
        has_xp = True
        ),
    "Blob": Archetype(
        display_name = "Blob", 
        filename = "images/blob.png",
        controller = (AIController_WanderAndChase, 5, 10),
        max_health_base = 100,
        max_health_per_level = 5,
        max_stamina_base = 0,
        max_stamina_per_level = 0,
        attack_power_base = 2,
        attack_power_per_level = 2,
        defense_power_base = 0,
        defense_power_per_level = 5
        ),
}
