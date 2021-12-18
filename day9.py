import numpy as np

def count_mins(rows):
    out = np.zeros(shape=rows.shape, dtype='bool')
    for x in range(rows.shape[0]):
        for y in range(rows.shape[1]):
            top = np.inf if y == 0 else rows[x, y - 1]
            bottom = np.inf if y == rows.shape[1] - 1 else rows[x, y + 1]
            left = np.inf if x == 0 else rows[x - 1, y]
            right = np.inf if x == rows.shape[0] - 1 else rows[x + 1, y]
            center = rows[x, y]
            if center < top and center < bottom and center < left and center < right:
                out[x, y] = True
    return out

def calc_basin_item(rows, y, x, ret, visited):
    if not (0 <= y < visited.shape[0]) or not (0 <= x < visited.shape[1]):
        return
    if visited[y, x]:
        return
    visited[y, x] = True
    if rows[y, x] == 9:
        return
    ret[y, x] = True
    calc_basin_item(rows, y - 1, x, ret, visited)
    calc_basin_item(rows, y + 1, x, ret, visited)
    calc_basin_item(rows, y, x - 1, ret, visited)
    calc_basin_item(rows, y, x + 1, ret, visited)


def calc_basin(rows):
    basins = []
    mins = count_mins(rows)
    pairs = np.array(mins.nonzero()).transpose()
    to_ret = []
    
    for y, x in pairs:
        ret = np.zeros(shape=rows.shape, dtype='bool')
        visited = np.zeros(shape=rows.shape, dtype='bool')
        calc_basin_item(rows, y, x, ret, visited)
        to_ret.append(ret.sum())
    
    return to_ret


def main():
    lines = [line.strip() for line in open("day9.txt").readlines()]
    board = np.array([[int(z) for z in line] for line in lines])
    mins = count_mins(board)
    print("part 1", (board[mins] + 1).sum())
    basins = sorted(calc_basin(board))
    print("part 2", basins[-1] * basins[-2] * basins[-3])

if __name__ == "__main__":
    main()
