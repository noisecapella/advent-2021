import math
import copy
import numpy as np
import json
from functools import reduce

def magnitude(n):
    if isinstance(n, int):
        return n
    return magnitude(n[0])*3 + magnitude(n[1])*2

def get_item_at_path(tree, path):
    current = tree
    for i, elem in enumerate(path):
        current = current[elem]
    return current

def set_item_at_path(tree, path, replacement):
    tree = copy.deepcopy(tree)
    item = get_item_at_path(tree, path[:-1])
    item[path[-1]] = replacement
    return tree

def get_sibling(tree, path, get_left):
    sibling = 0 if get_left else 1
    same = 1 if get_left else 0
    partial_path = None
    for i, elem in reversed(list(enumerate(path))):
        if elem == same:
            partial_path = [*path[:i], sibling]
            break
    if partial_path is None:
        return None, None

    item = get_item_at_path(tree, partial_path)
    while isinstance(item, list):
        item = item[same]
        partial_path.append(same)
    return item, partial_path


def find_depth_pairs(number, path):
    if isinstance(number, list):
        if len(path) == 4:
            yield number, path
            return
    
        for i, item in enumerate(number):
            yield from find_depth_pairs(item, [*path, i])

def find_regular_numbers_above_10(tree, path):
    if isinstance(tree, int):
        if tree >= 10:
            yield tree, path
    else:
        for i, item in enumerate(tree):
            yield from find_regular_numbers_above_10(item, [*path, i])

    
def reduce_snailfish(tree):
    current = tree
    while True:
        pairs = list(find_depth_pairs(current, []))
        if pairs:
            pair, path = pairs[0]
            # print("explode", path, len(pairs))
            left, left_path = get_sibling(current, path, True)
            right, right_path = get_sibling(current, path, False)
            if left_path is not None:
                current = set_item_at_path(current, left_path, left + pair[0])
            if right_path is not None:
                current = set_item_at_path(current, right_path, right + pair[1])
            current = set_item_at_path(current, path, 0)
            continue

        pairs = list(find_regular_numbers_above_10(current, []))
        if pairs:
            num, path = pairs[0]
            # print("split", path, len(pairs))
            a = math.floor(num / 2)
            b = math.ceil(num / 2)
            current = set_item_at_path(current, path, [a,b])
            continue
        return current

def add(total, element):
    new_total = [total, element]
    return reduce_snailfish(new_total)
        


def main():
    snailfish_numbers = [json.loads(line.strip()) for line in open("day18.txt").readlines()]
    total = snailfish_numbers[0]
    for number in snailfish_numbers[1:]:
        total = [total, number]
        total = reduce_snailfish(total)

    print("part 1", magnitude(total))

    magnitude_pairs = []
    for i in snailfish_numbers:
        for j in snailfish_numbers:
            magnitude_pairs.append(magnitude(reduce_snailfish([i, j])))
    print("part 2", sorted(magnitude_pairs)[-1])
    
if __name__ == "__main__":
    main()
