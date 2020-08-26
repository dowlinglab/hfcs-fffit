import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import seaborn

sys.path.append("../")

from utils.r32 import R32Constants
from utils.id_new_samples import prepare_df_density
from utils.analyze_samples import prepare_df_density_errors

R32 = R32Constants()

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

############################# QUANTITIES TO EDIT #############################
##############################################################################

liquid_density_threshold=500 #kg/m3
iternum = 4

##############################################################################
##############################################################################

csv_path = "../csv/"
in_csv_names = [
    "r32-density-iter" + str(i) + "-results.csv" for i in range(1, iternum + 1)
]

# Read files
df_csvs = [
    pd.read_csv(csv_path + in_csv_name, index_col=0)
    for in_csv_name in in_csv_names
]
dfs = [prepare_df_density(df_csv, R32, liquid_density_threshold)[0] for df_csv in df_csvs]


def main():

    # Create a dataframe with one row per parameter set
    dfs_paramsets = [prepare_df_density_errors(df, R32) for df in dfs]

    name = "mape_liq_density"
    fig, ax = plt.subplots()
    axins = inset_axes(ax, width="100%", height="100%",
            bbox_to_anchor=(0.35, 0.3, 0.55, 0.55),
            bbox_transform=ax.transAxes, loc=3)
    ax.plot(
        dfs_paramsets[0].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-1",
    )
    ax.plot(
        dfs_paramsets[1].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-2",
    )
    ax.plot(
        dfs_paramsets[2].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-3",
    )
    ax.plot(
        dfs_paramsets[3].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-4",
    )

    ax.set_ylim(0,205)
    ax.set_xlim(0,100)
    ax.set_yticks([0,50,100,150,200])
    ax.set_yticks([25,75,125,175], minor=True)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xticks([10, 30, 50, 70, 90], minor=True)
    ax.tick_params("both", direction="in", which="both", length=2, labelsize=16)
    ax.tick_params("both", which="major", length=4)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_ylabel("Cumulative number parameter sets", fontsize=18, labelpad=15)
    ax.set_xlabel("Mean abs. % error", fontsize=18, labelpad=10)
    ax.legend(fontsize=14, loc=(-0.03,1.02), ncol=4)

    axins.plot(
        dfs_paramsets[0].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-1",
    )
    axins.plot(
        dfs_paramsets[1].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-2",
    )
    axins.plot(
        dfs_paramsets[2].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-3",
    )
    axins.plot(
        dfs_paramsets[3].sort_values(name)[name],
        np.arange(1, 201,1),
        '-o',
        markersize=4,
        alpha=0.8,
        label="LD-4",
    )

    axins.set_xlim(0,5)
    axins.set_ylim(0,200)
    axins.tick_params("both", direction="in", which="both", length=2, labelsize=12)
    axins.tick_params("both", which="major", length=4)
    axins.xaxis.set_ticks_position("both")
    axins.yaxis.set_ticks_position("both")

    fig.tight_layout()
    fig.savefig("pdfs/fig2-r32-density-cumu.pdf")

if __name__ == "__main__":
    main()
