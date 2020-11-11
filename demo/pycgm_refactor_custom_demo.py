from demo.pyCGM_refactor_demo import LowerBody, pyCGM


class CustomLowerBody(LowerBody):

    @staticmethod
    def pelvis_joint_center(frame):
        return 10


cpycgm = pyCGM(CustomLowerBody)
cpycgm.run()
