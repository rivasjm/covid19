import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
from loader_spain import *


def int_formatter(x, pos):
    """Value and tick position"""
    return "{:d}".format(int(x))


def grid(data: Data, out_name, rows, cols,
             sizex=20, sizey=15, incremental = False, share_y = False, per_capita=False,
             bars=False, overview=False, yticks=None, log=False):

    fig: plt.Figure = plt.figure(figsize=(sizex, sizey))
    gs = fig.add_gridspec(rows, cols) #, wspace=0.05, hspace=0.1)
    dates = data.dates

    for i, community in enumerate(list(Community)):
        ax: plt.Axes = fig.add_subplot(gs[i])
        plot_func = ax.bar if bars else ax.plot

        if log:
            ax.set_yscale('log')

        # plot background communities
        if overview:
            if bars:
                background_values = data.values(Community.ESPANA, incremental, per_capita)
                plot_func(dates, background_values, color='silver')
            else:
                for c in list(Community):
                    background_values = data.values(c, incremental, per_capita)
                    plot_func(dates, background_values, color='silver')
                    if i % cols == cols-1:
                        ax.text(len(dates)-1, background_values[-1], c.name,
                                fontsize=8, color='dimgrey', horizontalalignment='left')

        values = data.values(community, incremental, per_capita)
        plot_func(dates, values, color='darkviolet')
        ax.text(0.05, 0.95, community.name, color='dimgrey', transform=ax.transAxes, va='top', ha='left',
                fontsize=12, fontweight='bold')
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(int_formatter))

        if yticks is not None:
            ax.yaxis.set_major_locator(ticker.FixedLocator(yticks))

        if (overview or share_y) and i % cols > 0:
            ax.set_yticklabels([])
            ax.tick_params(axis='y', which='both', length=0)  # hide just the ticks but not the horizontal grid

    title = data.name + (' por 100.000 hab.' if per_capita else '') + (' (diario)' if incremental else '') + \
            ' (' + dates[0] + '->' + dates[-1] + ')'
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout(h_pad=0.5, w_pad=0.1, rect=(0, 0, 1, 0.96))
    fig.savefig(out_name)
    print('![{}]({})'.format(out_name, out_name))  # ![charts/casos_hab.png](/charts/casos_hab.png)


if __name__ == '__main__':
    plt.style.use('Solarize_Light2')  # ft like style

    grid(Data.CASOS, "casos.png", 7, 3, sizex=12, sizey=17, incremental=False, per_capita=False, overview=True, log=True)
    grid(Data.CASOS, "casos_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False)
    grid(Data.CASOS, "casos_per_capita.png", 7, 3, sizex=12, sizey=17, incremental=False, per_capita=True, overview=True)
    grid(Data.HOSPITALIZADOS, "hospital_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False)
    grid(Data.FALLECIDOS, "fallecidos_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False)
    grid(Data.UCI, "uci_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False)
