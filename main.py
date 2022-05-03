import math
from tkinter import OFF
import pygame as pg
import datetime

from pygame.locals import *
from matrix import TileMap
from finder import Finder

OFFSET = 5


class Application():
    def __init__(self) -> None:
        self.width = 810
        self.height = 610
        self.screen = pg.display.set_mode([self.width, self.height])
        self.center = (self.width / 2, self.height / 2)
        self.map = None
        self.finder = Finder()
        pg.display.set_caption('A* Path Finder')

        print('Application has been Created')

    def render(self):
        self.map.render(self.screen)
        pg.display.flip()

    def init(self):
        self.map = TileMap(80, 60)
        self.map.init()
        print('Tile map created')

    def loop(self):
        run = True
        pg.font.init()
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))

        self.init()

        while run:
            self.render()

            for event in pg.event.get():
                if (event.type == MOUSEBUTTONDOWN):
                    print(pg.mouse.get_pos())
                    self.map.get_clicked_tile(pg.mouse.get_pos())

                if (event.type == pg.QUIT):
                    run = False                   

                if (event.type == KEYDOWN):
                    if(event.key == 32):
                        self.map.fill_maze()                        

                    if(event.key == 27):
                        print("Quiting")
                        run = False

                    if pg.key.get_pressed()[pg.K_1] or pg.key.get_pressed()[pg.K_KP1]:
                        if self.map.find_path():
                            self.map.draw_path(self.screen)
                    if pg.key.get_pressed()[pg.K_c]:
                        self.map.clear_map()




if __name__ == '__main__':
    app = Application()

    app.loop()
