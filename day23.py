import math
import bisect
from collections import deque

def is_amphipod(c):
    return ord('A') <= ord(c) <= ord('D')


def valid_hallway_spaces(room_num, hallway):
    # what hallway spaces are free to travel from the room?
    start_hallway_idx = (room_num * 2) + 2
    for idx in range(start_hallway_idx - 1, -1, -1):
        if idx % 2 == 0 and 2 <= idx <= 8:
            # blocking a room
            continue
        if hallway[idx] == ".":
            yield idx
        else:
            break
    for idx in range(start_hallway_idx + 1, len(hallway)):
        if idx % 2 == 0 and 2 <= idx <= 8:
            # blocking a room
            continue
        if hallway[idx] == ".":
            yield idx
        else:
            break


def valid_free_room(c, hallway_idx, board):
    # starting from hallway_idx, can you get to the appropriate room for c? if yes return that room number
    rooms, hallway = board

    dest_room_num = ord(c) - ord('A')
    dest_hallway_idx = (dest_room_num * 2) + 2
    first, second = sorted([hallway_idx, dest_hallway_idx])
    blocked = False
    for idx in range(first, second + 1):
        if idx == hallway_idx:
            continue
        if hallway[idx] != ".":
            blocked = True
            break
    if blocked:
        # hallway is blocked
        return None
    for occupant in rooms[dest_room_num]:

        if occupant != "." and occupant != c:
            # no space in room, or room occupied by another amphipod
            return None
    return dest_room_num

        

def possible_moves(board):
    # yield possible moves with their cost
    rooms, hallway = board

    # move from room
    for room_num, room in enumerate(rooms):
        for room_depth, c in enumerate(room):
            if not is_amphipod(c):
                continue
            cost = 10 ** (ord(c) - ord('A'))
            if room_depth == 1 and is_amphipod(room[0]):
                # blocked, no move possible
                continue

            # room to hallway
            for hallway_idx in valid_hallway_spaces(room_num, hallway):
                moves = (1 + room_depth) + abs(((room_num * 2) + 2) - hallway_idx)
                yield (room_num, room_depth, None), (None, None, hallway_idx), moves * cost

            # room to another room
            dest_room_num = valid_free_room(c, (room_num * 2) + 2, board)
            if dest_room_num is not None:
                if dest_room_num == room_num:
                    continue
                dest_room_depth = 1 if "." == rooms[dest_room_num][1] else 0
                moves = (1 + room_depth) + abs(room_num - dest_room_num) * 2 + (1 + dest_room_depth)
                yield (room_num, room_depth, None), (dest_room_num, dest_room_depth, None), moves * cost

    # from hallway to room
    for hallway_idx, c in enumerate(hallway):
        if not is_amphipod(c):
            continue
        cost = 10 ** (ord(c) - ord('A'))
        dest_room_num = valid_free_room(c, hallway_idx, board)
        if dest_room_num is not None:
            dest_room_depth = 1 if "." == rooms[dest_room_num][1] else 0
            moves = abs((dest_room_num * 2) + 2 - hallway_idx) + (1 + dest_room_depth)
            yield (None, None, hallway_idx), (dest_room_num, dest_room_depth, None), moves * cost

def is_final(board):
    return board[0] == ("AA", "BB", "CC", "DD")

def new_board_from_pos(board, old_position, new_position):
    rooms, hallway = board
    old_room_num, old_room_depth, old_hallway_idx = old_position
    new_room_num, new_room_depth, new_hallway_idx = new_position
    if old_room_num is None and new_room_num is None:
        raise Exception("unexpected")
    if old_room_num is None:
        # hallway to room
        new_room = rooms[new_room_num]
        c = hallway[old_hallway_idx]
        ret_hallway = list(hallway)
        ret_hallway[old_hallway_idx] = "."
        ret_hallway = "".join(ret_hallway)
        ret_rooms = list(rooms)
        if new_room[1] == ".":
            ret_rooms[new_room_num] = f".{c}"
        else:
            ret_rooms[new_room_num] = f"{c}{new_room[1]}"
        
        return (tuple(ret_rooms), ret_hallway)
    elif new_room_num is None:
        # room to hallway
        old_room = rooms[old_room_num]
        c = old_room[old_room_depth]
        ret_hallway = list(hallway)
        ret_hallway[new_hallway_idx] = c
        ret_hallway = "".join(ret_hallway)
        ret_rooms = list(rooms)
        if old_room_depth == 0:
            ret_rooms[old_room_num] = f".{old_room[1]}"
        else:
            ret_rooms[old_room_num] = ".."
        return (tuple(ret_rooms), ret_hallway)
    else:
        # room to room
        old_room = rooms[old_room_num]
        new_room = rooms[new_room_num]
        c = old_room[old_room_depth]
        ret_rooms = list(rooms)
        if old_room_depth == 0:
            ret_rooms[old_room_num] = f".{old_room[1]}"
        else:
            ret_rooms[old_room_num] = ".."
        if new_room[1] == ".":
            ret_rooms[new_room_num] = f".{c}"
        else:
            ret_rooms[new_room_num] = f"{c}{new_room[1]}"
        return (tuple(ret_rooms), hallway)
        

def sanity_check(board):
    if not ("".join(sorted(str(board)))).endswith("...AABBCCDD"):
        import pdb; pdb.set_trace()
        raise Exception()

def iterate_all_boards(initial_board):
    unvisited = [initial_board]
    visited = set()
    iterations = 0
    while unvisited:
        iterations += 1
        if iterations % 100000 == 0:
            print(len(visited))
        board = unvisited.pop(-1)
        yield board
        visited.add(board)
        for old_pos, new_pos, cost in possible_moves(board):
            new_board = new_board_from_pos(board, old_pos, new_pos)
            if new_board not in visited:
                unvisited.append(new_board)
    
def find_best_outcome_dijkstra(initial_board):

    # visited = set()  # visited boards
    heap = []  # always sorted, (-distance, board)
    distances = {}  # board: distance. May not contain all distances initially, new boards should assume to have inf distance
    prev = {}  # the path being created
    unvisited = set()

    for board in iterate_all_boards(initial_board):
        distances[board] = math.inf
        if board not in unvisited and board != initial_board:
            unvisited.add(board)
            heap.append((-math.inf, board))

    heap.append((0, initial_board))
    unvisited.add(initial_board)
    distances[initial_board] = 0
    heap = sorted(heap)

    while len(unvisited) > 0:  # while not at end
        current_tup = heap.pop(-1)
        current_board = current_tup[1]
        unvisited.remove(current_board)

        if len(heap) != len(unvisited):
            import pdb; pdb.set_trace()
        
        for old_pos, new_pos, cost in possible_moves(current_board):
            new_board = new_board_from_pos(current_board, old_pos, new_pos)
            if new_board not in unvisited:
                continue

            old_tup = (-distances[new_board], new_board)
            neighbor_distance = distances[current_board] + cost
            if distances[new_board] > neighbor_distance:
                index = bisect.bisect_left(heap, old_tup)
                popped = heap.pop(index)
                distances[new_board] = neighbor_distance
                new_tup = (-neighbor_distance, new_board)
                new_index = bisect.bisect_left(heap, new_tup)
                heap.insert(new_index, new_tup)
                prev[new_board] = current_board

    final_boards = [(distance, board) for (board, distance) in distances.items() if is_final(board)]
    final_board = sorted(final_boards)[0][1]
    path = []
    board = final_board
    while board != initial_board:
        path.append(board)
        board = prev[board]
    path.append(initial_board)
    path = list(reversed(path))

    return distances[final_board], path


def read_input():
    f = open("day23.txt")
    f.readline()
    hallway = tuple([c for c in f.readline() if c == "."])
    side_rooms = [[], [], [], []]
    for _ in range(2):
        line = [c for c in f.readline() if ord('A') <= ord(c) <= ord('D')]
        for i, c in enumerate(line):
            side_rooms[i].append(c)
    side_rooms = tuple(["".join(room) for room in side_rooms])
    return side_rooms, "".join(hallway)

def render_board(board):
    rooms, hallway = board
    s = "#" * 13
    s += "\n"
    s += "#" + hallway + "#\n"
    s += "###"
    for room in rooms:
        s += room[0] + "#"
    s += "##\n"
    s += "  #"
    for room in rooms:
        s += room[1] + "#"
    s += "\n"
    s += "  " + ("#" * 9)
    return s

def print_board(board):
    print(render_board(board))


def main():
    initial_board = read_input()
    x = (('BA','.D', 'CC', 'DA'), '...B.......')
    y = (('BA','..', 'CC', 'DA'), '...B.D.....')
    z = (('..', 'CD', 'BC', 'DA'), '.B.A.......')
    #print(list(valid_hallway_spaces(1, x[1])))
    print("initial board:")
    print_board(initial_board)
    #    print()
    #return

    print()
    #for old_pos, new_pos, cost in possible_moves(z):
    #    new_board = new_board_from_pos(z, old_pos, new_pos)
    #    print(f"  moved {old_pos} to {new_pos}")
    #    print_board(new_board)
    #    print()
    #return

    min_cost, path = find_best_outcome_dijkstra(initial_board)
    for i, board in enumerate(path):
        print()
        print_board(board)
        if i == 0:
            print(0)
        else:
            for old_pos, new_pos, cost in possible_moves(path[i-1]):
                if new_board_from_pos(path[i-1], old_pos, new_pos) == board:
                    print("cost", cost, old_pos, new_pos)
                    break
    print("part 1", min_cost)
    #print(len(list(iterate_all_boards(initial_board))))

if __name__ == "__main__":
    main()
