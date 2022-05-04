import pygame as pg
import random

OFFSET = 5
# variations
VARS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MyColors():
    @staticmethod
    def wall():
        return (0, 0, 102)

    @staticmethod
    def empty():
        return (96, 96, 96)
    
    @staticmethod
    def point():
        return (255, 0, 0)

    @staticmethod
    def path():
        return (0, 255, 0)


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 9
        self.color = MyColors.empty()
        self.value = 0
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)

    def set_tile_pos(self, x, y):
        self.rect.x = (x * 10) + OFFSET
        self.rect.y = (y * 10) + OFFSET

    def in_bounds(self, tm, x, y):
        if ((x + 1) >= len(tm.tilesMatrix)):
            return False
        if ((y + 1) >= len(tm.tilesMatrix[0])):
            return False
        return True

    def update_neighbors(self, tm):
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
                        next_tiles.append(((x), (y)))
                    if tm.tilesMatrix[x][y].value == 'I':
                        return tm.tilesMatrix[x][y]
        return next_tiles


class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = False
        self.init_point = None
        self.end_point = None
        self.tilesMatrix = [
            [0 for _ in range(self.height)] for _ in range(self.width)]

    def init(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(x, y)
                tile.set_tile_pos(x, y)
                self.tilesMatrix[x][y] = tile

    def clear_map(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tilesMatrix[x][y]
                tile.value = 0
                tile.color = MyColors.empty()
        self.maze = False
        self.init_point = None
        self.end_point = None


    def get_clicked_tile(self, pos):
        x = int(pos[0] / 10)
        y = int(pos[1] / 10)
        tile = self.tilesMatrix[x][y]

        if tile.value == 0:
            if not self.init_point:
                self.init_point = (x, y)
                tile.value = 'I'
                tile.color = MyColors.point()
            else:
                if not self.end_point:
                    self.end_point = (x, y)
                    tile.value = 'F'
                    tile.color = MyColors.point()

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

    def find_path(self):
        if not self.filled_init_end():
            print('Click the init and end point')
            return False

        points = []
        next_tiles = []
        points.append(self.end_point)
        found = False

        while not found:
            for point in points:
                x, y = point
                if (self.tilesMatrix[x][y]):
                    tile = self.tilesMatrix[x][y]
                    if tile.value == 'I':
                        found = True
                else:
                    continue
                next = tile.update_neighbors(self)
                if isinstance(next, Tile):
                    found = True
                else:
                    next_tiles.extend(next)

            points.clear()
            points = next_tiles.copy()
            next_tiles.clear()
            #found = True

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
