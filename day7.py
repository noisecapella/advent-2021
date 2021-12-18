import numpy as np

lookup = {}

def s(x):
    if x in lookup:
        return lookup[x]
    z = 0
    for n in range(1, x + 1):
        z += n
    lookup[x] = z
    return z

def main():
    line = open("day7.txt").readline().strip()
    nums = [int(z) for z in line.split(",")]
    inc = np.arange(np.min(nums), np.max(nums))
    diffs = np.array([np.abs(nums - n).sum() for n in inc])
    print("part 1", diffs[diffs.argmin()])
    sums = np.array([np.vectorize(s)(np.abs(nums - n)).sum() for n in inc])
    print("part 2", sums[sums.argmin()])

if __name__ == "__main__":
    main()
