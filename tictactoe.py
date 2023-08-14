import pygame
import sys
from settings import *
from grid import Grid
from minimax import Minimax
from menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.ai = True
        self.pause = True
        self.restart()
        self.menu = Menu(self)

    def restart(self):
        self.grid = Grid(self.screen)
        self.minimax = Minimax(self.grid)
        
    def draw(self):
        self.screen.fill("gray")
        self.grid.update()
        
    def ai_move(self):
        if not self.grid.check_turn():
            x, y = self.minimax.find_best_move('x')
            print(str(x), ', ', str(y))
            if x != -1 and y != -1:
                self.grid.grid[x][y].state = 'x'
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.restart()
                    
            if self.grid.win or not self.grid.check_if_move_possible():
                self.pause = True
            
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption('Tic Tac Toe')
        
    def run(self):
        while True:
            self.check_events()
            if self.pause:
                self.menu.update()
            else:
                if self.ai and not self.grid.win and self.grid.check_if_move_possible():
                    self.ai_move()
                self.draw()
                
                
            self.update()
        

if __name__ == '__main__':
    
    game = Game()
    game.run()