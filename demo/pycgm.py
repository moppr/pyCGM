import numpy as np
from demo.IO import trials


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
        data, markers = trials[trial]  # Substitute for loading in data from c3d

        # Associate each marker name with its index
        for i, marker in enumerate(markers):
            self.marker_index[marker] = i

        result = calc(data, (self.pelvis_calc, self.hip_calc, self.knee_calc), self.mapping, self.marker_index)
        self.all_angles = result

    def map(self, old=None, new=None, dic=None):
        if dic and type(dic) == dict:  # Entire dictionary given
            self.mapping.update(dic)
            return
        if old and new:  # Old and new marker name provided
            self.mapping[old] = new
            self.mapping[new] = new
        elif old and not new:  # Only one marker name provided
            self.mapping[old] = old  # Interpret it as adding a new marker

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
    result = np.zeros((len(data), len(mi), 3), dtype=int)
    for i, frame in enumerate(data):
        result[i][0] = pel(frame, mapping, mi)
        result[i][1] = hip(frame, mapping, mi)
        result[i][2] = kne(frame, mapping, mi)
    return result
