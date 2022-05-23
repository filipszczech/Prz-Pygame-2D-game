import pygame
from objects import Tile
from player import player

level_map = [
'                               ',
'                               ',
'                               ',
' XX    XXX               XX    ',
' XX                            ',
' XXXX            XX         XX ',
' XXXX          XX              ',
' XX    X     XXXX    XX  XX    ',
'       X     XXXX    XX  XXX   ',
'    XXXX     XXXXXX  XX  XXXX  ',
'XXXXXXXX     XXXXXX  XX  XXXX  ',
'XXXXXXXXX    XXXXXX  XX  XXXX  ',
'XXXXXXXXX    XXXXXX  XX  XXXX  ',
'XXXXXXXXX    XXXXXX  XX  XXXX  ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

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

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                #if cell == 'P':
                #    player_sprite = player((x, y))
                #    self.player.add(player_sprite)
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
                    print("KOLIZJA")
                elif player.left == False:
                    player.rect.right = sprite.rect.left

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

    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)