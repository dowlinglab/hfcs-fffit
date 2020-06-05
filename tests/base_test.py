import pytest
from hfcs.analysis.utils import R32Constants
from hfcs.analysis.utils import R125Constants

class BaseTest:
    @pytest.fixture
    def df_result_csv(self):
        df = pd.read_csv("files/example.csv", index_col=0)
        return df

    @pytest.fixture
    def R32(self):
        R32 = R32Constants()
        return R32

    @pytest.fixture
    def R125(self):
        R125 = R125Constants()
        return R125

