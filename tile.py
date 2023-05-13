import pygame as pg

from colors import MyColors

OFFSET = 5
TILE_SIZE = 9

# variations
VARS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = TILE_SIZE
        self.color = MyColors.empty()
        self.value = 0
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.area = ()

    def set_tile_pos(self, x, y):
        self.rect.x = (x * 10) + OFFSET
        self.rect.y = (y * 10) + OFFSET

    def in_bounds(self, tm, x, y):
        if ((x + 1) >= len(tm.tilesMatrix)):
            return False
        if ((y + 1) >= len(tm.tilesMatrix[0])):
            return False
        return True

    def update_neighbors(self, tm, show_step):
        next_tiles = []
        x = self.x
        y = self.y
        val = tm.tilesMatrix[x][y].value

        if val == 'F':
            val = 0

        for var in VARS:
            x = self.x
            y = self.y
            x = x + var[0]
            y = y + var[1]
            if self.in_bounds(tm, x, y):
                if (x >= 0) and (y >= 0):
                    if tm.tilesMatrix[x][y].value == 0:
                        tm.tilesMatrix[x][y].value = val + 1

                        if show_step:
                            #tm.tilesMatrix[x][y].color = (10,100,10)
                            tm.tilesMatrix[x][y].color = (tm.r, tm.g, tm.b)
                            tm.render(tm.screen)

                        pg.display.flip()
                        next_tiles.append(((x), (y)))
                    if tm.tilesMatrix[x][y].value == 'I':
                        return tm.tilesMatrix[x][y]
        return next_tiles
