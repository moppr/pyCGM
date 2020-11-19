import numpy as np
from demo.IO import *


class CGM:

    def __init__(self):
        self.all_angles = None
        self.all_axes = None
        # Default marker mapping probably has to be determined when c3d is loaded (this is placeholder)
        self.mapping = {"PELV": "PELV", "RHIP": "RHIP", "LHIP": "LHIP", "RKNE": "RKNE", "LKNE": "LKNE"}
        self.marker_index = {}
        self.output_index = {"PELVIS": 0, "HIP": 1, "KNEE": 2}
        # load(input_path)
        # after loading, figure out default marker mapping

    def run(self, trial):
        data, markers = trials[trial]
        for i, marker in enumerate(markers):
            self.marker_index[marker] = i

        result = calc(data, (self.pelvis_calc, self.hip_calc, self.knee_calc), self.mapping, self.marker_index)
        self.all_angles = result

    def map(self, old, new):
        self.mapping[old] = new
        self.mapping[new] = new

    @property
    def pelvis_angles(self):
        return self.all_angles[0:, self.output_index["PELVIS"]]

    @property
    def hip_angles(self):
        return self.all_angles[0:, self.output_index["HIP"]]

    @property
    def knee_angles(self):
        return self.all_angles[0:, self.output_index["KNEE"]]

    @staticmethod
    def pelvis_calc(frame, mapping, mi):
        return frame[mi[mapping["PELV"]]]

    @staticmethod
    def hip_calc(frame, mapping, mi):
        return np.mean(np.array([frame[mi[mapping["RHIP"]]], frame[mi[mapping["LHIP"]]]]), axis=0)

    @staticmethod
    def knee_calc(frame, mapping, mi):
        return frame[mi[mapping["RKNE"]]] - frame[mi[mapping["LKNE"]]]


def calc(data, methods, mapping, mi):
    pel, hip, kne = methods
    result = np.zeros((5, len(mi), 3), dtype=int)
    for i, frame in enumerate(data):
        result[i][0] = pel(frame, mapping, mi)
        result[i][1] = hip(frame, mapping, mi)
        result[i][2] = kne(frame, mapping, mi)
    return result
