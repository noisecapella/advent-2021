import numpy as np

def print_board(board):
    copy = np.full(board.shape, ' ')
    copy[board == True] = "#"
    for line in ["".join(line) for line in copy]:
        print(line)

def fold_board(dot_list, fold_list):
    dot_list = np.array(dot_list)
    dot_list_shape = dot_list.max(axis=0)
    board = np.zeros(shape=(dot_list_shape[1] + 3, dot_list_shape[0] + 1), dtype='bool')
    for x, y in dot_list:
        board[(y, x)] = True

    for fold_axis, fold_index in fold_list:
        fold_index = int(fold_index)
        old_shape = board.shape

        if fold_axis == "x":
            to_fold_diff = board.shape[1] - (fold_index + 1)
            to_fold_start = fold_index - to_fold_diff
            to_fold = board[:,fold_index + 1: fold_index + 1 + to_fold_diff]
            to_fold = np.flip(to_fold, axis=1)
            #print(f"x {to_fold_start} {to_fold_diff}")
            board = board[:,to_fold_start:to_fold_start + to_fold_diff] | to_fold
        elif fold_axis == "y":
            to_fold_diff = board.shape[0] - (fold_index + 1)
            to_fold_start = fold_index - to_fold_diff
            to_fold = board[fold_index + 1:fold_index + 1 + to_fold_diff,]
            to_fold = np.flip(to_fold, axis=0)
            #print(f"y {to_fold_start} {to_fold_diff}")
            board = board[to_fold_start:to_fold_start + to_fold_diff,] | to_fold
        #print_board(to_fold)
        #print(np.count_nonzero(board == True))
        #print(f"fold {fold_axis}={fold_index}")
        print(f"{fold_axis}={fold_index} {old_shape} => {board.shape}")

    return board


def main():
    dot_list = []
    fold_list = []
    with open("day13.txt") as f:
        while line := f.readline():
            if not line.strip():
                break
            x, y = line.strip().split(",")
            dot_list.append((int(x), int(y)))
        while line := f.readline():
            before, after = line.strip().split("=")
            fold_list.append((before[-1], int(after)))
    print("part 1", np.count_nonzero(fold_board(dot_list, [fold_list[0]])))
    print("part 2")
    print_board(fold_board(dot_list, fold_list))

if __name__ == "__main__":
    main()
