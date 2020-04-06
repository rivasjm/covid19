import collections
import urllib.request


def recursively_default_dict():
    return collections.defaultdict(recursively_default_dict)


def load():
    url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
    lines = urllib.request.urlopen(url).read().decode().split('\n')
    data = recursively_default_dict()

    # data[TYPE][COUNTRY]

    for line in lines[1:-1]:
        line = line.replace('"Korea, South"', 'South Korea')
        date, country, confirmed, recovered, deaths = line.split(',')


if __name__ == '__main__':
    load()
