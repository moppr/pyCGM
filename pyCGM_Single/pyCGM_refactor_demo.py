from pyCGM_Single.pycgmCalc_refactor_demo import *
from pyCGM_Single.pycgmIO_refactor_demo import *


class LowerBody:

    @staticmethod
    def pelvis_joint_center(frame, vsk=None):
        return 1
    
    @staticmethod
    def hip_joint_center(frame, pelvis_results):
        return pelvis_results + 1
    
    @staticmethod
    def knee_joint_center(frame, hip_results):
        return hip_results + 1


def pyCGM(lowerbody=LowerBody):
    class pyCGM(lowerbody):

        def __init__(self):
            self.pelvis_jc, self.hip_jc, self.knee_jc = [None]*3

        def run(self, path=None):
            if not path:
                path = "pyCGM_Single/data_refactor_demo.csv"
            frames = load_data(path)
            # frames = [None]  # this will come from importing IO
            methods = [self.pelvis_joint_center, self.hip_joint_center, self.knee_joint_center]
            results = do_calc(frames, methods)
            self.pelvis_jc, self.hip_jc, self.knee_jc = results
            print([item for item in results])

    return pyCGM()
