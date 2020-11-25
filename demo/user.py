from demo.pycgm import *

# Demonstrates basic case with no customization
subject0 = CGM(trial=0)
subject0.run()
print("Trial 0 pelvis angles at each frame with no modification\n", subject0.pelvis_angles)
print("Trial 0 all angles at frame 1\n", subject0.all_angles[0])
print("Trial 0 hip axes at each frame\n", subject0.hip_axes, "\n")


# Subclass that changes functionality of pelvis_calc to use an additional marker
class CGM1(CGM):

    @staticmethod
    def pelvis_calc(pelv, rank, measurements):
        pelv_angle = pelv + rank
        pelv_axis = np.array([pelv, pelv, pelv, pelv])
        return pelv_angle, pelv_axis

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, an_oi, ax_oi, measurements = mappings

        # mechanism responsible for changing size of output array
        an_result = np.zeros((len(data), len(an_oi), 3), dtype=int)
        ax_result = np.zeros((len(data), len(ax_oi), 4, 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELV"]]]
            rank = frame[mi[mmap["RANK"]]]
            pelv_angle, pelv_axis = pel(pelv, rank, measurements)
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


# Demonstrates adding a new marker and using a custom calculation with that marker
subject1 = CGM1(trial=1)
subject1.map("RANK")
subject1.run()
print("Trial 1 pelvis angles at each frame with 1 new marker and custom method\n", subject1.pelvis_angles, "\n")


# Demonstrates renaming all markers at once by providing a dictionary
subject2 = CGM(trial=2)
markers2 = {"PELV": "PELVIS", "RHIP": "RIGHTHIP", "LHIP": "LEFTHIP", "RKNE": "RIGHTKNEE", "LKNE": "LEFTKNEE"}
subject2.map(dic=markers2)
subject2.run()
print("Trial 2 pelvis angles at each frame after renaming all markers\n", subject2.pelvis_angles, "\n")


# Subclass that changes calculation behavior and uses custom marker name in that calculation
class CGM3(CGM):

    @staticmethod
    def pelvis_calc(pelv, rank, measurements):
        pelv_angle = pelv + rank
        pelv_axis = np.array([pelv, pelv, pelv, pelv])
        return pelv_angle, pelv_axis

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, an_oi, ax_oi, measurements = mappings

        # mechanism responsible for changing size of output array
        an_result = np.zeros((len(data), len(an_oi), 3), dtype=int)
        ax_result = np.zeros((len(data), len(ax_oi), 4, 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELVIS"]]]
            rank = frame[mi[mmap["RANK"]]]
            pelv_angle, pelv_axis = pel(pelv, rank, measurements)
            an_result[i][an_oi["Pelvis Angle"]] = pelv_angle
            ax_result[i][ax_oi["Pelvis Axis"]] = pelv_axis

            rhip = frame[mi[mmap["RHIP"]]]
            lhip = frame[mi[mmap["LHIP"]]]
            hip_angle, hip_axis = hip(pelv_axis, rhip, lhip, measurements)
            an_result[i][an_oi["Hip Angle"]] = hip_angle
            ax_result[i][ax_oi["Hip Axis"]] = hip_axis

            rkne = frame[mi[mmap["RKNEE"]]]
            lkne = frame[mi[mmap["LKNEE"]]]
            knee_angle, knee_axis = kne(hip_angle, rkne, lkne, measurements)
            an_result[i][an_oi["Knee Angle"]] = knee_angle
            ax_result[i][ax_oi["Knee Axis"]] = knee_axis

        return an_result, ax_result


# Demonstrates renaming some markers one at a time and adding a new marker w/ custom calculation
# Note that the custom calculation could reference either the old or new name, though it makes
# more sense to use the new one
# The only exception to that is if the new name replaces an existing one, but that probably
# isn't a situation we're going to encounter
subject3 = CGM3(trial=3)
subject3.map("PELV", "PELVIS")
subject3.map("RKNE", "RKNEE")
subject3.map("LKNE", "LKNEE")
subject3.map("RANK", "RANK")
subject3.run()
print("Trial 3 pelvis angles at each frame after renaming some markers, adding new one, and using \
custom calculation method\n", subject3.pelvis_angles, "\n")


# Subclass that creates two knee angle results based on same inputs, also modifies property to access
# aforementioned two angles
class CGM4(CGM):

    @property
    def knee_angles(self):
        return self.all_angles[0:, self.output_an_index["Knee Angle 1"]], self.all_angles[0:, self.output_an_index["Knee Angle 2"]]

    @staticmethod
    def knee_calc(hip_angle, rkne, lkne, measurements):
        knee_angle = np.array([rkne - lkne + hip_angle, rkne + lkne + hip_angle])
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
            an_result[i][an_oi["Knee Angle 1"]] = knee_angle[0]
            an_result[i][an_oi["Knee Angle 2"]] = knee_angle[1]
            ax_result[i][ax_oi["Knee Axis"]] = knee_axis

        return an_result, ax_result


# Demonstrates creating two angles (expanding output dimension) on one joint
subject4 = CGM4(trial=4)
# Note: output index would have to update all others (increment) if new value added in middle
# Also would make more sense with its own .map
subject4.output_an_index["Knee Angle 1"] = 2
subject4.output_an_index["Knee Angle 2"] = 3
subject4.run()
print("Trial 4 knee angles at each frame after creating two angle outputs per knee\n", subject4.knee_angles, "\n")


# Subclass that defines a knee calc method using offsets of subclassed static
class CGM5(CGM):

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
                           (self.mapping, self.marker_index, self.output_an_index, self.output_ax_index, measurements, self.static.offsets))
        self.all_angles, self.all_axes = result

    @staticmethod
    def knee_calc(hip_angle, rkne, lkne, lkne_offset, measurements):
        knee_angle = rkne - lkne + hip_angle + lkne_offset
        knee_axis = np.array([rkne, rkne, lkne, lkne])
        return knee_angle, knee_axis

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, an_oi, ax_oi, measurements, offsets = mappings

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
            lkne_offset = offsets[mmap["LKNE"]]
            knee_angle, knee_axis = kne(hip_angle, rkne, lkne, lkne_offset, measurements)
            an_result[i][an_oi["Knee Angle"]] = knee_angle
            ax_result[i][ax_oi["Knee Axis"]] = knee_axis

        return an_result, ax_result


class StaticCGM5(StaticCGM):
    def __init__(self, static_path, vsk_path):
        super().__init__(static_path, vsk_path)
        self._offsets = {"LKNE": np.ones(3, dtype=int)}

    @property
    def offsets(self):
        return self._offsets


subject5static = StaticCGM5(None, None)
subject5 = CGM5(trial=5, static=subject5static)
subject5.run()
print("Trial 5 knee angles at each frame after incorporating subclassed offset\n", subject5.knee_angles, "\n")
