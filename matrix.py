import pygame as pg
import random

OFFSET = 5
TILE_SIZE = 9
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
                            tm.tilesMatrix[x][y].color = (10,100,10)
                            tm.render(tm.screen)
                            
                        pg.display.flip()
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
        self.path = []
        self.found = False
        self.screen = None
        self.tilesMatrix = [
            [0 for _ in range(self.height)] for _ in range(self.width)]

    def init(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(x, y)
                tile.set_tile_pos(x, y)
                self.tilesMatrix[x][y] = tile

    def clear_path(self):
        keep = ['O', 'I', 'F']
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tilesMatrix[x][y]
                
                if tile.value not in keep:
                    tile.value = 0
                    tile.color = MyColors.empty()
        self.found = False

        

    def clear_map(self):
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
