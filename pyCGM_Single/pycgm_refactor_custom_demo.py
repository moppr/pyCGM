from pyCGM_Single.pyCGM_refactor_demo import LowerBody, pyCGM


class CustomLowerBody(LowerBody):

    @staticmethod
    def pelvis_joint_center(frame):
        return 10


# pycgm = pyCGM()
# pycgm.run()
cpycgm = pyCGM(CustomLowerBody)
cpycgm.run()