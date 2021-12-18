import numpy as np
from collections import Counter


def simulate(fish, iterations):
    counter = Counter(fish)
    
    for n in range(iterations):
        new_counter = Counter()
        for it in range(9):
            new_counter[it] = counter[it + 1]
        new_counter[6] += counter[0]
        new_counter[8] += counter[0]
        counter = new_counter
    return counter

def count(counter):
    return sum(counter.values())

def main():
    fish = [int(z) for z in open("day6.txt").readline().strip().split(",")]
    print("part 1", count(simulate(fish, 80)))
    print("part 2", count(simulate(fish, 256)))


if __name__ == "__main__":
    main()
