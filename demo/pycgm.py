import numpy as np
from demo.IO import trials


class CGM:

    def __init__(self, static_path=None, dynamic_path=None, vsk_path=None, trial=0):
        self.static_path = static_path
        self.dynamic_path = dynamic_path
        self.vsk_path = vsk_path
        self.trial = trial
        self.all_angles = None
        self.all_axes = None
        self.offsets = None
        self.mapping = {"PELV": "PELV", "RHIP": "RHIP", "LHIP": "LHIP", "RKNE": "RKNE", "LKNE": "LKNE"}
        self.marker_index = {}
        self.output_index = {"Pelvis": 0, "Hip": 1, "Knee": 2}

    def run(self):
        data, markers = trials[self.trial]  # Substitute for loading in data from c3d

        # Associate each marker name with its index
        for i, marker in enumerate(markers):
            self.marker_index[marker] = i

        # Static trial goes here
        static = StaticCGM(self.static_path, self.vsk_path)
        self.offsets = static.offsets

        result = calc(data,
                      (self.pelvis_calc, self.hip_calc, self.knee_calc),
                      (self.mapping, self.marker_index, self.output_index))
        self.all_angles = result

    def map(self, old=None, new=None, dic=None):
        if dic and type(dic) == dict:  # Entire dictionary given
            self.mapping.update(dic)
            return
        # TODO: Potential issue if 'new' is an existing marker that CGM expects, unless all
        # instances that use it are overridden
        if old and new:  # Old and new marker name provided
            self.mapping[old] = new
            self.mapping[new] = new
        elif old and not new:  # Only one marker name provided
            self.mapping[old] = old  # Interpret it as adding a new marker

    @property
    def pelvis_angles(self):
        return self.all_angles[0:, self.output_index["Pelvis"]]

    @property
    def hip_angles(self):
        return self.all_angles[0:, self.output_index["Hip"]]

    @property
    def knee_angles(self):
        return self.all_angles[0:, self.output_index["Knee"]]

    @staticmethod
    def pelvis_calc(frame, mapping, mi, i, oi, result):
        result[i][oi["Pelvis"]] = frame[mi[mapping["PELV"]]]

    @staticmethod
    def hip_calc(frame, mapping, mi, i, oi, result):
        result[i][oi["Hip"]] = np.mean(np.array([frame[mi[mapping["RHIP"]]], frame[mi[mapping["LHIP"]]]]), axis=0)

    @staticmethod
    def knee_calc(frame, mapping, mi, i, oi, result):
        result[i][oi["Knee"]] = frame[mi[mapping["RKNE"]]] - frame[mi[mapping["LKNE"]]]


class StaticCGM:

    def __init__(self, static_path, vsk_path):
        self.static_path = static_path
        self.vsk_path = vsk_path
        # In reality, measurements would be determined with appropriate functions
        self._measurements = {"MeanLegLength": 940.0, "RightKneeWidth": 105.0, "LeftKneeWidth": 105.0}
        # This is the extra thing that comes when using 6dof(?)
        self._offsets = {}

    @property
    def measurements(self):
        # Equivalent of getStatic
        return self._measurements

    @property
    def offsets(self):
        return self._offsets

    @staticmethod
    def pelvis_calc_static(frame, mapping, mi, i, oi, result):
        result[i][oi["Pelvis"]] = frame[mi[mapping["PELV"]]]

    @staticmethod
    def hip_calc_static(frame, mapping, mi, i, oi, result):
        result[i][oi["Hip"]] = np.mean(np.array([frame[mi[mapping["RHIP"]]], frame[mi[mapping["LHIP"]]]]), axis=0)

    @staticmethod
    def knee_calc_static(frame, mapping, mi, i, oi, result):
        result[i][oi["Knee"]] = frame[mi[mapping["RKNE"]]] - frame[mi[mapping["LKNE"]]]


def calc(data, methods, mappings):
    pel, hip, kne = methods
    mmap, mi, oi = mappings

    # mechanism responsible for changing size of output array
    result = np.zeros((len(data), len(oi), 3), dtype=int)

    for i, frame in enumerate(data):
        pel(frame, mmap, mi, i, oi, result)
        hip(frame, mmap, mi, i, oi, result)
        kne(frame, mmap, mi, i, oi, result)
    return result
