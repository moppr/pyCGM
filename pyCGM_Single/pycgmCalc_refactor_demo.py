from .pyCGM import *


def pelvis_joint_center(frame, calculation_method):
    if calculation_method == "single":
        return pelvis_joint_center_single(frame)
    elif calculation_method == "multiprocessing":
        return pelvis_joint_center_multi(frame)
    elif calculation_method == "HPC":
        return pelvis_joint_center_hpc(frame)


def pelvis_joint_center_single(frame):
    return []


def pelvis_joint_center_multi(frame):
    return []


def pelvis_joint_center_hpc(frame):
    return []