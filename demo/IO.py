import numpy as np


# default amount of markers (5)
example1 = np.array([[[0, 1, 2], [10, 10, 10], [8, 8, 8], [5, 5, 5], [5, 5, 5]],
                     [[3, 4, 5], [9, 9, 9], [7, 7, 7], [4, 4, 4], [4, 4, 4]],
                     [[6, 7, 8], [8, 8, 8], [6, 6, 6], [3, 3, 3], [3, 3, 3]],
                     [[5, 6, 7], [8, 8, 8], [4, 4, 4], [2, 2, 2], [2, 2, 2]],
                     [[4, 5, 6], [8, 8, 8], [2, 2, 2], [0, 0, 0], [0, 0, 0]]])
ex1markers = "PELV RHIP LHIP RKNE LKNE".split()

# one more marker
example2 = np.array([[[0, 1, 2], [10, 10, 10], [8, 8, 8], [5, 5, 5], [5, 5, 5], [0, 0, 0]],
                     [[3, 4, 5], [9, 9, 9], [7, 7, 7], [4, 4, 4], [4, 4, 4], [2, 2, 2]],
                     [[6, 7, 8], [8, 8, 8], [6, 6, 6], [3, 3, 3], [3, 3, 3], [4, 4, 4]],
                     [[5, 6, 7], [8, 8, 8], [4, 4, 4], [2, 2, 2], [2, 2, 2], [7, 7, 7]],
                     [[4, 5, 6], [8, 8, 8], [2, 2, 2], [0, 0, 0], [0, 0, 0], [9, 9, 9]]])
ex2markers = "PELV RHIP LHIP RKNE LKNE RANK".split()

# multiple different marker names
example3 = example1
ex3markers = "PELVIS RIGHTHIP LEFTHIP RIGHTKNEE LEFTKNEE".split()

# extra marker with partial renames
example4 = example2
ex4markers = "PELVIS RHIP LHIP RKNEE LKNEE RANK".split()

trials = [(example1, ex1markers), (example2, ex2markers), (example3, ex3markers), (example4, ex4markers)]