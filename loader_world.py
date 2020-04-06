import collections
import urllib.request
from enum import Enum


def to_incr(values):
    return [j-i for i, j in zip(values[:-1], values[1:])]


def avg(values):
    return sum(values)/len(values)


class Type(Enum):
    CONFIRMED = 2
    RECOVERED = 3
    DEATHS = 4
    ACTIVE = 5


class Loader:
    url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'

    def __init__(self):
        lines = urllib.request.urlopen(Loader.url).read().decode().split('\n')
        self.data = []

        for line in lines[1:-1]:
            l = line.replace('"Korea, South"', 'South Korea')
            date, country, confirmed, recovered, deaths = l.split(',')
            self.data.append((date, country, int(confirmed), int(recovered), int(deaths),
                              int(confirmed)-(int(recovered) + int(deaths))))

    @property
    def countries(self):
        countries = []
        for line in self.data:
            country = line[1]
            if country in countries:
                break
            else:
                countries.append(country)
        return countries

    @property
    def dates(self):
        dates = []
        for line in self.data:
            date = line[0]
            if date in dates:
                pass
            else:
                dates.append(date)
        return dates

    def get(self, country, type: Type):
        ret = [(line[0], line[type.value]) for line in self.data if line[1] == country]
        return list(zip(*ret))


class Country:
    def __init__(self, name, loader: Loader):
        self.name = name
        self.dates, self.confirmed = loader.get(name, Type.CONFIRMED)
        self.recovered = loader.get(name, Type.RECOVERED)[1]
        self.deaths = loader.get(name, Type.DEATHS)[1]
        self.active = loader.get(name, Type.ACTIVE)[1]

    def __repr__(self):
        return self.name

    def active_slope(self, days=7):
        m = max(self.active)
        values = [v/m for v in self.active[len(self.active)-days:]]
        return avg(to_incr(values))

    @property
    def outbreak(self):
        return self.confirmed[-1]


if __name__ == '__main__':
    loader = Loader()
    countries = [Country(name, loader) for name in loader.countries]
    print(len(countries))
    countries.sort(key=lambda c: c.active_slope())

