import urllib.request
from loader_spain import *


class Field(Enum):
    DATE = 'date'
    COMMUNITY = 'community'
    CASES = 'cases'
    HOSPITALIZED = 'hospitalized'
    UCI = 'uci'
    DIED = 'died'
    RECOVERED = 'recovered'
    ACTIVE = 'active'


class Status:
    def __init__(self, date, community, cases, hospitalized, uci, died, recovered):
        self.date = date
        self.community = community
        self.cases = cases
        self.hospitalized = hospitalized
        self.uci = uci
        self.died = died
        self.recovered = recovered

    @property
    def active(self):
        return self.cases-(self.died + self.recovered)

    def __repr__(self):
        return self.date + ' ' + self.community.__repr__()


class Data:
    url = 'https://covid19.isciii.es/resources/serie_historica_acumulados.csv'

    def __init__(self):
        lines = [line.split(',') for line in urllib.request.urlopen(Data.url).read().decode('mac-roman').split('\n')][1:-3]
        self.statuses = []
        for line in lines:
            iso, date, cases, hospitalized, uci, died, recovered = line
            status = Status(self.process_date(date), Community.from_iso(iso),
                            self.process_value(cases), self.process_value(hospitalized), self.process_value(uci),
                            self.process_value(died), self.process_value(recovered))
            self.statuses.append(status)

    def get(self, community: Community, field: Field):
        ret = [(s.date, getattr(s, field.value)) for s in self.statuses if s.community == community]
        return zip(*ret)  # tuple dates, values

    @staticmethod
    def process_date(date: str):
        day, month, year = date.split('/')
        return day + '-' + month

    @staticmethod
    def process_value(value: str):
        return int(value.rstrip('\r')) if value.isdigit() else 0


if __name__ == '__main__':
    data = Data()
    dates, values = data.get(Community.CANTABRIA, Field.ACTIVE)






