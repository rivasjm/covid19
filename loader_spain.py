from enum import Enum
import urllib.request

class Community(Enum):
    ESPANA = {'key': 'Total', 'population': 47026208, 'label': 'España'}
    ANDALUCIA = {'key': 'Andalucía', 'population': 8414240}
    ARAGON = {'key': 'Aragón', 'population': 1319291}
    ASTURIAS = {'key': 'Asturias', 'population': 1022800}
    BALEARES = {'key': 'Baleares', 'population': 1149460}
    CANARIAS = {'key': 'Canarias', 'population': 2153389}
    CANTABRIA = {'key': 'Cantabria', 'population': 581078}
    CASTILLA_LA_MANCHA = {'key': 'Castilla-La Mancha', 'population': 2032863}
    CASTILLA_Y_LEON = {'key': 'Castilla y León', 'population': 2399548}
    CATALUNA = {'key': 'Cataluña', 'population': 7675217}
    CEUTA = {'key': 'Ceuta', 'population': 84777}
    VALENCIA = {'key': 'C. Valenciana', 'population': 5003769}
    EXTREMADURA = {'key': 'Extremadura', 'population': 1067710}
    GALICIA = {'key': 'Galicia', 'population': 2699499}
    MADRID = {'key': 'Madrid', 'population': 6663394}
    MELILLA = {'key': 'Melilla', 'population': 86487}
    MURCIA = {'key': 'Murcia', 'population': 1493898}
    NAVARRA = {'key': 'Navarra', 'population': 654214}
    PAIS_VASCO = {'key': 'País Vasco', 'population': 2207776}
    LA_RIOJA = {'key': 'La Rioja', 'population': 316798}


    @property
    def key(self):
        return self.value['key']

    @property
    def name(self):
        return self.value['label'] if 'label' in self.value else self.value['key']

    @property
    def population(self):
        return self.value['population']

    @staticmethod
    def communities():
        return [c for c in list(Community) if c != Community.ESPANA]

    @staticmethod
    def total():
        return Community.ESPANA


class Data(Enum):
    CASOS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv', 'Casos')  #('datasets/COVID 19/ccaa_covid19_casos.csv', 'Casos')
    ALTAS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_altas.csv', 'Altas')
    FALLECIDOS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos.csv', 'Fallecidos')
    HOSPITALIZADOS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_hospitalizados.csv', 'Hospitalizados')
    UCI = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_uci.csv', 'Hospitalizados en UCIs')

    def __init__(self, url, label):
        pass
        self.label = label
        req = urllib.request.urlopen(url).read().decode()
        raw = [line.split(',') for line in req.split('\n')]

        # list of date strings
        self.__dates = [self.__process_date(date) for date in raw[0][2:]]
        # Community.key -> list of integer values
        self.__data = {line[1]: list(map(int, line[2:])) for line in raw[1:] if len(line) > 1}

    @staticmethod
    def __process_date(date: str):
        month, day = date.rstrip('\n').split('-')[1:]
        return day + '-' + month

    @property
    def dates(self):
        return self.__dates

    def values(self, community: Community, incremental=False, per_capita=False, per_capita_factor=100000):
        values: list = self.__data[community.key][:]

        if incremental:
            values.insert(0, 0)
            values = [j-i for i, j in zip(values[:-1], values[1:])]

        if per_capita:
            values = [(v/community.population)*float(per_capita_factor) for v in values]

        return values


if __name__ == '__main__':
    req = urllib.request.urlopen('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv').read().decode()
    raw = [line.split(',') for line in req.split('\n')]

    print(raw)
    # print(raw[0][2:])

    # print(raw[1:])
    for line in raw[1:]:
        if len(line) > 1:
            print(line)

    # lines = file.split('\n')
    # for line in lines:
    #     print(line)
    # lines = [line for line in file]
    # for line in lines:
    #     print(line.split(','))
