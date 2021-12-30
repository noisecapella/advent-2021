import numpy as np
from functools import cache

def read_input(filename):
    with open(filename) as f:
        algorithm = ""
        while True:
            line = f.readline()
            if not line.strip():
                break
            algorithm += line.strip()
        grid = np.array([[c == "#" for c in line.strip()] for line in f.readlines()], dtype='bool')
        return algorithm, grid

def calc_pixel(image, x, y, times, depth, algorithm, expand_x, expand_y):

    @cache
    def _calc_pixel(x, y, times, depth, expand_x, expand_y):
        if depth == 0:
            if not (0 <= x < image.shape[0]) or not (0 <= y < image.shape[1]):
                return False
            else:
                return image[x, y]
        
        binary = ''
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                inner_x = x + dx - (times - depth) * (expand_x // 2)
                inner_y = y + dy - (times - depth) * (expand_y // 2)
                bounds_x = image.shape[0] + (times * expand_x)
                bounds_y = image.shape[1] + (times * expand_y)
    
                if not (0 <= inner_x < bounds_x) or not (0 <= inner_y < bounds_y):
                    binary += '0'
                else:
                    value = _calc_pixel(x - (expand_x // 2) + dx, y - (expand_y // 2) + dy, times, depth - 1, expand_x, expand_y)
                    binary += '1' if value else '0'
        return algorithm[int(binary, 2)] == "#"

    return _calc_pixel(x, y, times, depth, expand_x, expand_y)
    
        
    
def enhance(image, algorithm, times):
    extra_x = 4
    extra_y = 4
    new_image = np.zeros(shape=(image.shape[0] + (extra_x * times), image.shape[1] + (extra_y * times)), dtype='bool')
    for x in range(new_image.shape[0]):
        for y in range(new_image.shape[1]):
            new_image[x, y] = calc_pixel(image, x, y, times, times, algorithm, extra_x, extra_y)

    for x in range(new_image.shape[0]):
        new_image[x, 0] = False
        new_image[x, new_image.shape[0] - 1] = False
    for y in range(new_image.shape[1]):
        new_image[0, y] = False
        new_image[new_image.shape[1] - 1, y] = False
    return new_image


def print_grid(image):
    print("".join(["".join([ "#" if c else "." for c in line]) + "\n" for line in image]))
    
def main():
    algorithm, image = read_input("day20.txt")
    #print_grid(image)
    #enhanced_1 = enhance(image, algorithm, 1)
    #print_grid(enhanced_1)
    enhanced_2 = enhance(image, algorithm, 2)
    #print_grid(enhanced_2)
    print("part 1", np.count_nonzero(enhanced_2))
    enhanced_50 = enhance(image, algorithm, 50)
    print("part 2", np.count_nonzero(enhanced_50))

if __name__ == "__main__":
    main()
