import random

import pygame as pg

from colors import MyColors
from tile import Tile

# variations
VARS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = False
        self.init_point = None
        self.end_point = None
        self.path = []
        self.found = False
        self.screen = None
        self.r = 250
        self.g = 250
        self.b = 250
        # Create a matrix filled with zero
        self.tilesMatrix = [
            [0 for _ in range(self.height)] for _ in range(self.width)]

    def init(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(x, y)
                tile.set_tile_pos(x, y)
                self.tilesMatrix[x][y] = tile

    def clear_path(self):
        self.r = 250
        self.g = 250
        self.b = 250
        keep = ['O', 'I', 'F']
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tilesMatrix[x][y]

                if tile.value not in keep:
                    tile.value = 0
                    tile.color = MyColors.empty()
        self.found = False

    def clear_map(self):
        self.r = 250
        self.g = 250
        self.b = 250
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tilesMatrix[x][y]
                tile.value = 0
                tile.color = MyColors.empty()
        self.maze = False
        self.init_point = None
        self.end_point = None
        self.found = False

    def add_wall(self, pos):
        x = int(pos[0] / 10)
        y = int(pos[1] / 10)
        tile = self.tilesMatrix[x][y]

        keep = ['O', 'I', 'F']
        if tile.value not in keep:
            if tile.value != self.init_point and tile.value != self.end_point:
                tile.value = 'O'
                tile.color = MyColors.wall()

    def get_clicked_tile(self, pos):
        clicked_tile = None

        for line in self.tilesMatrix:
            for tile in line:
                if tile.rect.collidepoint(pos):
                    clicked_tile = tile

        if clicked_tile and clicked_tile.value == 0:
            if not self.init_point:
                self.init_point = clicked_tile.x, clicked_tile.y
                clicked_tile.value = 'I'
                clicked_tile.color = MyColors.point()
            else:
                if not self.end_point:
                    self.end_point = clicked_tile.x, clicked_tile.y
                    clicked_tile.value = 'F'
                    clicked_tile.color = MyColors.point()

    def printM(self):
        for x in range(self.width):
            print("")
            for y in range(self.height):
                print(self.tilesMatrix[x][y].value, end='')

        print("")

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                t = self.tilesMatrix[x][y]
                pg.draw.rect(screen, t.color, t)

    def fill_maze(self):
        if not self.maze:
            for x in range(self.width):
                for y in range(self.height):
                    t = self.tilesMatrix[x][y]

                    r = int(random.randrange(0, 3))
                    if (r == 0):
                        t.color = MyColors.wall()
                        t.value = 'O'
            self.maze = True

    def filled_init_end(self):
        if not self.init_point or not self.end_point:
            return False
        return True

    def find_path(self, show_step):
        if not self.filled_init_end():
            print('Click the init and end point')
            return False
        if self.found:
            print('Path already found')
            return False

        points = []
        next_tiles = []
        points.append(self.end_point)
        self.found = False

        while not self.found:
            if self.r > 2:
                self.r -= 2
                self.g -= 2
                self.b -= 2
            for point in points:
                x, y = point
                if (self.tilesMatrix[x][y]):
                    tile = self.tilesMatrix[x][y]
                    if tile.value == 'I':
                        self.found = True
                else:
                    continue
                next = tile.update_neighbors(self, show_step)
                if isinstance(next, Tile):
                    self.found = True
                else:
                    next_tiles.extend(next)

            points.clear()
            points = next_tiles.copy()
            next_tiles.clear()

            if len(points) == 0:
                print("There's no path available")
                return False

        return True

    def add_value_to_path(self, value, path):
        if path.value == 0:
            return value + 1
        else:
            return path.value

    def paint_next(self, tile):
        next = None
        for var in VARS:
            x = tile.x
            y = tile.y
            x = x + var[0]
            y = y + var[1]

            nei = self.tilesMatrix[x][y]

            if nei.value == 'F':
                return nei

            if (nei.value != 0 and nei.value != 'O' and nei.value != 'I'):
                if not next:
                    next = nei
                else:
                    if nei.value < next.value:
                        next = nei

        next.color = MyColors.path()
        return next

    def draw_path(self):
        x, y = self.init_point
        init = self.tilesMatrix[x][y]
        next = init

        while next.value != 'F':
            next = self.paint_next(next)
