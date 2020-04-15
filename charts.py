import pandas as pd
from data import Column, DataSet, get_active, get_outbreak, get_deaths, get_dates, get_ordered_outbreaks, Community
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
import matplotlib.ticker as ticker
import numpy as np
import math


def time_repr(dt):
    return pd.to_datetime(str(dt)).strftime('%b %d')


def get_series(df, location, column, increment, average):
    ret = df[df[Column.LOCATION.label] == location][column]

    if increment:
        ret = ret.diff().fillna(0)

    if average > 1:
        ret = ret.ewm(span=average).mean()

    return ret


def grid(df: pd.DataFrame, locs, column: Column,
         width, height, out_name,
         increment=False, average=1):

    fig: plt.Figure = plt.figure(figsize=(width, height), facecolor='papayawhip')
    gs = fig.add_gridspec(math.ceil(len(locs)/4), 4)  # , wspace=0.05, hspace=0.1)

    for i, location in enumerate(locs):
        ax: plt.Axes = fig.add_subplot(gs[i])
        series: pd.Series = get_series(df, location, column.label, increment, average)
        series.plot(ax=ax)

        ax.xaxis.set_visible(False)
        ax.set_facecolor('whitesmoke')

        # Annotate maximum
        max_x = series.idxmax()
        max_y = series.loc[max_x]
        ax.plot(max_x, max_y, 'rx', markersize=8)
        ax.set_ylim(bottom=0)
        # ax.annotate('peak={}\n{}'.format(int(max_y), time_repr(max_x)),
        #             xy=(max_x, max_y), xycoords='data',
        #             xytext=(-50, -0),
        #             textcoords='offset pixels', ha='right', va='top',
        #             arrowprops=dict(arrowstyle='->'),
        #             fontsize='small', fontweight='bold')

        # add month markers
        month = pd.Timestamp(year=series.index.min().year, month=series.index.min().month+1, day=1)
        while month < series.index.max():
            ax.axvline(month, ls=':', color='silver', linewidth=1)
            ax.text(month, -0.01, month.month_name(), va='top', transform=ax.get_xaxis_transform(), color='grey')
            month = month + pd.DateOffset(months=1)

        # add a text box with additional information. To automatically place it in the best place, create
        # a fake legend (legends have a loc='best' feature), as in:
        # https://stackoverflow.com/questions/7045729/automatically-position-text-box-in-matplotlib
        # 3 fake handles, one per line in the fake legend

        handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)] * 2
        labels = [
            # 'confirmed={}'.format(get_outbreak(df, location)),
            # 'active={}'.format(get_active(df, location)),
            # 'deaths={}'.format(get_deaths(df, location)),
            'last={} on {}'.format(int(series.iloc[-1]), time_repr(max_x)),
            'peak={} on {}'.format(int(max_y), time_repr(max_x))

        ]
        legend: plt.legend = ax.legend(handles, labels, fontsize='10',
                                       title=location, facecolor=ax.get_facecolor(),
                                       handlelength=0, handletextpad=0, frameon=False,
                                       loc='upper left' if location != 'China' else 'best')
        legend_title: plt.Text = legend.get_title()
        legend_title.set_fontweight('bold')
        legend_title.set_fontsize(12)
        legend._legend_box.align = "left"

    dates = [time_repr(dt) for dt in get_dates(df)]
    fig.suptitle('{}{}{}, from {} to {}'.format(
        'Daily ' if increment else '',
        column.label,
        ', {} days average'.format(average) if average > 1 else '',
        dates[0],
        dates[-1]),
        fontsize=14, fontweight='bold')

    fig.tight_layout(h_pad=0.1, w_pad=0.8, rect=(0, 0.01, 1, 0.965))
    fig.text(1, 0, 'https://github.com/rivasjm/covid19 ', va='bottom', ha='right')
    fig.savefig(out_name, facecolor=fig.get_facecolor())
    print('![{}]({})'.format(out_name, out_name))


def comparison(df: pd.DataFrame, locs, type: Column, threshold,
               out_name,
               increment=False, average=1):
    fig: plt.Figure = plt.figure(facecolor='papayawhip')
    ax: plt.Axes = fig.subplots()
    ax.yaxis.set_major_locator(ticker.FixedLocator([100, 1000, 10000, 20000, 30000]))
    ax.set_yscale('log')

    for i, location in enumerate(locs):
        series = get_series(df, location, type.label, increment, average)
        series = series[series > threshold].reset_index()[type.label]
        series.plot(ax=ax)

    fig.savefig(out_name, facecolor=fig.get_facecolor())


def date_formatter(x, pos):
    if x.day == 1:
        return x
    else:
        return ''


def heatmap(df: pd.DataFrame, locs, type: Column, out_name,
            increment=False):
    fig: plt.Figure = plt.figure(facecolor='papayawhip', figsize=(15, 7))
    ax: plt.Axes = fig.subplots()
    y_labels = []
    values = []
    x_values = None

    for location in locs:
        series = get_series(df, location, type.label, increment, 1)
        vals = list(series/series.max())
        values.append(vals)
        y_labels.append(location)
        if x_values == None:
            x_values = list(series.index)

    values = np.array(values)
    im = ax.imshow(values, aspect='auto', cmap='OrRd')

    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_yticklabels(y_labels)
    # ax.set_xticks(x_values)
    # ax.set_xticklabels(x_values)
    # plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(date_formatter))

    fig.tight_layout()
    fig.savefig(out_name, facecolor=fig.get_facecolor())


def build_isciii():
    data = DataSet.ISCIII.load()
    locations = [c.label for c in Community]  # Spain + regions in alphabetical order

    grid(data, locations, Column.ACTIVE, 15, 10, 'spain_active.png', increment=False, average=1)
    grid(data, locations, Column.CONFIRMED, 15, 10, 'spain_daily_confirmed.png', increment=True, average=7)
    grid(data, locations, Column.DEATHS, 15, 10, 'spain_daily_deaths.png', increment=True, average=7)
    grid(data, locations, Column.HOSPITALIZED, 15, 10, 'spain_hospitalized.png', increment=False, average=1)
    grid(data, locations, Column.ICU, 15, 10, 'spain_icu.png', increment=False, average=1)


def build_world():
    data = DataSet.WORLD.load()
    locations, outbreaks = zip(*get_ordered_outbreaks(data)[:40])

    grid(data, locations, Column.ACTIVE, 15, 20, 'world_active.png', increment=False, average=1)
    grid(data, locations, Column.CONFIRMED, 15, 20, 'world_daily_confirmed.png', increment=True, average=7)
    grid(data, locations, Column.DEATHS, 15, 20, 'world_daily_deaths.png', increment=True, average=7)
    grid(data, locations, Column.HOSPITALIZED, 15, 20, 'world_daily_hospitalized.png', increment=False, average=1)

    # comparison(data, locations[:10], Column.DEATHS, 5, 'test.png', increment=True, average=7)
    heatmap(data, locations[:20], Column.CONFIRMED, 'heatmap.png', increment=True)


if __name__ == '__main__':
    build_isciii()
    build_world()


