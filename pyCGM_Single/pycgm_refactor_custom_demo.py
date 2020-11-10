from pyCGM_Single.pyCGM_refactor_demo import LowerBody, pyCGM


class CustomLowerBody(LowerBody):

    @staticmethod
    def pelvis_joint_center(frame):
        return 2 + 3 + 4


pycgm = pyCGM()
print(pycgm.pelvis_jc)
cpycgm = pyCGM(CustomLowerBody)
print(cpycgm.pelvis_jc)