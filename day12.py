def find_paths(connections, current, path, *, visited_twice):
    for node in [z[1] for z in connections if z[0] == current]:
        if node == "end":
            yield path + [node]
        elif node == "start":
            pass
        elif node.lower() == node:
            if node not in path or visited_twice is False:
                _visited_twice = visited_twice
                if node in path:
                    _visited_twice = True
                yield from find_paths(connections, node, path + [node], visited_twice=_visited_twice)
        elif node.upper() == node:
            yield from find_paths(connections, node, path + [node], visited_twice=visited_twice)

def main():
    lines = [line.strip() for line in open("day12.txt").readlines()]
    connections = [line.split("-") for line in lines]
    connections = [*connections, *[[z[1], z[0]] for z in connections]]
    print("part 1", len(list(find_paths(connections, "start", ["start"], visited_twice=True))))
    print("part 2", len(list(find_paths(connections, "start", ["start"], visited_twice=False))))

if __name__ == "__main__":
    main()
