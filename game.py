#/usr/bin/python3

# Inspired by Q42's binary puzzle game "Oh hi"
# See also https://www.binarypuzzle.com

grid = [
    "   0  00",
    "1    1  ",
    "0  0   0",
    " 1      ",
    "   1 1 1",
    "       0",
    "    0 0 ",
    "00 1    "
]

grid2 = [
    "  1 10",
    "1 1  0",
    "   1  ",
    "1 00  ",
    "      ",
    " 1    ",
]

grid = [
    " 1       0",
    " 10 1  0  ",
    "      00  ",
    "   0      ",
    "   0    0 ",
    "    1 0   ",
    "      0   ",
    "00 1 1   1",
    "00  0     ",
    "       00 "
]

# https://www.binarypuzzle.com/puzzles.php?size=14&level=4&nr=1
grid = [
    "    10       1",
    "1    0   1 1 1",
    "  1   1       ",
    "0    11    0 1",
    "0 0     1    1",
    " 0      0     ",
    "  1      1  1 ",
    "  1 0  1  0   ",
    "     1 1    1 ",
    "0 10 1    0   ",
    "  1       00  ",
    "   0          ",
    " 1       0    ",
    "  0   0    0  "
]

def parse_board(grid):
    board = {}
    empty = set()
    # record coordinates and values of the board. Record empty cells as well
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != ' ':
                board[(i, j)] = int(cell)
            else:
                empty.add((i, j))

    return board, empty

# Find the width of the board
def width(board):
    return max(x for _, x in board.keys()) + 1

# Find the height of the board
def height(board):
    return max(y for y, _ in board.keys()) + 1

def value(board, x, y):
    assert((x,y) in board)
    return board[(x,y)]

def get_pair(board, pos1, pos2):
    if pos1 in board and pos2 in board:
        return (value(board, pos1[0], pos1[1]), value(board, pos2[0], pos2[1]))
    return None

# if the two positions are the same, return the opposite value
def infer_same(board, pos1, pos2):
    p = get_pair(board, pos1, pos2)
    if p is not None:
        if p[0] == p[1]:
            return 1 - p[0]
    return None

def count_values_row(board, row):
    counts = [0, 0]
    for i in range(width(board)):
        if (row, i) in board:
            counts[board[(row, i)]] += 1
    return counts

def count_values_col(board, col):
    counts = [0, 0]
    for i in range(height(board)):
        if (i, col) in board:
            counts[board[(i, col)]] += 1
    return counts

# Given a cell not known on the board, see if we can infer the value that belongs there
# Return None if we can't. Otherwise, return the value that belongs there.
def infer(board, x, y):
    pairs = [
        # if the cells to the left and right of the cell are the same, the cell must be different
        ((x-1,y), (x+1,y)),
        # if the cells above and below the cell are the same, the cell must be different
        ((x,y-1), (x,y+1)),
        # if the two cells to the left are the same, the cell must be different
        ((x-1,y), (x-2,y)),
        # if the two cells to the right are the same, the cell must be different
        ((x+1,y), (x+2,y)),
        # if the two cells above are the same, the cell must be different
        ((x,y-1), (x,y-2)),
        # if the two cells below are the same, the cell must be different
        ((x,y+1), (x,y+2))
    ]
    for p1, p2 in pairs:
        p = infer_same(board, p1, p2)
        if p is not None:
            return p

    h = height(board)
    w = width(board)

    # if the row already has w/2 of the same value, the rest must be the opposite value
    c0,c1 = count_values_row(board, x)
    if c0 == w//2:
        return 1
    elif c1 == w//2:
        return 0

    # if the col already has w/2 of the same value, the rest must be the opposite value
    c0,c1 = count_values_col(board, y)
    if c0 == h//2:
        return 1
    elif c1 == h//2:
        return 0

    return None

YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
END = "\033[0m"
colors = [YELLOW, LIGHT_BLUE]

def print_board(board):
    global colors, END
    h = height(board)
    w = width(board)
    for i in range(h):
        for j in range(w):
            if (i, j) in board:
                print(colors[board[(i, j)]] + '██' + END, end='')
            else:
                print('  ', end='')
        print()

def solve_immediates(board, todo):
    while todo:
        t = todo.copy()
        for x,y in t:
            val = infer(board, x, y)
            if val is not None:
                board[(x,y)] = val
                todo.remove((x,y))
                # print_board(board)
                # print('='*20)
        if t == todo:
            return

import itertools

def valid_set(s, w):
    for i in range(w-2):
        if i in s:
            if i+1 in s and i+2 in s:
                return False
        else:
            if i+1 not in s and i+2 not in s:
                return False
    return True

# >>> s = list(all_sets(14))
# >>> print(len(s))
# >>> 259
# Return all valid sets of a given width
def all_sets(width):
    for combo in itertools.combinations(list(range(width)), width//2):
        s = frozenset(combo)
        if valid_set(s, width):
            yield s

def solve_set(cells, solved, sets, size):
    if len(cells) == size:
        # already solved
        return

    zeros = frozenset([i for i, v in cells if v == 0])
    ones = frozenset([i for i, v in cells if v == 1])
    todo = set(range(size)) - ones - zeros

    valid_sets = [s for s in sets if s not in solved and all(i in s for i in ones) and all(i not in s for i in zeros)]
    # print("valid sets", len(valid_sets))
    # find the values in todo which are also in every one of valid_sets
    # if the value is in every valid set, we can infer that the value is that value
    for i in todo:
        if all(i in s for s in valid_sets):
            yield (i, 1)
        elif all(i not in s for s in valid_sets):
            yield (i, 0)

def get_row(board, row, size):
    return [(i, board[(row,i)]) for i in range(size) if (row, i) in board]

def get_col(board, col, size):
    return [(i, board[(i, col)]) for i in range(size) if (i, col) in board]

# returns the row's 1-indexes if the row is solved
def get_solved_row(board, row, size):
    cells = get_row(board, row, size)
    if len(cells) == size:
        return frozenset([i for i, v in cells if v == 1])
    return None

# returns the col's 1-indexes if the col is solved
def get_solved_col(board, col, size):
    cells = get_col(board, col, size)
    if len(cells) == size:
        return frozenset([i for i, v in cells if v == 1])
    return None

def get_solved_rows(board, size):
    for row in range(size):
        r = get_solved_row(board, row, size)
        if r:
            yield r

def get_solved_cols(board, size):
    for col in range(size):
        r = get_solved_col(board, col, size)
        if r:
            yield r

def solve_row(board, todo, row, sets, size):
    solved = set(get_solved_rows(board, size))
    for i, v in solve_set(get_row(board, row, size), solved, sets, size):
        board[(row, i)] = v
        # print("row: Solved", (row, i), "to", v)
        todo.remove((row, i))

def solve_col(board, todo, col, sets, size):
    solved = set(get_solved_cols(board, size))
    for i, v in solve_set(get_col(board, col, size), solved, sets, size):
        board[(i, col)] = v
        # print("col: Solved", (i, col), "to", v)
        todo.remove((i, col))

def solve_exhaustive(board, todo, sets, size):
    # iterate each row and determine the set of all possible values for each cell
    # if a cell has only one possible value, set it to that value
    for i in range(size):
        solve_row(board, todo, i, sets, size)
        solve_col(board, todo, i, sets, size)

board, todo = parse_board(grid)


print_board(board)
# print(todo)
print("="*20)
size = width(board)
all_solutions = list(all_sets(size))
# print(len(all_solutions))
while True:
    print("Solving", len(todo))
    t = todo.copy()
    # solve_immediates(board, todo)
    solve_exhaustive(board, todo, all_solutions, size)
    if t == todo:
        break

print_board(board)