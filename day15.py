import bisect
import numpy as np

def _in_bounds(board, coord):
    return (0 <= coord[0] < board.shape[0]) and (0 <= coord[1] < board.shape[1])


def neighbors(board, unvisited, coord):
    left = (coord[0], coord[1] - 1)
    right = (coord[0], coord[1] + 1)
    up = (coord[0] - 1, coord[1])
    down = (coord[0] + 1, coord[1])
    for each in [left, right, up, down]:
        if _in_bounds(board, each):
            if each in unvisited:
                yield each

def find_path_dijkstra(board):
    start = (0,0)
    end = (board.shape[0] - 1, board.shape[1] - 1)
    unvisited = set()
    heap = []
    distances = {start: 0}
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            coord = (y,x)
            unvisited.add(coord)
            if coord != start:
                heap.append((-np.inf, coord))
                distances[coord] = np.inf
    heap.append((0, start))

    while unvisited:
        current = heap[-1][1]
        # print(len(unvisited))
        for neighbor in neighbors(board, unvisited, current):
            old_tup = (-distances[neighbor], neighbor)
            neighbor_distance = min(distances[neighbor], distances[current] + board[neighbor])
            distances[neighbor] = neighbor_distance
            heap.pop(bisect.bisect_left(heap, old_tup))
            new_tup = (-neighbor_distance, neighbor)
            new_index = bisect.bisect_left(heap, new_tup)
            heap.insert(new_index, new_tup)

        unvisited.remove(current)
        heap.pop(-1)

        if current == end:
            print(distances, current)
            return distances[current]

def embiggen(board):
    newboard = np.zeros(shape=(board.shape[0] * 5, board.shape[1] * 5))
    for y in range(5):
        for x in range(5):
            piece = np.array(board)
            for i in range(x + y):
                piece += 1
                piece[piece > 9] = 1

            newboard[board.shape[0] * y:board.shape[0] * (y+1), board.shape[1] * x:board.shape[1] * (x+1)] = piece
    return newboard

        
def main():
    lines = [line.strip() for line in open("day15.txt").readlines()]
    board = np.array([[int(x) for x in line] for line in lines])
    print("part 1", find_path_dijkstra(board))

    print("part 2", find_path_dijkstra(embiggen(board)))
    

if __name__ == "__main__":
    main()
