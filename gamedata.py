import pygame
from map import *
from character import *
from combattext import *

class GameData:
    res = (1280, 720)
    tile_size = (32, 32)
    map_pos = (0, 0)
    map_size = (28 * 32, 22 * 32)
    enemies = []
    images = {}
    game_over = False
    tracked_enemy = None
    combat_text = []

    def load_map(self, filename, tileset):
        self.map_data = Map(self.tile_size)
        self.map_data.load(filename, tileset)

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Pyrogue")

    def init_assets(self):
        self.font = pygame.freetype.Font("font/Deutsch.ttf", 12)
        self.images["Blood"] = pygame.image.load("images/blood.png")

    def get_image(self, name):
        if (name in self.images):
            return self.images[name]
        else:
            print(f"Can't find image {name}!")

    def set_player_archetype(self, archetype):
        self.player = Character(archetype, (0,0), self)

    def set_player_position(self, c, x, y, param):
        self.player.position = (x, y)

    def spawn_enemy(self, c, x, y, param):
        self.enemies.append(Character(param, (x, y), self))

    def get_enemy_in_position(self, x, y):
        for enemy in self.enemies:
            if (enemy.position == (x,y)) and (enemy.health > 0):
                return enemy
        
        return None

    def track_enemy(self, enemy):
        self.tracked_enemy = enemy

    def center_camera(self, pos):
        tsx = self.map_size[0] / self.tile_size[0]
        tsy = self.map_size[1] / self.tile_size[1]

        camera_x = pos[0] - tsx / 2
        camera_y = pos[1] - tsy / 2
        if (camera_x + tsx >= self.map_data.sx):
            camera_x = self.map_data.sx - tsx
        if (camera_y + tsy >= self.map_data.sy):
            camera_y = self.map_data.sy - tsy
        if (camera_x < 0):
            camera_x = 0
        if (camera_y < 0):
            camera_y = 0

        self.camera_pos = (int(camera_x), int(camera_y))

    def render(self):
        self.render_map()
        self.render_enemies()
        self.render_player()
        self.render_stats()

        for ct in self.combat_text:
            ct.render(self.screen)

        if (self.game_over):
            center_text_xy(self.screen, (self.res[0] / 2, self.res[1] / 2), self.font, "  GAME OVER  ", (255, 0, 0), 60, (0, 0, 0)) 
            self.font.render_to(self.screen, (self.map_pos[0] + self.map_size[0] + 10, self.map_pos[1] + 270), "(R): Rest", (150, 150, 150), None, pygame.freetype.STYLE_DEFAULT, 0, 20)

    def render_map(self):
        self.map_data.draw(self.map_pos, self.map_size, self.camera_pos, self.screen)

    def render_player(self):
        self.player.render(self.map_pos, self.tile_size, self.camera_pos, self.screen)

    def render_enemies(self):
        for enemy in self.enemies:
            enemy.render(self.map_pos, self.tile_size, self.camera_pos, self.screen)

    def render_stats(self):
        mx = self.map_pos[0] + self.map_size[0]
        rect = (mx, 0, self.res[0] - mx, self.res[1])

        pygame.draw.rect(self.screen, (0,0,0), rect, 0)

        y = self.player.render_stats((self.map_pos[0] + self.map_size[0] + 10, self.map_pos[1] + 10), self.font, (0, 200, 200), self.screen)

        y = y + 30
        y = self.render_player_actions(y)

        if (self.tracked_enemy != None):
            if (self.tracked_enemy.health <= 0):
                self.tracked_enemy = None
            else:
                y = y + 30
                y = self.tracked_enemy.render_stats((self.map_pos[0] + self.map_size[0] + 10, y), self.font, (255, 0, 0), self.screen)

    def render_player_actions(self, y):
        # Write player actions (instructions)
        self.font.render_to(self.screen, (self.map_pos[0] + self.map_size[0] + 10, y), "(R): Rest", (150, 150, 150), None, pygame.freetype.STYLE_DEFAULT, 0, 20)

        return y + 25

    def handle_keypress(self, key):
        if (self.game_over):
            return False

        if (key == pygame.K_r):
            tile = self.map_data.get_tile(self.player.position[0], self.player.position[1])
            if (tile.need_stamina):
                self.player.modify_stamina(-tile.stamina_cost)
            return True
        if (key == pygame.K_RIGHT):
            return self.player.move(self.map_data, 1, 0)
        if (key == pygame.K_LEFT):
            return self.player.move(self.map_data, -1, 0)
        if (key == pygame.K_UP):
            return self.player.move(self.map_data, 0, -1)
        if (key == pygame.K_DOWN):
            return self.player.move(self.map_data, 0, 1)

        return False

    def update_player(self):
        # Check if player runs out of stamina in a place where he needs stamina - like drowning
        if (self.player.stamina <= 0):
            tile = self.map_data.get_tile(self.player.position[0], self.player.position[1])
            if (tile.need_stamina):
                # Player takes damage
                self.player.modify_health(-10)

        # Check if player died
        if (self.player.health <= 0):
            self.game_over = True
        else:
            # Update stamina, etc
            self.player.update()

    def update_enemies(self):
        pass

    def spawn_combat_text(self, tile_pos, color, text, size, life = 1, total_delta = 40):
        pos = self.convert_tile_pos_to_pixel(tile_pos)
        pos = (pos[0] + self.tile_size[0] / 2, pos[1])

        self.combat_text.append(CombatText(pos, color, text, self.font, size, life, total_delta))

    def convert_tile_pos_to_pixel(self, tile_pos):
        px = self.map_pos[0] + self.tile_size[0] * (tile_pos[0] - self.camera_pos[0])
        py = self.map_pos[1] + self.tile_size[1] * (tile_pos[1] - self.camera_pos[1])

        return (px, py)

    def animate(self, elapsed_time):
        for ct in self.combat_text:
            ct.update(elapsed_time)

        self.combat_text = [ct for ct in self.combat_text if ct.life > 0]


global GAMEDATA
GAMEDATA = GameData()