from enum import Enum


class Community(Enum):
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
    ESPANA = {'key': 'Total', 'population': 47026208, 'label': 'España'}


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
    CASOS = {'path': '../spain/datasets/COVID 19/ccaa_covid19_casos.csv', 'label': 'Casos'}
    ALTAS = {'path': '../spain/datasets/COVID 19/ccaa_covid19_altas.csv', 'label': 'Altas'}
    FALLECIDOS = {'path': '../spain/datasets/COVID 19/ccaa_covid19_fallecidos.csv', 'label': 'Fallecidos'}
    HOSPITALIZADOS = {'path': '../spain/datasets/COVID 19/ccaa_covid19_hospitalizados.csv', 'label': 'Hospitalizados'}
    UCI = {'path': '../spain/datasets/COVID 19/ccaa_covid19_uci.csv', 'label': 'Hospitalizados en UCIs'}

    @property
    def path(self):
        return self.value['path']

    @property
    def label(self):
        return self.value['label']


class Parser:
    def __init__(self, source: Data):
        self.source = source
        file = source.path
        raw = [line.split(',') for line in open(file).readlines()]
        self.dates = [self.__process_date(date) for date in raw[0][2:]]
        self.data = {line[1]: line[2:] for line in raw[1:]}

    def get(self, community: Community, incremental: bool = False, per_capita: bool = False):
        if incremental:
            ret = self.__incremental(community)
        else:
            ret = list(map(int, self.data[community.key]))

        if (per_capita) :
            population = community.population if per_capita else 1
            return [v/population*100000 for v in ret]
        else:
            return ret

    def __incremental(self, community: Community):
        cumulative = self.get(community)
        ret = [0]
        inc = [j-i for i, j in zip(cumulative[:-1], cumulative[1:])]
        ret.extend(inc)
        return ret

    @property
    def communities(self):
        return Community.communities()

    @staticmethod
    def __process_date(date: str):
        month, day = date.rstrip('\n').split('-')[1:]
        return day + '-' + month


if __name__ == '__main__':
    parser = Parser(Data.CASOS)
    # print(parser.communities)
    # print(parser.total)
    # print(parser.dates)
    # print(parser.incremental(Community.ANDALUCIA))
    # y = parser.get(Community.CEUTA)

    v = parser.get(Community.CANTABRIA, per_capita=True)
    print(v)


