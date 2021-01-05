import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import seaborn

sys.path.append("../")

from fffit.utils import values_scaled_to_real
from utils.r32 import R32Constants
from matplotlib import ticker

R32 = R32Constants()

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

NM_TO_ANGSTROM = 10
K_B = 0.008314 # J/MOL K
KJMOL_TO_K = 1.0 / K_B


def main():
    # ID the top ten by lowest average MAPE
    df = pd.read_csv("../csv/r32-pareto.csv", index_col=0)
    #df = df.loc[df.filter(regex="mape*").mean(axis=1).sort_values()[:10].index]

    colors = seaborn.color_palette('bright', n_colors=len(df))
    #data = values_scaled_to_real(df[list(R32.param_names)].values, R32.param_bounds)
    #data[:,:3] = data[:,:3] * NM_TO_ANGSTROM
    #data[:,4:6] = data[:,4:] * KJMOL_TO_K
    data = df[list(R32.param_names)].values
    param_bounds = R32.param_bounds
    param_bounds[:3] = param_bounds[:3] * NM_TO_ANGSTROM
    param_bounds[3:] = param_bounds[3:] * KJMOL_TO_K

    col_names = [
        r"$\sigma_C$",
        r"$\sigma_F$",
        r"$\sigma_H$",
        r"$\epsilon_C$",
        r"$\epsilon_F$",
        r"$\epsilon_H$",
    ]
    n_axis = len(col_names)
    assert data.shape[1] == n_axis
    x_vals = [i for i in range(n_axis)]
    
    # Create (N-1) subplots along x axis
    fig, axes = plt.subplots(1, n_axis-1, sharey=False, figsize=(12,5))
    
    # Get min, max and range for each column
    # Normalize the data for each column
    #min_max_range = {}
    #for col in cols:
    #    min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
    #    #df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))
    #    min_max_range[col] = [0, 1.0]
    
    # Plot each row
    for i, ax in enumerate(axes):
        for line in data:
            ax.plot(x_vals, line, alpha=0.65)
        ax.set_xlim([x_vals[i], x_vals[i+1]])
        
    for dim, ax in enumerate(axes):
        ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
        set_ticks_for_axis(ax, param_bounds[dim], nticks=6)
        ax.set_xticklabels([col_names[dim]], fontsize=40)
        ax.set_ylim(-0.05,1.05)
        # Add white background behind labels
        for label in ax.get_yticklabels():
            label.set_bbox(
                dict(
                    facecolor='white',
                    edgecolor='none',
                    alpha=0.45,
                    boxstyle=mpatch.BoxStyle("round4")
                )
            )
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_linewidth(2.0)

    ax = axes[-1]
    ax.xaxis.set_major_locator(ticker.FixedLocator([n_axis-2, n_axis-1]))
    ax.set_xticklabels([col_names[-2], col_names[-1]], fontsize=40)

    ax = plt.twinx(axes[-1])
    ax.set_ylim(-0.05, 1.05)
    set_ticks_for_axis(ax, param_bounds[-1], nticks=6)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_linewidth(2.0)

    # Remove space between subplots
    plt.subplots_adjust(wspace=0, bottom=0.2)
    
    fig.savefig("pdfs/fig4-r32-parallel.pdf")


def set_ticks_for_axis(ax, param_bounds, nticks):
    """Set the tick positions and labels on y axis for each plot

    Tick positions based on normalised data
    Tick labels are based on original data
    """
    min_val, max_val = param_bounds
    step = (max_val - min_val) / float(nticks-1)
    tick_labels = [round(min_val + step * i, 2) for i in range(nticks)]
    ticks = np.linspace(0, 1.0, nticks)
    ax.yaxis.set_ticks(ticks)
    ax.set_yticklabels(tick_labels, fontsize=24)
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax.tick_params("y", direction="inout", which="both", length=7)
    ax.tick_params("y", which="major", length=14)
    ax.tick_params("x", pad=15) 

if __name__ == "__main__":
    main()

