import numpy as np

def read_board():
    f = open("day4.txt")
    picks = [int(n) for n in f.readline().strip().split(",")]
    lines = [l.strip() for l in f.readlines()]
    boards = []
    for n in range(1, len(lines), 6):
        boards.append(np.array([[int(c) for c in line.strip().split()] for line in lines[n:n+5]]))
    return picks, boards

def main():
    picks, boards = read_board()

    board_statuses = [np.zeros(shape=board.shape, dtype='bool') for board in boards]
    board_wins = [None for board in boards]
    for pick_num, pick in enumerate(picks):
        for i in range(len(board_statuses)):
            board_statuses[i] |= boards[i] == pick

            if np.any(np.all(board_statuses[i], axis=0)) or np.any(np.all(board_statuses[i], axis=1)):
                if board_wins[i] is None:
                    board = boards[i]
                    board_status = board_statuses[i]
                    score = board[board_status == False].sum()
                    board_wins[i] = (pick_num, pick, score)
    board_wins = sorted(board_wins)
    print("part 1", board_wins[0][1] * board_wins[0][2])
    print("part 2", board_wins[-1][1] * board_wins[-1][2])


if __name__ == "__main__":
    main()

        
