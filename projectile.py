
class Projectile:
    def __init__(self, position, direction, ability_data, src):
        self.ability_data = ability_data
        self.src = src
        self.position = position
        self.direction = direction
        self.duration = ability_data.ability.projectile_duration

    def render(self):
        gamedata = self.src.gamedata
        p = gamedata.map_pos + gamedata.tile_size * (self.position - gamedata.camera_pos)

        image = self.ability_data.ability.image
        if (self.direction.x < 0):
            image = self.ability_data.ability.image_flipx
        elif (self.direction.y < 0):
            image = self.ability_data.ability.image_up
        elif (self.direction.y > 0):
            image = self.ability_data.ability.image_down

        self.src.gamedata.screen.blit(image, p.to_int_tuple())

    def tick(self):
        self.duration = self.duration - 1
        self.position = self.position + self.direction

        enemy = self.src.gamedata.get_enemy_in_position(self.position, self.src.faction)
        if (enemy != None):
            # Hit an enemy!
            self.execute_damage(enemy)

        tile = self.src.gamedata.map_data.get_tile(self.position)
        if (tile.solid):
            # Hits a wall
            self.duration = 0

    def execute_damage(self, target):
        self.duration = 0
        target.deal_damage(self.ability_data.ability.get_damage(self.src.level), self.src)
        self.ability_data.ability.apply_buffs(target, self.src)
