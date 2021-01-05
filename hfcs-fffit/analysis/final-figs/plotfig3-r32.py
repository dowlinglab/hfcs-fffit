import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn

sys.path.append("../")

from utils.r32 import R32Constants

R32 = R32Constants()

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

df = pd.read_csv("../csv/r32-pareto.csv", index_col=0)
df_gaff = pd.read_csv("../csv/r32-gaff.csv", index_col=0)
df_rabbe = pd.read_csv("../csv/r32-rabbe.csv", index_col=0)


def main():

    # Plot VLE envelopes
    clrs = seaborn.color_palette('bright', n_colors=len(df))
    np.random.seed(11)
    np.random.shuffle(clrs)

    fig, ax = plt.subplots()
    temps = R32.expt_liq_density.keys()
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
        R32.expt_liq_density.values(),
        R32.expt_liq_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(
        R32.expt_vap_density.values(),
        R32.expt_vap_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(R32.expt_rhoc, R32.expt_Tc, color="black", marker="x", s=240)

    ax.set_ylim(230,370)
    ax.set_yticks([240, 280, 320, 360])
    ax.set_yticks([250,260,270,290,300,310,330,340,350], minor=True)
    ax.set_xticks([0,400,800,1200])
    ax.set_xticks([100,200,300,500,600,700,900,1000,1100,1300], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_ylabel("T (K)", fontsize=32, labelpad=10)
    ax.set_xlabel(r"$\mathregular{\rho}$ (kg/m$\mathregular{^3}$)", fontsize=32, labelpad=20)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    fig.tight_layout()
    fig.savefig("pdfs/fig3-vle-r32.pdf")

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
        R32.expt_Pvap.keys(),
        R32.expt_Pvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(230,330)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([250,260,270,290,300,310,330], minor=True)
    ax.set_yticks([0,10,20,30])
    ax.set_yticks([2,4,6,8,12,14,16,18,22,24,26,28,32,34], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{P_{vap}}$ (bar)", fontsize=32, labelpad=10)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)


    fig.tight_layout()
    fig.savefig("pdfs/fig3-pvap-r32.pdf")

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
        R32.expt_Hvap.keys(),
        R32.expt_Hvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(230,330)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([250,260,270,290,300,310,330], minor=True)
    ax.set_yticks([200, 250, 300, 350])
    ax.set_yticks([210,220,230,240,260,270,280,390,310,320,330,340,360,370,380], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{\Delta H_{vap}}$ (kJ/kg)", fontsize=32, labelpad=10)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    fig.tight_layout()
    fig.savefig("pdfs/fig3-hvap-r32.pdf")

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
    temps = R32.expt_liq_density.keys()
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
        R32.expt_liq_density.values(),
        R32.expt_liq_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(
        R32.expt_vap_density.values(),
        R32.expt_vap_density.keys(),
        color="black",
        marker="x",
        s=240,
    )
    ax.scatter(R32.expt_rhoc, R32.expt_Tc, color="black", marker="x", s=240)

    ax.set_ylim(230,370)
    ax.set_yticks([240, 280, 320, 360])
    ax.set_yticks([250,260,270,290,300,310,330,340,350], minor=True)
    ax.set_xticks([0,400,800,1200])
    ax.set_xticks([100,200,300,500,600,700,900,1000,1100,1300], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_ylabel("T (K)", fontsize=32, labelpad=10)
    ax.set_xlabel(r"$\mathregular{\rho}$ (kg/m$\mathregular{^3}$)", fontsize=32, labelpad=10)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    fig.tight_layout()
    fig.savefig("pdfs/fig3-vle-top-r32.pdf")

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
        R32.expt_Pvap.keys(),
        R32.expt_Pvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(230,330)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([250,260,270,290,300,310,330], minor=True)
    ax.set_yticks([0,10,20,30])
    ax.set_yticks([2,4,6,8,12,14,16,18,22,24,26,28,32,34], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{P_{vap}}$ (bar)", fontsize=32, labelpad=10)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)

    fig.tight_layout()
    fig.savefig("pdfs/fig3-pvap-top-r32.pdf")

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
        R32.expt_Hvap.keys(),
        R32.expt_Hvap.values(),
        color="black",
        marker="x",
        s=240,
    )

    ax.set_xlim(230,330)
    ax.set_xticks([240, 280, 320])
    ax.set_xticks([250,260,270,290,300,310,330], minor=True)
    ax.set_yticks([200, 250, 300, 350])
    ax.set_yticks([210,220,230,240,260,270,280,390,310,320,330,340,360,370,380], minor=True)
    ax.tick_params("both", direction="in", which="both", length=4, labelsize=26, pad=10)
    ax.tick_params("both", which="major", length=8)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    ax.set_xlabel("T (K)", fontsize=32, labelpad=20)
    ax.set_ylabel(r"$\mathregular{\Delta H_{vap}}$ (kJ/kg)", fontsize=32, labelpad=10)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)


    fig.tight_layout()
    fig.savefig("pdfs/fig3-hvap-top-r32.pdf")


if __name__ == "__main__":
    main()
