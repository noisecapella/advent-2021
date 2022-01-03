def read_instructions():
    return [line.strip().split() for line in open("day24.txt")]
    

def process(instructions, numbers):
    input_counter = 0
    storage = {'x':0, 'y':0, 'z':0, 'w': 0}
    for tup in instructions:
        command = tup[0]
        a = tup[1]
        if len(tup) >= 3:
            try:
                b = int(tup[2])
                b_is_var = False
            except:
                b = tup[2]
                b_is_var = True

        if command == "inp":
            storage[a] = int(numbers[input_counter])
            input_counter += 1
        elif command == "add":
            storage[a] += storage[b] if b_is_var else b
        elif command == "mul":
            storage[a] *= storage[b] if b_is_var else b
        elif command == "div":
            storage[a] //= storage[b] if b_is_var else b
        elif command == "mod":
            storage[a] %= storage[b] if b_is_var else b
        elif command == "eql":
            storage[a] = 1 if storage[a] == (storage[b] if b_is_var else b) else 0
    return storage['z']


def process(instructions):
    z = ["z"]
    x = ["x"]
    y = ["y"]
    w = ["w"]

    inputs = [[None] for _ in range(14)]
    
    variables = {"z": z, "y": y, "x": x, "w": w}
    inputs_count = 13
    for i, tup in enumerate(instructions):
        command = tup
        a = tup[1]
        if len(tup) >= 3:
            try:
                b = int(tup[2])
                is_var = False
            except:
                b = tup[2]
                is_var = True

        if command == "add":
            variables[a][0] = ("sub", variables[a], variables[b] if is_var else b)
        elif command == "sub":
            variables[a][0] = ("add", variables[a], variables[b] if is_var else b)
        elif command == "mul":
            if b == 0:
                variables[a][0] = "any"
            else:
                variables[a][0] = ("div", variables[a], variables[b] if is_var else b)
        elif command == "div":
            variables[a][0] = ("mul", variables[a], variables[b] if is_var else b)
        elif command == "mod":
            # a = a % b, b must be greater than a
            variables[a][0] = "any"
        elif command == "inp":
            variables[a][0] = ("inp", inputs[inputs_count])
            inputs_count -= 1
        


def main():
    instructions = read_instructions()
    print(process(instructions, "13579246899999"))

if __name__ == "__main__":
    main()
