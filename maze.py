import pygame
from pygame.locals import *
import constants
import random

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = constants.APP_WIDTH, constants.APP_HEIGHT
        self.grid = []
        self.current = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(constants.COLOR_DEFAULT_BG)
        self._running = True
        self.cols = int(self._display_surf.get_width() / constants.CELL_SIZE)
        self.rows = int(self._display_surf.get_height() / constants.CELL_SIZE)


        for j in range(self.rows):
            for i in range(self.cols):
                cell = Cell(i, j)
                self.grid.append(cell)

        self.current = self.grid[0]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.current.visited = True
        next_neighbour =  self.current.checkNeighbors(self.grid, self.cols, self.rows)
        if next_neighbour:
           self.current = next_neighbour


    def on_render(self):
        pygame.time.Clock().tick(5)
        pygame.display.flip()
 
    def on_cleaup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            for cell in self.grid:
                cell.show(self._display_surf)

            self.on_loop()
            self.on_render()
        self.on_cleaup()

class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        # TOP, RIGHT, BOTTOM, LEFT
        self.walls = [True, True, True, True]
        self.visited = False

    def index(self, i, j, cols, rows):
        if (i < 0) or (j < 0) or (i > cols -1) or (j > rows -1):
            print("Undefined")
            return 0
        return i + j * cols

    def checkNeighbors(self, grid, cols, rows):
        neighbours = []
        top  =  grid[self.index(self.i, self.j - 1, cols, rows)]
        right  =  grid[self.index(self.i + 1, self.j, cols, rows)]
        bottom  =  grid[self.index(self.i, self.j + 1, cols, rows)]
        left  =  grid[self.index(self.i - 1, self.j, cols, rows)]
        if not top.visited and top:
            neighbours.append(top)
        if not right.visited and right:
            neighbours.append(right)
        if not bottom.visited and bottom:
            neighbours.append(bottom)
        if not left.visited and left:
            neighbours.append(left)

        if len(neighbours) > 0:
            r = int(random.randrange(0, len(neighbours)))
            return neighbours[r]
        else:
            return None



    def show(self, surface):
        x = self.i*constants.CELL_SIZE
        y = self.j*constants.CELL_SIZE
        w = surface.get_width()
        h = surface.get_height()
        if self.visited:
            pygame.draw.rect(surface, constants.COLOR_PURPLE, (x, y, constants.CELL_SIZE, constants.CELL_SIZE), 0)
        if self.walls[0]:
            pygame.draw.line(surface, constants.COLOR_WHITE, (x,         y), (x + w,     y), 1 )
        if self.walls[1]:
            pygame.draw.line(surface, constants.COLOR_WHITE, (x + w,     y), (x + w, y + w), 1 )
        if self.walls[2]:
            pygame.draw.line(surface, constants.COLOR_WHITE, (x + w, y + w), (x,     y + w), 1 )
        if self.walls[3]:
            pygame.draw.line(surface, constants.COLOR_WHITE, (x,     y + w), (x,         y), 1 )

if __name__=="__main__":
    theApp = App()
    theApp.on_execute()
