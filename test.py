import os
import pathlib
from blockchain_parser.blockchain import Blockchain
from databaseAPI import DatabaseAPI
import time

api = DatabaseAPI()
# g = api.get_query_generator("SELECT tx_from_id FROM inputs")

# print(type(next(g)[0]))

# api.reset_database()
#
# num_checked = 1
# num_found = 0
# for row in g:
#     ba_2_compare = row[0].hex()
#     # print(type(ba_2_compare))
#     query = f"SELECT EXISTS(SELECT tx_id FROM transactions WHERE BINARY tx_id = BINARY 0x{ba_2_compare})"
#     # print(query)
#     api.cursor.execute(query)
#     found = bool(api.cursor.fetchall()[0][0])
#
#     if found:
#         num_found += 1
#     num_checked += 1
#
# print(f"checked '{num_checked}'. found '{num_found}'")

# g2 = api.get_query_generator("SELECT * FROM transactions")

api.create_views()