import pygame
from pygame.locals import *
import random
from sudoku_solver import *

WIDTH = 540
HEIGHT =  630
BLANK_SPACE = 90
CELL_SIZE = WIDTH // 9

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (224, 224, 224)
GRAY2 = (130, 128, 124)
GREEN = (27, 184, 13)
RED = (227, 39, 18)
YELLOW = (201, 133, 6)

font = pygame.font.Font(None, 32)

grid = [[0] * 9 for i in range(9)]
permanent_numbers = [[False] * 9 for i in range(9)]
solved_grid = [[0] * 9 for i in range(9)]
incorrect_numbers = [[False] * 9 for i in range(9)]
show_incorrect = [False]
inputting_puzzle = [False]

# Define button properties

random_button_width = 108
random_button_height = 40
random_button_x = 0
random_button_y = 50
random_button_color = GRAY2
random_button_text = "Random Puzzle"
random_button_font = pygame.font.SysFont(None, 16)

solution_button_width = 108
solution_button_height = 40
solution_button_x = 108
solution_button_y = 50
solution_button_color = GRAY
solution_button_text = "Check Solution"
solution_button_font = pygame.font.SysFont(None, 16)

reveal_button_width = 108
reveal_button_height = 40
reveal_button_x = 216
reveal_button_y = 50
reveal_button_color = GRAY2
reveal_button_text = "Reveal Incorrect"
reveal_button_font = pygame.font.SysFont(None, 16)

input_button_width = 108
input_button_height = 40
input_button_x = 324
input_button_y = 50
input_button_color = GRAY
input_button_text = "Input Puzzle"
input_button_font = pygame.font.SysFont(None, 16)

check_valid_button_width = 108
check_valid_button_height = 40
check_valid_button_x = 432
check_valid_button_y = 50
check_valid_button_color = GRAY2
check_valid_button_text = "Set Puzzle"
check_valid_button_font = pygame.font.SysFont(None, 16)

def draw_button():
    pygame.draw.rect(WIN, solution_button_color, (solution_button_x, solution_button_y, solution_button_width, solution_button_height))
    text = solution_button_font.render(solution_button_text, True, BLACK)
    text_rect = text.get_rect(center=(solution_button_x + solution_button_width / 2, solution_button_y + solution_button_height / 2))
    WIN.blit(text, text_rect)

def draw_reveal_button():
    pygame.draw.rect(WIN, reveal_button_color, (reveal_button_x, reveal_button_y, reveal_button_width, reveal_button_height))
    text = reveal_button_font.render(reveal_button_text, True, BLACK)
    text_rect = text.get_rect(center=(reveal_button_x + reveal_button_width / 2, reveal_button_y + reveal_button_height / 2))
    WIN.blit(text, text_rect)
    
def draw_input_button():
    pygame.draw.rect(WIN, input_button_color, (input_button_x, input_button_y, input_button_width, input_button_height))
    text = input_button_font.render(input_button_text, True, BLACK)
    text_rect = text.get_rect(center=(input_button_x + input_button_width / 2, input_button_y + input_button_height / 2))
    WIN.blit(text, text_rect)

def draw_check_valid_button():
    pygame.draw.rect(WIN, check_valid_button_color, (check_valid_button_x, check_valid_button_y, check_valid_button_width, check_valid_button_height))
    text = check_valid_button_font.render(check_valid_button_text, True, BLACK)
    text_rect = text.get_rect(center=(check_valid_button_x + check_valid_button_width / 2, check_valid_button_y + check_valid_button_height / 2))
    WIN.blit(text, text_rect)

def is_button_clicked(pos):
    return solution_button_x <= pos[0] <= solution_button_x + solution_button_width and solution_button_y <= pos[1] <= solution_button_y + solution_button_height

def is_reveal_button_clicked(pos):
    return reveal_button_x <= pos[0] <= reveal_button_x + reveal_button_width and reveal_button_y <= pos[1] <= reveal_button_y + reveal_button_height

def is_input_puzzle_clicked(pos):
    return input_button_x <= pos[0] <= input_button_x + input_button_width and input_button_y <= pos[1] <= input_button_y + input_button_height

def is_valid_puzzle_click(pos):
    return check_valid_button_x <= pos[0] <= check_valid_button_x + check_valid_button_width and check_valid_button_y <= pos[1] <= check_valid_button_y + check_valid_button_height

def draw_grid():
    # Draw vertical grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        if x % (CELL_SIZE*3) == 0 and x != 0 and x != WIDTH:
            pygame.draw.line(WIN, BLACK, (x, BLANK_SPACE), (x, HEIGHT), 5)
        else:
            pygame.draw.line(WIN, BLACK, (x, BLANK_SPACE), (x, HEIGHT), 1)

    # Draw horizontal grid liness
    for y in range(BLANK_SPACE, HEIGHT, CELL_SIZE):
        if (y - BLANK_SPACE) % (CELL_SIZE*3) == 0 and y != BLANK_SPACE and y != HEIGHT:
            pygame.draw.line(WIN, BLACK, (0, y), (WIDTH, y), 5)
        else:
            pygame.draw.line(WIN, BLACK, (0, y), (WIDTH, y), 1)

def draw_numbers():
    for i in range(9):
        for j in range(9):
            number = grid[i][j]
            if number != 0:
                text = font.render(str(number), True, GRAY2)
                x = j * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2
                y = i * CELL_SIZE + BLANK_SPACE + CELL_SIZE // 2 - text.get_height() // 2
                if show_incorrect[0]:
                    if incorrect_numbers[i][j]:
                        text = font.render(str(number), True, RED)
                    else:
                        text = font.render(str(number), True, GREEN)
                if permanent_numbers[i][j]:
                    text = font.render(str(number), True, BLACK)
                WIN.blit(text, (x, y))

def check_if_correct():
    if check_solution():
        print("Congratulations! You solved the puzzle correctly.")
    else:
        print("Oops! The solution is incorrect.")

def check_solution():
    # Compare the current grid with the solved grid
    print(solved_grid)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != solved_grid[i][j]:
                return False
    return True

def find_incorrect_numbers():
    if (show_incorrect[0]):
        # Find the positions where the numbers are incorrect
        for i in range(9):
            for j in range(9):
                incorrect_numbers[i][j] = False
                if grid[i][j] != solved_grid[i][j] and grid[i][j] != 0:
                    incorrect_numbers[i][j] = True

def generate_random_puzzle():
    puzzles = "puzzles.txt"
    with open(puzzles, "r") as file:
        puzzle_data = file.read().split("\n\n")

    # Select a random puzzle
    random_puzzle = random.choice(puzzle_data)

    # Populate the grid with the selected puzzle
    lines = random_puzzle.strip().split("\n")
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            if char.isdigit():
                grid[i][j] = int(char)
                solved_grid[i][j] = int(char)
            else:
                grid[i][j] = 0
                solved_grid[i][j] = 0

    # Assign the preset puzzle values and update the permanent_numbers list accordingly
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                permanent_numbers[i][j] = True
            else:
                permanent_numbers[i][j] = False
    
    # Solve the puzzle
    solve_sudoku(solved_grid)

def set_puzzle():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                permanent_numbers[i][j] = True
            else:
                permanent_numbers[i][j] = False
    
    
def reset():
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0
            permanent_numbers[i][j] = False
            solved_grid[i][j] = 0
            incorrect_numbers[i][j] = False
    show_incorrect[0] = False

def main():
    generate_random_puzzle()
    run = True
    selected_cell = None # Track the currently selected cell
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouse_pos = pygame.mouse.get_pos()
                # Calculate the cell indices based on the mouse position
                cell_x = mouse_pos[0] // CELL_SIZE
                cell_y = (mouse_pos[1] - BLANK_SPACE) // CELL_SIZE
                # Update the selected cell with a number
                if cell_x < 9 and cell_y < 9 and mouse_pos[1] > BLANK_SPACE:
                    selected_cell = (cell_x, cell_y)
                elif mouse_pos[1] <= BLANK_SPACE:
                    selected_cell = None

                if not inputting_puzzle[0]:
                    if is_button_clicked(mouse_pos):
                        check_if_correct()
                    elif is_reveal_button_clicked(mouse_pos):
                        show_incorrect[0] = not show_incorrect[0]
                        find_incorrect_numbers()
                    elif is_input_puzzle_clicked(mouse_pos):
                        reset()
                        inputting_puzzle[0] = True
                elif is_valid_puzzle_click(mouse_pos) and inputting_puzzle[0]:
                    for i in range(9):
                        for j in range(9):
                            solved_grid[i][j] = grid[i][j]
                    if (solve_sudoku(solved_grid)):
                        set_puzzle()
                        inputting_puzzle[0] = False
                    else:
                        print("Not a valid puzzle!")
            
            elif event.type == pygame.KEYDOWN:
                # Check if a cell is selected and a valid number key is pressed
                if selected_cell and not permanent_numbers[selected_cell[1]][selected_cell[0]] :
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        number = event.key - pygame.K_0  # Convert key code to number value
                        grid[selected_cell[1]][selected_cell[0]] = number
                    elif event.key == pygame.K_BACKSPACE:
                        grid[selected_cell[1]][selected_cell[0]] = 0  
        
        # Fill the screen with white
        WIN.fill(WHITE)
        
        # Highlight selected cell
        if selected_cell:
            highlight_rect = pygame.Rect(selected_cell[0] * CELL_SIZE + 1, selected_cell[1] * CELL_SIZE + BLANK_SPACE + 1, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(WIN, GRAY, highlight_rect)
        
        # Draw components
        draw_grid()
        draw_numbers()
        draw_button()
        draw_reveal_button()
        draw_input_button()
        draw_check_valid_button()

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()