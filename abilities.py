from ability import *
from buffs import *

ABILITIES = {
    "ShieldBash": Ability_Melee(
        display_name = "Shield Bash",
        cooldown = 2,
        stamina_cost_base = 10,
        stamina_cost_per_level = 5,
        damage_base = 20,
        damage_per_level = 10,
        buffs = [ BUFFS["Stun"] ]),
    "ToxicLick": Ability_Melee(
        display_name = "Toxic Lick",
        cooldown = 4,
        buffs = [ BUFFS["ToxicLickDOT"] ]),
    "Firebolt": Ability_Projectile(
        display_name = "Firebolt",
        filename = "images/firebolt.png",
        cooldown = 2,
        mana_cost_base = 20,
        mana_cost_per_level = 10,
        damage_base = 15,
        damage_per_level = 8,
        duration = 6),
    "Fireball": Ability_Projectile(
        display_name = "Fireball",
        filename = "images/fireball.png",
        cooldown = 4,
        mana_cost_base = 30,
        mana_cost_per_level = 15,
        damage_base = 30,
        damage_per_level = 15,
        duration = 10,
        buffs = [ BUFFS["BurnDOT"] ]),
}
