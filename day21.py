import numpy as np
from functools import cache
import re

def read_input():
    lines = [line.strip() for line in open("day21.txt").readlines()]
    positions = {}
    for line in lines:
        if not line:
            break
        group = re.search("Player (\d+) starting position: (\d+)", line).groups()
        positions[int(group[0])] = int(group[1])
    return positions

def calc_score_part1(initial_positions):
    players = [1, 2]
    player_index = 0

    dice = list(range(1, 101))
    dice_index = 0

    board = list(range(1, 11))
    board_indices = {
        player: board.index(initial_positions[player]) for player in players
    }
    totals = {player: 0 for player in players}
    num_rolls = 0
    
    while True:
        player = players[player_index]
        board_index = board_indices[player]

        roll = dice[dice_index] + dice[(dice_index + 1) % len(dice)] + dice[(dice_index + 2) % len(dice)]
        new_board_index = (board_index + roll) % len(board)
        num_rolls += 3
        board_indices[player] = new_board_index
        new_position = board[new_board_index]
        totals[player] += new_position
        print(f"player {player} moved to {new_position} and now has {totals[player]} points")

        if totals[player] >= 1000:
            other_player = players[(player_index + 1) % len(players)]
            return player, totals[player], other_player, totals[other_player], num_rolls
        
        player_index = (player_index + 1) % len(players)
        dice_index = (dice_index + 3) % len(dice)

def calc_score_part2(initial_positions):

    @cache
    def _calc_score(current_player_index, player1_board_index, player2_board_index, player1_score, player2_score, rolls):
        # return value is number of additional winning universes for player1, player2
        totals = np.array([0, 0])
        next_player = (current_player_index + 1) % 2 if roll_count == 2 else current_player_index

        if len(rolls) < 2:
            for roll in (3, 2, 1):
                totals += np.array(_calc_score(next_player, player1_board_index, player2_board_index, player1_score, player2_score, rolls + (roll, )))
            return totals
            
        for last_roll in (3, 2, 1):
            roll = sum(rolls) + last_roll
            if current_player_index == 0:
                
                new_player1_board_index = (player1_board_index + roll) % 10
                new_player1_score = player1_score + new_player1_board_index + 1

                if new_player1_score >= 21:
                    totals += np.array([1, 0])
                else:
                    pair = np.array(_calc_score(next_player, new_player1_board_index, player2_board_index, new_player1_score, player2_score, ()))
                    totals += pair
                
            else:
                new_player2_board_index = (player2_board_index + roll) % 10
                new_player2_score = player2_score + new_player2_board_index + 1
                if new_player2_score >= 21:
                    totals += np.array([0, 1])
                else:
                    pair = np.array(_calc_score(next_player, player1_board_index, new_player2_board_index, player1_score, new_player2_score, ()))
                    totals += pair

        return tuple(totals)


    # go in reverse order of score to better cache values
    scores = []
    for _player1_score in range(20, -1, -1):
        for _player2_score in range(20, -1, -1):
            scores.append((_player1_score, _player2_score))
    scores = reversed(sorted(scores, key=sum))

    tup = []
    for _score1, _score2 in scores:
        if _score1 > _score2:
            tup.append((_score1, _score2, 0))
            tup.append((_score1, _score2, 1))
        else:
            tup.append((_score1, _score2, 1))
            tup.append((_score1, _score2, 0))

    roll_possibilities = set()
    for roll_count in range(3):
        for roll1 in (3,2,1):
            for roll2 in (3,2,1):
                for roll3 in (3,2,1):
                    rolls = tuple([roll3, roll2, roll1][:roll_count])
                    roll_possibilities.add(rolls)
    roll_possibilities = list(reversed(sorted(roll_possibilities, key=lambda z: (len(z), sum(z)))))
            
    iterations = 0
    for player1_score, player2_score, current_player_index in tup:
        for player1_board_index in range(10):
            for player2_board_index in range(10):
                for rolls in roll_possibilities:
                    _calc_score(current_player_index, player1_board_index, player2_board_index, player1_score, player2_score, rolls)
                    iterations += 1
                    if iterations % 10000 == 0:
                        print(".", (player1_score, player2_score, iterations))


    return _calc_score(0, initial_positions[1] - 1, initial_positions[2] - 1, 0, 0, ())
                                         

def main():
    positions = read_input()
    winning_player, winning_player_score, losing_player, losing_player_score, num_rolls = calc_score_part1(positions)
    print("part 1", losing_player_score, num_rolls, losing_player_score * num_rolls)

    print("part 2", calc_score_part2(positions))

if __name__ == "__main__":
    main()
    
