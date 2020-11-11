import demo.pycgm_calc as calc
import demo.pycgm_io as io


class LowerBody:

    @staticmethod
    def pelvis_joint_center(frame, markers, marker="A", vsk=None):
        return frame[markers[marker]]

    @staticmethod
    def hip_joint_center(frame, pelvis_results):
        return pelvis_results + 1

    @staticmethod
    def knee_joint_center(frame, hip_results):
        return hip_results + 1


def pyCGM(lowerbody=LowerBody):
    class pyCGM(lowerbody):

        def __init__(self):
            self.markers = {"A": "A", "B": "B"}

        def rename(self, old, new):
            self.markers[old] = new

        def run(self, in_path=None):
            self._load(in_path)

            methods = [self.pelvis_joint_center, self.hip_joint_center, self.knee_joint_center]

            results = calc.do_calc(self.frames, methods, self.markers)
            self.pelvis_jc, self.hip_jc, self.knee_jc = results[0]

            print([item for item in results])
            
            self._write(str(results))

        def _load(self, in_path=None):
            if not in_path:
                in_path = "demo_data.csv"
            self.frames = io.load_data(in_path)
            
        def _write(self, results, out_path=None):
            if not out_path:
                out_path = "pycgm_results.csv"
            io.write_data(out_path, results)

    return pyCGM()
