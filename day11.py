import numpy as np

def calc_flashes(initboard, iterations):
    board = np.array(initboard)
    num_flashes = 0
    all_flash = []
    def _inbounds(tup):
        return 0 <= tup[0] < board.shape[0] and 0 <= tup[1] < board.shape[1]

    def _inc(tup):
        if not _inbounds(tup):
            return
        board[tup] += 1

    for n in range(iterations):
        board += 1
        board_flash = np.zeros(dtype='bool', shape=board.shape)
        marked_something = True
        while marked_something:
            marked_something = False
            it = np.nditer(board_flash, flags=['multi_index'])
            for flash in it:
                if flash:
                    continue
                mi = it.multi_index
                if board[mi] <= 9:
                    continue
                board_flash[mi] = True
                num_flashes += 1
                marked_something = True
                for x in (-1, 0, 1):
                    for y in (-1, 0, 1):
                        if x == 0 and y == 0:
                            continue
                        _inc((mi[0] + y, mi[1] + x))
        board[board > 9] = 0
        if np.all(board == 0):
            all_flash.append(n + 1)
            
    return board, num_flashes, all_flash


def main():
    lines = [line.strip() for line in open("day11.txt").readlines()]
    board = np.array([[int(z) for z in line] for line in lines])
    print("part 1", calc_flashes(board, 100)[1])
    print("part 2", calc_flashes(board, 1000)[2][0])
    

if __name__ == "__main__":
    main()
