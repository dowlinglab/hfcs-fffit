import pytest
import numpy as np

from utils.r32 import R32Constants
from utils.r125 import R125Constants

class TestConstants(BaseTest):
    def test_instantiate_R32(self):
        R32 = R32Constants()
    def test_instantiate_R125(self):
        R32 = R125Constants()
