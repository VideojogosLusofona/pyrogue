import math
from vector2 import *

class Map:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def load(self, filename, tileset):
        file = open(filename, "r")
        if (file == None):
            print(f"Error opening {filename}!")
            return False

        self.map = []
        self.size = Vector2()
        
        for line in file:
            row = []
            x = 0
            for c in line:
                if ((c == '\n') or (c == '\r')):
                    c = None
                elif (c not in tileset):
                    if ("default" in tileset):
                        c = "default"
                    else:
                        print(f"Unknown tile {c}!")
                        c = None
                if (c != None):
                    t = tileset[c]
                    row.append(t["tile"])

                    if ("func" in t):
                        p = None
                        if ("func_param" in t):
                            p = t["func_param"]
                        t["func"](c, x , self.size.y, p)

                    x += 1

            self.size.x = max(self.size.x, len(row))
            self.size.y += 1
            self.map.append(row)

        file.close()

        return True

    def get_tile(self, p):
        return self.map[int(p.y)][int(p.x)]
        
    def draw(self, screen_pos, screen_size, offset, screen):
        msx = math.ceil(screen_size.x / self.tile_size.x)
        msy = math.ceil(screen_size.y / self.tile_size.y)

        for y in range(offset.y, min(self.size.y, offset.y + msy)):
            map_row = self.map[y]
            py = screen_pos.y + (y - offset.y) * self.tile_size.y
            for x in range(offset.x, min(min(len(map_row), self.size.x), offset.x + msx)):
                px = screen_pos.x + (x - offset.x) * self.tile_size.x
                if (map_row[x].image != None):
                    screen.blit(map_row[x].image, (px,py))




