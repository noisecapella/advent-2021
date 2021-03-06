import math
import json
from collections import defaultdict


def read_instructions():
    return [line.strip().split() for line in open("day24.txt")]

def _iter(a):
    if isinstance(a, int):
        yield a
    else:
        yield from a


def _concat_join(func, a, b, *, predicate=None, short_circuit_after_len=None):
    ret = set()
    
    for a_item in _iter(a):
        for b_item in _iter(b):
            if predicate is not None:
                a_vals = _iter(a_item)
                b_vals = _iter(b_item)
            else:
                a_vals = [a_item]
                b_vals = [b_item]

            for a_val in a_vals:
                for b_val in b_vals:
                    result = func(a_item, b_item)
                    if isinstance(result, set):
                        ret |= result
                    elif isinstance(result, list):
                        for item in result:
                            ret.add(item)
                    else:
                        ret.add(result)

            if short_circuit_after_len is not None and len(ret) >= short_circuit_after_len:
                return ret
    return ret
    

def _neg(a):
    if isinstance(a, int):
        return -a
    if isinstance(a, range):
        return range(-a.start, -a.stop, -a.step)
    return [_neg(x) for x in a]

    
def _add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    
    if not isinstance(a, int) and not isinstance(b, int):
        if isinstance(a, range) and isinstance(b, range):
            if len(a) < len(b):
                smaller = a
                bigger = b
            else:
                smaller = b
                bigger = a
            return [_add(x, bigger) for x in smaller]
        else:
            return _concat_join(_add, a, b)

    if isinstance(a, int):
        int_param = a
        other_param = b
    else:
        other_param = a
        int_param = b

    if int_param == 0:
        return other_param
        
    if isinstance(other_param, range):
        return range(other_param.start + int_param, other_param.stop + int_param, other_param.step)
    
    return [_add(int_param, x) for x in other_param]
    
def _sub(a, b):
    return _add(a, _neg(b))

def _mul(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a * b
    
    if not isinstance(a, int) and not isinstance(b, int):
        return _concat_join(_mul, a, b)

    if isinstance(a, int):
        int_param = a
        other_param = b
    else:
        other_param = a
        int_param = b

    if int_param == 1:
        return other_param
    elif int_param == 0:
        return 0
        
    if isinstance(other_param, range):
        return range(other_param.start * int_param, other_param.stop * int_param, other_param.step * int_param)
    return [_mul(x, int_param) for x in other_param]

def can_divide(a, b):
    return b != 0

def can_mod(a, b):
    return a >= 0 and b > 0

def _div_round_zero(a, b):
    return int(a / b)

def _div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if can_divide(a, b):
            return _div_round_zero(a, b)
        return []

    if isinstance(b, int):
        if b == 1:
            return a
        if isinstance(a, range):
            if a.step % b == 0:
                return range(_div_round_zero(a.start, b), _div_round_zero(a.stop, b), _div_round_zero(a.step, b))
    
    # TODO: maybe range() // b can be optimized?
    return _concat_join(_div, a, b, predicate=can_divide)

def _max(a):
    if a == "all":
        return 2**100
    if isinstance(a, int):
        return a
    elif isinstance(a, range):
        if a.step > 0:
            return a.stop - 1
        else:
            return a.start

    z = None
    for item in a:
        if z is None or _max(z) < _max(item):
            z = item
    
    return _max(z)

def _min(a):
    if a == "all":
        return -2**100
    if isinstance(a, int):
        return a
    elif isinstance(a, range):
        if a.step > 0:
            return a.start
        else:
            return a.stop - 1

    z = None
    for item in a:
        if z is None or _min(z) > _min(item):
            z = item
    
    return z


def _mod(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if can_mod(a, b):
            return a % b
        else:
            return []

    if not isinstance(a, int) and not isinstance(b, int):        
        return _concat_join(_mod, a, b, predicate=can_mod)

    if isinstance(b, int):
        if b <= 0:
            return []
        if isinstance(a, range) and len(a) > 0:
            max_val = _max(a)
            if max_val < b:
                # no need to modulo
                return a
            elif a.step == b:
                if can_mod(a.start, b):
                    return a.start % b
                else:
                    return []

        return [_mod(x, b) for x in a]
    if isinstance(a, int):
        if _max(a) < _min(b):
            return a
    return _concat_join(_mod, a, b, predicate=can_mod)
            


def _eql(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return 1 if a == b else 0

    return _concat_join(_eql, a, b, short_circuit_after_len=2)


def _all():
    return "all"

def _invmul(a, b):
    # ? * b = a
    # ? == a invmul b
    # if b != 0, a // b where a % b == 0
    # if b == 0, a can be anything
    if b == 0:
        return _all()

    s = set()
    for a_item in _iter(a):
        for b_item in _iter(b):
            if _mod(a_item, b_item) == 0:
                result = _div(a_item, b_item)
                if isinstance(result, set):
                    s |= result
                elif isinstance(result, int):
                    s.add(result)
                elif isinstance(result, range):
                    s.add(result)
                else:
                    for item in result:
                        s.add(item)
                    
    return s

def _invdiv(a, b):
    if not isinstance(b, int):
        raise Exception("TODO")
    # ? // b = a
    # ? = a * b, where b != 0
    if b == 0:
        return set()

    #import pdb; pdb.set_trace()
    if isinstance(a, range) and a.step == 1:
        if a.start == 0:
            start = -b + 1
        else:
            start = a.start * b
        stop = a.stop * b
        return range(start, stop)
    elif isinstance(a, int):
        if a == 0:
            return range(-b + 1, b)
        else:
            return range(a*b, (a+1)*b)
    else:
        return {_invdiv(x, b) for x in a}

                     
def _invmod(a, b):
    # ? % b = a
    # ? = a invmod b
    if not isinstance(b, int):
        raise Exception("TODO")

    eval_a = _eval(a)
    if eval_a == set(range(b)):
        return range(2**100)
    return [
        range(a_item, 2**100, b) for a_item in eval_a
    ]


def _inveql(a, b):
    # 1 if (? == b) else 0 = a
    # TODO
    return _all()
    


def _truncate(item, _min, _max):
    if isinstance(item, range):
        return {range(max(item.start, _min), min(item.stop, _max + 1), item.step)}
    elif isinstance(item, int):
        if _min <= item <= _max:
            return {item}
        else:
            return set()
    elif item == "all":
        return range(_min, _max + 1)
    else:
        s = set()
        for x in item:
            s |= _truncate(x, _min, _max)
        return s


def _intersect(a, b):
    if a == "all":
        return b
    elif b == "all":
        return a

    #import pdb; pdb.set_trace()
    if a == set() or b == set():
        return set()

    a_max = _max(a)
    a_min = _min(a)
    b_min = _min(b)
    b_max = _max(b)

    if a == range(2**100) and b_min >= 0:
        return b

    
    ret = set()
    # intersection of a and b
    b_eval = _eval(b)
    for item_a in ([a] if isinstance(a, range) else _iter(a)):
        for item_b in _iter(b_eval):
            # item_b must be a number since it was eval'ed
            if item_a == item_b or (not isinstance(item_a, int) and item_b in item_a):
                ret.add(item_b)
    
    
    return ret
    


def _eval(option):

    ret = set()
    def _eval_inner(a):
        if isinstance(a, int):
            ret.add(a)
        elif isinstance(a, range):
            for i in a:
                ret.add(i)
        elif a == "all":
            raise Exception("can't evaluate all")
        else:
            for x in a:
                _eval_inner(x)
    _eval_inner(option)
    return ret

def _looks_like_range(s):
    if {type(x) for x in s} != {int}:
        return None
    sorted_s = sorted(s)
    if len(sorted_s) == 1:
        return None
    possible_range = range(min(sorted_s), max(sorted_s) + 1)
    if len(possible_range) == len(sorted_s) and list(possible_range) == sorted_s:
        return possible_range

def _add_to_set(s, option):
    if isinstance(option, range):
        s.add(option)
    elif isinstance(option, int):
        s.add(option)
    elif option == "all":
        s.add(option)
    else:
        possible_range = _looks_like_range(option)
        if possible_range:
            s.add(possible_range)
        else:
            for _option in option:
                _add_to_set(s, _option)


def calc_options(instructions, inp_inputs):
    number_index = 0
    valid_options = {var: 0 for var in ("x", "y", "z", "w")}

    for i, instruction in enumerate(instructions):
        #print("instruction", instruction, i)
        if len(instruction) == 3:
            command, arg1, arg2 = instruction

            try:
                arg2 = int(arg2)
                options_args2 = arg2
            except ValueError:
                options_args2 = valid_options[arg2]
            
        else:
            # inp instruction
            command, arg1 = instruction
            arg2 = number_index
            try:
                options_args2 = inp_inputs[number_index]
            except IndexError:
                options_args2 = range(1, 10)
            number_index += 1

        options_args1 = valid_options[arg1]
        new_options = set()

        if i >= 67:
            # import pdb; pdb.set_trace()
            pass
        if command == "inp":
            _add_to_set(new_options, options_args2)
        elif command == "add":
            _add_to_set(new_options, _add(options_args1, options_args2))
        elif command == "sub":
            _add_to_set(new_options, _sub(options_args1, options_args2))
        elif command == "mul":
            _add_to_set(new_options, _mul(options_args1, options_args2))
        elif command == "div":
            _add_to_set(new_options, _div(options_args1, options_args2))
        elif command == "mod":
            _add_to_set(new_options, _mod(options_args1, options_args2))
        elif command == "eql":
            _add_to_set(new_options, _eql(options_args1, options_args2))

        if len(new_options) > 40:
            #import pdb; pdb.set_trace()
            pass

        if len(new_options) == 1:
            new_options = list(new_options)[0]

        #import pdb; pdb.set_trace()
        #print(f"calc i={i} {arg1}={new_options}")
        valid_options[arg1] = new_options
        

        
    return valid_options['z']


def eval_instructions(instructions, number):
    number_index = 0
    variables = {var: 0 for var in ("x", "y", "z", "w")}

    for i, instruction in enumerate(instructions):
        try:
            command, arg1, arg2 = instruction
        except ValueError:
            command, arg1 = instruction
            arg2 = int(number[number_index])
            number_index += 1

        try:
            arg2 = int(arg2)
        except ValueError:
            arg2 = variables[arg2]
        
        if command == "inp":
            variables[arg1] = arg2
        elif command == "add":
            variables[arg1] += arg2
        elif command == "sub":
            variables[arg1] -= arg2
        elif command == "mul":
            variables[arg1] *= arg2
        elif command == "div":
            variables[arg1] = _div_round_zero(variables[arg1], arg2)
        elif command == "mod":
            variables[arg1] %= arg2
        elif command == "eql":
            variables[arg1] = 1 if variables[arg1] == arg2 else 0

        #print(f"eval i={i} {arg1}={variables[arg1]}")
    return variables["z"]

def pprint(x):
    if isinstance(x, list):
        print(json.dumps(x, indent="  "))
    else:
        print(x)

def calc_model_number(instructions, result, highest):
    if len(result) == 14:
        return result
    for inp_idx in range(14):
        r = range(10 - 1, 0, -1) if highest else range(1, 10)
        for n in r:
            inputs = [*result, n]
            options = calc_options(instructions, inputs)
            if options == 0 or _intersect(options, 0) == {0}:
                print("possible match", "".join([str(x) for x in inputs]))
                sub_result = calc_model_number(instructions, inputs, highest=highest)
                if sub_result is not None:
                    return sub_result
        # didn't work, backtrack
        return None


def main():
    instructions = read_instructions()

    print("looking for the highest/lowest inputs...")
    print("part 1", calc_model_number(instructions, [], True))
    print("part 2", calc_model_number(instructions, [], False))
        

if __name__ == "__main__":
    main()
