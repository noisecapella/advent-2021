import numpy as np
from collections import Counter

def update_polymer(polymer, lookup, iterations):
    counter = Counter()
    letter = Counter(polymer)
    for n in range(1, len(polymer)):
        counter[polymer[n-1:n+1]] += 1
    for iteration in range(iterations):
        replacements = Counter()
        for pair, replacement in lookup.items():
            if pair in counter:
                replacements[pair] -= counter[pair]
                replacements[f"{pair[0]}{replacement}"] += counter[pair]
                replacements[f"{replacement}{pair[1]}"] += counter[pair]
                letter[replacement] += counter[pair]
        counter += replacements
    return letter


def main():
    f = open("day14.txt")
    polymer_start = f.readline().strip()
    f.readline()
    
    lookup = {line.split(" -> ")[0]: line.split(" -> ")[1].strip() for line in f.readlines()}
    common = update_polymer(polymer_start, lookup, 10).most_common()
    print("part 1", common[0][1] - common[-1][1])

    common = update_polymer(polymer_start, lookup, 40).most_common()
    print("part 2", common[0][1] - common[-1][1])


if __name__ == "__main__":
    main()
