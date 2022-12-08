# Pyrogue

This is a simple roguelike game built in Python, as a students exercise of the [Licenciatura em Videojogos][lv] da
[Universidade Lusófona de Humanidades e Tecnologias][ULHT] in Lisbon.

The particle system was built using:
* Python 3.11
* Pygame (https://www.pygame.org/news)

## Current state

### (2022/12/08) 

![Image](progress/screen01.png)

* Tiles can be created, and maps can be loaded from HD using a translation unit (that converts ASCII characters to tiles)
* Player can move around using the arrow keys. Camera will focus on the player at all times

## Code Files

* pyrogue.py: Entrypoint for the code. Creates tiles, does the main application loop, retrieves input and calls the rendering code
* gamedata.py: Implements the GameData class, and creates the GAMEDATA singleton, through which most of the gamecode runs
* map.py: Implements the Map class, which takes care of the map, including rendering
* maptile.py: Implements the MapTile class, which acts like a prototype of an individual tile. There's only one instance of each map tile (for example, even if the map has 1000 grass tiles, they only point to a single MapTile object)

## Licenses

All code in this repo is made available through the [Apache License 2.0] license.
The text and all the other files are made available through the 
[CC BY-NC-SA 4.0] license.

## Metadata

* Autor: [Diogo Andrade][]

[Diogo Andrade]:https://github.com/DiogoDeAndrade
[Apache License 2.0]:LICENSE
[CC BY-NC-SA 4.0]:https://creativecommons.org/licenses/by-nc-sa/4.0/
[ULHT]:https://www.ulusofona.pt/
[lv]:https://www.ulusofona.pt/licenciatura/videojogos