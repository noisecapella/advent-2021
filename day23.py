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

def is_room_blocked(room, room_depth):
    for i in range(room_depth):
        if room[i] != ".":
            return True
    return False

def get_empty_room_depth(room):
    for i in range(len(room)):
        if room[i] != '.':
            return i - 1
    return len(room) - 1
            

def possible_moves(board):
    # yield possible moves with their cost
    rooms, hallway = board

    # move from room
    for room_num, room in enumerate(rooms):
        for room_depth, c in enumerate(room):
            if not is_amphipod(c):
                continue
            cost = 10 ** (ord(c) - ord('A'))
            if is_room_blocked(room, room_depth):
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

                dest_room_depth = get_empty_room_depth(rooms[dest_room_num])
                moves = (1 + room_depth) + abs(room_num - dest_room_num) * 2 + (1 + dest_room_depth)
                yield (room_num, room_depth, None), (dest_room_num, dest_room_depth, None), moves * cost

    # from hallway to room
    for hallway_idx, c in enumerate(hallway):
        if not is_amphipod(c):
            continue
        cost = 10 ** (ord(c) - ord('A'))
        dest_room_num = valid_free_room(c, hallway_idx, board)
        if dest_room_num is not None:
            dest_room_depth = get_empty_room_depth(rooms[dest_room_num])
            try:
                moves = abs((dest_room_num * 2) + 2 - hallway_idx) + (1 + dest_room_depth)
            except TypeError:
                import pdb; pdb.set_trace()
            yield (None, None, hallway_idx), (dest_room_num, dest_room_depth, None), moves * cost

def is_final(board):
    rooms, hallway = board
    room_len = len(rooms[0])
    return board[0] == ("A" * room_len, "B" * room_len, "C" * room_len, "D" * room_len)

def add_to_room(room, c):
    depth = get_empty_room_depth(room)
    room_list = list(room)
    room_list[depth] = c
    return "".join(room_list)

def remove_from_room(room):
    depth = get_empty_room_depth(room)
    room_list = list(room)
    if depth + 1 >= len(room):
        raise Exception("unexpected")
    room_list[depth + 1] = "."
    return "".join(room_list)

def new_board_from_pos(board, old_position, new_position):
    rooms, hallway = board
    old_room_num, old_room_depth, old_hallway_idx = old_position
    new_room_num, new_room_depth, new_hallway_idx = new_position
    if old_room_num is None and new_room_num is None:
        raise Exception("unexpected")
    if old_room_num is None:
        # hallway to room
        c = hallway[old_hallway_idx]
        ret_hallway = list(hallway)
        ret_hallway[old_hallway_idx] = "."
        ret_hallway = "".join(ret_hallway)
        ret_rooms = list(rooms)
        ret_rooms[new_room_num] = add_to_room(ret_rooms[new_room_num], c)
        return (tuple(ret_rooms), ret_hallway)
    elif new_room_num is None:
        # room to hallway
        old_room = rooms[old_room_num]
        c = old_room[old_room_depth]
        ret_hallway = list(hallway)
        ret_hallway[new_hallway_idx] = c
        ret_hallway = "".join(ret_hallway)
        ret_rooms = list(rooms)
        ret_rooms[old_room_num] = remove_from_room(ret_rooms[old_room_num])
        return (tuple(ret_rooms), ret_hallway)
    else:
        # room to room
        old_room = rooms[old_room_num]
        new_room = rooms[new_room_num]
        c = old_room[old_room_depth]
        ret_rooms = list(rooms)
        ret_rooms[old_room_num] = remove_from_room(ret_rooms[old_room_num])
        ret_rooms[new_room_num] = add_to_room(ret_rooms[new_room_num], c)
        return (tuple(ret_rooms), hallway)
        

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
    #unvisited = set()

    #for board in iterate_all_boards(initial_board):
    #    distances[board] = math.inf
    #    if board not in unvisited and board != initial_board:
    #        unvisited.add(board)
    #        heap.append((-math.inf, board))

    heap.append((0, initial_board))
    #unvisited.add(initial_board)
    distances[initial_board] = 0
    heap = sorted(heap)
    visited = set()

    final_board = None
    while True:  # while not at end
        current_tup = heap.pop(-1)
        current_board = current_tup[1]
        visited.add(current_board)

        if is_final(current_board):
            final_board = current_board
            break
        
        for old_pos, new_pos, cost in possible_moves(current_board):
            new_board = new_board_from_pos(current_board, old_pos, new_pos)
            if new_board in visited:
                continue

            if new_board not in distances:
                distances[new_board] = math.inf
                tup = (-math.inf, new_board)
                index = bisect.bisect_left(heap, tup)
                heap.insert(index, tup)
            
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

def make_part2_board(board):
    rooms, hallway = board
    to_insert = ['DD', 'CB', 'BA', 'AC']
    rooms = tuple([f"{room[0]}{to_insert[idx]}{room[1]}" for idx, room in enumerate(rooms)])
    return rooms, hallway

def render_board(board):
    rooms, hallway = board
    s = "#" * 13
    s += "\n"
    s += "#" + hallway + "#\n"

    room_len = len(rooms[0])
    for room_depth in range(room_len):
        if room_depth == 0:
            s += "##"
        else:
            s += "  "
        s += "#"
        for room in rooms:
            s += room[room_depth] + "#"
        if room_depth == 0:
            s += "##"
        s += "\n"
    s += "  " + ("#" * 9) + "\n"
    return s

def print_board(board):
    print(render_board(board))


def print_path(path):
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


def main():
    initial_board = read_input()
    print("initial board (part 1):")
    print_board(initial_board)

    print()

    min_cost, path = find_best_outcome_dijkstra(initial_board)
    print_path(path)
    print("part 1", min_cost)
    #print(len(list(iterate_all_boards(initial_board))))

    board_part2 = make_part2_board(initial_board)
    print("initial board (part 2):")
    print_board(board_part2)

    min_cost, path = find_best_outcome_dijkstra(board_part2)
    print_path(path)
    print("part 2", min_cost)
    

if __name__ == "__main__":
    main()
