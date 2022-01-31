import os
import pathlib
from blockchain_parser.blockchain import Blockchain
from databaseAPI import DatabaseAPI
import time
from analyzer import Analyzer
import matplotlib.pyplot as plt
import numpy as np

api = DatabaseAPI()
analyzer = Analyzer(api)

vol_by_day = list(analyzer.get_volume_by_day())

days = [str(x[0]) for x in vol_by_day]
print(days)
vols = [int(x[1]) for x in vol_by_day]
print(vols)
print(type(vols[0]))

x = np.arange(len(days))

plt.plot(x, vols)
plt.xticks(x, days)
plt.show()
