from demo.pycgm import *

subject = CGM()
subject.run()
print("Pelvis angles at each frame\n", subject.pelvis_angles)
# print("Hip angles at each frame\n", subject.hip_angles)
# print("Knee angles at each frame\n", subject.knee_angles)

print("=" * 80)


class MyCGM(CGM):
    @staticmethod
    def pelvis_calc(frame, mapping):
        return frame[mapping["PELVIS"]] + np.array([1, 1, 1])


subject2 = MyCGM()
subject2.rename("PELV", "PELVIS")
subject2.rename("RKNE", "RKNEE")
subject2.rename("LKNE", "LKNEE")
subject2.run()
print("Pelvis angles at each frame\n", subject2.pelvis_angles)
# print("Hip angles at each frame\n", subject2.hip_angles)
# print("Knee angles at each frame\n", subject2.knee_angles)
