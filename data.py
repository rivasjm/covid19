import pandas as pd
import datetime as dt
import numpy as np
from enum import Enum
from typing import List, Tuple


class Community(Enum):
    ESPANA = 'Spain', 47026208, 'ES'
    ANDALUCIA = 'Andalucía', 8414240, 'AN'
    ARAGON = 'Aragón', 1319291, 'AR'
    ASTURIAS = 'Asturias', 1022800, 'AS'
    BALEARES = 'Baleares', 1149460, 'IB'
    CANARIAS = 'Canarias', 2153389, 'CN'
    CANTABRIA = 'Cantabria', 581078, 'CB'
    CASTILLA_LA_MANCHA = 'Castilla-La Mancha', 2032863, 'CM'
    CASTILLA_Y_LEON = 'Castilla y León', 2399548, 'CL'
    CATALUNA = 'Cataluña', 7675217, 'CT'
    CEUTA = 'Ceuta', 84777, 'CE'
    VALENCIA = 'C. Valenciana', 5003769, 'VC'
    EXTREMADURA = 'Extremadura', 1067710, 'EX'
    GALICIA = 'Galicia', 2699499, 'GA'
    MADRID = 'Madrid', 6663394, 'MD'
    MELILLA = 'Melilla', 86487, 'ML'
    MURCIA = 'Murcia', 1493898, 'MC'
    NAVARRA = 'Navarra', 654214, 'NC'
    PAIS_VASCO = 'País Vasco', 2207776, 'PV'
    LA_RIOJA = 'La Rioja', 316798, 'RI'

    def __init__(self, label, population, iso):
        self.label = label
        self.population = population
        self.iso = iso


def iso_to_name(iso):
    ret = [c.label for c in list(Community) if c.iso == iso]
    return ret[0] if len(ret) > 0 else iso


class Column(Enum):
    LOCATION = 'Location'
    DATE = 'Date'
    CONFIRMED = 'Cases', True
    HOSPITALIZED = 'Hospitalized', True
    ICU = 'ICU', True
    DEATHS = 'Deaths', True
    RECOVERED = 'Recovered', True
    ACTIVE = 'Active Cases', True

    def __init__(self, label, isdata=False):
        self.label = label
        self.isdata = isdata

    @staticmethod
    def get_data_cols():
        return [c for c in Column if c.isdata]


class DataSet(Enum):
    ISCIII = 'https://covid19.isciii.es/resources/serie_historica_acumulados.csv', \
            (Column.LOCATION, Column.DATE, Column.CONFIRMED, Column.HOSPITALIZED, Column.ICU,
             Column.DEATHS, Column.RECOVERED)

    WORLD = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', \
            (Column.DATE, Column.LOCATION, Column.CONFIRMED, Column.RECOVERED, Column.DEATHS)

    def __init__(self, url, cols: Tuple[Column]):
        self.url = url
        self.cols: Tuple[Column] = cols

    def load(self):
        df = None
        if self == DataSet.ISCIII:
            df: pd.DataFrame = pd.read_csv(self.url, header=0, names=[c.label for c in self.cols],
                                           parse_dates=['Date'],
                                           date_parser=lambda x: dt.datetime.strptime(x, '%d/%m/%Y'),
                                           encoding='mac-roman', skipfooter=6, engine='python')
        elif self == DataSet.WORLD:
            df: pd.DataFrame = pd.read_csv(self.url, header=0, names=[c.label for c in self.cols],
                                           parse_dates=['Date'],
                                           encoding='mac-roman', engine='python')

        # add undefined columns as empty columns
        for c in Column:
            if c.isdata and c.label not in df:
                df[c.label] = 0

        # if ISCII, change community iso codes to names
        if self == DataSet.ISCIII:
            df = df.fillna(0)
            df['Location'] = df['Location'].apply(iso_to_name)
            df = add_totals(df)

        df = df.set_index('Date')

        # create Active Cases column
        df[Column.ACTIVE.label] = df[Column.CONFIRMED.label] - \
                                  (df[Column.RECOVERED.label] + df[Column.DEATHS.label])

        return df


def add_totals(df: pd.DataFrame):
    temp = pd.DataFrame()  # empty temporal dataframe where Total (i.e. Spain) data will be stored
    for date in df[Column.DATE.label].unique():
        _df = df[df[Column.DATE.label] == date]  # data frame for this given date
        row = {col.label: _df[col.label].sum() for col in Column.get_data_cols()}
        row[Column.LOCATION.label] = Community.ESPANA.label
        row[Column.DATE.label] = date
        temp = temp.append(row, ignore_index=True)

    return df.append(temp)


def get_outbreak(df, location):
    return int(df[df[Column.LOCATION.label] == location][Column.CONFIRMED.label].values[-1])


def get_active(df, location):
    return int(df[df[Column.LOCATION.label] == location][Column.ACTIVE.label].values[-1])


def get_deaths(df, location):
    return int(df[df[Column.LOCATION.label] == location][Column.DEATHS.label].values[-1])


def get_locations(df):
    return [loc for loc in df[Column.LOCATION.label].unique()]


def get_ordered_outbreaks(df):
    locs = [(loc, get_outbreak(df, loc)) for loc in get_locations(df)]
    locs.sort(key=lambda l: l[1], reverse=True)
    return locs


def get_dates(df):
    return df.index.unique()


if __name__ == '__main__':
    df = DataSet.ISCIII.load()

    print(get_dates(df))
    get_deaths(df, Community.ESPANA.label)
