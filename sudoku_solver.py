
def find_next_empty(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return row, col
    return None, None


def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    
    for row in range(row_start, row_start + 3):
        for col in range(col_start, col_start + 3):
            if puzzle[row][col] == guess:
                return False
     
    return True


def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)
    
    if row is None:
        return True
    
    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True
        puzzle[row][col] = 0
    return False


if __name__ == '__main__':
    puzzle =   [[3, 0, 6, 5, 0, 8, 4, 0, 0], 
                [5, 2, 0, 0, 0, 0, 0, 0, 0], 
                [0, 8, 7, 0, 0, 0, 0, 3, 1], 
                [0, 0, 3, 0, 1, 0, 0, 8, 0], 
                [9, 0, 0, 8, 6, 3, 0, 0, 5], 
                [0, 5, 0, 0, 9, 0, 6, 0, 0], 
                [1, 3, 0, 0, 0, 0, 2, 5, 0], 
                [0, 0, 0, 0, 0, 0, 0, 7, 4], 
                [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    invalid = [[1, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    print(solve_sudoku(invalid))
    print(invalid)
