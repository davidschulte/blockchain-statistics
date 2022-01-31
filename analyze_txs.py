import pickle

with open('all_txs.pickle', 'rb') as handle:
    tx_dict = pickle.load(handle)

print(len(tx_dict))
a = iter(tx_dict)
b = iter(tx_dict.values())
for _ in range(10):
    print(next(a), next(b))
