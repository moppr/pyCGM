from demo.pycgm import *

# Most basic example, no customization
subject0 = CGM()
subject0.run(0)
print("Pelvis angles at each frame\n", subject0.pelvis_angles)
# print("Hip angles at each frame\n", subject0.hip_angles)
# print("Knee angles at each frame\n", subject0.knee_angles)


class CGM1(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping, mi):
        return frame[mi[mapping["PELV"]]] + frame[mi[mapping["RANK"]]]


# Adds extra marker w/ calculation method but no renaming
subject1 = CGM1()
# subject2.map("PELV", "PELVIS")
# subject2.map("RKNE", "RKNEE")
# subject2.map("LKNE", "LKNEE")
subject1.map("RANK", "RANK")
subject1.run(1)
print("Pelvis angles at each frame\n", subject1.pelvis_angles)
# print("Hip angles at each frame\n", subject1.hip_angles)
# print("Knee angles at each frame\n", subject1.knee_angles)


# Renames all the markers at once by providing its own dictionary
subject2 = CGM()
markers2 = {"PELV": "PELVIS", "RHIP": "RIGHTHIP", "LHIP": "LEFTHIP", "RKNE": "RIGHTKNEE", "LKNE": "LEFTKNEE"}
subject2.map(dic=markers2)
subject2.run(2)
print("Pelvis angles at each frame\n", subject2.pelvis_angles)
# print("Hip angles at each frame\n", subject2.hip_angles)
# print("Knee angles at each frame\n", subject2.knee_angles)
