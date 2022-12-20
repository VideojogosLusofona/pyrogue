import pygame

class MapTyle:
    def __init__(self, filename, solid):
        if (filename != None):
            self.image = pygame.image.load(filename)
            if (self.image == None):
                print(f"Can't load image {filename}!")
        else:
            self.image = None

        self.solid = solid

