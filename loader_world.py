import collections
import urllib.request
from enum import Enum


def to_incr(values):
    return [j-i for i, j in zip(values[:-1], values[1:])]


def avg(values):
    return sum(values)/len(values)


def w_avg(values, avg_w):
    if len(values) <= avg_w:
        return values

    ret = []
    i = 0
    while i + avg_w - 1 < len(values):
        w = values[i:i + avg_w]
        ret.append(sum(w) / len(w))
        i += 1
    return ret


class Type(Enum):
    CONFIRMED = 2, 'Confirmed Cases'
    RECOVERED = 3, 'Recovered'
    DEATHS = 4, 'Deaths'
    ACTIVE = 5, 'Active Cases'

    def __init__(self, index, label):
        self.index = index
        self.label = label


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
        ret = [(line[0], line[type.index]) for line in self.data if line[1] == country]
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

    def get(self, type: Type, increment=False, avg_w=1):
        ret = (self.confirmed, self.recovered, self.deaths, self.active)[type.index-2]
        ret = to_incr(ret) if increment else ret
        return w_avg(ret, avg_w) if avg_w>1 else ret

    @property
    def outbreak(self):
        return self.confirmed[-1]
