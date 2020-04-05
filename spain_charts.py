import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
from loader_spain import *
import numpy as np


def int_formatter(x, pos):
    """Value and tick position"""
    return "{:d}".format(int(x))


def grid(data: Data, out_name, rows, cols,
             sizex=20, sizey=15, incremental = False, share_y = False, per_capita=False,
             bars=False, overview=False, yticks=None, log=False, avg_window=1):

    fig: plt.Figure = plt.figure(figsize=(sizex, sizey))
    gs = fig.add_gridspec(rows, cols) #, wspace=0.05, hspace=0.1)
    dates = data.dates(avg_w=avg_window)

    for i, community in enumerate(list(Community)):
        ax: plt.Axes = fig.add_subplot(gs[i])
        plot_func = ax.bar if bars else ax.plot

        if log:
            ax.set_yscale('log')

        # plot background communities
        if overview:
            if bars:
                background_values = data.values(Community.ESPANA, incremental, per_capita, avg_w=avg_window)
                plot_func(dates, background_values, color='silver')
            else:
                for c in list(Community):
                    background_values = data.values(c, incremental, per_capita, avg_w=avg_window)
                    plot_func(dates, background_values, color='silver')
                    if i % cols == cols-1:
                        ax.text(len(dates)-1, background_values[-1], c.name,
                                fontsize=8, color='dimgrey', horizontalalignment='left')

        values = data.values(community, incremental, per_capita, avg_w=avg_window)
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

    title = data.label + (' diarios' if incremental else ' acumulados') + (' por 100.000 hab.' if per_capita else '')  + \
            ' (' + dates[0] + '->' + dates[-1] + ')' + (' (media 7 dias)' if avg_window > 1 else '')

    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout(h_pad=0.5, w_pad=0.1, rect=(0, 0, 1, 0.96))
    fig.text(1, 0, 'https://github.com/rivasjm/covid19', va='bottom', ha='right')
    fig.savefig(out_name)
    print('![{}]({})'.format(out_name, out_name))  # ![charts/casos_hab.png](/charts/casos_hab.png)


def overview(community: Community, out_name):
    fig: plt.Figure = plt.figure(figsize=(12, 6))
    ax: plt.Axes = fig.subplots()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # CASOS
    dates = Data.CASOS.dates()
    values = Data.CASOS.values(community)
    ax.plot(dates, values, color='royalblue', linewidth=1)
    ax.fill_between(dates, values, [0]*len(dates), facecolor='skyblue')
    ax.text(len(dates)-1, values[-1], ' Casos={}'.format(values[-1]), va='center')

    # ALTAS
    v = Data.ALTAS.values(community)
    values = [0]*(len(dates)-len(v)) + v
    ax.plot(dates, values, color='olivedrab', linewidth=1)
    ax.fill_between(dates, values, [0] * len(dates), facecolor='lightgreen')
    ax.text(len(dates) - 1, values[-1], ' Recuperados={}'.format(values[-1]), va='center')

    # FALLECIDOS
    v = Data.FALLECIDOS.values(community)
    values = [0] * (len(dates) - len(v)) + v
    ax.plot(dates, values, color='red', linewidth=1)
    ax.fill_between(dates, values, [0] * len(dates), facecolor='lightsalmon')
    ax.text(len(dates) - 1, values[-1], ' Fallecidos={}'.format(values[-1]), va='center')

    # label the chart
    ax.text(0.02, 0.95, community.name, color='dimgrey', transform=ax.transAxes, va='top', ha='left',
            fontsize=18, fontweight='bold')

    # rotate x tick labels
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, ha='center')

    ax.set_ylim(bottom=0)

    # inset for active cases
    ax = fig.add_axes([.22, 0.5, .15, .2], facecolor='w')
    plot_active_cases(community, ax)

    fig.text(1, 0, 'https://github.com/rivasjm/covid19', va='bottom', ha='right')
    fig.savefig(out_name)
    print('![{}]({})'.format(out_name, out_name))  # ![charts/casos_hab.png](/charts/casos_hab.png)


def plot_active_cases(community: Community, ax: plt.Axes):
    fechas = Data.CASOS.dates()
    casos = np.asarray(Data.CASOS.values(community))
    fallecidos = np.asarray(pad(Data.FALLECIDOS.values(community), len(casos)))
    altas = np.asarray(pad(Data.ALTAS.values(community), len(casos)))
    activos = casos-(altas+fallecidos)
    ax.plot(fechas, activos)

    ax.text(len(fechas)-1, activos[-1], ' activos={}'.format(activos[-1]), va='center', ha='left', fontsize='8')

    ax.xaxis.set_visible(False)
    ax.set_title('casos activos', fontsize=10)

    labels = ax.get_yticklabels()
    plt.setp(labels, fontsize=8)

    ax.set_ylim(bottom=0)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


def pad(seq, length, padding=0):
    return [padding]*(max(0, length-len(seq))) + seq


if __name__ == '__main__':
    # overview for spain
    overview(Community.ESPANA, 'overview.png')

    plt.style.use('Solarize_Light2')  # ft like style
    grid(Data.CASOS, "casos_diarios_per_capita.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=True, avg_window=7, overview=True)
    grid(Data.CASOS, "casos_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False, avg_window=7)
    grid(Data.FALLECIDOS, "fallecidos_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False, avg_window=7)
    grid(Data.UCI, "uci_diarios.png", 7, 3, sizex=12, sizey=17, incremental=True, per_capita=False, avg_window=7)
    grid(Data.CASOS, "casos_per_capita.png", 7, 3, sizex=12, sizey=17, incremental=False, per_capita=True, overview=True)
    grid(Data.CASOS, "casos.png", 7, 3, sizex=12, sizey=17, incremental=False, per_capita=False, overview=True, log=True)


