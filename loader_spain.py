from enum import Enum
import urllib.request

class Community(Enum):
    ESPANA = {'key': 'Total', 'population': 47026208, 'label': 'España', 'iso':'ES'}
    ANDALUCIA = {'key': 'Andalucía', 'population': 8414240, 'iso':'AN'}
    ARAGON = {'key': 'Aragón', 'population': 1319291, 'iso':'AR'}
    ASTURIAS = {'key': 'Asturias', 'population': 1022800, 'iso':'AS'}
    BALEARES = {'key': 'Baleares', 'population': 1149460, 'iso':'IB'}
    CANARIAS = {'key': 'Canarias', 'population': 2153389, 'iso':'CN'}
    CANTABRIA = {'key': 'Cantabria', 'population': 581078, 'iso':'CB'}
    CASTILLA_LA_MANCHA = {'key': 'Castilla-La Mancha', 'population': 2032863, 'iso':'CM'}
    CASTILLA_Y_LEON = {'key': 'Castilla y León', 'population': 2399548, 'iso':'CL'}
    CATALUNA = {'key': 'Cataluña', 'population': 7675217, 'iso':'CT'}
    CEUTA = {'key': 'Ceuta', 'population': 84777, 'iso':'CE'}
    VALENCIA = {'key': 'C. Valenciana', 'population': 5003769, 'iso':'VC'}
    EXTREMADURA = {'key': 'Extremadura', 'population': 1067710, 'iso':'EX'}
    GALICIA = {'key': 'Galicia', 'population': 2699499, 'iso':'GA'}
    MADRID = {'key': 'Madrid', 'population': 6663394, 'iso':'MD'}
    MELILLA = {'key': 'Melilla', 'population': 86487, 'iso':'ME'}
    MURCIA = {'key': 'Murcia', 'population': 1493898, 'iso':'MC'}
    NAVARRA = {'key': 'Navarra', 'population': 654214, 'iso':'NC'}
    PAIS_VASCO = {'key': 'País Vasco', 'population': 2207776, 'iso':'PV'}
    LA_RIOJA = {'key': 'La Rioja', 'population': 316798, 'iso':'RI'}


    @property
    def key(self):
        return self.value['key']

    @property
    def name(self):
        return self.value['label'] if 'label' in self.value else self.value['key']

    @property
    def population(self):
        return self.value['population']

    @property
    def iso(self):
        return self.value['iso']

    @staticmethod
    def communities():
        return [c for c in list(Community) if c != Community.ESPANA]

    @staticmethod
    def total():
        return Community.ESPANA

    @staticmethod
    def from_iso(iso):
        ret = [c for c in list(Community) if c.iso == iso]
        return ret[0] if len(ret) > 0 else None


class Data(Enum):
    CASOS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv', 'Casos')  #('datasets/COVID 19/ccaa_covid19_casos.csv', 'Casos')
    ALTAS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_altas.csv', 'Altas')
    FALLECIDOS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos.csv', 'Fallecidos')
    HOSPITALIZADOS = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_hospitalizados.csv', 'Hospitalizados')
    UCI = ('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_uci.csv', 'Ingresos en UCIs')

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

    def dates(self, avg_w=1):
        if avg_w > 1 and avg_w <= len(self.__dates):
            return self.__dates[avg_w-1:]
        return self.__dates

    def values(self, community: Community, incremental=False, per_capita=False, per_capita_factor=100000, avg_w=1):
        values: list = self.__data[community.key][:]

        if incremental:
            values.insert(0, 0)
            values = [j-i for i, j in zip(values[:-1], values[1:])]

        if per_capita:
            values = [(v/community.population)*float(per_capita_factor) for v in values]

        if avg_w > 1 and avg_w <= len(values):
            ret = []
            i = 0
            while i+avg_w-1 < len(values):
                slice = values[i:i+avg_w]
                ret.append(sum(slice)/len(slice))
                i += 1
            values = ret

        return values
