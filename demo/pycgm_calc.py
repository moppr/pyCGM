def run_calculation(frames, methods, markers, nprocs):
    results = []

    # This part can be be run in parallel
    for frame in frames:
        results.append(joint_angle_calc(frame, methods, markers))

    return results


def joint_angle_calc(frame, methods, markers):
    # Pass in functions themselves as parameters
    pelvis_jc_method, hip_jc_method, knee_jc_method = methods

    pelvis_jc = pelvis_jc_method(frame, markers)
    hip_jc = hip_jc_method(frame, pelvis_jc)
    knee_jc = knee_jc_method(frame, hip_jc)
    return [pelvis_jc, hip_jc, knee_jc]
