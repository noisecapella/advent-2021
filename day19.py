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

    return transform_matrices

TRANSFORM_LOOKUP = make_matrices()


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


def intersects(a, b):

    for transformation_number in range(len(TRANSFORM_LOOKUP)):
        adjusted_b = transform(b, transformation_number)
        diff = pick_diff(a, adjusted_b)
        if diff is not None:
            return diff, transformation_number


def calc_beacons(reports):
    locations = {0: np.array([0, 0, 0]) }
    transformation_numbers = {}
    prev = {}
    beacons = set()

    while len(locations) < len(reports):
        for i, report in enumerate(reports):
            if i in locations:
                continue

            known_location_indices = list(locations.keys())
            for known_location_index in known_location_indices:
                if i in locations:
                    break

                result = intersects(reports[known_location_index], reports[i])
                if result is not None:
                    diff, transformation_number = result
                    transformation_numbers[i] = transformation_number
                    prev[i] = known_location_index
                    prev_index = known_location_index
                    while True:
                        if prev_index != 0:
                            diff = transform(diff, transformation_numbers[prev_index])
                        else:
                            break
                        prev_index = prev[prev_index]
                    locations[i] = -diff + locations[known_location_index]
                    print(f"found location {i} {locations[i]}")


    for i, report in enumerate(reports):
        prev_index = i
        while True:
            if prev_index != 0:
                report = transform(report, transformation_numbers[prev_index])
            else:
                break
            prev_index = prev[prev_index]
        report = report + locations[i]
        for coord in report:
            beacons.add(tuple(coord))

    #import pdb; pdb.set_trace()
    return len(beacons)

def load_reports():
    lines = [line.strip() for line in open("day19.txt").readlines()]
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
    print("part 1", calc_beacons(reports))
    


if __name__ == "__main__":
    main()
