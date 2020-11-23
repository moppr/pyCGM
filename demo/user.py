from demo.pycgm import *

# Demonstrates basic case with no customization
subject0 = CGM(trial=0)
subject0.run()
print("Trial 0 pelvis angles at each frame with no modification\n", subject0.pelvis_angles, "\n")


# Subclass that changes functionality of pelvis_calc to use an additional marker
class CGM1(CGM):

    @staticmethod
    def pelvis_calc(pelv, rank):
        return pelv + rank

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, oi = mappings

        # mechanism responsible for changing size of output array
        result = np.zeros((len(data), len(oi), 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELV"]]]
            rank = frame[mi[mmap["RANK"]]]
            result[i][oi["Pelvis"]] = pel(pelv, rank)
            rhip = frame[mi[mmap["RHIP"]]]
            lhip = frame[mi[mmap["LHIP"]]]
            result[i][oi["Hip"]] = hip(rhip, lhip)
            rkne = frame[mi[mmap["RKNE"]]]
            lkne = frame[mi[mmap["LKNE"]]]
            result[i][oi["Knee"]] = kne(rkne, lkne)
        return result


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
    def pelvis_calc(pelv, rank):
        return pelv + rank

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, oi = mappings

        # mechanism responsible for changing size of output array
        result = np.zeros((len(data), len(oi), 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELV"]]]
            rank = frame[mi[mmap["RANK"]]]
            result[i][oi["Pelvis"]] = pel(pelv, rank)
            rhip = frame[mi[mmap["RHIP"]]]
            lhip = frame[mi[mmap["LHIP"]]]
            result[i][oi["Hip"]] = hip(rhip, lhip)
            rkne = frame[mi[mmap["RKNE"]]]
            lkne = frame[mi[mmap["LKNE"]]]
            result[i][oi["Knee"]] = kne(rkne, lkne)
        return result


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
        return self.all_angles[0:, self.output_index["Knee1"]], self.all_angles[0:, self.output_index["Knee2"]]

    @staticmethod
    def knee_calc(rkne, lkne):
        return rkne - lkne, rkne + lkne

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, oi = mappings

        # mechanism responsible for changing size of output array
        result = np.zeros((len(data), len(oi), 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELV"]]]
            result[i][oi["Pelvis"]] = pel(pelv)
            rhip = frame[mi[mmap["RHIP"]]]
            lhip = frame[mi[mmap["LHIP"]]]
            result[i][oi["Hip"]] = hip(rhip, lhip)
            rkne = frame[mi[mmap["RKNE"]]]
            lkne = frame[mi[mmap["LKNE"]]]
            result[i][oi["Knee1"]], result[i][oi["Knee2"]] = kne(rkne, lkne)
        return result


# Demonstrates creating two angles (expanding output dimension) on one joint
subject4 = CGM4(trial=4)
# Note: output index would have to update all others (increment) if new value added in middle
# Also would make more sense with its own .map
subject4.output_index["Knee1"] = 2
subject4.output_index["Knee2"] = 3
subject4.run()
print("Trial 4 knee angles at each frame after creating two angle outputs per knee\n", subject4.knee_angles, "\n")


# Subclass that defines a knee calc method using offsets of subclassed static
class CGM5(CGM):

    def run(self, static):
        data, markers = trials[self.trial]  # Substitute for loading in data from c3d

        # Associate each marker name with its index
        for i, marker in enumerate(markers):
            self.marker_index[marker] = i

        result = self.calc(data,
                           (self.pelvis_calc, self.hip_calc, self.knee_calc),
                           (self.mapping, self.marker_index, self.output_index, static.offsets))
        self.all_angles = result

    @staticmethod
    def knee_calc(rkne, lkne, lkne_offset):
        return rkne - lkne + lkne_offset

    @staticmethod
    def calc(data, methods, mappings):
        pel, hip, kne = methods
        mmap, mi, oi, offsets = mappings

        # mechanism responsible for changing size of output array
        result = np.zeros((len(data), len(oi), 3), dtype=int)

        for i, frame in enumerate(data):
            pelv = frame[mi[mmap["PELV"]]]
            result[i][oi["Pelvis"]] = pel(pelv)
            rhip = frame[mi[mmap["RHIP"]]]
            lhip = frame[mi[mmap["LHIP"]]]
            result[i][oi["Hip"]] = hip(rhip, lhip)
            rkne = frame[mi[mmap["RKNE"]]]
            lkne = frame[mi[mmap["LKNE"]]]
            lkne_offset = offsets[mmap["LKNE"]]
            result[i][oi["Knee"]] = kne(rkne, lkne, lkne_offset)
        return result


class StaticCGM5(StaticCGM):
    def __init__(self, static_path, vsk_path):
        super().__init__(static_path, vsk_path)
        self._offsets = {"LKNE": np.ones(3, dtype=int)}

    @property
    def offsets(self):
        return self._offsets


subject5 = CGM5(trial=5)
subject5static = StaticCGM5(None, None)
subject5.run(static=subject5static)
print("Trial 5 knee angles at each frame after incorporating subclassed offset\n", subject5.knee_angles, "\n")