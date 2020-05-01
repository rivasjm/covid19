import pandas as pd
import datetime as dt
import numpy as np
from enum import Enum
from typing import List, Tuple


class Datadista(Enum):
    CASOS = "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos_long.csv"
    PCR = "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_confirmados_pcr_long.csv"
    FALLECIDOS = "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos_long.csv"
    HOSPITALIZADOS = "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_hospitalizados_long.csv"

    def __init__(self, url):
        self.url = url

