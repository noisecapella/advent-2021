def _calc(numbers, type_id):
    if type_id == 0:
        return sum(numbers)
    elif type_id == 1:
        ret = 1
        for number in numbers:
           ret *= number
        return ret
    elif type_id == 2:
        return min(numbers)
    elif type_id == 3:
        return max(numbers)
    elif type_id == 5:
        return 1 if numbers[0] > numbers[1] else 0
    elif type_id == 6:
        return 1 if numbers[0] < numbers[1] else 0
    elif type_id == 7:
        return 1 if numbers[0] == numbers[1] else 0

def parse_packet(l):
    n = int(l, 16)
    b = bin(n)[2:]
    remainder = 4 - (len(b) % 4)
    if remainder < 4:
        b = ("0" * remainder) + b
    return _parse_packet(b)

def _parse_packet(b, indent=""):
    print(f"b {b}")
    version = int(b[:3], 2)
    version_sum = version
    print(f"{indent}version {version}")

    type_id = int(b[3:6], 2)
    print(f"{indent}type id {type_id}")
    if type_id == 4:
        #number packet
        number_bits = []
        pointer = 6
        while True:

            number_bits.extend(b[pointer+1:pointer+5])
            if b[pointer] == "0":
                break
            pointer += 5
        number = int("".join(number_bits), 2)
        print(f"{indent}number {number}")
        return pointer + 5, version_sum, number
    else:
        length_type_id = int(b[6], 2)
        print(f"{indent}length type id = {length_type_id}")
        if length_type_id == 0:
            subpacket_len = int(b[7:7+15], 2)
            print(f"{indent}{b[7:7+15]}  {subpacket_len}")
            pointer = 7+15
            numbers = []
            while subpacket_len:
                count, sub_packet_version, number = _parse_packet(b[pointer:], indent + "  ")
                version_sum += sub_packet_version
                pointer += count
                subpacket_len -= count
                numbers.append(number)
            return pointer, version_sum, _calc(numbers, type_id)
        elif length_type_id == 1:
            num_subpackets = int(b[7:7+11], 2)
            print(f"{indent}num_subpackets {num_subpackets} {b[7:]}")
            pointer = 7+11
            numbers = []
            for n in range(num_subpackets):
                count, sub_packet_version, number = _parse_packet(b[pointer:], indent + "  ")
                version_sum += sub_packet_version
                pointer += count
                numbers.append(number)
            return pointer, version_sum, _calc(numbers, type_id)




def main():
    pointer, version_sum, calc_result = parse_packet(open("day16.txt").readline().strip())
    print("part 1", version_sum)
    print("part 2", calc_result)
    

if __name__ == "__main__":
    main()
