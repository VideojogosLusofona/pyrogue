import pygame

class MapTyle:
    def __init__(self, filename, solid, stamina_cost = 0, need_stamina = False):
        if (filename != None):
            self.image = pygame.image.load(filename)
            if (self.image == None):
                print(f"Can't load image {filename}!")
        else:
            self.image = None

        self.solid = solid
        self.stamina_cost = stamina_cost
        self.need_stamina = need_stamina

