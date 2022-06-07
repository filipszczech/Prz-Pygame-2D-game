import pygame
from objects import Tile, Kolce, Meta
from player import player

level_map = [
'                                        ',
' M                                      ',
'                                        ',
' X       X      X      XYX              ',
'                                        ',
'                                 X      ',
'                                        ',
'                                        ',
' XXX                     XXX            ',
'                                        ',
'                                        ',
'       XX           XXXX                ',
'                                        ',
'                                        ',
'XXX          X   X       X   X      X   ',
'             XYYYX       XYYYX          ']

level_map2 = [
'                                        ',
' M                                      ',
'                                        ',
' X       X      X      XYX              ',
'                                        ',
'                                 X      ',
'                                        ',
'                                        ',
' XXX                     XXX            ',
'                                        ',
'                                        ',
'       XX           XXXX                ',
'                                        ',
'                                        ',
'XXX          X   X       X   X      X   ',
'             XYYYX       XYYYX          ']

tile_size = 32
screen_width = 1200
screen_height = len(level_map) * tile_size

class Level:
    def __init__(self, surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_map)
        self.world_shift = 0
        self.current_x = 0
        self.delay = 27

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.kolce = pygame.sprite.Group()
        self.meta = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                    tile.draw(self.display_surface, x, y)

                if cell == 'Y':
                    kolec = Kolce((x, y), tile_size)
                    self.kolce.add(kolec)
                    kolec.draw(self.display_surface, x, y)

                if cell == 'M':
                    meta = Meta((x, y), tile_size)
                    self.meta.add(meta)
                    meta.draw(self.display_surface, x, y)

    """
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    """
    

    def horizontal_movement_collision(self, player):
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.left:
                    player.rect.left = sprite.rect.right
                elif player.left == False:
                    player.rect.right = sprite.rect.left
        for sprite in self.meta.sprites():
            if sprite.rect.colliderect(player.rect):
                print("wygralem")
                return True

    def vertical_movement_collision(self, player):
        player.aply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.y = player.rect.bottom
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.y = player.rect.top  + 64
                    player.direction.y = 0

        for sprite in self.kolce.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.y = player.rect.bottom
                    player.onGround = True
                    self.hit(player)
    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        #self.tiles.draw(self.display_surface)
        for tile in self.tiles:
            tile.draw(self.display_surface, tile.rect.x, tile.rect.y)

        for kolec in self.kolce:
            kolec.draw(self.display_surface, kolec.rect.x, kolec.rect.y)
        pygame.display.update()


        for meta in self.meta:
            meta.draw(self.display_surface, meta.rect.x, meta.rect.y)
    #obrażenia od lawy
    def hit(self, player):
        if self.delay == 27:
            player.hit()
            self.delay = 0
        else:
            self.delay = self.delay + 1

"""
    current_level_index = 0
    game_over = 0
    total_levels = 2
    poziomy = [
        level_map,
        level_map2
    ]

    def reset_level(current_level_index):
        # Reset player position
        player.reset(100, screen_height - 130)
        # Empty groups
        # bat_group.empty()
        # door_group.empty()
        # Load in level data and create world)
        return world

    if current_level_index <= total_levels:
        poziom = poziomy[current_level_index]
"""