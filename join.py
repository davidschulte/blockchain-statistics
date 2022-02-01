from databaseAPI import DatabaseAPI

api = DatabaseAPI()
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
