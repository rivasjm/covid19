from loader_world import Loader, Country
import matplotlib.pyplot as plt


def grid(loader, out_name):
    # load country data, sort by position of actives curve
    countries = [Country(name, loader) for name in loader.countries]

    # sort by outbreak size
    countries.sort(key=lambda c: c.outbreak, reverse=True)

    # select 50 bigger outbreak countries
    countries = countries[:40]

    fig: plt.Figure = plt.figure(figsize=(15, 20))
    gs = fig.add_gridspec(10, 4)  # , wspace=0.05, hspace=0.1)

    for i, country in enumerate(countries):
        dates = country.dates
        values = country.active

        ax: plt.Axes = fig.add_subplot(gs[i])
        ax.xaxis.set_visible(False)
        ax.plot(dates, values)

        ax.text(0.05, 0.95, country.name, color='black', transform=ax.transAxes,
                va='top', ha='left', fontsize=12, fontweight='bold')
        ax.text(0.05, 0.80, 'active={}'.format(country.active[-1]), color='k', transform=ax.transAxes,
                va='top', ha='left', fontsize=10, fontweight='normal')
        ax.text(0.05, 0.70, 'confirmed={}'.format(country.confirmed[-1]), color='k', transform=ax.transAxes,
                va='top', ha='left', fontsize=10, fontweight='normal')
        ax.text(0.05, 0.60, 'recovered={}'.format(country.recovered[-1]), color='k', transform=ax.transAxes,
                va='top', ha='left', fontsize=10, fontweight='normal')
        ax.text(0.05, 0.50, 'deaths={}'.format(country.deaths[-1]), color='k', transform=ax.transAxes,
                va='top', ha='left', fontsize=10, fontweight='normal')

    dates = loader.dates
    fig.suptitle('Active Cases, for {} largest outbreaks ({}->{})'.format(len(countries), dates[0], dates[-1]),
                 fontsize=14, fontweight='bold')
    fig.tight_layout(h_pad=0.5, w_pad=1, rect=(0, 0.01, 1, 0.965))
    fig.text(1, 0, 'https://github.com/rivasjm/covid19\ndataset:https://github.com/datasets/covid-19', va='bottom', ha='right')
    fig.savefig(out_name)
    print('![{}]({})'.format(out_name, out_name))  # ![charts/casos_hab.png](/charts/casos_hab.png)


def build():
    loader = Loader()
    grid(loader, "world_active.png")
