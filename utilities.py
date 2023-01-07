import pygame
import pygame.freetype
import math

def center_text_x(screen, pos, font, text, fg_color, size, bg_color = None, style = pygame.freetype.STYLE_DEFAULT, rotation = 0):
        text, text_rect = font.render(text, fg_color, bg_color, style, rotation, size)
        screen.blit(text, (pos.x - text_rect.width / 2, pos.y))

def center_text_y(screen, pos, font, text, fg_color, size, bg_color = None, style = pygame.freetype.STYLE_DEFAULT, rotation = 0):
        text, text_rect = font.render(text, fg_color, bg_color, style, rotation, size)
        screen.blit(text, (pos.x, pos.y - text_rect.height / 2))

def center_text_xy(screen, pos, font, text, fg_color, size, bg_color = None, style = pygame.freetype.STYLE_DEFAULT, rotation = 0):
        text, text_rect = font.render(text, fg_color, bg_color, style, rotation, size)
        screen.blit(text, (pos.x - text_rect.width / 2, pos.y - text_rect.height / 2))

def render_progress_bar(screen, pos, size, out_color, bg_color, bar_color, font, text_color, outline_width, value, max_value, pre_text):
        if (bg_color != None):
            pygame.draw.rect(screen, bg_color, (pos.x, pos.y, size.x, size.y), 0)

        d = int(math.floor(size.x * value / max_value))
        pygame.draw.rect(screen, bar_color, (pos.x, pos.y, d, size.y), 0)

        if (font != None):
            center_text_xy(screen, pos + size / 2, font, f"{pre_text}{int(value)}/{int(max_value)}", text_color, size.y - 8)

        if (out_color != None) and (outline_width != None):
            pygame.draw.rect(screen, out_color, (pos.x, pos.y, size.x, size.y), outline_width)
