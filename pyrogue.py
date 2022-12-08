import pygame
from maptile import *
from map import *
from gamedata import *

def set_player_pos(c, x, y):
    GAMEDATA.set_player_pos(x, y)

def main():
    GAMEDATA.init_pygame()
    GAMEDATA.init_assets()

    wall_tile = MapTyle(pygame.image.load("images/wall.png"), True)
    grass_tile = MapTyle(pygame.image.load("images/grass.png"), False)

    tileset_outdoors = {
        '#' : { "tile" : wall_tile },
        '.' : { "tile" : grass_tile },
        '@' : { "tile" : grass_tile, "func" : set_player_pos }
    }

    GAMEDATA.load_map("maps/test.map", tileset_outdoors)

    last_time = pygame.time.get_ticks()
    exit = False
    while not exit:
        # Process system events
        player_action = False

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit = True
            elif (event.type == pygame.KEYDOWN):
                player_action = GAMEDATA.handle_keypress(event.key)

        if (player_action):
            GAMEDATA.update_enemies()

        GAMEDATA.center_camera(GAMEDATA.player_pos)

        # Compute elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - last_time) / 1000
        
        # Update time stamp
        last_time = pygame.time.get_ticks()
        
        # Clears the screen to black
        GAMEDATA.screen.fill((0,0,8))
        
        # Draw map
        GAMEDATA.render_map()
        GAMEDATA.render_player()
        GAMEDATA.render_stats()

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

main()
    