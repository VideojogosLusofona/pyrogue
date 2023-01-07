import pygame
import sys
import math

from map import *
from character import *
from combattext import *
from controllers import *

class GameData:
    res = (1280, 720)
    tile_size = (32, 32)
    map_pos = (0, 0)
    map_size = (28 * 32, 22 * 32)
    characters = []
    images = {}
    game_over = False
    tracked_character = None
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

    def set_player_archetype(self, archetype, level):
        self.player_archetype = archetype
        self.player_level = level

    def spawn_player(self, c, x, y, param):
        self.player = Character(self.player_archetype, self.player_level, (x, y), 0, self)
        self.player.controller = KeyboardController(self.player)
        self.characters.append(self.player)

    def spawn_enemy(self, c, x, y, param):
        enemy = Character(param[0], param[1], (x, y), 1, self)
        enemy.controller = AIController(enemy)
        self.characters.append(enemy)

    def get_enemy_in_position(self, x, y, faction):
        for character in self.characters:
            if (self.is_hostile(character.faction,faction)):
                if (character.position == (x,y)) and (character.health > 0):
                    return character
        
        return None

    def get_character_in_position(self, x, y):
        for character in self.characters:
            if (character.position == (x,y)) and (character.health > 0):
                return character
        
        return None

    def get_closest_enemy(self, x, y, faction):
        closest_dist = sys.float_info.max
        closest = None
        for character in self.characters:
            if (self.is_hostile(character.faction,faction)):
                if (character.health > 0):
                    dist = math.sqrt((character.position[0] - x)**2 + (character.position[1] - y)**2)
                    if (dist < closest_dist):
                        closest_dist = dist
                        closest = character
        
        return closest


    def is_hostile(self, f1, f2):
        return f1 != f2

    def track_character(self, character):
        self.tracked_character = character

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
        self.render_characters()
        self.render_stats()

        for ct in self.combat_text:
            ct.render(self.screen)

        if (self.game_over):
            center_text_xy(self.screen, (self.res[0] / 2, self.res[1] / 2), self.font, "  GAME OVER  ", (255, 0, 0), 60, (0, 0, 0)) 
            self.font.render_to(self.screen, (self.map_pos[0] + self.map_size[0] + 10, self.map_pos[1] + 270), "(R): Rest", (150, 150, 150), None, pygame.freetype.STYLE_DEFAULT, 0, 20)

    def render_map(self):
        self.map_data.draw(self.map_pos, self.map_size, self.camera_pos, self.screen)

    def render_characters(self):
        for character in self.characters:
            character.render()

    def render_stats(self):
        mx = self.map_pos[0] + self.map_size[0]
        rect = (mx, 0, self.res[0] - mx, self.res[1])

        pygame.draw.rect(self.screen, (0,0,0), rect, 0)

        y = self.player.render_stats((self.map_pos[0] + self.map_size[0] + 10, self.map_pos[1] + 10))

        y = y + 30
        y = self.render_player_actions(y)

        if (self.tracked_character != None):
            if (self.tracked_character.health <= 0):
                self.tracked_character = None
            else:
                y = y + 30
                y = self.tracked_character.render_stats((self.map_pos[0] + self.map_size[0] + 10, y))

    def render_player_actions(self, y):
        # Write player actions (instructions)
        self.font.render_to(self.screen, (self.map_pos[0] + self.map_size[0] + 10, y), "(R): Rest", (150, 150, 150), None, pygame.freetype.STYLE_DEFAULT, 0, 20)

        return y + 25

    def update_characters(self):
        for character in self.characters:
            if (character.health >= 0):
                character.update()

        if (self.player.health <= 0):
            self.game_over = True

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