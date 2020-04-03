import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter, FuncFormatter
from loader_spain import *


def int_formatter(x, pos):
    """Value and tick position"""
    return "{:d}".format(int(x))


class Ax_Iterator:
    def __init__(self, fig: plt.Figure, rows, cols):
        self.fig = fig
        self.gs: plt.GridSpec = fig.add_gridspec(rows, cols)
        self.i = 0

    def get_ax(self, span) -> plt.Axes:
        size = self.gs.ncols*self.gs.nrows
        if self.i+span >= size:
            raise ValueError

        ax = self.fig.add_subplot(self.gs[self.i:self.i + span])
        self.i += span
        return ax


def plot_bars(data: Data, community: Community, ax: plt.Axes, incremental: bool = False, xticklabels: bool = True):
    parser = Parser(data)
    dates = parser.dates
    values = parser.get(community, incremental)

    ax.bar(dates, values)

    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set(ylabel=data.label + (' (cada día)' if incremental else ' (acumulados)'),
           title=community.name)
    ax.xaxis.set_visible(xticklabels)


def plot_lines(data: Data, community: Community, ax: plt.Axes,
               per_capita: bool = False, incremental: bool = False, overview: bool = False, log: bool = True,
               xticklabels: bool = True):

    parser = Parser(data)
    dates = parser.dates
    if log:
        ax.set_yscale('symlog')
        ax.yaxis.set_major_formatter(FuncFormatter(int_formatter))

    # Show rest of communities data as background lines (greyed out)
    if overview:
        for c in Community.communities():
            if c == community:
                continue
            values = parser.get(c, incremental, per_capita)
            line: plt.Line2D = ax.plot(dates, values)[0]
            line.set(color='silver', linewidth=1)

            ax.text(len(dates)-1, values[-1], c.name, fontsize=8, color='dimgrey', horizontalalignment='left')

    # Plot line for
    values = parser.get(community, incremental, per_capita)
    line: plt.Line2D = ax.plot(dates, values)[0]
    line.set(color='darkviolet', linewidth=2)

    ax.xaxis.set_visible(xticklabels)

    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    ylabel = data.label + (' por 100000 hab.' if per_capita else '') + (' (cada día)' if incremental else '')
    ax.set(ylabel=ylabel, title=community.name)


def build_bars(data: Data, file_name, rows, cols, incremental: bool = False):
    fig: plt.Figure = plt.figure(figsize=(20, 15))
    fig.suptitle(data.label + (' (cada día)' if incremental else ''),
                 y=0.99, x=0.5, fontsize=20, fontweight='bold')

    ax_iter = Ax_Iterator(fig, rows, cols)
    main_ax = ax_iter.get_ax(span=2)
    plot_bars(data, Community.ESPANA, main_ax, incremental)

    for i, community in enumerate(Community.communities()):
        ax = ax_iter.get_ax(span=1)
        plot_bars(data, community, ax, incremental, xticklabels=False)

    ax_iter.gs.tight_layout(fig, rect=(0, 0, 1, 0.965))
    fig.savefig(file_name)
    # print("![{}](/{})".format(file_name, file_name))


def build_lines(data: Data, file_name, rows, cols, per_capita: bool = False, incremental: bool = False, overview: bool = False, log: bool = True):
    fig: plt.Figure = plt.figure(figsize=(20, 15))
    fig.suptitle(data.label + (' por 100000 hab.' if per_capita else '') + (' (cada día)' if incremental else ''),
                 y=0.99, x=0.5, fontsize=20, fontweight='bold')

    ax_iter = Ax_Iterator(fig, rows, cols)
    main_ax = ax_iter.get_ax(span=2)
    plot_lines(data, Community.ESPANA, main_ax, per_capita, incremental, overview, log, xticklabels=True)

    for i, community in enumerate(Community.communities()):
        ax = ax_iter.get_ax(span=1)
        plot_lines(data, community, ax, per_capita, incremental, overview, log, xticklabels=False)

    ax_iter.gs.tight_layout(fig, rect=(0, 0, 1, 0.965))
    fig.savefig(file_name)
    # print("![{}](/{})".format(file_name, file_name))


plt.style.use('Solarize_Light2')

build_lines(Data.CASOS, 'charts/casos_hab.png', 5, 5, log=False, overview=True, per_capita=True, incremental=False)
build_lines(Data.FALLECIDOS, 'charts/fallecidos_hab.png', 5, 5, log=False, overview=True, per_capita=True, incremental=False)
build_lines(Data.CASOS, 'charts/casos.png', 5, 5, log=True, overview=True, per_capita=False, incremental=False)
build_lines(Data.FALLECIDOS, 'charts/fallecidos.png', 5, 5, log=True, overview=True, per_capita=False, incremental=False)

build_bars(Data.CASOS, 'charts/casos_diario.png', 5, 5, incremental=True)
build_bars(Data.FALLECIDOS, 'charts/fallecidos_diario.png', 5, 5, incremental=True)
build_bars(Data.UCI, 'charts/uci_diario.png', 5, 5, incremental=True)
build_bars(Data.HOSPITALIZADOS, 'charts/hospitalizados_diario.png', 5, 5, incremental=True)
build_bars(Data.ALTAS, 'charts/altas_diario.png', 5, 5, incremental=True)

