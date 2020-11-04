from .pyCGM import *
import pyCGM_Single.pycgmCalc_refactor_demo as pycgmCalc


class LowerBody:

    def __init__(self, calculation_method="single"):
        self.calculation_method = calculation_method.strip().lower()
        self.pelvis_jc = None
        
    class Pelvis:
        
        def __init__(self, marker_name='PEL'):
            self.marker_name = marker_name
            self.pelvis_jc = None
            
        def rename(self, new):
            self.marker_name = new

        def pelvis_joint_center(self, frame):
            self.pelvis_jc = pycgmCalc.pelvis_joint_center(frame, self.calculation_method)


class CustomLowerBody(LowerBody):

    def custom_pelvis_jc(self, frame):
        # Custom code here
        pass
