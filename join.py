import os
import pathlib
from blockchain_parser.blockchain import Blockchain
from databaseAPI import DatabaseAPI
import time

api = DatabaseAPI()
#g = api.get_query_generator("SELECT tx_from_id FROM inputs")

# print(type(next(g)[0]))

# api.reset_database()

#queryt = f"SELECT COUNT(*) FROM inputs INNER JOIN outputs ON inputs.tx_from_id = outputs.tx_from_id AND inputs.tx_output_no = outputs.tx_output_no"
query = api.join_tables(['inputs', 'outputs'])


g = api.get_query_generator(f'SELECT COUNT(*) FROM {query}')

a = next(g)
inputs_with_outputs = a[0]
print(inputs_with_outputs)

query2 = f"SELECT COUNT(*) FROM inputs"
g2 = api.get_query_generator(query2)

a = next(g2)
inputs = a[0]
print(inputs)

print(inputs_with_outputs/inputs)