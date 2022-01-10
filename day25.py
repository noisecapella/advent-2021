import numpy as np

def read_board():
    lines = [line.strip() for line in open("day25.txt").readlines() if line.strip()]
    board = np.array([[ord(c) for c in line] for line in lines], dtype='byte')
    return board


def print_board(board):
    for row in board:
        line = [chr(x) for x in row]
        print("".join(line))
    print()

def iterate(board):
    half_step_board = np.full(shape=board.shape, fill_value=ord('.'), dtype='byte')
    it = np.nditer(board, flags=['multi_index'])
    for c in it:
        right = (it.multi_index[0], (it.multi_index[1] + 1) % board.shape[1])
        if c == ord('>'):
            if board[right] == ord('.'):
                half_step_board[right] = ord('>')
            else:
                half_step_board[it.multi_index] = ord('>')
        elif c == ord('v'):
            half_step_board[it.multi_index] = c

    full_step_board = np.full(shape=board.shape, fill_value=ord('.'), dtype='byte')
    it = np.nditer(half_step_board, flags=['multi_index'])
    for c in it:
        down = ((it.multi_index[0] + 1) % board.shape[0], it.multi_index[1])
        if c == ord('>'):
            full_step_board[it.multi_index] = c
        elif c == ord('v'):
            if half_step_board[down] == ord('.'):
                full_step_board[down] = ord('v')
            else:
                full_step_board[it.multi_index] = c

    return full_step_board


def main():
    board = read_board()
    print_board(board)
    iterate_count = 0
    next_board = board
    while True:
        new_board = iterate(next_board)
        if np.all(next_board == new_board):
            print("part 1", iterate_count + 1)
            break
        print_board(next_board)
        iterate_count += 1
        next_board = new_board
        #print_board(next_board)


if __name__ == "__main__":
    main()
    
    
