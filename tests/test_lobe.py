import pytest 
import numpy as np
import flowpy as fpy

@pytest.fixture
def lobe():
    ''' 
    Creates a lobe which you can reuse.
    '''
    lobe = fpy.flowpycpp.Lobe()
    lobe.semi_axes = [8, 2]
    lobe.thickness = 20.0
    lobe.set_azimuthal_angle(np.pi / 4.0)
    lobe.center = [20, 10]
    return lobe

def test_lobe(lobe):
    '''
    Test some lobe functions. TODO: add more tests!
    '''
    assert lobe.get_azimuthal_angle() == np.pi / 4.0