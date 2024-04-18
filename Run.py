from itertools import product
import copy

def readInput(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    matrix = []

    for l in lines:
        row = l.strip().split(", ")
        matrix.append(row)
    
    return matrix

# Brute-Force
def countTrapsAround(board, x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == 'T':
                count += 1
    return count

def isValid(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y].isdigit():
                expected_count = int(board[x][y])
                if countTrapsAround(board, x, y) != expected_count:
                    return False
    return True

def processBruteFore(grid):
    rows = len(grid)
    cols = len(grid[0])
    indices = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == '_']

    # Mặc định tất cả là đá quý không có số liền kề
    for i, j in indices:
        if all(not grid[x][y].isdigit() for x in range(max(0, i-1), min(rows, i+2)) for y in range(max(0, j-1), min(cols, j+2))):
            grid[i][j] = 'F'
    
    # Chỉ xem xét kết hợp cho các ô chưa được chỉ định còn lại
    remaining_indices = [(i, j) for i, j in indices if grid[i][j] == '_']
    
    for combo in product(['T', 'G'], repeat=len(remaining_indices)):
        # Đặt ô dựa trên trạng thái hiện tại
        for (index, value) in zip(remaining_indices, combo):
            grid[index[0]][index[1]] = value
        
        if isValid(grid):
            return  # Tìm thấy giải pháp hợp lệ đầu tiên thì thoát
        
        else:
            # Đặt lại các ô để kiểm tra sự kết hợp tiếp theo
            for index, value in zip(remaining_indices, combo):
                grid[index[0]][index[1]] = '_'
    
    print("No valid solutions found.")
    
def resetFgrid(grid): # Chuyển F lại thành '_'
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'F':
                grid[i][j] = '_'
        
def solveBruteFore(grid):
    processBruteFore(grid)
    resetFgrid(grid)
    return grid
      
# Backtracking
def get_neighbors(grid, row, col): # Get neighbor cells
    neighbors = []
    rows, cols = len(grid), len(grid[0])

    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))

    return neighbors

def is_valid(grid, solveBoard): # Check if the solveBoard sastisfies the requirrment
    rows, cols = len(grid), len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if grid[row][col].isnumeric():  # If current cell is a number
                trap_count = 0        
                for neighbor_row, neighbor_col in get_neighbors(grid, row, col):
                    if isinstance(solveBoard[neighbor_row][neighbor_col], bool) and solveBoard[neighbor_row][neighbor_col] == True:  # If neighbor cell is True (Trap)
                        trap_count += 1 # Increase Trap count
                if trap_count != int(grid[row][col]):   # If trap count does not equal the current cell's value
                    return False
                
    return True

def backtrack(grid, solveBoard, row=0, col=0): # Use recursion for backtracking
    rows, cols = len(grid), len(grid[0])

    if row == rows - 1 and col == cols: # If current cell is the final cell
        return is_valid(grid, solveBoard)   # Check if the solveBoard sasstisfies the requirement

    if col == cols: # If the current cell is the last cell of the row
        return backtrack(grid, solveBoard, row + 1, 0)  # Continue recursion with the next row

    # Try assigning True (trap) and False (gem) to the current cell
    if isinstance(solveBoard[row][col], bool) or solveBoard[row][col] == '_':   # If the current cell has Boolean value of '_'
        solveBoard[row][col] = True # Set the current cell to True

    if backtrack(grid, solveBoard, row, col + 1):   # Continue recursion with the next cell
        return True
    
    if isinstance(solveBoard[row][col], bool) or solveBoard[row][col] == '_': # Vice versa
        solveBoard[row][col] = False

    if backtrack(grid, solveBoard, row, col + 1): 
        return True

    return False

def solveBackTrack(grid): # Solve the fird
    rows, cols = len(grid), len(grid[0])
    solveBoard = copy.deepcopy(grid)

    if backtrack(grid, solveBoard): # If the grid is solvable
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "_":   # Set 'T' and 'G' to corresponding cells
                    grid[row][col] = "T" if solveBoard[row][col] == True else "G"
        return grid
    
    else: 
        return None
  
grid = readInput("9x9.txt")
print('Problem:')
for i in grid:
    print(i)

# solved_grid = solveBackTrack(grid)
solved_grid = solveBruteFore(grid)

if solved_grid:
    print('\nSolved:')
    for row in solved_grid:
        print(row)
else:
    print('\nNo solution')