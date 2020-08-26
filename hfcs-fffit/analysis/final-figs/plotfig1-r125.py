import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn

from fffit.utils import (
    values_real_to_scaled,
    values_scaled_to_real,
)

sys.path.append("../")

from utils.r125 import R125Constants
from utils.id_new_samples import prepare_df_vle
from utils.analyze_samples import prepare_df_vle_errors
from utils.plot import plot_property, render_mpl_table

R125 = R125Constants()

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

csv_path = "/scratch365/rdefever/hfcs-fffit/hfcs-fffit/analysis/csv/r125-pareto.csv"
df = pd.read_csv(csv_path, index_col=0)

def main():

    # Plot VLE envelopes
    clrs = seaborn.color_palette('bright', n_colors=len(df))
    #random.seed(13)
    #random.seed(12)
    np.random.seed(10)
    np.random.shuffle(clrs)

    fig, ax = plt.subplots()
    temps = R125.expt_liq_density.keys()
    for temp in temps:
        ax.scatter(
            df.filter(regex=(f"liq_density_{float(temp):.0f}K")),
            np.tile(temp, len(df)),
            c=clrs,
            s=180,
            alpha=0.1,
        )
        ax.scatter(
            df.filter(regex=(f"vap_density_{float(temp):.0f}K")),
            np.tile(temp, len(df)),
            c=clrs,
            s=180,
            alpha=0.1,
        )
    ax.scatter(
        df.filter(regex=("sim_rhoc")),
        df.filter(regex=("sim_Tc")),
        c=clrs,
        s=180,
        alpha=0.1,
    )
    ax.scatter(
        R125.expt_liq_density.values(),
        R125.expt_liq_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(
        R125.expt_vap_density.values(),
        R125.expt_vap_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(R125.expt_rhoc, R125.expt_Tc, color="black", marker="x", s=240)

    ax.set_ylim(220,360)
    ax.set_yticks([240, 280, 320, 360])
    ax.set_yticks([230,250,260,270,290,300,310,330,340,350], minor=True)
    ax.set_xticks([0,400,800,1200,1600])
    ax.set_xticks([100,200,300,500,600,700,900,1000,1100,1300,1400,1500], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_ylabel("T (K)", fontsize=32, labelpad=20)
    ax.set_xlabel(r"$\mathregular{\rho}$ (kg/m$\mathregular{^3}$)", fontsize=32, labelpad=10)
    fig.tight_layout()
    fig.savefig("fig1-vle-r125.pdf")

    # Plot Vapor Pressure
    fig, ax = plt.subplots()

    for temp in temps:
        ax.scatter(
            np.tile(temp, len(df)),
            df.filter(regex=(f"Pvap_{float(temp):.0f}K")),
            c=clrs,
            s=180,
            alpha=0.1,
        )
    ax.scatter(
        R125.expt_Pvap.keys(),
        R125.expt_Pvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(220,320)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([220,230,240,250,260,270,290,300,310], minor=True)
    ax.set_yticks([0,10,20])
    ax.set_yticks([2,4,6,8,12,14,16,18,22,24,26], minor=True)
    #ax.set_yscale("log")
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{P_{vap}}$ (bar)", fontsize=32, labelpad=10)

    fig.tight_layout()
    fig.savefig("fig1-pvap-r125.pdf")

    # Plot Enthalpy of Vaporization
    fig, ax = plt.subplots()
    for temp in temps:
        ax.scatter(
            np.tile(temp, len(df)),
            df.filter(regex=(f"Hvap_{float(temp):.0f}K")),
            c=clrs,
            s=180,
            alpha=0.1,
        )
    ax.scatter(
        R125.expt_Hvap.keys(),
        R125.expt_Hvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(220,320)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([220,230,240,250,260,270,290,300,310], minor=True)
    ax.set_yticks([100, 125, 150, 175])
    ax.set_yticks([85,90,95,105,110,115,120,130,135,140,145,155,160,165,170], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{\Delta H_{vap}}$ (kJ/kg)", fontsize=32, labelpad=10)


    fig.tight_layout()
    fig.savefig("fig1-hvap-r125.pdf")

    df["mape_norm_tot"] = (
        df["mape_Tc"] / df["mape_Tc"].max() +
        df["mape_rhoc"] / df["mape_rhoc"].max() +
        df["mape_Pvap"] / df["mape_Pvap"].max() +
        df["mape_Hvap"] / df["mape_Hvap"].max()
    )
    topn = df.sort_values("mape_norm_tot")[:5]

    # Plot VLE envelopes
    clrs = seaborn.color_palette('bright', n_colors=len(topn))

    fig, ax = plt.subplots()
    temps = R125.expt_liq_density.keys()
    for temp in temps:
        ax.scatter(
            topn.filter(regex=(f"liq_density_{float(temp):.0f}K")),
            np.tile(temp, len(topn)),
            c=clrs,
            s=180,
            alpha=0.2,
        )
        ax.scatter(
            topn.filter(regex=(f"vap_density_{float(temp):.0f}K")),
            np.tile(temp, len(topn)),
            c=clrs,
            s=180,
            alpha=0.2,
        )
    ax.scatter(
        topn.filter(regex=("sim_rhoc")),
        topn.filter(regex=("sim_Tc")),
        c=clrs,
        s=180,
        alpha=0.2,
    )
    ax.scatter(
        R125.expt_liq_density.values(),
        R125.expt_liq_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(
        R125.expt_vap_density.values(),
        R125.expt_vap_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(R125.expt_rhoc, R125.expt_Tc, color="black", marker="x", s=240)

    ax.set_ylim(220,360)
    ax.set_yticks([240, 280, 320, 360])
    ax.set_yticks([230,250,260,270,290,300,310,330,340,350], minor=True)
    ax.set_xticks([0,400,800,1200,1600])
    ax.set_xticks([100,200,300,500,600,700,900,1000,1100,1300,1400,1500], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_ylabel("T (K)", fontsize=32, labelpad=20)
    ax.set_xlabel(r"$\mathregular{\rho}$ (kg/m$\mathregular{^3}$)", fontsize=32, labelpad=10)
    fig.tight_layout()
    fig.savefig("fig1-vle-top-r125.pdf")

    # Plot Vapor Pressure
    fig, ax = plt.subplots()

    for temp in temps:
        ax.scatter(
            np.tile(temp, len(topn)),
            topn.filter(regex=(f"Pvap_{float(temp):.0f}K")),
            c=clrs,
            s=180,
            alpha=0.2,
        )
    ax.scatter(
        R125.expt_Pvap.keys(),
        R125.expt_Pvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(220,320)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([220,230,240,250,260,270,290,300,310], minor=True)
    ax.set_yticks([0,10,20])
    ax.set_yticks([2,4,6,8,12,14,16,18,22,24,26], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{P_{vap}}$ (bar)", fontsize=32, labelpad=10)

    fig.tight_layout()
    fig.savefig("fig1-pvap-top-r125.pdf")

    # Plot Enthalpy of Vaporization
    fig, ax = plt.subplots()
    for temp in temps:
        ax.scatter(
            np.tile(temp, len(topn)),
            topn.filter(regex=(f"Hvap_{float(temp):.0f}K")),
            c=clrs,
            s=180,
            alpha=0.2,
        )
    ax.scatter(
        R125.expt_Hvap.keys(),
        R125.expt_Hvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(220,320)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([220,230,240,250,260,270,290,300,310], minor=True)
    ax.set_yticks([100, 125, 150, 175])
    ax.set_yticks([85,90,95,105,110,115,120,130,135,140,145,155,160,165,170], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{\Delta H_{vap}}$ (kJ/kg)", fontsize=32, labelpad=10)


    fig.tight_layout()
    fig.savefig("fig1-hvap-top-r125.pdf")


if __name__ == "__main__":
    main()
