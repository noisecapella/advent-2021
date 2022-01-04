import json

def read_instructions():
    return [line.strip().split() for line in open("day24.txt")]


def calc_options(ast):
    def _set_times(a, b):
        ret = set()
        if isinstance(a, int):
            a = (a,)
        if isinstance(b, int):
            b = (b,)
        for itema in a:
            for itemb in b:
                ret.add(itema * itemb)
        return tuple(ret)
    
    def _set_add(a, b):
        ret = set()
        if isinstance(a, int):
            a = (a,)
        if isinstance(b, int):
            b = (b,)
        for itema in a:
            for itemb in b:
                ret.add(itema + itemb)
        return tuple(ret)

    def _set_sub(a, b):
        ret = set()
        if isinstance(a, int):
            a = (a,)
        if isinstance(b, int):
            b = (b,)
        for itema in a:
            for itemb in b:
                ret.add(itema - itemb)
        return tuple(ret)

    def _set_div(a, b):
        ret = set()
        if isinstance(a, int):
            a = (a,)
        if isinstance(b, int):
            b = (b,)

        for itema in a:
            for itemb in b:
                if itemb == 0:
                    continue
                ret.add(itema // itemb)
        return tuple(ret)

    def _set_mod(a, b):
        ret = set()
        if isinstance(a, int):
            a = (a,)
        if isinstance(b, int):
            b = (b,)
        for itema in a:
            for itemb in b:
                if itemb == 0:
                    continue
                ret.add(itema % itemb)
        return tuple(ret)

    def _set_eql(a, b):
        ret = set()
        if isinstance(a, int) and isinstance(b, int):
            return (1,) if a == b else (0,)
        return (0, 1)

    def _calc_options(tup, lookup):
        if id(tup) in lookup:
            return lookup[id(tup)]

        if not isinstance(tup, tuple):
            if tup is None:
                ret = (tup, ())
            else:
                ret = (tup, (tup,))
            lookup[id(tup)] = ret
            return ret

        a_options_tup = _calc_options(tup[1], lookup)
        b_options_tup = _calc_options(tup[2], lookup)

        if id(tup) in lookup:
            return lookup[id(tup)]

        options = [a_options_tup[1], b_options_tup[1]]

        command = tup[0]
        new_tup = (command, a_options_tup, b_options_tup)
        if command == "inp":
            ret = (new_tup, (1,2,3,4,5,6,7,8,9))
        elif command == "mul":
            ret = (new_tup, _set_times(*options))
        elif command == "add":
            ret = (new_tup, _set_add(*options))
        elif command == "sub":
            ret = (new_tup, _set_sub(*options))
        elif command == "div":
            ret = (new_tup, _set_div(*options))
        elif command == "mod":
            ret = (new_tup, _set_mod(*options))
        elif command == "eql":
            ret = (new_tup, _set_eql(*options))


        if len(ret[1]) == 1:
            ret = (ret[1][0], ret[1])
        lookup[id(tup)] = ret
        return ret
            
    return _calc_options(ast, {})
    
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


def find_inp(tup, depth, id_lookup):
    if not isinstance(tup, list) or id(tup[0]) in id_lookup:
        return

    id_lookup.add(id(tup[0]))
    if isinstance(tup, int):
        return

    if tup is None:
        return

    if tup[0] == "inp":
        import pdb; pdb.set_trace()
        yield tup, depth

    yield from find_inp(tup[1], depth + 1, id_lookup)
    yield from find_inp(tup[2], depth + 1, id_lookup)


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

    import pdb; pdb.set_trace()
    for inp in find_inp(ast_with_options, 0, set()):
        ...

    #print(eval_ast(ast["z"], "1" * 14))
    #print(eval_ast(ast["z"], "2" * 14))

if __name__ == "__main__":
    main()
