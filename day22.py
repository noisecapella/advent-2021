import re
import math

def read_input():
    lines = [line.strip() for line in open("day22.txt").readlines() if line.strip()]
    groups = [
        re.search(r"(on|off) x=([-\d]+)..([-\d]+),y=([-\d]+)..([-\d]+),z=([-\d]+)..([-\d]+)", line).groups()
        for line in lines
    ]
    steps = [(t[0], int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]), int(t[6])) for t in groups]
    return steps

def should_omit_block(order, x1, x2, y1, y2, z1, z2):
    return x1 > x2 or y1 > y2 or z1 > z2 or order == "off"

def _clamp(start, end, s_start, s_end):
    s_start = min(max(start, s_start), end + 1)
    s_end = max(min(end, s_end), start - 1)
    return s_start, s_end

def split_blocks(block, step):
    # cut block to make space for step
    order, x1, x2, y1, y2, z1, z2 = block
    _, s_x1, s_x2, s_y1, s_y2, s_z1, s_z2 = step

    # split old block into 6 blocks surrounding the step
    # some blocks may have zero volume, those will be removed

    s_x1, s_x2 = _clamp(x1, x2, s_x1, s_x2)
    s_y1, s_y2 = _clamp(y1, y2, s_y1, s_y2)
    s_z1, s_z2 = _clamp(z1, z2, s_z1, s_z2)
    
    new_blocks = []
    for nx1, nx2, ny1, ny2, nz1, nz2 in [
            # top and bottom
            (x1, x2, y1, s_y1 - 1, z1, z2),
            (x1, x2, s_y2 + 1, y2, z1, z2),
            
            # left and right
            (x1, s_x1 - 1, s_y1, s_y2, z1, z2),
            (s_x2 + 1, x2, s_y1, s_y2, z1, z2),
            
            # front and back
            (s_x1, s_x2, s_y1, s_y2, z1, s_z1 - 1),
            (s_x1, s_x2, s_y1, s_y2, s_z2 + 1, z2),
    ]:
        new_block = (order, nx1, nx2, ny1, ny2, nz1, nz2)
        if not should_omit_block(*new_block):
            new_blocks.append(new_block)

    #print("old_block", step, block)
    #for new_block in new_blocks:
    #    print("    ", new_block)
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

    for i, step in enumerate(steps):
        print(f"processing {step} {i} out of {len(steps)}")
        blocks = process_step(blocks, step)

    return blocks

def calc_volume(blocks, x1, x2, y1, y2, z1, z2):
    volume = 0
    for block in blocks:
        b_x1, b_x2 = _clamp(block[1], block[2], x1, x2)
        b_y1, b_y2 = _clamp(block[3], block[4], y1, y2)
        b_z1, b_z2 = _clamp(block[5], block[6], z1, z2)
        if block[0] == "on":
            volume += (b_x2 - b_x1 + 1) * (b_y2 - b_y1 + 1) * (b_z2 - b_z1 + 1)
    return volume

def main():
    steps = read_input()
    blocks = process_steps(steps)
    print("part 1", calc_volume(blocks, -50, 50, -50, 50, -50, 50))
    print("part 2", calc_volume(blocks, -math.inf, math.inf, -math.inf, math.inf, -math.inf, math.inf))


if __name__ == "__main__":
    main()
