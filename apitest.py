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

days = [str(x[0]) for x in vol_by_day][1:-1]
# print(days)
vols = [int(x[1])/10**14 for x in vol_by_day][1:-1]
# print(vols)
# print(type(vols[0]))

x = np.arange(len(days))

plt.plot(x, vols)
plt.xticks(x, days)
plt.title('Trading volume in a short timeframe in August 2021')
plt.xlabel('Day of the month')
plt.ylabel('Trading volume in mil btc')
plt.show()
plt.savefig('tradevol.png', transparent=True)
