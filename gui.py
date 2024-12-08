import pygame
import sys
from ai import moveAI  
from utils import gameOver,gameOver, setDifficulty   
pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
BG_COLOR = (210, 180, 140)
TEXT_COLOR = (0, 0, 0)
FONT = pygame.font.Font(None, 33)

BOARD_BG_COLOR = (210, 180, 140)
LINE_COLOR = (0, 0, 0)

def draw_text(screen, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def grid_size_gui():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Select GOMOKU Size")

    input_box = pygame.Rect(100, 80, 200, 40)
    user_input = ""
    grid_size = None

    while True:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.isdigit() and int(user_input) >= 5:
                        grid_size = int(user_input)
                        print("Enjoy the game!")
                        return grid_size
                    else:
                        print("Invalid size, grid size >= 5")
                        user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        draw_text(screen, "Enter Grid Size:", FONT, TEXT_COLOR, (WINDOW_WIDTH // 2, 40))
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        draw_text(screen, user_input, FONT, TEXT_COLOR, input_box.center)

        pygame.display.flip()

def draw_board(screen, grid_size, cell_size):
    for i in range(grid_size + 1):
        pygame.draw.line(screen, LINE_COLOR, (0, i * cell_size), (grid_size * cell_size, i * cell_size))
        pygame.draw.line(screen, LINE_COLOR, (i * cell_size, 0), (i * cell_size, grid_size * cell_size))

def draw_stones(screen, board, cell_size):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 1:  # Black stone
                pygame.draw.circle(
                    screen, (0, 0, 0),
                    (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2),
                    cell_size // 3
                )
            elif board[row][col] == 2:  # White stone
                pygame.draw.circle(
                    screen, (255, 255, 255),
                    (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2),
                    cell_size // 3
                )

def get_cell_from_mouse(pos, cell_size):
    x, y = pos
    return y // cell_size, x // cell_size

def draw_button(screen, text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))  
    draw_text(screen, text, FONT, text_color, (x + width // 2, y + height // 2))


def handle_button_click(pos, button_x, button_y, button_width, button_height):
    x, y = pos
    return button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height

def display_winner_in_external_window(winner):
    winner_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Winner Winner Chicken Dinner!")

    winner_bg_color = (210, 180, 140)
    winner_text_color = (0, 0, 0)

    winner_window.fill(winner_bg_color)

    if winner == 1:
        draw_text(winner_window, "You win!", FONT, winner_text_color, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
    elif winner == 2:
        draw_text(winner_window, "Game Over, AI wins!", FONT, winner_text_color, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

    button_width = 120
    button_height = 40
    replay_button_x = WINDOW_WIDTH // 4 - button_width // 2
    quit_button_x = WINDOW_WIDTH * 3 // 4 - button_width // 2
    button_y = WINDOW_HEIGHT // 2

    draw_button(winner_window, "Replay", replay_button_x, button_y, button_width, button_height, (242, 210, 189), winner_text_color)
    draw_button(winner_window, "Quit", quit_button_x, button_y, button_width, button_height, (242, 210, 189), winner_text_color)

    pygame.display.flip()

    waiting_for_close = True
    while waiting_for_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_button_click(event.pos, replay_button_x, button_y, button_width, button_height):
                    print("Replay the game")
                    return main()  
                elif handle_button_click(event.pos, quit_button_x, button_y, button_width, button_height):
                    print("Quit the game")
                    pygame.quit()
                    sys.exit()


def difficulty_gui():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Select Difficulty")

    button_width = 120
    button_height = 40
    button_y = WINDOW_HEIGHT // 2
    easy_button_x = WINDOW_WIDTH // 4 - button_width // 2
    medium_button_x = WINDOW_WIDTH // 2 - button_width // 2
    hard_button_x = WINDOW_WIDTH * 3 // 4 - button_width // 2

    while True:
        screen.fill(BG_COLOR)

        draw_text(screen, "Select Difficulty:", FONT, TEXT_COLOR, (WINDOW_WIDTH // 2, 40))
        draw_button(screen, "Easy", easy_button_x, button_y, button_width, button_height, (242, 210, 189), TEXT_COLOR)
        draw_button(screen, "Medium", medium_button_x, button_y, button_width, button_height, (242, 210, 189), TEXT_COLOR)
        draw_button(screen, "Hard", hard_button_x, button_y, button_width, button_height, (242, 210, 189), TEXT_COLOR)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_button_click(event.pos, easy_button_x, button_y, button_width, button_height):
                    return "easy"
                elif handle_button_click(event.pos, medium_button_x, button_y, button_width, button_height):
                    return "medium"
                elif handle_button_click(event.pos, hard_button_x, button_y, button_width, button_height):
                    return "hard"

def main():
    grid_size = grid_size_gui()
    difficulty = difficulty_gui()
    depth = setDifficulty(difficulty) 
    cell_size = 40
    board_size = grid_size * cell_size
    screen = pygame.display.set_mode((board_size, board_size + 80))
    pygame.display.set_caption("Gomoku")

    board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    current_player = 1
    game_over = False
    winner = None

    button_width = 120
    button_height = 40
    replay_button_x = board_size // 4 - button_width // 2
    quit_button_x = board_size * 3 // 4 - button_width // 2
    button_y = board_size + 20

    need_redraw = True

    while True:
        if need_redraw:
            screen.fill(BOARD_BG_COLOR)
            draw_board(screen, grid_size, cell_size)
            draw_stones(screen, board, cell_size)
            if game_over:
                display_winner_in_external_window(winner)
            draw_button(screen, "Replay", replay_button_x, button_y, button_width, button_height, (229, 170, 112), TEXT_COLOR)
            draw_button(screen, "Quit", quit_button_x, button_y, button_width, button_height, (229, 170, 112), TEXT_COLOR)
            pygame.display.flip()
            need_redraw = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_cell_from_mouse(event.pos, cell_size)
                if 0 <= row < grid_size and 0 <= col < grid_size and board[row][col] == 0:
                    board[row][col] = 1
                    winner = gameOver(board, grid_size)
                    if winner == 1:
                        game_over = True
                    else:

                        ai_move = moveAI(board, grid_size, depth=depth)
                        if ai_move:
                            ai_row, ai_col = ai_move
                            board[ai_row][ai_col] = 2
                            winner = gameOver(board, grid_size)
                            if winner == 2:
                                game_over = True
                        current_player = 1

                    need_redraw = True

            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if handle_button_click(event.pos, replay_button_x, button_y, button_width, button_height):
                    print("Replay the game")
                    return main()
                elif handle_button_click(event.pos, quit_button_x, button_y, button_width, button_height):
                    print("Quit the game")
                    pygame.quit()
                    sys.exit()


