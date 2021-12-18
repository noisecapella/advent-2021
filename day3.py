import numpy as np

def _pick_bincount(bincounts, is_oxygen):
    if bincounts[0] == bincounts[1]:
        return 1 if is_oxygen else 0
    return bincounts.argmax() if is_oxygen else bincounts.argmin()

def _calc_oxygen_co2(board, is_oxygen=False):
    board = np.array(board)
    for n in range(board.shape[1]):
        bincounts = np.bincount(board[:,n])
        num = _pick_bincount(bincounts, is_oxygen)
        board = board[board[:,n] == num,]
        if board.shape[0] == 1:
            break
    return board

def _row_as_number(row):
    return int("".join([str(z) for z in row]), 2)

def calc_oxygen_co2(board):
    oxygen_board = _calc_oxygen_co2(board, True)
    co2_board = _calc_oxygen_co2(board, False)
    return _row_as_number(oxygen_board[0]) * _row_as_number(co2_board[0])
        


def calc_gamma_episilon(board):
    gamma = [np.bincount(board[:,n]).argmax() for n in range(board.shape[1])]
    episilon = [np.bincount(board[:,n]).argmin() for n in range(board.shape[1])]

    return _row_as_number(gamma) * _row_as_number(episilon)


def main():
    lines = [[int(z) for z in line.strip()] for line in open("day3.txt").readlines()]
    board = np.array(lines)
    print("part 1", calc_gamma_episilon(board))
    print("part 2", calc_oxygen_co2(board))


if __name__ == "__main__":
    main()
