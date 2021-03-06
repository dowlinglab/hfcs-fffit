import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn

sys.path.append("../../")

from scipy.stats import linregress
from utils.r32 import R32Constants
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

R32 = R32Constants()

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

df = pd.read_csv("../../csv/r32-pareto.csv", index_col=0)
df_gaff = pd.read_csv("../../csv/r32-gaff.csv", index_col=0)
df_raabe = pd.read_csv("../../csv/r32-raabe.csv", index_col=0)


def main():

    # Plot VLE envelopes
    clrs = seaborn.color_palette('bright', n_colors=len(df))
    np.random.seed(11)
    np.random.shuffle(clrs)

    fig, ax = plt.subplots(figsize=(8,6))
    temps = R32.expt_liq_density.keys()

    tc, rhoc = calc_critical(df_gaff)
    ax.scatter(
        df_gaff["rholiq_kgm3"],
        df_gaff["T_K"],
        c='gray',
        s=120,
        alpha=0.7,
        label="GAFF",
        marker='s',
    )
    ax.scatter(
        df_gaff["rhovap_kgm3"],
        df_gaff["T_K"],
        c='gray',
        s=120,
        alpha=0.7,
        marker='s',
    )
    ax.scatter(
        rhoc,
        tc,
        c='gray',
        s=120,
        alpha=0.7,
        marker='s',
    )

    tc, rhoc = calc_critical(df_raabe)
    ax.scatter(
        df_raabe["rholiq_kgm3"],
        df_raabe["T_K"],
        c='#0989d9',
        s=140,
        alpha=0.7,
        label="Raabe",
        marker='^',
    )
    ax.scatter(
        df_raabe["rhovap_kgm3"],
        df_raabe["T_K"],
        c='#0989d9',
        s=140,
        alpha=0.7,
        marker='^',
    )
    ax.scatter(
        rhoc,
        tc,
        c='#0989d9',
        s=140,
        alpha=0.7,
        marker='^',
    )

    ax.scatter(
        R32.expt_liq_density.values(),
        R32.expt_liq_density.keys(),
        color="black",
        marker="x",
        linewidths=3,
        s=220,
        label="Experiment",
        zorder=-1,
    )
    ax.scatter(
        R32.expt_vap_density.values(),
        R32.expt_vap_density.keys(),
        color="black",
        marker="x",
        linewidths=3,
        s=220,
        zorder=-1,
    )
    ax.scatter(R32.expt_rhoc, R32.expt_Tc, color="black", marker="x", linewidths=3, s=220, zorder=-1)
    ax.text(0.65, 0.8, "HFC-32", fontsize=34, transform=ax.transAxes)

    ax.set_xlim(-100, 1550)
    ax.xaxis.set_major_locator(MultipleLocator(400))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    
    ax.set_ylim(220,380)
    ax.yaxis.set_major_locator(MultipleLocator(40))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_ylabel("T (K)", fontsize=32, labelpad=15)
    ax.set_xlabel(r"$\mathregular{\rho}$ (kg/m$\mathregular{^3}$)", fontsize=32, labelpad=12)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    ax.legend(loc="lower left", bbox_to_anchor=(-0.1, 1.0), ncol=3, fontsize=20, handletextpad=0.1, markerscale=0.8)
    fig.subplots_adjust(bottom=0.3, top=0.85, left=0.25, right=0.95)
    fig.savefig("ffo_pdfs/vle-r32_prev.pdf")

    # Plot Vapor Pressure
    fig, ax = plt.subplots(figsize=(8,6))

    ax.scatter(
        1000/df_gaff["T_K"],
        df_gaff["pvap_bar"],
        c='gray',
        s=120,
        alpha=0.7,
        label="GAFF",
        marker='s',
    )
    ax.scatter(
        1000/df_raabe["T_K"],
        df_raabe["pvap_bar"],
        c='#0989d9',
        s=140,
        alpha=0.7,
        label="Raabe",
        marker='^',
    )
    ax.scatter(
        1000/np.array(list(R32.expt_Pvap.keys())),
        R32.expt_Pvap.values(),
        color="black",
        marker="x",
        linewidths=3,
        s=220,
        label="Experiment",
        zorder=-1,
    )

    ax.set_xlim(2.9,4.3)
    ax.xaxis.set_major_locator(MultipleLocator(0.3))
    ax.xaxis.set_minor_locator(AutoMinorLocator(3))

    ax.set_ylim(1,100)
    #ax.yaxis.set_major_locator(MultipleLocator(10))
    #ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    ax.set_yscale("log")

    ax.set_xlabel(r"1000 / T (K$^{-1}$)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{P_{vap}}$ (bar)", fontsize=32, labelpad=20)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    ax.legend(loc="lower left", bbox_to_anchor=(-0.1, 1.05), ncol=3, fontsize=20, handletextpad=0.1, markerscale=0.8)
    ax.text(0.65, 0.8, "HFC-32", fontsize=34, transform=ax.transAxes)
    fig.subplots_adjust(bottom=0.3, top=0.85, left=0.25, right=0.95)
    fig.savefig("ffo_pdfs/pvap-r32_prev.pdf")


    # Plot Enthalpy of Vaporization
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(
        df_gaff["T_K"],
        df_gaff["hvap_kJmol"] / R32.molecular_weight * 1000.0,
        c='gray',
        s=120,
        alpha=0.7,
        label="GAFF",
        marker='s',
    )
    ax.scatter(
        df_raabe["T_K"],
        df_raabe["hvap_kJmol"] / R32.molecular_weight * 1000.0,
        c='#0989d9',
        s=140,
        alpha=0.7,
        label="Raabe",
        marker='^',
    )
    ax.scatter(
        R32.expt_Hvap.keys(),
        R32.expt_Hvap.values(),
        color="black",
        marker="x",
        linewidths=3,
        s=220,
        label="Experiment",
        zorder=-1,
    )

    ax.set_xlim(220,330)
    ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_minor_locator(AutoMinorLocator(3))

    ax.set_ylim(-10,410)
    ax.yaxis.set_major_locator(MultipleLocator(100))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{\Delta H_{vap}}$ (kJ/kg)", fontsize=32, labelpad=20)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    ax.legend(loc="lower left", bbox_to_anchor=(-0.1, 1.0), ncol=3, fontsize=20, handletextpad=0.1, markerscale=0.8)
    ax.text(0.65, 0.8, "HFC-32", fontsize=34, transform=ax.transAxes)
    fig.subplots_adjust(bottom=0.3, top=0.85, left=0.25, right=0.95)
    fig.savefig("ffo_pdfs/hvap-r32_prev.pdf")


def calc_critical(df):
    """Compute the critical temperature and density

    Accepts a dataframe with "T_K", "rholiq_kgm3" and "rhovap_kgm3"
    Returns the critical temperature (K) and density (kg/m3)

    Computes the critical properties with the law of rectilinear diameters
    """
    temps = df["T_K"].values
    liq_density = df["rholiq_kgm3"].values
    vap_density = df["rhovap_kgm3"].values
    # Critical Point (Law of rectilinear diameters)
    slope1, intercept1, r_value1, p_value1, std_err1 = linregress(
        temps,
        (liq_density + vap_density) / 2.0,
    )

    slope2, intercept2, r_value2, p_value2, std_err2 = linregress(
        temps,
        (liq_density - vap_density) ** (1 / 0.32),
    )

    Tc = np.abs(intercept2 / slope2)
    rhoc = intercept1 + slope1 * Tc

    return Tc, rhoc

if __name__ == "__main__":
    main()
