import json
from collections import defaultdict

def read_instructions():
    return [line.strip().split() for line in open("day24.txt")]


def _set_times(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a*b
    if isinstance(a, int):
        return {n*a for n in b}
    if isinstance(b, int):
        return {n*b for n in a}

    ret = set()
    for itema in a:
        for itemb in b:
            n = itema * itemb
            ret.add(n)
    return ret

def _set_add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a+b
    if isinstance(a, int):
        if a == 0:
            return b
        else:
            return {n+a for n in b}
    if isinstance(b, int):
        if b == 0:
            return a
        else:
            return {n+b for n in a}

    ret = set()
    for itema in a:
        for itemb in b:
            n = itema + itemb
            ret.add(n)

    return ret

def _set_sub(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a-b
    if isinstance(a, int):
        return {a-n for n in b}
    if isinstance(b, int):
        if b == 0:
            return a
        else:
            return {n-b for n in a}

    ret = set()
    for itema in a:
        for itemb in b:
            n = itema - itemb
            ret.add(n)

    return ret

def _set_div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a // b

    ret = set()
    if isinstance(a, int):
        for n in b:
            if n != 0:
                p = a // n
                ret.add(p)
    
    elif isinstance(b, int):
        if b == 1:
            return a
        for n in a:
            p = n // b
            ret.add(p)

    else:
        for itema in a:
            for itemb in b:
                if itemb == 0:
                    continue
                n = itema // itemb
                ret.add(n)

    return ret

def _set_mod(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a % b
    ret = set()
    if isinstance(a, int):
        if a < 0:
            raise Exception("unexpected")
        for n in b:
            if n > 0:
                p = a % n
                ret.add(p)
    
    elif isinstance(b, int):
        if b == 1:
            return a
        if b <= 0:
            raise Exception("unexpected")
        for n in a:
            if n >= 0:
                p = n % b
                ret.add(p)
    else:
        a_nums = [itema for itema, sources in a if itema >= 0]
        b_nums = [itemb for itemb, sources in b if itemb > 0]
        if max(a_nums) < min(b_nums):
            # no need for modulo
            return a
    
        for itema in a:
            if itema < 0:
                continue
            for itemb in b:
                if itemb <= 0:
                    continue
                p = itema % itemb
                ret.add(p)
    return ret

def _set_eql(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return 1 if a == b else 0
    ret = set()
    if isinstance(a, int):
        for n in b:
            r = 1 if n == a else 0
            ret.add(r)
    elif isinstance(b, int):
        for n in a:
            r = 1 if n == b else 0
            ret.add(r)
    else:
        for itema in a:
            for itemb in b:
                r = 1 if itema == itemb else 0
                ret.add(r)

    if len(ret) == 1:
        return list(ret)[0]
    return ret


def _calc_source(inp_idx, sample):
    return 2**((inp_idx * 9) + (sample - 1))


def calc_options(ast):
    def _calc_options(tup, lookup):
        if id(tup) in lookup:
            return lookup[id(tup)]

        if tup is None:
            ret = (tup, ())
            lookup[id(tup)] = ret
            return ret

        elif isinstance(tup, int):
            ret = tup
            lookup[id(tup)] = ret
            return ret

        a_options_tup = _calc_options(tup[1], lookup)
        b_options_tup = _calc_options(tup[2], lookup)
        a_options = a_options_tup if isinstance(a_options_tup, int) else a_options_tup[1]
        b_options = b_options_tup if isinstance(b_options_tup, int) else b_options_tup[1]
        a_options_values = {a_options} if isinstance(a_options, int) else a_options
        b_options_values = {b_options} if isinstance(b_options, int) else b_options

        if id(tup) in lookup:
            return lookup[id(tup)]

        command = tup[0]
        new_tup = (command, a_options_tup, b_options_tup)
        if command == "inp":
            inp_idx = tup[1]
            ret = (new_tup, {sample for sample in range(1, 10)})
        elif command == "mul":
            if a_options_values == {1}:
                ret = b_options_tup
            elif b_options_values == {1}:
                ret = a_options_tup
            else:
                ret = (new_tup, _set_times(a_options, b_options))
        elif command == "add":
            if a_options_values == {0}:
                ret = b_options_tup
            elif b_options_values == {0}:
                ret = a_options_tup
            else:
                ret = (new_tup, _set_add(a_options, b_options))
        elif command == "sub":
            if b_options_values == {0}:
                ret = a_options_tup
            else:
                ret = (new_tup, _set_sub(a_options, b_options))
        elif command == "div":
            if b_options_values == {1}:
                ret = a_options_tup
            else:
                ret = (new_tup, _set_div(a_options, b_options))
        elif command == "mod":
            ret = (new_tup, _set_mod(a_options, b_options))
        elif command == "eql":
            ret = (new_tup, _set_eql(a_options, b_options))

        ret_options_values = {ret} if isinstance(ret, int) else ({ret[1]} if isinstance(ret[1], int) else ret[1])
        #import pdb; pdb.set_trace()
        if ret_options_values == a_options_values:
            ret = a_options_tup
        elif ret_options_values == b_options_values:
            ret = b_options_tup

        if len(ret_options_values) == 1:
            ret = list(ret_options_values)[0]
        lookup[id(tup)] = ret
        return ret
            
    return _calc_options(ast, {})


def find_options(ast_with_options):
    lookup = {}
    #valid_options = {}  # idx to list of options

    def _find_options(tup, allowed_options):
        if not isinstance(tup, tuple):
            return

        a_options = tup[0][1][1] if isinstance(tup[0][1], tuple) else {tup[0][1]}
        b_options = tup[0][2][1] if isinstance(tup[0][2], tuple) else {tup[0][2]}
        allowed_a_options = set()
        allowed_b_options = set()
        command = tup[0][0]

        if command == "inp":
            #import pdb; pdb.set_trace()
            print(tup[0][1], allowed_options)
            yield tup[0][1], allowed_options
            return

        for option in allowed_options:
            if option not in tup[1]:
                continue

            if command == "add":
                # a + b = option
                # a = option - b
                # b = option - a

                for a_option in a_options:
                    for b_option in b_options:
                        if a_option + b_option == option:
                            allowed_a_options.add(a_option)
                            allowed_b_options.add(b_option)
                
            elif command == "sub":
                # a - b = option
                # a = option + b
                # b = a - option
                for a_option in a_options:
                    for b_option in b_options:
                        if a_option - b_option == option:
                            allowed_a_options.add(a_option)
                            allowed_b_options.add(b_option)


            elif command == "mul":
                # a * b = option
                # a = option // b
                # b = option // a
                for a_option in a_options:
                    for b_option in b_options:
                        if a_option * b_option == option:
                            allowed_a_options.add(a_option)
                            allowed_b_options.add(b_option)
            elif command  == "div":
                # a // b = option
                # a = option * b
                # b = a // option
                for a_option in a_options:
                    for b_option in b_options:
                        if b_option != 0 and a_option // b_option == option:
                            allowed_a_options.add(a_option)
                            allowed_b_options.add(b_option)
                
            elif command == "mod":
                # a % b = option
                # a is any positive number or 0
                # b is any positive number
                for a_option in a_options:
                    for b_option in b_options:
                        if a_option >= 0 and b_option > 0 and a_option % b_option == option:
                            allowed_a_options.add(a_option)
                            allowed_b_options.add(b_option)
                
            elif command == "eql":
                # option = 1 if a == b else 0
                for a_option in a_options:
                    for b_option in b_options:
                        if (1 if a_option == b_option else 0) == option:
                            allowed_a_options.add(a_option)
                            allowed_b_options.add(b_option)

        import pdb; pdb.set_trace()
        if len(allowed_a_options) > 0 and len(allowed_b_options) > 0:
            if isinstance(tup[0][1], tuple):
                yield from _find_options(tup[0][1], allowed_a_options)
            if isinstance(tup[0][2], tuple):
                yield from _find_options(tup[0][2], allowed_b_options)

    yield from _find_options(ast_with_options, {0})
    
    


def find_inps(ast_with_options):
    id_lookup = set()
    def _find_inps(tup, path):
        if not isinstance(tup, tuple) or id(tup[0]) in id_lookup:
            return

        id_lookup.add(id(tup[0]))

        if isinstance(tup[0], tuple):
            if tup[0][0] == "inp":
                yield tup, path

            yield from _find_inps(tup[0][1], [*path, 0])
            yield from _find_inps(tup[0][2], [*path, 1])
    return _find_inps(ast_with_options, [])



def calc_max_inputs(inps, ast_with_options):
    def _calc_root_options(inp_node, path, current_options):
        if len(path) == 0:
            return current_options

        parent_inp_node = ast_with_options
        for index in path[:-1]:
            parent_inp_node = parent_inp_node[0][index + 1]

        child_index = path[-1]
        command = parent_inp_node[0][0]
        options = [
            (_options(parent_inp_node[0][idx + 1]) if idx != child_index else current_options) for idx in range(2)
        ]
        if command == "inp":
            raise Exception("unexpected")
        elif command == "mul":
            parent_options = _set_times(*options)
        elif command == "add":
            parent_options = _set_add(*options)
        elif command == "sub":
            parent_options = _set_sub(*options)
        elif command == "div":
            parent_options = _set_div(*options)
        elif command == "mod":
            parent_options = _set_mod(*options)
        elif command == "eql":
            parent_options = _set_eql(*options)

        return _calc_root_options(parent_inp_node, path[:-1], parent_options)

    zeros = []
    for inp_idx in range(13, -1, -1):
        inp, path = inps[inp_idx]
        if inp[0][1] != inp_idx:
            continue
        for sample in (9, 8, 7, 6, 5, 4, 3, 2, 1):
            option = _calc_root_options(inps, path, (sample,))
            if 0 in option:
                print(inp_idx, sample)
                zeros.append((inp_idx, sample))

    import pdb; pdb.set_trace()
        
    

def make_ast(instructions):
    ast = {"x": 0, "y": 0, "z": 0, "w": 0}
    input_counter = 0
    
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
            ast[a] = ("inp", input_counter, None)
            input_counter += 1
        elif command == "mul":
            if b == 0:
                ast[a] = 0
            elif b == 1:
                pass
            elif ast[a] == 1:
                ast[a] = ast[b] if b_is_var else b
            elif b_is_var:
                if ast[b] == 1:
                    pass
                else:
                    ast[a] = ("mul", ast[a], ast[b])
            else:
                ast[a] = ("mul", ast[a], b)

        elif command == "div":
            if b_is_var:
                ast[a] = ("div", ast[a], ast[b])
            elif b == 1:
                pass
            elif ast[a] == 1:
                ast[a] = ast[b] if b_is_var else b
            else:
                ast[a] = ("div", ast[a], b)
        elif command == "add":
            if b == 0:
                pass
            elif ast[a] == 0:
                ast[a] = ast[b] if b_is_var else b
            elif b_is_var:
                if ast[b] == 0:
                    pass
                else:
                    ast[a] = ("add", ast[a], ast[b])
            else:
                ast[a] = ("add", ast[a], b)
        elif command == "sub":
            if b == 0:
                pass
            elif ast[a] == 0:
                ast[a] = ast[b] if b_is_var else b
            elif b_is_var:
                ast[a] = ("sub", ast[a], ast[b])
            else:
                ast[a] = ("sub", ast[a], b)
        elif command == "mod":
            if b == 0:
                pass
            elif b_is_var:
                ast[a] = ("mod", ast[a], ast[b])
            else:
                ast[a] = ("mod", ast[a], b)
        elif command == "eql":                
            if b_is_var:
                ast[a] = ("eql", ast[a], ast[b])
            else:
                if isinstance(ast[a], int):
                    ast[a] = 1 if b == ast[a] else 0
                else:
                    ast[a] = ("eql", ast[a], b)
                

        #if len(_options(ast[a])) == 1:
        #    ast[a] = list(_options(ast[a]))[0]
                
    return ast



def pprint(x):
    if isinstance(x, list):
        print(json.dumps(x, indent="  "))
    else:
        print(x)

def main():
    instructions = read_instructions()
    print("calculating ast...")
    ast = make_ast(instructions)
    print("calculating ast_with_options...")
    ast_with_options = calc_options(ast["z"])
    print("looking for the highest inputs...")
    inps = list(find_inps(ast_with_options))
    x = list(find_options(ast_with_options))
    import pdb; pdb.set_trace()

    #print(eval_ast(ast["z"], "1" * 14))
    #print(eval_ast(ast["z"], "2" * 14))

if __name__ == "__main__":
    main()
