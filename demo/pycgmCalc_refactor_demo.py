def do_calc(frames, methods):
    results = []
    pjcm, hjcm, kjcm = methods
    for frame in frames:
        pelvis_jc = pjcm(frame)
        hip_jc = hjcm(frame, pelvis_jc)
        knee_jc = kjcm(frame, hip_jc)
        results.append([pelvis_jc, hip_jc, knee_jc])
    return results
