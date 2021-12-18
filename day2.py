def calc_position_part_2(instructions):
    pos = 0
    depth = 0
    aim = 0
    for instruction, amount in instructions:
        if instruction == "down":
            aim += amount
        elif instruction == "up":
            aim -= amount
        elif instruction == "forward":
            pos += amount
            depth += aim * amount
    return pos * depth


def calc_position_part_1(instructions):
    pos = 0
    depth = 0
    for instruction, amount in instructions:
        if instruction == "down":
            depth += amount
        elif instruction == "up":
            depth -= amount
        elif instruction == "forward":
            pos += amount
    return pos * depth

def main():
    lines = [line.strip() for line in open("day2.txt").readlines()]
    instructions = [(line.split()[0], int(line.split()[1])) for line in lines]
    print("part 1", calc_position_part_1(instructions))
    print("part 2", calc_position_part_2(instructions))

if __name__ == "__main__":
    main()
