from loader_world import Loader, Country, Type
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
from collections import defaultdict


def autodict():
    return defaultdict(autodict)


def annotation_offset(type, increment, country):
    offsets = autodict()
    #       type         inc
    offsets[Type.ACTIVE][False] = {'South Korea': (40, -80), 'China': (50, -100)}
    offsets[Type.DEATHS][True] = {'South Korea': (35, -80), 'China': (25, -100), 'Iran': (-10, -80)}
    offsets[Type.CONFIRMED][True] = {'South Korea': (120, -40), 'China': (120, -100)}

    _defaults = autodict()
    _defaults[Type.ACTIVE][False] = -50, -25
    _defaults[Type.DEATHS][True] = -50, -25
    _defaults[Type.CONFIRMED][True] = -20, -25

    try:
        return offsets[type][increment][country]
    except KeyError:
        return _defaults[Type.DEATHS][True]


def grid(loader, type: Type, out_name, increment=False, avg_w=1, linecolor='tab:blue'):
    # load country data, sort by position of actives curve
    countries = [Country(name, loader) for name in loader.countries]

    # sort by outbreak size
    countries.sort(key=lambda c: c.outbreak, reverse=True)

    # select 50 bigger outbreak countries
    countries = countries[:40]

    fig: plt.Figure = plt.figure(figsize=(15, 20), facecolor='#EEE8D5')
    gs = fig.add_gridspec(10, 4)  # , wspace=0.05, hspace=0.1)

    for i, country in enumerate(countries):
        values = country.get(type, increment, avg_w=avg_w)
        dates = country.dates[len(country.dates)-len(values):]

        ax: plt.Axes = fig.add_subplot(gs[i])  # axisbg='#E6E6E6'
        ax.xaxis.set_visible(False)
        ax.set_facecolor('#E6E6E6')
        ax.plot(dates, values, color=linecolor, linewidth=2)

        # country label
        # ax.text(0.05, 0.95, country.name, color='black', transform=ax.transAxes,
        #         va='top', ha='left', fontsize=12, fontweight='bold')

        # annotate peak
        max_index = values.index(max(values))
        ax.annotate('peak={}\n{}'.format(int(values[max_index]), dates[max_index]),
                    xy=(max_index, values[max_index]), xycoords='data',
                    xytext=annotation_offset(type, increment, country.name),
                    textcoords='offset pixels', ha='right', va='top',
                    arrowprops=dict(arrowstyle='->'),
                    fontsize='small', fontweight='bold')

        # add a text bos with additional information. To automatically place it in the best place, create
        # a fake legend (legends have a loc='best' feature), as in:
        # https://stackoverflow.com/questions/7045729/automatically-position-text-box-in-matplotlib

        # 4 fake handles, one per line in the fake legend
        handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)] * 4

        labels = ['active={}'.format(country.active[-1]), 'confirmed={}'.format(country.confirmed[-1]),
                  'recovered={}'.format(country.recovered[-1]), 'deaths={}'.format(country.deaths[-1])]

        legend: plt.legend = ax.legend(handles, labels, loc='best', fontsize='small',
                  title=country.name, facecolor=ax.get_facecolor(),
                  handlelength=0, handletextpad=0, frameon=False)

        legend_title: plt.Text = legend.get_title()
        legend_title.set_fontweight('bold')
        legend_title.set_fontsize(12)
        legend._legend_box.align = "left"

    dates = loader.dates
    fig.suptitle('{} {}, for {} largest outbreaks {} (from {} to {})'.format(
        'Daily' if increment else '', type.label,
        len(countries), '({} days average)'.format(avg_w) if avg_w>1 else '',
        dates[0], dates[-1]), fontsize=14, fontweight='bold')

    fig.tight_layout(h_pad=0.5, w_pad=0.8, rect=(0, 0.01, 1, 0.965))
    fig.text(1, 0, 'https://github.com/rivasjm/covid19\ndataset:https://github.com/datasets/covid-19', va='bottom', ha='right')
    fig.savefig(out_name, facecolor=fig.get_facecolor())
    print('![{}]({})'.format(out_name, out_name))  # ![charts/casos_hab.png](/charts/casos_hab.png)


def build():
    loader = Loader()
    grid(loader, Type.ACTIVE, "world_active.png", increment=False, linecolor='tab:blue')
    grid(loader, Type.CONFIRMED, "world_daily_confirmed.png", increment=True, avg_w=7, linecolor='tab:blue')
    grid(loader, Type.DEATHS, "world_daily_deaths.png", increment=True, avg_w=7, linecolor='tab:red')


if __name__ == '__main__':
    build()
