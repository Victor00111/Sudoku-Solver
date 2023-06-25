import pygame
from pygame.locals import *
import random
from sudoku_solver import *

WIDTH = 540
HEIGHT =  660
BLANK_SPACE = 120
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
BLUE = (86, 232, 240)
BLUE2 = (54, 187, 194)

font = pygame.font.Font(None, 32)

grid = [[0] * 9 for i in range(9)]
permanent_numbers = [[False] * 9 for i in range(9)]
solved_grid = [[0] * 9 for i in range(9)]
incorrect_numbers = [[False] * 9 for i in range(9)]
show_incorrect = False
inputting_puzzle = False

# Define button properties
random_button_width = 180
random_button_height = 40
random_button_x = 0
random_button_y = 0
random_button_color = BLUE
random_button_text = "Random Puzzle"
random_button_font = pygame.font.SysFont(None, 20)

input_button_width = 180
input_button_height = 40
input_button_x = 180
input_button_y = 0
input_button_color = BLUE
input_button_text = "Input Puzzle"
input_button_font = pygame.font.SysFont(None, 20)

set_button_width = 180
set_button_height = 40
set_button_x = 360
set_button_y = 0
set_button_color = BLUE
set_button_text = "Set Puzzle (if inputting)"
set_button_font = pygame.font.SysFont(None, 20)

solution_button_width = 180
solution_button_height = 40
solution_button_x = 0
solution_button_y = 40
solution_button_color = BLUE
solution_button_text = "Check Solution"
solution_button_font = pygame.font.SysFont(None, 20)

reveal_button_width = 180
reveal_button_height = 40
reveal_button_x = 180
reveal_button_y = 40
reveal_button_color = BLUE
reveal_button_text = "Reveal Incorrect numbers"
reveal_button_font = pygame.font.SysFont(None, 20)

solve_button_width = 180
solve_button_height = 40
solve_button_x = 360
solve_button_y = 40
solve_button_color = BLUE
solve_button_text = "Solve Puzzle"
solve_button_font = pygame.font.SysFont(None, 20)

# Define message properties
message_text = ""
message_color = BLACK
message_font = pygame.font.SysFont(None, 25)

def draw_solution_button(pos):
    color = BLUE2 if is_solution_button_clicked(pos) or inputting_puzzle else BLUE
    pygame.draw.rect(WIN, color, (solution_button_x, solution_button_y, solution_button_width, solution_button_height))
    pygame.draw.rect(WIN, BLACK, (solution_button_x, solution_button_y, solution_button_width, solution_button_height), 1)
    text = solution_button_font.render(solution_button_text, True, BLACK)
    text_rect = text.get_rect(center=(solution_button_x + solution_button_width / 2, solution_button_y + solution_button_height / 2))
    WIN.blit(text, text_rect)

def draw_reveal_button(pos):
    color = BLUE2 if is_reveal_button_clicked(pos) or inputting_puzzle else BLUE
    pygame.draw.rect(WIN, color, (reveal_button_x, reveal_button_y, reveal_button_width, reveal_button_height))
    pygame.draw.rect(WIN, BLACK, (reveal_button_x, reveal_button_y, reveal_button_width, reveal_button_height), 1)
    text = reveal_button_font.render(reveal_button_text, True, BLACK)
    text_rect = text.get_rect(center=(reveal_button_x + reveal_button_width / 2, reveal_button_y + reveal_button_height / 2))
    WIN.blit(text, text_rect)
    
def draw_input_button(pos):
    color = BLUE2 if is_input_button_clicked(pos) or inputting_puzzle else BLUE
    pygame.draw.rect(WIN, color, (input_button_x, input_button_y, input_button_width, input_button_height))
    pygame.draw.rect(WIN, BLACK, (input_button_x, input_button_y, input_button_width, input_button_height), 1)
    text = input_button_font.render(input_button_text, True, BLACK)
    text_rect = text.get_rect(center=(input_button_x + input_button_width / 2, input_button_y + input_button_height / 2))
    WIN.blit(text, text_rect)

def draw_set_button(pos):
    color = BLUE2 if is_set_button_clicked(pos) or not inputting_puzzle else BLUE
    pygame.draw.rect(WIN, color, (set_button_x, set_button_y, set_button_width, set_button_height))
    pygame.draw.rect(WIN, BLACK, (set_button_x, set_button_y, set_button_width, set_button_height), 1)
    text = set_button_font.render(set_button_text, True, BLACK)
    text_rect = text.get_rect(center=(set_button_x + set_button_width / 2, set_button_y + set_button_height / 2))
    WIN.blit(text, text_rect)

def draw_random_button(pos):
    color = BLUE2 if is_random_button_clicked(pos) or inputting_puzzle else BLUE
    pygame.draw.rect(WIN, color, (random_button_x, random_button_y, random_button_width, random_button_height))
    pygame.draw.rect(WIN, BLACK, (random_button_x, random_button_y, random_button_width, random_button_height), 1)
    text = random_button_font.render(random_button_text, True, BLACK)
    text_rect = text.get_rect(center=(random_button_x + random_button_width / 2, random_button_y + random_button_height / 2))
    WIN.blit(text, text_rect)

def draw_solve_button(pos):
    color = BLUE2 if is_solve_button_clicked(pos) or inputting_puzzle else BLUE
    pygame.draw.rect(WIN, color, (solve_button_x, solve_button_y, solve_button_width, solve_button_height))
    pygame.draw.rect(WIN, BLACK, (solve_button_x, solve_button_y, solve_button_width, solve_button_height), 1)
    text = solve_button_font.render(solve_button_text, True, BLACK)
    text_rect = text.get_rect(center=(solve_button_x + solve_button_width / 2, solve_button_y + solve_button_height / 2))
    WIN.blit(text, text_rect)

def is_solution_button_clicked(pos):
    return solution_button_x <= pos[0] <= solution_button_x + solution_button_width and solution_button_y <= pos[1] <= solution_button_y + solution_button_height

def is_reveal_button_clicked(pos):
    return reveal_button_x <= pos[0] <= reveal_button_x + reveal_button_width and reveal_button_y <= pos[1] <= reveal_button_y + reveal_button_height

def is_input_button_clicked(pos):
    return input_button_x <= pos[0] <= input_button_x + input_button_width and input_button_y <= pos[1] <= input_button_y + input_button_height

def is_set_button_clicked(pos):
    return set_button_x <= pos[0] <= set_button_x + set_button_width and set_button_y <= pos[1] <= set_button_y + set_button_height

def is_random_button_clicked(pos):
    return random_button_x <= pos[0] <= random_button_x + random_button_width and random_button_y <= pos[1] <= random_button_y + random_button_height

def is_solve_button_clicked(pos):
    return solve_button_x <= pos[0] <= solve_button_x + solve_button_width and solve_button_y <= pos[1] <= solve_button_y + solve_button_height

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
                if show_incorrect:
                    if incorrect_numbers[i][j]:
                        text = font.render(str(number), True, RED)
                    else:
                        text = font.render(str(number), True, GREEN)
                if permanent_numbers[i][j]:
                    text = font.render(str(number), True, BLACK)
                WIN.blit(text, (x, y))

def check_solution():
    # Compare the current grid with the solved grid
    for i in range(9):
        for j in range(9):
            if grid[i][j] != solved_grid[i][j]:
                return False
    return True

def find_incorrect_numbers():
    if (show_incorrect):
        # Find the positions where the numbers are incorrect
        for i in range(9):
            for j in range(9):
                incorrect_numbers[i][j] = False
                if grid[i][j] != solved_grid[i][j] and grid[i][j] != 0:
                    incorrect_numbers[i][j] = True

def find_random_puzzle():
    puzzles = "puzzles.txt"
    with open(puzzles, "r") as file:
        puzzle_data = file.read().split("\n\n")

    # Select a random puzzle
    random_int = random.randint(0, len(puzzle_data) - 1)

    # Display the Puzzle number
    global message_text
    message_text = "Puzzle # " + str(random_int)

    # Populate the grid with the selected puzzle
    lines = puzzle_data[random_int].strip().split("\n")
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            if char.isdigit():
                grid[i][j] = int(char)
                solved_grid[i][j] = int(char)
            else:
                grid[i][j] = 0
                solved_grid[i][j] = 0

    # Set numbers from puzzle onto the grid and create solved grid
    set_puzzle()   

def set_puzzle():
    # Set permanent values
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                permanent_numbers[i][j] = True
            else:
                permanent_numbers[i][j] = False
    
    # Solve the puzzle
    solve_sudoku(solved_grid)

def solve_puzzle():
    for i in range(9):
        for j in range(9):
            grid[i][j] = solved_grid[i][j]

def reset():
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0
            permanent_numbers[i][j] = False
            solved_grid[i][j] = 0
            incorrect_numbers[i][j] = False
    global show_incorrect
    show_incorrect = False

def display_message():
    text = message_font.render(message_text, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, BLANK_SPACE - 15))
    WIN.blit(text, text_rect)

def check_if_valid(row, col):
    value = grid[row][col]
    for i in range(9):
        if i != row and value == grid[i][col]:
            return False
    for j in range(9):
        if j != col and value == grid[row][j]:
            return False
    
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if i != row and j != col and grid[i][j] == value:
                return False
    return True

def main():
    find_random_puzzle()
    run = True
    selected_cell = None # Track currently selected cell
    mouse_pos = [0, 0] # Track mouse position
    global inputting_puzzle
    global show_incorrect
    global message_text
    while run:
        for event in pygame.event.get():
            # Get the position of the mouse
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Calculate the cell indices based on the mouse position
                cell_x = mouse_pos[0] // CELL_SIZE
                cell_y = (mouse_pos[1] - BLANK_SPACE) // CELL_SIZE
                # Update the selected cell with a number
                if cell_x < 9 and cell_y < 9 and mouse_pos[1] > BLANK_SPACE:
                    selected_cell = (cell_x, cell_y)
                elif mouse_pos[1] <= BLANK_SPACE:
                    selected_cell = None
                
                if not inputting_puzzle:
                    if is_solution_button_clicked(mouse_pos):
                        if check_solution():
                            message_text = "Congratulations! You solved the puzzle correctly."
                        else:
                            message_text = "Oops! The solution is incorrect."
                    elif is_reveal_button_clicked(mouse_pos):
                        show_incorrect = not show_incorrect
                    elif is_input_button_clicked(mouse_pos):
                        reset()
                        inputting_puzzle = True
                        message_text = "Make sure to set the puzzle!"
                    elif is_random_button_clicked(mouse_pos):
                        reset()
                        find_random_puzzle()
                    elif is_solve_button_clicked(mouse_pos):
                        solve_puzzle()
                        message_text = "Puzzle has been Solved!"
                elif is_set_button_clicked(mouse_pos) and inputting_puzzle:
                    valid = True
                    for i in range(9):
                        for j in range(9):
                            if grid[i][j] != 0 and not check_if_valid(i, j):
                                valid = False
                                break
                        if valid == False:
                            break
                    if (valid):
                        for i in range(9):
                            for j in range(9):
                                solved_grid[i][j] = grid[i][j]
                        set_puzzle()
                        inputting_puzzle = False
                    else:
                        message_text = "Not a valid puzzle!"
            
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
        find_incorrect_numbers()
        draw_random_button(mouse_pos)
        draw_solution_button(mouse_pos)
        draw_input_button(mouse_pos)
        draw_set_button(mouse_pos)
        draw_reveal_button(mouse_pos)
        draw_solve_button(mouse_pos)
        display_message()

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
