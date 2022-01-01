import re

def read_input():
    lines = [line.strip() for line in open("day22_small.txt").readlines() if line.strip()]
    groups = [
        re.search(r"(on|off) x=([-\d]+)..([-\d]+),y=([-\d]+)..([-\d]+),z=([-\d]+)..([-\d]+)", line).groups()
        for line in lines
    ]
    steps = [(t[0], int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]), int(t[6])) for t in groups]
    return steps

def should_omit_block(order, x1, x2, y1, y2, z1, z2):
    return x1 > x2 or y1 > y2 or z1 > z2 or order == "off"

def split_blocks(block, step):
    # cut block to make space for step
    order, x1, x2, y1, y2, z1, z2 = block
    _, s_x1, s_x2, s_y1, s_y2, s_z1, s_z2 = step

    # split old block into 27 - 1 blocks, surrounding the step
    # some blocks may have zero volume, those will be removed

    def _clamp_coords(start, end, s_start, s_end):
        s_start = min(max(start, s_start), end + 1)
        s_end = max(min(end, s_end), start - 1)
        ret = [
            (start, s_start - 1, -1),
            (s_start, s_end, 0),
            (s_end + 1, end, 1)
        ]
        return [tup for tup in ret if tup[0] <= tup[1]]
    
    new_blocks = []
    for nx1, nx2, nxindex in _clamp_coords(x1, x2, s_x1, s_x2):
        for ny1, ny2, nyindex in _clamp_coords(y1, y2, s_y1, s_y2):
            for nz1, nz2, nzindex in _clamp_coords(z1, z2, s_z1, s_z2):
                if nxindex == 0 and nyindex == 0 and nzindex == 0:
                    # skip center block, leave space for step
                    continue
                new_block = (order, nx1, nx2, ny1, ny2, nz1, nz2)
                if not should_omit_block(*new_block):
                    new_blocks.append(new_block)

    return new_blocks
    
    
    
def process_step(blocks, step):
    updated_blocks = []
    for block in blocks:
        subblocks = split_blocks(block, step)
        for subblock in subblocks:
            updated_blocks.append(subblock)

    if step[0] == "on":
        updated_blocks.append(step)
    return updated_blocks

def process_steps(steps):
    blocks = []

    for step in steps:
        print("processing", step)
        blocks = process_step(blocks, step)

    return blocks

def calc_volume(blocks, x1, x2, y1, y2, z1, z2):
    volume = 0
    for block in blocks:
        b_x1 = max(x1, block[1])
        b_x2 = min(x2, block[2])
        b_y1 = max(y1, block[3])
        b_y2 = min(y2, block[4])
        b_z1 = max(z1, block[5])
        b_z2 = min(z2, block[6])
        if block[0] == "on":
            volume += (b_x2 - b_x1 + 1) * (b_y2 - b_y1 + 1) * (b_z2 - b_z1 + 1)
    return volume

def main():
    steps = read_input()
    blocks = process_steps(steps)
    print("part 1", calc_volume(blocks, -50, 50, -50, 50, -50, 50))


if __name__ == "__main__":
    main()
