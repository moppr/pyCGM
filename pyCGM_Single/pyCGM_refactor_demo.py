from pyCGM_Single.pycgmCalc_refactor_demo import calc_pelvis_jc


class LowerBody:

    @staticmethod
    def pelvis_joint_center(frame):
        return 1 + 2 + 3


def pyCGM(lowerbody=LowerBody):
    class pyCGM(lowerbody):
        pelvis_jc = calc_pelvis_jc(None, lowerbody.pelvis_joint_center)
    return pyCGM()
