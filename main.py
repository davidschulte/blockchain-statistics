import os
import pathlib
from blockchain_parser.blockchain import Blockchain
from databaseAPI import DatabaseAPI
import time

# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
#blockchain = Blockchain(pathlib.Path().resolve())
path = '/media/sf_blocks'
blockchain = Blockchain(path)
api = DatabaseAPI()
tic = time.time()
block_counter = 0
blocks = blockchain.get_unordered_blocks()
start = 451
stop = 500
for block_num in range(stop):
    block = next(blocks)
    block_counter += 1
    if block_num >= start - 1:
        print("Block {}".format(block_num+1))
        api.add_block(block)

        # for tx in block.transactions:
        # api.create_tables()

        # api.add_transaction(tx)
        # tx_counter += 1

toc = time.time() - tic

print("It took {}s for {} transaction. {} average".format(toc, block_counter, toc/block_counter))

# for block in blockchain.get_unordered_blocks():