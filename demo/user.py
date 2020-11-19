from demo.pycgm import *

subject = CGM()
subject.run(0)
print("Pelvis angles at each frame\n", subject.pelvis_angles)
# print("Hip angles at each frame\n", subject.hip_angles)
# print("Knee angles at each frame\n", subject.knee_angles)


class CGM2(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping, mi):
        return frame[mi[mapping["PELV"]]] + frame[mi[mapping["RANK"]]]


subject2 = CGM2()
# subject2.map("PELV", "PELVIS")
# subject2.map("RKNE", "RKNEE")
# subject2.map("LKNE", "LKNEE")
subject2.map("RANK", "RANK")
subject2.run(1)
print("Pelvis angles at each frame\n", subject2.pelvis_angles)
# print("Hip angles at each frame\n", subject2.hip_angles)
# print("Knee angles at each frame\n", subject2.knee_angles)
