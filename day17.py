import numpy as np
import re

def intersects_target(initial_velocity, targetx, targety):
    pos = [0, 0]
    velocity = [initial_velocity[1], initial_velocity[0]]
    positions = []
    max_y = -np.inf
    while True:
        #print(f"pos {pos}")
        positions.append(pos)
        max_y = max(max_y, pos[0])
        if targety[0] <= pos[0] <= targety[1] and targetx[0] <= pos[1] <= targetx[1]:
            return True, pos, positions, max_y
        elif pos[0] < min(targety) or pos[1] > max(targetx):
            return False, pos, positions, max_y
        pos = [pos[0] + velocity[0], pos[1] + velocity[1]]
        velocity[0] -= 1
        if velocity[1] > 0:
            velocity[1] -= 1
        elif velocity[1] < 0:
            velocity[1] += 1



def main():
    line = open("day17.txt").readline().strip()
    parts = [int(n) for n in re.findall("[-\d]+", line)]
    targetx = parts[:2]
    targety = parts[2:]
    values = set()
    max_y = 0
    # just guessed at these values
    for x in range(0, 400):
        for y in range(-100, 100):
            hit, pos, _, new_max_y = intersects_target((x, y), targetx, targety)
            if not hit:
                continue
            values.add((y,x))
            max_y = max(max_y, new_max_y)
            #max_y = max(intersects_target((y, x), targetx, targety)[3], max_y)
    print("part1", max_y)
    print("part2", len(values))

if __name__ == "__main__":
    main()


