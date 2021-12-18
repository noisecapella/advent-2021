import numpy as np
from collections import Counter

def sorted_str(z):
    return "".join(sorted(z))

def split_line(line):
    return [[subpiece for subpiece in piece.split()] for piece in line.split("|")]


def row_to_num(line):
    nums, notes = line
    letters = calc(line)
    print(letters)
    digits = [letters[sorted_str(note)] for note in notes]
    coef = np.flip(10**np.arange(len(digits)))
    return (np.array(digits) * coef).sum()


def calc(line):
    letters = {}  # sorted letter string to int
    nums, notes = line
    nums = [sorted_str(z) for z in nums]
    nums = np.array(nums)
    lens = np.char.str_len(nums)
    one_letters_index = (lens == 2).nonzero()[0][0]
    seven_letters_index = (lens == 3).nonzero()[0][0]
    top_line = list(set(nums[seven_letters_index]) - set(nums[one_letters_index]))[0]
    right_line = nums[one_letters_index]
    four_letters_index = (lens == 4).nonzero()[0][0]
    four_choices = np.array(list(set(nums[four_letters_index]) - set(nums[one_letters_index])))
    eight_letters_index = (lens == 7).nonzero()[0][0]
    
    letters[sorted_str(nums[seven_letters_index])] = 7
    letters[sorted_str(nums[one_letters_index])] = 1
    letters[sorted_str(nums[four_letters_index])] = 4
    letters[sorted_str(nums[eight_letters_index])] = 8
    
    ## 1,4,7,8 have unique segments
    ## 2,3,5 have 5 segments, 6,9, 0 have 6 each
    # 4 has upper left and middle segments. match with the len-5's -- the upper left segment shows up 1 time but the middle segment is 3 
    len5s = nums[lens == 5]
    #print(np.char.count(len5s, four_choices[1]))
    if np.count_nonzero(np.char.count(len5s, four_choices[1])) == 3:
        middle_line = four_choices[1]
        up_left_line = four_choices[0]
    else:
        middle_line = four_choices[0]
        up_left_line = four_choices[1]

    sorted_five = sorted_str(len5s[np.char.count(len5s, up_left_line) == 1][0])
    letters[sorted_five] = 5
    #print(letters)
    lower_right = list(set(right_line).intersection(set(sorted_five)))[0]
    sorted_two = sorted_str(len5s[np.char.count(len5s, lower_right) == 0][0])
    letters[sorted_two] = 2
    sorted_three = sorted_str(list({sorted_str(word) for word in len5s} - {sorted_two, sorted_five})[0])
    letters[sorted_three] = 3
    len6s = nums[lens == 6]
    upper_right = list(set(right_line) - {lower_right})[0]
    letters[sorted_str(len6s[np.char.count(len6s, upper_right) == 0][0])] = 6
    letters[sorted_str(set(nums[eight_letters_index]) - {middle_line})] = 0
    letters[sorted_str(list(set(nums) - set(letters.keys()))[0])] = 9
    return letters

def main():
    lines = [line.strip() for line in open("day8.txt").readlines()]
    counter_part1 = Counter()
    output_values = 0
    for line in lines:
        nums, notes = split_line(line)
        letters = calc((nums, notes))
        digits = []
        for note in notes:
            num = letters["".join(sorted([z for z in note]))]
            digits.append(num)
            counter_part1[num] += 1
        output_values += int("".join([str(z) for z in digits]))
    print("part 1", counter_part1[1] + counter_part1[4] + counter_part1[7] + counter_part1[8])
    print("part 2", output_values)
        

if __name__ == "__main__":
    main()
