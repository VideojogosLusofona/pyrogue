from buff import *

BUFFS = {
    "Stun": Buff(display_name = "Stun", duration = 2, color = (240, 0, 0), status_text = "STUN", can_take_actions = False),
    "ToxicLickDOT": Buff_DOT(display_name = "Toxic Lick", duration = 3, color = (240, 0, 0), status_text = "POISON", damage_base = 5, damage_per_level = 3),
    "BurnDOT": Buff_DOT(display_name = "Burn", duration = 3, color = (240, 0, 0), status_text = "BURN", damage_base = 10, damage_per_level = 5)
}
