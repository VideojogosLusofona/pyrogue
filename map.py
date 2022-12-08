import math

class Map:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def load(self, filename, tileset):
        file = open(filename, "r")
        if (file == None):
            print(f"Error opening {filename}!")
            return False

        self.map = []
        self.sx = 0
        self.sy = 0
        
        for line in file:
            row = []
            x = 0
            for c in line.strip():
                if (c not in tileset):
                    print(f"Unknown tile {c}!")
                else:
                    t = tileset[c]
                    row.append(t["tile"])

                    if ("func" in t):
                        t["func"](c, x , self.sy)

                    x += 1

            self.sx = max(self.sx, len(row))
            self.sy += 1
            self.map.append(row)

        file.close()

        return True

    def is_wall(self, x, y):
        return self.map[y][x].solid

    def draw(self, screen_pos, screen_size, offset, screen):
        msx = math.ceil(screen_size[0] / self.tile_size[0])
        msy = math.ceil(screen_size[1] / self.tile_size[1])

        for y in range(offset[1], min(self.sy, offset[1] + msy)):
            map_row = self.map[y]
            py = screen_pos[1] + (y - offset[1]) * self.tile_size[1]
            for x in range(offset[0], min(min(len(map_row), self.sx), offset[0] + msx)):
                px = screen_pos[0] + (x - offset[0]) * self.tile_size[0]
                screen.blit(map_row[x].image, (px,py))




