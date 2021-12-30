from collections import Counter
import numpy as np

def sin_cos_q(quarter):
    if quarter == 0:
        sin_q = 0
        cos_q = 1
    elif quarter == 1:
        sin_q = 1
        cos_q = 0
    elif quarter == 2:
        sin_q = 0
        cos_q = -1
    elif quarter == 3:
        sin_q = -1
        cos_q = 0
    return sin_q, cos_q


def rx(quarter):
    sin_q, cos_q = sin_cos_q(quarter)
    return np.array([[1, 0, 0],
                   [0, cos_q, -sin_q],
                   [0, sin_q, cos_q]])

def ry(quarter):
    sin_q, cos_q = sin_cos_q(quarter)
    return np.array([[cos_q, 0, sin_q],
                   [0, 1, 0],
                   [-sin_q, 0, cos_q]])

def rz(quarter):
    sin_q, cos_q = sin_cos_q(quarter)
    return np.array([[cos_q, -sin_q, 0],
                   [sin_q, cos_q, 0],
                   [0, 0, 1]])


def make_matrices():
    transform_matrices = []
    neg_vecs = []
    for x_pos in range(3):
        for y_pos in range(3):
            if x_pos == y_pos:
                continue
            for z_pos in range(3):
                if z_pos == x_pos or z_pos == y_pos:
                    continue
                for x_neg in (-1, 1):
                    for y_neg in (-1, 1):
                        for z_neg in (-1, 1):
                            mat = np.zeros(shape=(3,3))
                            mat[0, x_pos] = x_neg
                            mat[1, y_pos] = y_neg
                            mat[2, z_pos] = z_neg
                            transform_matrices.append(mat)

                            neg_vec = np.zeros(shape=(3,))
                            neg_vec[x_pos] = x_neg
                            neg_vec[y_pos] = y_neg
                            neg_vec[z_pos] = z_neg
                            neg_vecs.append(neg_vec)
                            
    return transform_matrices, neg_vecs

TRANSFORM_LOOKUP, NEG_VECS = make_matrices()


def transform(vecs, transformation_number):
    # TODO: optimize

    vecs_t = np.transpose(vecs)
    result = np.matmul(TRANSFORM_LOOKUP[transformation_number], vecs_t)
    result = np.transpose(result)
    return result


def pick_diff(a, b):
    # pick a value for diff which causes b - diff == a to have at least 12 matches
    # (b - diff) - a should have a minimal value
    a_set = {tuple(z) for z in a}
    for coord_a in a:
        for coord_b in b:
            diff = coord_b - coord_a
            b_set = {tuple(z)  for z in b - diff}
            overlap = a_set.intersection(b_set)
            overlap_count = len(overlap)
            if overlap_count >= 12:
                return diff
                
    return None


def intersects(a, b, a_transformation_number):

    for transformation_number in range(len(TRANSFORM_LOOKUP)):
        adjusted_b = transform(b, transformation_number)
        diff = pick_diff(a, adjusted_b)
        if diff is not None:
            return diff, transformation_number


def mul(args):
    x = 1
    for arg in args:
        x *= arg
    return x
    
def calc_beacons(reports):
    locations = {0: np.array([0, 0, 0]) }
    transformation_numbers = {0: len(NEG_VECS) - 1}
    beacons = set()

    while len(locations) < len(reports):
        print("locations", locations)
        for i, report in enumerate(reports):
            if i in locations:
                continue

            known_location_indices = list(locations.keys())
            for known_location_index in known_location_indices:
                if i in locations:
                    break

                result = intersects(reports[known_location_index], reports[i], known_location_index)
                if result is not None:
                    location_coord, transformation_number = result
                    transformation_numbers[i] = transformation_number
                    locations[i] = -(location_coord * NEG_VECS[transformation_numbers[known_location_index]]) + locations[known_location_index]
                    print(f"found location {i} {known_location_index} {location_coord} {locations[known_location_index]}")
                    
    for location in sorted(list(locations.items())):
        print(location)
    return locations

def load_reports():
    lines = [line.strip() for line in open("day19_medium.txt").readlines()]
    reports = []
    latest_report = []
    for line in lines:
        if not line:
            reports.append(np.array(latest_report))
            latest_report = []
        else:
            if not line.startswith("---"):
                coords = np.array([int(coord) for coord in line.split(",")])
                latest_report.append(coords)

    reports.append(np.array(latest_report))
    latest_report = None
    return reports


def main():
    reports = load_reports()

    #print(intersects(reports[0], reports[1]))
    #print(intersects(reports[1], reports[4]))
    print("part 1", len(calc_beacons(reports)))
    


if __name__ == "__main__":
    main()
