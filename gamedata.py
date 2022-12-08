import pygame
from map import *

class GameData:
    res = (1280, 720)
    tile_size = (32, 32)
    map_pos = (0, 0)
    map_size = (28 * 32, 22 * 32)

    def load_map(self, filename, tileset):
        self.map_data = Map(self.tile_size)
        self.map_data.load(filename, tileset)

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Pyrogue")

    def init_assets(self):
        self.player_img = pygame.image.load("images/player.png")

    def set_player_pos(self, x, y):
        self.player_pos = (x, y)

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

    def render_map(self):
        self.map_data.draw(self.map_pos, self.map_size, self.camera_pos, self.screen)

    def render_player(self):
        px = self.map_pos[0] + self.tile_size[0] * (self.player_pos[0] - self.camera_pos[0])
        py = self.map_pos[1] + self.tile_size[1] * (self.player_pos[1] - self.camera_pos[1])

        self.screen.blit(self.player_img, (px, py))

    def render_stats(self):
        mx = self.map_pos[0] + self.map_size[0]
        rect = (mx, 0, self.res[0] - mx, self.res[1])

        pygame.draw.rect(self.screen, (0,0,0), rect, 0)

    def move_player(self, delta_x, delta_y):
        npx = self.player_pos[0] + delta_x
        npy = self.player_pos[1] + delta_y
        if (not self.map_data.is_wall(npx, npy)):
            self.player_pos = (npx, npy)

    def handle_keypress(self, key):
        if (key == pygame.K_RIGHT):
            self.move_player(1, 0)
            return True
        if (key == pygame.K_LEFT):
            self.move_player(-1, 0)
            return True
        if (key == pygame.K_UP):
            self.move_player(0, -1)
            return True
        if (key == pygame.K_DOWN):
            self.move_player(0, 1)
            return True

    def update_enemies(self):
        pass

global GAMEDATA
GAMEDATA = GameData()