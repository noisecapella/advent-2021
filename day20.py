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

def calc_pixels(image, times, algorithm):
    inc_x = 1
    inc_y = 1

    new_image = np.zeros(shape=(image.shape[0] + (times * 2 * inc_x), image.shape[1] + (times * 2 * inc_y)), dtype='bool')

    @cache
    def _calc_pixel(x, y, depth):
        if depth == 0:
            inner_x = x - times*inc_x
            inner_y = y - times*inc_y
            if 0 <= inner_x < image.shape[0] and 0 <= inner_y < image.shape[1]:
                return image[inner_x, inner_y]
            else:
                return False
                
        
        binary = ''
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                inner_x = x + dx
                inner_y = y + dy
    
                value = _calc_pixel(inner_x, inner_y, depth - 1)
                binary += '1' if value else '0'
        return algorithm[int(binary, 2)] == "#"

    for _x in range(new_image.shape[0]):
        for _y in range(new_image.shape[1]):
            new_image[_x, _y] = _calc_pixel(_x, _y, times)

    return new_image
        
    
def enhance(image, algorithm, times):
    return calc_pixels(image, times, algorithm)


def make_grid(image):
    return "".join(["".join([ "#" if c else "." for c in line]) + "\n" for line in image])

def print_grid(image):
    print(make_grid(image))


def main():
    algorithm, image = read_input("day20.txt")

    #print_grid(image)
    #enhanced_1 = enhance(image, algorithm, 1)
    #print_grid(enhanced_1)

    enhanced_2 = enhance(image, algorithm, 2)
    print_grid(enhanced_2)
    print("part 1", np.count_nonzero(enhanced_2))
    enhanced_50 = enhance(image, algorithm, 50)
    print_grid(enhanced_50)
    print("part 2", np.count_nonzero(enhanced_50))

if __name__ == "__main__":
    main()
