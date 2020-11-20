import pytest
from demo import pycgm
import numpy as np


class TestClassMethods:
    # The parametrize method can hold varying CGM optional arguments
    @pytest.mark.parametrize(
        ["cgm_parameters", "expected_all_angles", "expected_offsets"], [
            ([None, None, None, 0], ([[0, 1, 2], [9, 9, 9], [0, 0, 0]]), {}),
            ([None, None, None, 1], ([[0, 1, 2], [9, 9, 9], [0, 0, 0]]), {}),
        ]
    )
    def test_run(self, cgm_parameters, expected_all_angles, expected_offsets):
        # Create a CGM object for each test, allowing different initialization arguments and cases to be tested.
        subject = pycgm.CGM(*cgm_parameters)
        subject.run()

        # Multiple attributes for each CGM can be tested at any time.
        np.testing.assert_equal(subject.all_angles[0], expected_all_angles)
        np.testing.assert_equal(subject.offsets, expected_offsets)

    @pytest.mark.parametrize(
        ["cgm_parameters", "old", "new", "dic"], [
            ([None, None, None, 0], "RANK", None, None),
            ([None, None, None, 1], "LANK", "RLANK", None),
            ([None, None, None, 1], "PELV", "PELVIS", None)
        ]
    )
    def test_map(self, cgm_parameters, old, new, dic):
        subject = pycgm.CGM(*cgm_parameters)
        subject.map(old, new, dic)

        if new and old:
            result = subject.mapping[old] == subject.mapping[new]
        elif old:
            result = subject.mapping[old] == old
        else:
            result = subject.mapping[new] == new
        assert result
