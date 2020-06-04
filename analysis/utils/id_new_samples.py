import numpy as np
import pandas as pd

from fffit.utils import (
    values_real_to_scaled,
    values_scaled_to_real
)

def prepare_df_density(df_csv, molecule, liquid_density_threshold):
    """Prepare a pandas dataframe for fitting a GP model to density data

    Performs the following actions:
       - Renames "density" to "md_density"
       - Adds "expt_density"
       - Adds "is_liquid"
       - Converts all values from physical values to scaled values

    Parameters
    ----------
    df_csv : pd.DataFrame
        The dataframe as loaded from a CSV file with the signac results
    molecule : R32Constants, R125Constants
        An instance of a molecule constants class
    liquid_density_threshold : float
        Density threshold (kg/m^3) for distinguishing liquid and vapor

    Returns
    -------
    df_all : pd.DataFrame
        The dataframe with scaled parameters, temperature, density, and is_liquid
    df_liquid : pd.DataFrame
        `df_all` where `is_liquid` is True
    df_vapor : pd.DataFrame
        `df_all` where `is_liquid` is False
    """

    # Add expt density and is_liquid
    df_all = df_csv.rename(columns={"density": "md_density"})
    df_all["expt_density"] = df_all["temperature"].apply(
        lambda temp: molecule.expt_liq_density[int(temp)]
    )
    df_all["is_liquid"] = df_all["md_density"].apply(
        lambda x: x > liquid_density_threshold
    )

    # Scale all values
    scaled_param_values = values_real_to_scaled(
        df_all[list(molecule.param_names)], molecule.param_bounds
    )
    scaled_temperature = values_real_to_scaled(
        df_all["temperature"], molecule.temperature_bounds
    )
    scaled_md_density = values_real_to_scaled(
        df_all["md_density"], molecule.liq_density_bounds
    )
    scaled_expt_density = values_real_to_scaled(
        df_all["expt_density"], molecule.liq_density_bounds
    )
    df_all[list(molecule.param_names)] = scaled_param_values
    df_all["temperature"] = scaled_temperature
    df_all["md_density"] = scaled_md_density
    df_all["expt_density"] = scaled_expt_density

    # Split out vapor and liquid samples
    df_liquid = df_all[df_all["is_liquid"] == True]
    df_vapor = df_all[df_all["is_liquid"] == False]

    return df_all, df_liquid, df_vapor


def rank_hypercube_samples(latin_hypercube, classifier, gp_model, molecule):
    """Evalulate the GP model for a latin hypercube and return ranked results

    Parameters
    ----------
    latin_hypercube : np.ndarray, shape=(n_samples, n_params)
        Samples to rank
    classifier : sklearn.svm.SVC
        Classifier to distinguish between liquid and vapor
    gp_model : gpflow.model
        GP model to predict the density of each sample
    molecule : R32Constants, R125Constants
        An instance of a molecule constants class

    Returns
    -------
    ranked_liquid_samples : pd.DataFrame
        Samples classified as liquid, sorted by MSE
    ranked_vapor_samples : pd.DataFrame
        Samples classified as vapor, sorted by MSE
    """

    # Use a classifier to predict which samples give liquid vs. vapor
    # Classification performed at the highest temperature
    # Append highest temperature (1.0) to LH samples
    samples = np.hstack(
        (latin_hypercube, np.tile(1.0, (latin_hypercube.shape[0], 1)))
    )

    # Apply clasifier
    pred = classifier.predict(samples)

    # Separate LH samples into predicted liquid and predicted vapor
    liquid_samples = latin_hypercube[np.where(pred == 1)]
    vapor_samples = latin_hypercube[np.where(pred == 0)]
    print("Shape of Latin hypercube sample:", latin_hypercube.shape)
    print("Shape of the predicted liquid samples:", liquid_samples.shape)
    print("Shape of the predicted vapor samples:", vapor_samples.shape)

    # Apply GP model and calculate mean squared errors (MSE) between
    # GP model predictions and experimental data for all parameter samples
    liquid_mse = _calc_gp_mse(gp_model, liquid_samples, molecule)
    vapor_mse = _calc_gp_mse(gp_model, vapor_samples, molecule)

    # Make liquid and vapor pandas dataframes, rank, and return
    liquid_samples_mse = np.hstack((liquid_samples, liquid_mse.reshape(-1, 1)))
    liquid_samples_mse = pd.DataFrame(
        liquid_samples_mse, columns=list(molecule.param_names) + ["mse"]
    )
    vapor_samples_mse = np.hstack((vapor_samples, vapor_mse.reshape(-1, 1)))
    vapor_samples_mse = pd.DataFrame(
        vapor_samples_mse, columns=list(molecule.param_names) + ["mse"]
    )
    ranked_liquid_samples = liquid_samples_mse.sort_values("mse")
    ranked_vapor_samples = vapor_samples_mse.sort_values("mse")

    return ranked_liquid_samples, ranked_vapor_samples


def _calc_gp_mse(gp_model, samples, molecule):
    """Calculate the MSE between the GP model and experiment for samples"""

    all_errs = np.empty(
        shape=(samples.shape[0], len(molecule.expt_liq_density.keys()))
    )
    col_idx = 0
    for (temp, density) in molecule.expt_liq_density.items():
        scaled_temp = values_real_to_scaled(temp, molecule.temperature_bounds)
        xx = np.hstack((samples, np.tile(scaled_temp, (samples.shape[0], 1))))
        means_scaled, vars_scaled = gp_model.predict_f(xx)
        means = values_scaled_to_real(
            means_scaled, molecule.liq_density_bounds
        )
        err = means - density
        all_errs[:, col_idx] = err[:, 0]
        col_idx += 1

    return np.mean(all_errs ** 2, axis=1)
