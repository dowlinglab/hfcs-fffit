import pytest
import numpy as np

class TestIDSamplles(BaseTest):
    def test_prepare_df(self, df_result_csv):
        df_all, df_liq, df_vap = prepare_df_density(df_result_csv, R32, 500.0)
        assert "is_liquid" in df_all.columns
        assert "is_liquid" in df_liq.columns
        assert "is_liquid" in df_vap.columns

        assert "md_density" in df_all.columns
        assert "md_density" in df_liq.columns
        assert "md_density" in df_vap.columns

        assert "expt_density" in df_all.columns
        assert "expt_density" in df_liq.columns
        assert "expt_density" in df_vap.columns

        assert "density" not in df_all.columns
        assert "density" not in df_liq.columns
        assert "density" not in df_vap.columns

        assert df_all[df_all["temperature"] >= 0.0].all()
        assert df_all[df_all["temperature"] <= 1.0].all()
        assert df_all[df_all["expt_density"] >= 0.0].all()
        assert df_all[df_all["expt_density"] <= 1.0].all()

    def test_prepare_df_bad_input(self, df_result_csv):

        df = df_result_csv.drop("temperature")
        with pytest.raises(ValueError, match=r"must contain column 'temperature'"):
            df_all, df_liq, df_vap = prepare_df_density(df, R32, 500.0)
        df = df_result_csv.drop("density")
        with pytest.raises(ValueError, match=r"must contain column 'density'"):
            df_all, df_liq, df_vap = prepare_df_density(df, R32, 500.0)

        df = df_result_csv.drop("sigma_C")
        with pytest.raises(ValueError, match=r"column for parameter 'sigma_C'"):
            df_all, df_liq, df_vap = prepare_df_density(df, R32, 500.0)

    def test_gp_mse():


    def test_ranked_samples(self, df_result_csv):

