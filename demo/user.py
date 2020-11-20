from demo.pycgm import *

# Demonstrates basic case with no customization
subject0 = CGM(trial=0)
subject0.run()
print("Pelvis angles at each frame\n", subject0.pelvis_angles)


# Subclass that changes functionality of pelvis_calc to use an additional marker
class CGM1(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping, mi, i, oi, result):
        result[i][oi["Pelvis"]] = frame[mi[mapping["PELV"]]] + frame[mi[mapping["RANK"]]]


# Demonstrates adding a new marker and using a custom calculation with that marker
subject1 = CGM1(trial=1)
subject1.map("RANK")
subject1.run()
print("Pelvis angles at each frame\n", subject1.pelvis_angles)


# Demonstrates renaming all markers at once by providing a dictionary
subject2 = CGM(trial=2)
markers2 = {"PELV": "PELVIS", "RHIP": "RIGHTHIP", "LHIP": "LEFTHIP", "RKNE": "RIGHTKNEE", "LKNE": "LEFTKNEE"}
subject2.map(dic=markers2)
subject2.run()
print("Pelvis angles at each frame\n", subject2.pelvis_angles)


# Subclass that changes calculation behavior and uses custom marker name in that calculation
class CGM3(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping, mi, i, oi, result):
        result[i][oi["Pelvis"]] = frame[mi[mapping["PELVIS"]]] + frame[mi[mapping["RANK"]]]


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
print("Pelvis angles at each frame\n", subject3.pelvis_angles)


# Subclass that creates two knee angle results based on same inputs, also modifies property to access
# aforementioned two angles
class CGM4(CGM):
    @property
    def knee_angles(self):
        return self.all_angles[0:, self.output_index["Knee1"]], self.all_angles[0:, self.output_index["Knee2"]]

    @staticmethod
    def knee_calc(frame, mapping, mi, i, oi, result):
        result[i][oi["Knee1"]] = frame[mi[mapping["RKNE"]]] - frame[mi[mapping["LKNE"]]]
        result[i][oi["Knee2"]] = frame[mi[mapping["RKNE"]]] + frame[mi[mapping["LKNE"]]]


# Demonstrates creating two angles (expanding output dimension) on one joint
subject4 = CGM4(trial=4)
# Note: output index would have to update all others (increment) if new value added in middle
# Also would make more sense with its own .map
subject4.output_index["Knee1"] = 2
subject4.output_index["Knee2"] = 3
subject4.run()
print("Knee angles at each frame\n", subject4.knee_angles)
