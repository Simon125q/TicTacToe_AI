import pygame
from settings import *

class Minimax:
    def __init__(self, board):
        self.board = board
        
    def minimax(self, depth, isMax, ai):
        score = self.evaluation(ai)
        
        if score != 0:
            return score
        
        if not self.board.check_if_move_possible():
            return 0
        
        if isMax:
            best = -1000
            
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.board.grid[row][col].state == '':
                        self.board.grid[row][col].state = ai
                        
                        best = max(best, self.minimax(depth + 1, not isMax, ai))
                        
                        self.board.grid[row][col].state = ''
                      
            return best
        
        else:
            best = 1000
            
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.board.grid[row][col].state == '':
                        if ai == 'x':
                            player = 'o'
                        else:
                            player = 'x'
                        self.board.grid[row][col].state = player
                        
                        best = min(best, self.minimax(depth + 1, not isMax, ai))
                        
                        self.board.grid[row][col].state = ''
            
            return best
        
    def find_best_move(self, ai):
        best_val = -1000
        best_move = (-1, -1)
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                 if self.board.grid[row][col].state == '':
                     self.board.grid[row][col].state = ai
                     
                     move_val = self.minimax(0, False, ai)
                     
                     self.board.grid[row][col].state = ''
                     
                     if move_val > best_val:
                         
                         best_move = (row, col)
                         best_val = move_val
                         
        return best_move
    
    def evaluation(self, ai):
        self.board.check_win()
        if self.board.win:
            if self.board.winner == 'x':
                self.board.reset_win()
                return 10
            elif self.board.winner == 'o': 
                self.board.reset_win()
                return -10
            
        else: return 0