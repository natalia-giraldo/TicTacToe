# coding: utf-8
import sys
import pygame # Graphics module
import numpy as np # Numerical Python Library
import time


pygame.init() # Initialize pygame

# ==== TIC TAC TOE vs. AI=====

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# PROPORTIONS & Sizes
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 3
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_ROWS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15

# Create the board game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe vs. AI")
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int) # Build the board

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)
        
# Define the figures for players: Player-circle = 1, AI-cross = 2
# Reading from Top-left to Bottom-right
def signe(color=GREEN):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Player: circle
                center = (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2))
                pygame.draw.circle(screen, color, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

            elif board[row][col] == 2: # AI: cross 
                start1 = (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4)
                end1 = (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4)
                
                start2 = (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4)
                end2 = (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4)
                pygame.draw.line(screen, color, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, color, start2, end2, CROSS_WIDTH)

# Define square figure
def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col): # is it a square available?
    return board[row][col] == 0
        
# is it a space left on the board? -> important for AI Algo
def is_board_full(check_board=None):
    if check_board is None:
        check_board = board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True  # If there is no zero

# Check if someone has won
def check_win(player, check_board=None):
    if check_board is None:
        check_board = board

    # Columns
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True

    # Rows
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    # Diagonals
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True

    return False

# How the AI makes decisions. Applies the minimax Algorithm   
def ia(is_mini, depth, is_maxi):
    # Check terminal states (when the game is over)
    if check_win(2, is_mini):
        return 10 - depth
    if check_win(1, is_mini):
        return depth - 10
    if is_board_full(is_mini):
        return 0
    
    if is_maxi:
        best_score = -float("inf") # MAX state
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if is_mini[row][col] == 0:
                    is_mini[row][col] = 2 
                    score = ia(is_mini, depth + 1, False)
                    is_mini[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf") # MIN state
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if is_mini[row][col] == 0:
                    is_mini[row][col] = 1
                    score = ia(is_mini, depth + 1, True)
                    is_mini[row][col] = 0
                    best_score = min(score, best_score) # if set to "max" Allows to win player 1
        return best_score


# AI defines the next move
def best_move():
    best_score = -float("inf")
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = ia(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
                print(row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], player=2)
        return True
    return False

# Restart the game
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# Gameloop -> Starts the game
draw_lines()

player = 1
game_over = False
start = time.time()
time_limit = 2  # seconds    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE # X Axe
            mouseY = event.pos[1] // SQUARE_SIZE # Y Axe           

            # Note: mouseY is row, mouseX is col
            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

        # AI move
        if not game_over and player == 2:
            if best_move():
                if check_win(2):
                    game_over = True
                player = player % 2 + 1
       # Test start 
        if not game_over and player == 2:
            if best_move():
                if check_win(1):
                    game_over = False
                player = player % 2 + 1             
       # Test end
        if not game_over:
            if is_board_full():
                game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
                


    # Rendering
    screen.fill(BLACK)
    draw_lines()
    if not game_over:
        signe()
    else:
        if check_win(1):
            signe(GREEN) # Player 1: Circle = 1
            draw_lines(GREEN)
        elif check_win(2):
            signe(RED) # Player 2: Cross = -1
            draw_lines(RED)
        else:
            signe(GRAY) # It's a tail! = 0
            draw_lines(GRAY)

    pygame.display.update()

# Improvements:
# Added an option to restart the game by pressing the spacebar
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE and game_over:
            restart_game()
            game_over = False
            player = 1
            draw_lines()   
   