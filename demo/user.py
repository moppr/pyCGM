from demo.pycgm import *

# Demonstrates basic case with no customization
subject0 = CGM()
subject0.run(0)
print("Pelvis angles at each frame\n", subject0.pelvis_angles)


# Subclass that changes functionality of pelvis_calc to use an additional marker
class CGM1(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping, mi):
        return CGM.pelvis_calc(frame, mapping, mi) + frame[mi[mapping["RANK"]]]


# Demonstrates adding a new marker and using a custom calculation with that marker
subject1 = CGM1()
subject1.map("RANK")
subject1.run(1)
print("Pelvis angles at each frame\n", subject1.pelvis_angles)


# Demonstrates renaming all markers at once by providing a dictionary
subject2 = CGM()
markers2 = {"PELV": "PELVIS", "RHIP": "RIGHTHIP", "LHIP": "LEFTHIP", "RKNE": "RIGHTKNEE", "LKNE": "LEFTKNEE"}
subject2.map(dic=markers2)
subject2.run(2)
print("Pelvis angles at each frame\n", subject2.pelvis_angles)


# Subclass that changes calculation behavior and uses custom marker name in that calculation
class CGM3(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping, mi):
        return frame[mi[mapping["PELVIS"]]] + frame[mi[mapping["RANK"]]]


# Demonstrates renaming some markers one at a time and adding a new marker w/ custom calculation
subject3 = CGM3()
subject3.map("PELV", "PELVIS")
subject3.map("RKNE", "RKNEE")
subject3.map("LKNE", "LKNEE")
subject3.map("RANK", "RANK")
subject3.run(3)
print("Pelvis angles at each frame\n", subject3.pelvis_angles)