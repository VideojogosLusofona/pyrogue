
class Buff:
    def __init__(self, display_name, duration = 5, color = (0, 200, 0), status_text = None, can_take_actions = True):
        self.display_name = display_name
        self.duration = duration
        self.has_duration = duration > 0
        self.color = color
        self.status_text = status_text
        self.can_take_actions = can_take_actions

    def tick(self, data):
        pass

class Buff_DOT(Buff):
    def __init__(self, display_name, duration = 5, color = (0, 200, 0), status_text = None, can_take_actions = True, damage_base = 0, damage_per_level = 0):
        super().__init__(display_name, duration, color, status_text, can_take_actions)

        self.damage_base = damage_base
        self.damage_per_level = damage_per_level

    def get_damage(self, level):
        return self.damage_base + self.damage_per_level * (level - 1)

    def tick(self, data):
        data.target.deal_damage(self.get_damage(data.src.level), data.src)

####################################################################################################

class BuffData:
    def __init__(self, buff, target, src):
        self.buff = buff
        self.target = target
        self.src = src
        # Need to add one since one of them will be consumed in the same turn as the player inflicts it
        self.duration = buff.duration + 1

    def tick(self):
        self.duration = self.duration - 1

        self.buff.tick(self)

        return self.duration >= 0
