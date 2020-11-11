from demo.pycgm import LowerBody, pyCGM


class CustomLowerBody(LowerBody):

    @staticmethod
    def pelvis_joint_center(frame, markers, vsk=None):
        # Demonstrates alternate functionality, in this case giving an output 10x that of the default
        return frame[markers["A"]] * 10


if __name__ == "__main__":
    # Creating the pycgm object with a custom class to inherit from
    cpycgm = pyCGM(lowerbody=CustomLowerBody)

    # Static methods don't come with class overhead, and are internally functions rather than bound methods
    print(type(cpycgm.pelvis_joint_center))
    print(type(cpycgm.rename))

    # What pycgm by default expects marker "A" to be is actually "X" in the input
    try:
        cpycgm.run()
    except KeyError:
        print("Before renaming marker, KeyError encountered")

    # Renaming the marker to reflect what is in the input resolves the issue
    cpycgm.rename("A", "X")
    try:
        cpycgm.run()
    except KeyError:
        print("After renaming marker, KeyError encountered")

    # Demonstrates user using their custom marker name
    # to access value of that marker at arbitrary frame
    frame1 = cpycgm.frames[0]
    print(frame1["X"])

    # Demonstrates accessing the list of joint centers at each frame for some joint
    print(cpycgm.hip_jcs)
