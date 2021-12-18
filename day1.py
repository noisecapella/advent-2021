import numpy as np

def calc_depth_increases(depths, window_size):
    increases = 0
    for n in range(window_size, depths.shape[0]):
        if depths[n-window_size:n].sum() < depths[n-window_size+1:n+1].sum():
            increases += 1
    return increases

def main():
    depths = np.array([int(line.strip()) for line in open("day1.txt").readlines()])
    print("part 1", calc_depth_increases(depths, 1))
    print("part 2", calc_depth_increases(depths, 3))

if __name__ == "__main__":
    main()
