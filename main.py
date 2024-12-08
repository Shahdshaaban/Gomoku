import pygame
import sys

# def place_stone(board, pos, current_player):
#     """Place a stone at the clicked position."""
#     row, col = pos
#     if board[row][col] == 0:  # 0 means empty
#         board[row][col] = current_player
#         return True
#     return False

from gui import main
from ai import moveAI
from eval import evalWindow
if __name__ == "__main__":
    main()
    moveAI()
    evalWindow()
    
   
    
