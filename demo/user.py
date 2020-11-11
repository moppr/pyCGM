from demo.pycgm import LowerBody, pyCGM


class CustomLowerBody(LowerBody):

    @staticmethod
    def pelvis_joint_center(frame, markers, marker="A", vsk=None):
        return frame[markers[marker]] * 10


cpycgm = pyCGM(CustomLowerBody)
cpycgm.run()
