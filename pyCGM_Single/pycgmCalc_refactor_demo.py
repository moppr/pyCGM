def do_calc(frames, methods):
    pjcm, hjcm, kjcm = methods
    for frame in frames:
        pelvis_jc = pjcm(frame)
        hip_jc = hjcm(frame, pelvis_jc)
        knee_jc = kjcm(frame, hip_jc)
    return pelvis_jc, hip_jc, knee_jc