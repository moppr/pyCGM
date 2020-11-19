import numpy as np


class CGM:

    def __init__(self):
        self.all_angles = None
        self.all_axes = None
        # Default marker mapping probably has to be determined when c3d is loaded (this is placeholder)
        self.mapping = {"PELV": 0, "RHIP": 1, "LHIP": 2, "RKNE": 3, "LKNE": 4}
        # load(input_path)
        # after loading, figure out default marker mapping

    def run(self):
        data = np.array([[[0, 1, 2], [10, 10, 10], [8, 8, 8], [5, 5, 5], [5, 5, 5]],
                         [[3, 4, 5], [9, 9, 9], [7, 7, 7], [4, 4, 4], [4, 4, 4]],
                         [[6, 7, 8], [8, 8, 8], [6, 6, 6], [3, 3, 3], [3, 3, 3]],
                         [[5, 6, 7], [8, 8, 8], [4, 4, 4], [2, 2, 2], [2, 2, 2]],
                         [[4, 5, 6], [8, 8, 8], [2, 2, 2], [0, 0, 0], [0, 0, 0]]])
        result = calc(data, (self.pelvis_calc, self.hip_calc, self.knee_calc), self.mapping)
        self.all_angles = result

    def rename(self, old, new):
        # Intentionally don't pop old, default code may reference old name
        # This would actually be mapping[old] = mapping[new] if default was
        # determined from the c3d input file
        self.mapping[new] = self.mapping[old]

    @property
    def pelvis_angles(self):
        return self.all_angles[0:, 0]

    @property
    def hip_angles(self):
        return self.all_angles[0:, 1]

    @property
    def knee_angles(self):
        return self.all_angles[0:, 2]

    @staticmethod
    def pelvis_calc(frame, mapping):
        return frame[mapping["PELV"]]

    @staticmethod
    def hip_calc(frame, mapping):
        return np.mean(np.array([frame[mapping["RHIP"]], frame[mapping["LHIP"]]]), axis=0)

    @staticmethod
    def knee_calc(frame, mapping):
        return frame[mapping["RKNE"]] - frame[mapping["LKNE"]]


def calc(data, methods, mapping):
    pel, hip, kne = methods
    result = np.zeros((5, 3, 3), dtype=int)
    for i, frame in enumerate(data):
        result[i][0] = pel(frame, mapping)
        result[i][1] = hip(frame, mapping)
        result[i][2] = kne(frame, mapping)
    return result
