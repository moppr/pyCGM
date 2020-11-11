def do_calc(frames, methods, markers):
    results = []
    pjcm, hjcm, kjcm = methods
    for frame in frames:
        pelvis_jc = pjcm(frame, markers)
        hip_jc = hjcm(frame, pelvis_jc)
        knee_jc = kjcm(frame, hip_jc)
        results.append([pelvis_jc, hip_jc, knee_jc])
    return results
