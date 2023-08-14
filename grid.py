import pygame
from settings import *

class Grid:
    def __init__(self, screen):
        self.screen = screen
        self.create_grid()
        self.win = False
        self.winner = None
        
    def __str__(self):
        visual = ''
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col].state != '':
                    visual += self.grid[row][col].state
                else: visual += ' '
            visual += '\n'
            
        return visual
    
    def create_grid(self):
        self.grid = [[0 for row in range(GRID_SIZE)] for col in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.grid[row][col]=Box(row, col, self)
                
    def check_turn(self):
        """ check whose turn is it
        return True if O turn, False if X turn"""
        x_count = 0
        o_count = 0
        for row in self.grid:
            for box in row:
                if box.state == 'x':
                    x_count += 1
                elif box.state == 'o':
                    o_count += 1
        
        return bool(x_count >= o_count)
    
    def check_if_move_possible(self):
        count = 0
        for row in self.grid:
            for box in row:
                if box.state == '':
                    count += 1
        
        return bool(count)
    
    def check_win(self):
        wins = {'col1': set(),
                'col2': set(),
                'col3': set(),
                'row1': set(),
                'row2': set(),
                'row3': set(),
                'diagonal1': set(),
                'diagonal2': set(),}
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                wins['col'+str(row+1)].add(self.grid[row][col].state)
                wins['row'+str(col+1)].add(self.grid[row][col].state)
                if row == col:
                    wins['diagonal1'].add(self.grid[row][col].state)
                if row + col == 2:
                    wins['diagonal2'].add(self.grid[row][col].state)
                
        for win in wins.keys():
            if len(wins[win]) == 1 and '' not in wins[win]:
                for winner in wins[win]:
                    self.winner = winner 
                self.win = True
                self.select_win(win)
                break
        
    def reset_win(self):
        self.winner = ''
        self.win = False
        
    def select_win(self, win):
        if win == 'diagonal1':
            self.line_start = (0, 0)
            self.line_end = RES
        elif win == 'diagonal2':
            self.line_start = (WIDTH, 0)
            self.line_end = (0, HEIGHT)
        elif win[:3] == 'row':
            self.line_start = (0, (2 * int(win[3]) - 1)*TILE//2)
            self.line_end = (WIDTH, (2 * int(win[3]) - 1)*TILE//2)
        elif win[:3] == 'col':
            self.line_start = ((2 * int(win[3]) - 1)*TILE//2, 0)
            self.line_end = ((2 * int(win[3]) - 1)*TILE//2, HEIGHT)
        
    def update(self):
        for row in self.grid:
            for box in row:
                box.draw(self.screen)
                
        self.check_win()
        
        if self.win:
            pygame.draw.line(self.screen, 'red', self.line_start, self.line_end, 10)
            

class Box:
    def __init__(self, x, y, grid):
        self.x = x * TILE
        self.y = y * TILE
        self.grid = grid
        self.state = ""
        self.hovered = False
        
        self.rect = pygame.Rect((self.x + 1, self.y + 1), (TILE - 2, TILE - 2))
        
        
    def __str__(self):
        return f"{self.state} box at {self.x} {self.y}"
        
    def draw(self, screen):
        self.check_click()
        if self.hovered:
            pygame.draw.rect(screen, '#999999', self.rect, border_radius = 12)
        else:
            pygame.draw.rect(screen, '#dedcd7', self.rect, border_radius = 12)
            
        self.text_surf = FONT.render(self.state, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)
        screen.blit(self.text_surf, self.text_rect)
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if pygame.mouse.get_pressed()[0]:
                if self.grid.check_turn() and self.state == '':
                    self.state = 'o'
                elif self.state == '':
                    self.state = 'x'
        else:
            self.hovered = False
            
    
        
        

