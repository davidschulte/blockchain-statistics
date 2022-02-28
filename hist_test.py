from analyzer import Analyzer
import matplotlib.pyplot as plt
import numpy as np
from databaseAPI import DatabaseAPI

api = DatabaseAPI()
analyzer = Analyzer(api)

query_result = analyzer.get_values()

vols = np.array([x[0] for x in query_result])
print(vols.shape)
print(np.mean(vols))

plt.hist(np.log10(vols))
plt.show()
