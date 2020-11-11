from demo.pycgm import LowerBody, pyCGM


class CustomLowerBody(LowerBody):

    @staticmethod
    def pelvis_joint_center(frame, markers, vsk=None):
        return frame[markers["A"]] * 10


cpycgm = pyCGM(CustomLowerBody)
cpycgm.run()
