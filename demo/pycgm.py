import numpy as np
from demo.IO import trials


class CGM:

    def __init__(self, static_path=None, dynamic_path=None, vsk_path=None, static=None, trial=0):
        self.static_path = static_path
        self.dynamic_path = dynamic_path
        self.vsk_path = vsk_path
        self.static = static
        if not static:
            self.static = StaticCGM(self.static_path, self.vsk_path)
        self.trial = trial
        self.all_angles = None
        self.all_axes = None
        self.offsets = None
        self.mapping = {"PELV": "PELV", "RHIP": "RHIP", "LHIP": "LHIP", "RKNE": "RKNE", "LKNE": "LKNE"}
        self.marker_index = {}
        self.output_an_index = {"Pelvis Angle": 0, "Hip Angle": 1, "Knee Angle": 2}
        self.output_ax_index = {"Pelvis Axis": 0, "Hip Axis": 1, "Knee Axis": 2}

    def run(self):
        # Loading in data from IO
        data, markers = trials[self.trial]  # Substitute for loading in data from c3d

        # Associate each marker name with its index
        for i, marker in enumerate(markers):
            self.marker_index[marker] = i

        # This is where prep/pipelines things happen

        # Get measurements from static trial
        measurements = self.static.measurements

        result = self.calc(data,
                           (self.pelvis_calc, self.hip_calc, self.knee_calc),
                           (self.mapping, self.marker_index, self.output_an_index, self.output_ax_index, measurements))
        self.all_angles, self.all_axes = result

    def map(self, old=None, new=None, dic=None):
        if dic and type(dic) == dict:  # Entire dictionary given
            self.mapping.update(dic)
            return
        # Potential issue if 'new' is an existing marker that CGM expects, unless all
        # instances that use it are overridden
        if old and new:  # Old and new marker name provided
            self.mapping[old] = new
            self.mapping[new] = new
        elif old and not new:  # Only one marker name provided
            self.mapping[old] = old  # Interpret it as adding a new marker

    @property
    def pelvis_angles(self):
        return self.all_angles[0:, self.output_an_index["Pelvis Angle"]]

    @property
    def hip_angles(self):
        return self.all_angles[0:, self.output_an_index["Hip Angle"]]

    @property
    def knee_angles(self):
        return self.all_angles[0:, self.output_an_index["Knee Angle"]]

    @property
    def pelvis_axes(self):
        return self.all_axes[0:, self.output_ax_index["Pelvis Axis"]]

    @property
    def hip_axes(self):
        return self.all_axes[0:, self.output_ax_index["Hip Axis"]]

    @property
    def knee_axes(self):
        return self.all_axes[0:, self.output_ax_index["Knee Axis"]]

    @staticmethod
    def pelvis_calc(pelv, measurements):
        pelv_angle = pelv
        pelv_axis = np.array([pelv, pelv, pelv, pelv])
        return pelv_angle, pelv_axis

    @staticmethod
    def hip_calc(pelv_axis, rhip, lhip, measurements):
        hip_angle = np.mean(np.array([rhip, lhip, pelv_axis[0]]), axis=0)
        hip_axis = np.array([rhip, lhip, pelv_axis[0], rhip+lhip])
        return hip_angle, hip_axis

    @staticmethod
    def knee_calc(hip_angle, rkne, lkne, measurements):
        knee_angle = rkne - lkne + hip_angle
        knee_axis = np.array([rkne, rkne, lkne, lkne])
        return knee_angle, knee_axis

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, an_oi, ax_oi, measurements = mappings

        # mechanism responsible for changing size of output array
        an_result = np.zeros((len(data), len(an_oi), 3), dtype=int)
        ax_result = np.zeros((len(data), len(ax_oi), 4, 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELV"]]]
            pelv_angle, pelv_axis = pel(pelv, measurements)
            an_result[i][an_oi["Pelvis Angle"]] = pelv_angle
            ax_result[i][ax_oi["Pelvis Axis"]] = pelv_axis

            rhip = frame[mi[mmap["RHIP"]]]
            lhip = frame[mi[mmap["LHIP"]]]
            hip_angle, hip_axis = hip(pelv_axis, rhip, lhip, measurements)
            an_result[i][an_oi["Hip Angle"]] = hip_angle
            ax_result[i][ax_oi["Hip Axis"]] = hip_axis

            rkne = frame[mi[mmap["RKNE"]]]
            lkne = frame[mi[mmap["LKNE"]]]
            knee_angle, knee_axis = kne(hip_angle, rkne, lkne, measurements)
            an_result[i][an_oi["Knee Angle"]] = knee_angle
            ax_result[i][ax_oi["Knee Axis"]] = knee_axis

        return an_result, ax_result


class StaticCGM:

    def __init__(self, static_path, vsk_path):
        self.static_path = static_path
        self.vsk_path = vsk_path
        # In reality, measurements would be determined with appropriate functions
        self._measurements = {"MeanLegLength": 940.0, "RightKneeWidth": 105.0, "LeftKneeWidth": 105.0}

    @property
    def measurements(self):
        # Equivalent of getStatic
        return self._measurements
