import demo.pycgm_calc as calc
import demo.pycgm_io as io


class LowerBody:

    @staticmethod
    def pelvis_joint_center(frame, markers, vsk=None):
        # Demonstrates obtaining some value based on frame input
        # markers["A"] is used instead of simply "A" in the event that the user
        # needed to rename a marker
        return frame[markers["A"]]

    @staticmethod
    def hip_joint_center(frame, pelvis_results):
        # Demonstrates that subsequent joint center calculations rely on result of previous step
        return pelvis_results + 1

    @staticmethod
    def knee_joint_center(frame, hip_results):
        return hip_results + 1


def pyCGM(lowerbody=LowerBody):
    # There is no way to have a "default parent" when inheriting, so the next best thing
    # is to define the class inside a function that accepts class in its default parameter

    class pyCGM(lowerbody):

        def __init__(self):
            # Storing markers in a dicionary like this allows for easy translation between
            # default pycgm behavior and any renaming that's been done

            # The purpose of this is to get pycgm to understand when an input differs
            # from its expected input, i.e. if pycgm's "A" marker was named "X" in the user's input,
            # pycgm would know to look up "X" from its frame dictionary and the user could
            # continue referring to that marker as "X" if they looked it up in the dict themselves
            self.markers = {"A": "A", "B": "B", "C": "C"}
            self.pelvis_jcs = None
            self.hip_jcs = None
            self.knee_jcs = None

        def rename(self, old, new):
            self.markers[old] = new

        def run(self, in_path=None):
            self._load(in_path)

            # Static trials, which can't be done in parallel, would go here
            # Their methods can similarly be defined and overridden similar to dynamic examples

            # Despite having the "self" prefix, these methods are actually being passed
            # as functions (no overhead) rather than bound methods of an instance (with overhead)
            # because they were defined as static methods
            # Defining them as static is safe because the calculations don't rely on anything
            # from the instance anyway, all they need is the input of the frames
            methods = (self.pelvis_joint_center,
                       self.hip_joint_center,
                       self.knee_joint_center)

            results = calc.run_calculation(self.frames, methods, self.markers)
            self.pelvis_jcs = [item[0] for item in results]
            self.hip_jcs = [item[1] for item in results]
            self.knee_jcs = [item[2] for item in results]

            print("results:", results)

            self._write(str(results))

        def _load(self, in_path=None):
            if not in_path:
                in_path = "demo_data.csv"
            # Storing frames in instance variable allows user to select isolated data
            self.frames = io.load_data(in_path)

        def _write(self, results, out_path=None):
            if not out_path:
                out_path = "pycgm_results.csv"
            io.write_data(out_path, results)

    return pyCGM()
