import numpy as np
import re

def get_diff(y2, y1):
    if y2 > y1:
        return 1
    elif y2 < y1:
        return -1
    return 0

def mark_board(coords, skip_diagonals):
    max_coords = (0, 0)
    for y1, x1, y2, x2 in coords:
        max_coords = (max(max_coords[0], y1, y2), max(max_coords[1], x1, x2))

    board = np.zeros(shape=(max_coords[0] + 1, max_coords[1] + 1))
    for y1, x1, y2, x2 in coords:
        if skip_diagonals and y1 != y2 and x1 != x2:
            continue
        iterations = max(abs(y1-y2), abs(x1-x2))
        diff = (get_diff(y2, y1), get_diff(x2, x1))
        for n in range(iterations + 1):
            board[(y1 + diff[0]*n, x1 + diff[1]*n)] += 1

    return np.count_nonzero(board[board > 1])

def main():
    lines = [line.strip() for line in open("day5.txt").readlines()]
    coords = [[int(z) for z in re.findall("\d+", line)] for line in lines]
    print("part 1", mark_board(coords, True))
    print("part 2", mark_board(coords, False))
    

if __name__ == "__main__":
    main()
