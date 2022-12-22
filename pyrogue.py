import pygame
from maptile import *
from archetype import *
from map import *
from gamedata import *
from archetypes import *

def main():
    GAMEDATA.init_pygame()
    GAMEDATA.init_assets()

    GAMEDATA.set_player_archetype(ARCHETYPES["PlayerWarrior"])

    wall_tile = MapTyle("images/wall.png", True)
    grass_tile = MapTyle("images/grass.png", False, stamina_cost = 1)
    water_tile = MapTyle("images/water.png", False, stamina_cost = 2, need_stamina = True)
    tree_tile = MapTyle("images/tree.png", True)
    empty_tile = MapTyle(None, True)

    tileset_outdoors = {
        '#' : { "tile" : wall_tile },
        'T' : { "tile" : tree_tile },
        '.' : { "tile" : grass_tile },
        'w' : { "tile" : water_tile },
        '@' : { "tile" : grass_tile, "func" : GAMEDATA.set_player_position },
        'B' : { "tile" : grass_tile, "func" : GAMEDATA.spawn_enemy, "func_param" : ARCHETYPES["Blob"] },
        ' ' : { "tile" : empty_tile },
        'default' : { "tile" : empty_tile }
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
                # Only handle one action per frame - we might miss actions
                if (not player_action):
                    player_action = GAMEDATA.handle_keypress(event.key)

        if (player_action):
            GAMEDATA.update_player()
            GAMEDATA.update_enemies()

        GAMEDATA.center_camera(GAMEDATA.player.position)

        # Compute elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - last_time) / 1000
        
        # Update time stamp
        last_time = pygame.time.get_ticks()

        # Realtime animate
        GAMEDATA.animate(elapsed_time)
        
        # Clears the screen to black
        GAMEDATA.screen.fill((0,0,8))
        
        GAMEDATA.render()

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

main()
